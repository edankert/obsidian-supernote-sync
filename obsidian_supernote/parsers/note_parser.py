"""Parse and inspect Supernote .note files."""

import zipfile
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from io import BytesIO

from PIL import Image


class NoteFileParser:
    """Parser for Supernote .note files.

    .note files have a three-section structure:
    1. Binary header with metadata
    2. Embedded PNG images (PDF template pages)
    3. ZIP archive with handwriting data (MyScript iink format)
    """

    def __init__(self, note_file: Path):
        """Initialize the parser.

        Args:
            note_file: Path to .note file
        """
        self.note_file = Path(note_file)
        self.file_data = self.note_file.read_bytes()
        self.metadata: Dict[str, Any] = {}
        self.png_images: List[bytes] = []
        self.zip_data: Optional[bytes] = None
        self.zip_contents: Dict[str, Any] = {}

    def parse(self) -> Dict[str, Any]:
        """Parse the entire .note file.

        Returns:
            Dictionary containing all parsed information
        """
        self._parse_header()
        self._extract_png_images()
        self._extract_zip_archive()
        self._parse_zip_contents()

        return {
            "file_path": str(self.note_file),
            "file_size": len(self.file_data),
            "metadata": self.metadata,
            "png_count": len(self.png_images),
            "png_images": self.png_images,
            "zip_size": len(self.zip_data) if self.zip_data else 0,
            "zip_contents": self.zip_contents,
        }

    def _parse_header(self) -> None:
        """Parse the binary header section (Section 1)."""
        # Find the first PNG signature (marks end of header)
        png_signature = b"\x89PNG\r\n\x1a\n"
        header_end = self.file_data.find(png_signature)

        if header_end == -1:
            # No PNGs found, try to find ZIP signature
            zip_signature = b"PK\x03\x04"
            header_end = self.file_data.find(zip_signature)

        if header_end == -1:
            # Neither PNG nor ZIP found - might be a different format
            # Try to find end of XML-like tags (look for last '>')
            # Supernote header ends with tags like <TAG:value>
            # Look for the pattern of end of tags followed by binary data
            last_tag_end = self.file_data.rfind(b">", 0, 2000)  # Search first 2KB
            if last_tag_end != -1:
                # Header ends shortly after the last tag
                header_end = last_tag_end + 1
            else:
                raise ValueError("Unable to locate header boundary")

        # Decode header (it's ASCII/UTF-8 text with XML-like tags)
        header_bytes = self.file_data[:header_end]
        header_text = header_bytes.decode("utf-8", errors="ignore")

        # Extract file signature
        if header_text.startswith("noteSN_FILE_VER_"):
            signature_match = re.search(r"noteSN_FILE_VER_(\d+)", header_text)
            if signature_match:
                self.metadata["file_version"] = signature_match.group(1)

        # Extract metadata tags (format: <TAG_NAME:value>)
        tag_pattern = r"<([A-Z_]+):([^>]+)>"
        for match in re.finditer(tag_pattern, header_text):
            tag_name = match.group(1)
            tag_value = match.group(2)
            self.metadata[tag_name.lower()] = tag_value

        # Extract base64-encoded page references (comma-separated after tags)
        # These appear after all the <TAG:value> entries
        base64_pattern = r"([A-Za-z0-9+/=]{20,}),"
        base64_matches = re.findall(base64_pattern, header_text)
        if base64_matches:
            self.metadata["page_references"] = base64_matches

    def _extract_png_images(self) -> None:
        """Extract embedded PNG images (Section 2)."""
        png_signature = b"\x89PNG\r\n\x1a\n"
        png_end_marker = b"IEND\xaeB`\x82"

        offset = 0
        while True:
            # Find next PNG
            png_start = self.file_data.find(png_signature, offset)
            if png_start == -1:
                break

            # Find end of this PNG
            png_end = self.file_data.find(png_end_marker, png_start)
            if png_end == -1:
                break

            # Include the 8-byte end marker (4 bytes CRC + 4 bytes chunk end)
            png_end += 8

            # Extract PNG data
            png_data = self.file_data[png_start:png_end]
            self.png_images.append(png_data)

            offset = png_end

    def _extract_zip_archive(self) -> None:
        """Extract ZIP archive (Section 3)."""
        # ZIP files start with "PK\x03\x04"
        zip_signature = b"PK\x03\x04"

        # Find the last occurrence (ZIP is at the end)
        zip_start = self.file_data.rfind(zip_signature)

        if zip_start == -1:
            # No ZIP archive found
            self.zip_data = None
            return

        self.zip_data = self.file_data[zip_start:]

    def _parse_zip_contents(self) -> None:
        """Parse the ZIP archive contents."""
        if not self.zip_data:
            return

        try:
            with zipfile.ZipFile(BytesIO(self.zip_data)) as zf:
                # Get file list
                file_list = zf.namelist()
                self.zip_contents["files"] = file_list

                # Parse root-level JSON files
                if "meta.json" in file_list:
                    meta_json = json.loads(zf.read("meta.json"))
                    self.zip_contents["meta"] = meta_json

                if "rel.json" in file_list:
                    rel_json = json.loads(zf.read("rel.json"))
                    self.zip_contents["relationships"] = rel_json

                # Parse page metadata
                pages = {}
                for filename in file_list:
                    if filename.startswith("pages/") and filename.endswith("meta.json"):
                        page_id = filename.split("/")[1]
                        page_meta = json.loads(zf.read(filename))
                        pages[page_id] = {
                            "meta": page_meta,
                            "has_content": page_meta.get("pageHasContent", False),
                        }

                        # Check for ink data
                        ink_file = f"pages/{page_id}/ink.bink"
                        if ink_file in file_list:
                            ink_size = zf.getinfo(ink_file).file_size
                            pages[page_id]["ink_size"] = ink_size

                self.zip_contents["pages"] = pages

        except zipfile.BadZipFile as e:
            self.zip_contents["error"] = f"Bad ZIP file: {e}"

    def get_png_image(self, index: int) -> Optional[Image.Image]:
        """Get a PNG image by index.

        Args:
            index: Index of PNG image (0-based)

        Returns:
            PIL Image object, or None if not found
        """
        if 0 <= index < len(self.png_images):
            return Image.open(BytesIO(self.png_images[index]))
        return None

    def save_png_images(self, output_dir: Path) -> List[Path]:
        """Save all PNG images to a directory.

        Args:
            output_dir: Directory to save images

        Returns:
            List of saved file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []
        stem = self.note_file.stem

        for i, png_data in enumerate(self.png_images, start=1):
            output_file = output_dir / f"{stem}_page{i:02d}.png"
            output_file.write_bytes(png_data)
            saved_files.append(output_file)

        return saved_files

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the .note file structure.

        Returns:
            Dictionary with summary information
        """
        return {
            "file_name": self.note_file.name,
            "file_size_mb": round(len(self.file_data) / 1024 / 1024, 2),
            "format_version": self.metadata.get("file_version", "Unknown"),
            "file_type": self.metadata.get("file_type", "Unknown"),
            "device": self.metadata.get("apply_equipment", "Unknown"),
            "language": self.metadata.get("file_recogn_language", "Unknown"),
            "pdf_template": self.metadata.get("pdfstyle", "None"),
            "pdf_template_md5": self.metadata.get("pdfstylemd5", "None"),
            "png_images_count": len(self.png_images),
            "png_images_size_mb": round(
                sum(len(png) for png in self.png_images) / 1024 / 1024, 2
            ),
            "zip_archive_size_kb": round(len(self.zip_data) / 1024, 2)
            if self.zip_data
            else 0,
            "pages_count": len(self.zip_contents.get("pages", {})),
            "has_handwriting": any(
                p.get("has_content", False)
                for p in self.zip_contents.get("pages", {}).values()
            ),
        }


def inspect_note_file(note_file: str | Path) -> Dict[str, Any]:
    """Convenience function to inspect a .note file.

    Args:
        note_file: Path to .note file

    Returns:
        Dictionary containing parsed information
    """
    parser = NoteFileParser(Path(note_file))
    return parser.parse()
