"""Create Supernote .note files from PDFs or images."""

import hashlib
import base64
import json
import struct
import random
import string
import tempfile
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import List, Tuple

import fitz  # PyMuPDF
from PIL import Image

from obsidian_supernote.converters.pandoc_converter import PandocConverter


class NoteFileWriter:
    """Create Supernote .note files from PDF files or images.

    .note file structure (X-series format, reverse-engineered from parser.py):
    1. Filetype: "note" (4 bytes)
    2. Signature: "SN_FILE_VER_20230015" (20 bytes)
    3. Header block (4-byte length + metadata tags)
    4. Layer content blocks (4-byte length + PNG/RLE data)
    5. Layer metadata blocks (4-byte length + tags)
    6. Page metadata blocks (4-byte length + tags)
    7. Footer block (4-byte length + tags + "tail")
    8. Footer address (4 bytes, little-endian)

    Supported devices and resolutions:
    - A5X: 1404 x 1872 pixels (226 DPI)
    - A5X2 (Manta): 1920 x 2560 pixels (300 DPI)
    - A6X: 1404 x 1872 pixels (300 DPI)
    - A6X2 (Nomad): 1404 x 1872 pixels (300 DPI)
    """

    # Device resolution mapping: (width, height, dpi)
    DEVICE_SPECS = {
        "A5X": (1404, 1872, 226),
        "A5X2": (1920, 2560, 300),  # Manta
        "Manta": (1920, 2560, 300),  # Alias for A5X2
        "A6X": (1404, 1872, 300),
        "A6X2": (1404, 1872, 300),  # Nomad
        "Nomad": (1404, 1872, 300),  # Alias for A6X2
    }

    # File format constants
    FILETYPE = b"note"
    SIGNATURE = b"SN_FILE_VER_20230015"
    ADDRESS_SIZE = 4
    LENGTH_FIELD_SIZE = 4

    # Layer names in order - all 5 must be present in page metadata
    # Only MAINLAYER and BGLAYER have actual content, others have address 0
    ALL_LAYER_NAMES = ["MAINLAYER", "LAYER1", "LAYER2", "LAYER3", "BGLAYER"]
    ACTIVE_LAYERS = ["MAINLAYER", "BGLAYER"]  # Layers with actual content

    # Empty layer RLE data (600 bytes of 0x62 0xff pattern = blank white layer)
    EMPTY_LAYER_RLE = bytes([0x62, 0xff] * 300)  # 600 bytes

    # Device equipment name mapping (internal codes used by device)
    DEVICE_EQUIPMENT = {
        "A5X": "A5X",      # Unknown internal code, using commercial name
        "A5X2": "N5",      # Manta uses "N5"
        "Manta": "N5",     # Alias for A5X2
        "A6X": "A6X",      # Unknown internal code
        "A6X2": "A6X2",    # Unknown internal code, Nomad
        "Nomad": "A6X2",   # Alias for A6X2
    }

    def __init__(
        self,
        device: str = "A5X2",
        language: str = "en_GB",
    ):
        """Initialize the note writer.

        Args:
            device: Target Supernote device (A5X, A5X2/Manta, A6X, A6X2/Nomad)
            language: Recognition language (en_GB, en_US, etc.)
        """
        self.device = device
        self.language = language

        # Set device-specific dimensions
        if device in self.DEVICE_SPECS:
            self.template_width, self.template_height, self.native_dpi = self.DEVICE_SPECS[device]
        else:
            # Default to A5X2 (Manta) for unknown devices
            self.template_width, self.template_height, self.native_dpi = self.DEVICE_SPECS["A5X2"]

    def convert_pdf_to_note(
        self,
        pdf_path: Path,
        output_path: Path,
        dpi: int | None = None,
        realtime: bool = False,
    ) -> None:
        """Convert a PDF file to a Supernote .note file.

        Args:
            pdf_path: Path to input PDF file
            output_path: Path to output .note file
            dpi: DPI for rendering PDF pages (defaults to device native DPI)
            realtime: Enable realtime handwriting recognition mode
        """
        pdf_path = Path(pdf_path)
        output_path = Path(output_path)

        # Use device native DPI if not specified
        render_dpi = dpi if dpi is not None else self.native_dpi

        # Read PDF and convert pages to PNG
        png_pages = self._convert_pdf_to_pngs(pdf_path, render_dpi)

        # Calculate PDF hash and size
        pdf_data = pdf_path.read_bytes()
        pdf_md5 = hashlib.md5(pdf_data).hexdigest()
        pdf_size = len(pdf_data)

        # Generate per-page MD5 hashes
        page_md5s = [hashlib.md5(png).hexdigest() for png in png_pages]

        # PDF style MD5 uses the last page's MD5 (observed from golden files)
        # instead of the PDF file's MD5
        pdf_md5_to_use = page_md5s[-1] if page_md5s else pdf_md5

        # Generate .note file
        self._write_note_file(
            output_path,
            png_pages,
            pdf_path.stem,
            pdf_md5_to_use,
            pdf_size,
            page_md5s,
            realtime=realtime,
        )

    def convert_images_to_note(
        self,
        image_paths: List[Path],
        output_path: Path,
        name: str = "note",
    ) -> None:
        """Convert a list of images to a Supernote .note file.

        Args:
            image_paths: List of paths to PNG/image files
            output_path: Path to output .note file
            name: Base name for the note
        """
        output_path = Path(output_path)

        # Load and resize images
        png_pages = []
        for img_path in image_paths:
            img = Image.open(img_path)
            # Resize to Supernote dimensions if needed
            if img.size != (self.template_width, self.template_height):
                img = img.resize(
                    (self.template_width, self.template_height),
                    Image.Resampling.LANCZOS,
                )
            # Convert to PNG bytes
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            png_pages.append(buffer.getvalue())

        # Generate MD5 hashes
        page_md5s = [hashlib.md5(png).hexdigest() for png in png_pages]
        combined_md5 = hashlib.md5(b''.join(png_pages)).hexdigest()
        total_size = sum(len(png) for png in png_pages)

        # Generate .note file
        self._write_note_file(
            output_path,
            png_pages,
            name,
            combined_md5,
            total_size,
            page_md5s,
        )

    def convert_png_template_to_note(
        self,
        png_path: Path,
        output_path: Path,
        template_name: str | None = None,
        realtime: bool = False,
    ) -> None:
        """Convert a PNG template to a Supernote .note file.

        This creates a .note file using PNG template format, which is simpler
        than the PDF format and matches how the device creates notes from
        PNG templates in MyStyle folder.

        Args:
            png_path: Path to input PNG template file
            output_path: Path to output .note file
            template_name: Template name (defaults to PNG filename without extension)
            realtime: Enable realtime handwriting recognition mode
        """
        png_path = Path(png_path)
        output_path = Path(output_path)

        # Check if PNG needs resizing
        img = Image.open(png_path)
        if img.size == (self.template_width, self.template_height):
            # Use raw PNG data to preserve exact bytes (avoid re-encoding)
            png_data = png_path.read_bytes()
        else:
            # Resize and re-encode
            img = img.resize(
                (self.template_width, self.template_height),
                Image.Resampling.LANCZOS,
            )
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            png_data = buffer.getvalue()

        # Calculate MD5 of PNG data
        png_md5 = hashlib.md5(png_data).hexdigest()

        # Use filename as template name if not specified
        if template_name is None:
            template_name = png_path.stem

        # Generate .note file with PNG template format
        self._write_png_template_note_file(
            output_path,
            png_data,
            template_name,
            png_md5,
            realtime=realtime,
        )

    def _convert_pdf_to_pngs(
        self,
        pdf_path: Path,
        dpi: int | None = None,
    ) -> List[bytes]:
        """Convert PDF pages to PNG images.

        Args:
            pdf_path: Path to PDF file
            dpi: DPI for rendering (defaults to device native DPI)

        Returns:
            List of PNG image data as bytes
        """
        render_dpi = dpi if dpi is not None else self.native_dpi
        png_pages = []

        # Open PDF with PyMuPDF
        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):
            page = doc[page_num]

            # Calculate zoom factor for target DPI
            zoom = render_dpi / 72.0  # PDF is 72 DPI by default
            mat = fitz.Matrix(zoom, zoom)

            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat, alpha=True)

            # Convert to PIL Image
            img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)

            # Resize to Supernote dimensions
            img = img.resize(
                (self.template_width, self.template_height),
                Image.Resampling.LANCZOS,
            )

            # Convert to PNG bytes
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            png_pages.append(buffer.getvalue())

        doc.close()
        return png_pages

    def _write_note_file(
        self,
        output_path: Path,
        png_pages: List[bytes],
        pdf_name: str,
        pdf_md5: str,
        pdf_size: int,
        page_md5s: List[str],
        realtime: bool = False,
    ) -> None:
        """Write the .note file with correct binary structure.

        File structure (matching real device files):
        1. Filetype + Signature (24 bytes)
        2. Header block
        3. PDFSTYLELIST data block (base64-encoded style names)
        4. PNG data for each page (BGLAYER content)
        5. Default style RLE data (STYLE_style_white_a5x2)
        6. Empty MAINLAYER RLE data for each page
        7. Layer metadata blocks (MAINLAYER + BGLAYER per page)
        8. Page metadata blocks
        9. Footer block (no "tail" marker)
        10. Footer address (4 bytes)

        Args:
            output_path: Path to output file
            png_pages: List of PNG image data
            pdf_name: Name of original PDF (without extension)
            pdf_md5: MD5 hash of original PDF
            pdf_size: Size of original PDF in bytes
            page_md5s: List of MD5 hashes for each page
            realtime: Enable realtime handwriting recognition mode
        """
        num_pages = len(png_pages)
        file_id = self._generate_file_id()

        # Build header content
        header_content = self._build_header_content(
            pdf_name, num_pages, pdf_md5, pdf_size, file_id, realtime=realtime
        )
        header_bytes = header_content.encode("utf-8")

        # Build PDFSTYLELIST content (base64-encoded style names, comma-separated)
        pdfstylelist_entries = []
        for i, page_md5 in enumerate(page_md5s, start=1):
            style_name = f"user_pdf_{pdf_name}_{i}_{page_md5}_{pdf_size}"
            encoded = base64.b64encode(style_name.encode()).decode()
            pdfstylelist_entries.append(encoded)
        pdfstylelist_content = ",".join(pdfstylelist_entries) + ","
        pdfstylelist_bytes = pdfstylelist_content.encode("utf-8")

        # We'll build the file in stages, tracking addresses
        # Start position after filetype + signature
        current_pos = len(self.FILETYPE) + len(self.SIGNATURE)

        # Header block starts at position 24 (4 bytes filetype + 20 bytes signature)
        header_address = current_pos
        current_pos += self.LENGTH_FIELD_SIZE + len(header_bytes)

        # PDFSTYLELIST data block
        pdfstylelist_address = current_pos
        current_pos += self.LENGTH_FIELD_SIZE + len(pdfstylelist_bytes)

        # PNG data for each page (BGLAYER content)
        bglayer_content_addresses = []
        for png_data in png_pages:
            bglayer_content_addresses.append(current_pos)
            current_pos += self.LENGTH_FIELD_SIZE + len(png_data)

        # Default style RLE data (STYLE_style_white_a5x2)
        style_white_address = current_pos
        current_pos += self.LENGTH_FIELD_SIZE + len(self.EMPTY_LAYER_RLE)

        # Empty MAINLAYER RLE data for each page
        mainlayer_content_addresses = []
        for _ in range(num_pages):
            mainlayer_content_addresses.append(current_pos)
            current_pos += self.LENGTH_FIELD_SIZE + len(self.EMPTY_LAYER_RLE)

        # Layer metadata blocks (MAINLAYER + BGLAYER per page)
        layer_metadata_addresses = []
        for page_idx in range(num_pages):
            page_layer_addrs = {}
            # MAINLAYER metadata
            mainlayer_addr = current_pos
            mainlayer_meta = self._build_layer_metadata(
                "MAINLAYER",
                mainlayer_content_addresses[page_idx],
            )
            current_pos += self.LENGTH_FIELD_SIZE + len(mainlayer_meta.encode("utf-8"))
            page_layer_addrs["MAINLAYER"] = mainlayer_addr

            # BGLAYER metadata
            bglayer_addr = current_pos
            bglayer_meta = self._build_layer_metadata(
                "BGLAYER",
                bglayer_content_addresses[page_idx],
            )
            current_pos += self.LENGTH_FIELD_SIZE + len(bglayer_meta.encode("utf-8"))
            page_layer_addrs["BGLAYER"] = bglayer_addr

            # Unused layers have address 0
            for layer_name in ["LAYER1", "LAYER2", "LAYER3"]:
                page_layer_addrs[layer_name] = 0
            layer_metadata_addresses.append(page_layer_addrs)

        # Page metadata blocks
        page_metadata_addresses = []
        for page_idx in range(num_pages):
            page_addr = current_pos
            page_meta = self._build_page_metadata(
                page_idx,
                pdf_name,
                page_md5s[page_idx],
                pdf_size,
                layer_metadata_addresses[page_idx],
            )
            current_pos += self.LENGTH_FIELD_SIZE + len(page_meta.encode("utf-8"))
            page_metadata_addresses.append(page_addr)

        # Footer block
        footer_address = current_pos
        footer_content = self._build_footer_content(
            header_address,
            page_metadata_addresses,
            bglayer_content_addresses,
            pdf_name,
            page_md5s,
            pdf_size,
            pdfstylelist_address=pdfstylelist_address,
            style_white_address=style_white_address,
        )
        footer_bytes = footer_content.encode("utf-8")

        # Now write the file
        with open(output_path, "wb") as f:
            # 1. Filetype (4 bytes)
            f.write(self.FILETYPE)

            # 2. Signature (20 bytes)
            f.write(self.SIGNATURE)

            # 3. Header block
            f.write(struct.pack("<I", len(header_bytes)))
            f.write(header_bytes)

            # 4. PDFSTYLELIST data block
            f.write(struct.pack("<I", len(pdfstylelist_bytes)))
            f.write(pdfstylelist_bytes)

            # 5. PNG data for each page (BGLAYER content)
            for png_data in png_pages:
                f.write(struct.pack("<I", len(png_data)))
                f.write(png_data)

            # 6. Default style RLE data (STYLE_style_white_a5x2)
            f.write(struct.pack("<I", len(self.EMPTY_LAYER_RLE)))
            f.write(self.EMPTY_LAYER_RLE)

            # 7. Empty MAINLAYER RLE data for each page
            for _ in range(num_pages):
                f.write(struct.pack("<I", len(self.EMPTY_LAYER_RLE)))
                f.write(self.EMPTY_LAYER_RLE)

            # 8. Layer metadata blocks (MAINLAYER + BGLAYER per page)
            for page_idx in range(num_pages):
                # MAINLAYER
                mainlayer_meta = self._build_layer_metadata(
                    "MAINLAYER",
                    mainlayer_content_addresses[page_idx],
                )
                f.write(struct.pack("<I", len(mainlayer_meta.encode("utf-8"))))
                f.write(mainlayer_meta.encode("utf-8"))

                # BGLAYER
                bglayer_meta = self._build_layer_metadata(
                    "BGLAYER",
                    bglayer_content_addresses[page_idx],
                )
                f.write(struct.pack("<I", len(bglayer_meta.encode("utf-8"))))
                f.write(bglayer_meta.encode("utf-8"))

            # 9. Page metadata blocks
            for page_idx in range(num_pages):
                page_meta = self._build_page_metadata(
                    page_idx,
                    pdf_name,
                    page_md5s[page_idx],
                    pdf_size,
                    layer_metadata_addresses[page_idx],
                )
                f.write(struct.pack("<I", len(page_meta.encode("utf-8"))))
                f.write(page_meta.encode("utf-8"))

            # 10. Footer block
            f.write(struct.pack("<I", len(footer_bytes)))
            f.write(footer_bytes)

            # 11. "tail" marker
            f.write(b"tail")

            # 12. Footer address (last 4 bytes)
            f.write(struct.pack("<I", footer_address))

    def _write_png_template_note_file(
        self,
        output_path: Path,
        png_data: bytes,
        template_name: str,
        png_md5: str,
        realtime: bool = False,
    ) -> None:
        """Write .note file with PNG template format.

        PNG template format is simpler than PDF format:
        1. Filetype + Signature (24 bytes)
        2. Header block (simpler - no PDF fields)
        3. PNG data for BGLAYER
        4. Empty MAINLAYER RLE data (600 bytes)
        5. MAINLAYER metadata
        6. BGLAYER metadata
        7. Page metadata
        8. Footer (simpler - no PDFSTYLELIST, no COVER_0)
        9. Footer address (4 bytes)

        Args:
            output_path: Path to output file
            png_data: PNG image data for background
            template_name: Template name (e.g., "blank_template_a5x2")
            png_md5: MD5 hash of PNG data
            realtime: Enable realtime handwriting recognition mode
        """
        file_id = self._generate_file_id()

        # Build header content (PNG template format - simpler than PDF)
        header_content = self._build_png_header_content(file_id, realtime=realtime)
        header_bytes = header_content.encode("utf-8")

        # Calculate addresses
        # Start position after filetype + signature
        current_pos = len(self.FILETYPE) + len(self.SIGNATURE)

        # Header block at position 24
        header_address = current_pos
        current_pos += self.LENGTH_FIELD_SIZE + len(header_bytes)

        # PNG data for BGLAYER
        bglayer_content_address = current_pos
        current_pos += self.LENGTH_FIELD_SIZE + len(png_data)

        # Empty MAINLAYER RLE data
        mainlayer_content_address = current_pos
        current_pos += self.LENGTH_FIELD_SIZE + len(self.EMPTY_LAYER_RLE)

        # MAINLAYER metadata
        mainlayer_meta = self._build_layer_metadata("MAINLAYER", mainlayer_content_address)
        mainlayer_meta_address = current_pos
        current_pos += self.LENGTH_FIELD_SIZE + len(mainlayer_meta.encode("utf-8"))

        # BGLAYER metadata
        bglayer_meta = self._build_layer_metadata("BGLAYER", bglayer_content_address)
        bglayer_meta_address = current_pos
        current_pos += self.LENGTH_FIELD_SIZE + len(bglayer_meta.encode("utf-8"))

        # Layer addresses dict
        layer_addresses = {
            "MAINLAYER": mainlayer_meta_address,
            "LAYER1": 0,
            "LAYER2": 0,
            "LAYER3": 0,
            "BGLAYER": bglayer_meta_address,
        }

        # Page metadata (PNG template format)
        page_meta = self._build_png_page_metadata(
            template_name,
            png_md5,
            layer_addresses,
        )
        page_metadata_address = current_pos
        current_pos += self.LENGTH_FIELD_SIZE + len(page_meta.encode("utf-8"))

        # Footer (PNG template format - simpler)
        footer_address = current_pos
        footer_content = self._build_png_footer_content(
            header_address,
            page_metadata_address,
            bglayer_content_address,
            template_name,
            png_md5,
        )
        footer_bytes = footer_content.encode("utf-8")

        # Write the file
        with open(output_path, "wb") as f:
            # 1. Filetype (4 bytes)
            f.write(self.FILETYPE)

            # 2. Signature (20 bytes)
            f.write(self.SIGNATURE)

            # 3. Header block
            f.write(struct.pack("<I", len(header_bytes)))
            f.write(header_bytes)

            # 4. PNG data for BGLAYER
            f.write(struct.pack("<I", len(png_data)))
            f.write(png_data)

            # 5. Empty MAINLAYER RLE data
            f.write(struct.pack("<I", len(self.EMPTY_LAYER_RLE)))
            f.write(self.EMPTY_LAYER_RLE)

            # 6. MAINLAYER metadata
            f.write(struct.pack("<I", len(mainlayer_meta.encode("utf-8"))))
            f.write(mainlayer_meta.encode("utf-8"))

            # 7. BGLAYER metadata
            f.write(struct.pack("<I", len(bglayer_meta.encode("utf-8"))))
            f.write(bglayer_meta.encode("utf-8"))

            # 8. Page metadata
            f.write(struct.pack("<I", len(page_meta.encode("utf-8"))))
            f.write(page_meta.encode("utf-8"))

            # 9. Footer block
            f.write(struct.pack("<I", len(footer_bytes)))
            f.write(footer_bytes)

            # 10. "tail" marker (PNG template format has this)
            f.write(b"tail")

            # 11. Footer address (last 4 bytes)
            f.write(struct.pack("<I", footer_address))

    def _build_png_header_content(self, file_id: str, realtime: bool = False) -> str:
        """Build header content for PNG template format.

        PNG template headers are simpler - no PDF-related fields.
        Tag order must match real device files exactly.

        Args:
            file_id: Unique file ID
            realtime: Enable realtime handwriting recognition mode

        Returns:
            Header content string
        """
        equipment = self.DEVICE_EQUIPMENT.get(self.device, "N5")

        # Realtime recognition settings
        recogn_type = "1" if realtime else "0"
        recogn_language = self.language if realtime else "none"

        # Tag order from real PNG template file
        tags = [
            f"<FILE_TYPE:NOTE>",
            f"<APPLY_EQUIPMENT:{equipment}>",
            f"<FINALOPERATION_PAGE:1>",
            f"<FINALOPERATION_LAYER:1>",
            f"<DEVICE_DPI:0>",
            f"<SOFT_DPI:0>",
            f"<FILE_PARSE_TYPE:0>",
            f"<RATTA_ETMD:0>",
            f"<FILE_ID:{file_id}>",
            f"<FILE_RECOGN_TYPE:{recogn_type}>",
            f"<FILE_RECOGN_LANGUAGE:{recogn_language}>",
            f"<HORIZONTAL_CHECK:0>",
            f"<IS_OLD_APPLY_EQUIPMENT:1>",
            f"<ANTIALIASING_CONVERT:2>",
        ]

        return "".join(tags)

    def _build_png_page_metadata(
        self,
        template_name: str,
        png_md5: str,
        layer_addresses: dict,
    ) -> str:
        """Build page metadata for PNG template format.

        PNG template page metadata differs from PDF:
        - PAGESTYLE: user_{template_name} (no page number)
        - PAGESTYLEMD5: {md5} (no size suffix)
        - No EXTERNALLINKINFO, no IDTABLE

        Tag order must match real device files exactly.

        Args:
            template_name: Template name
            png_md5: MD5 hash of PNG
            layer_addresses: Dict of layer name to metadata address

        Returns:
            Page metadata string
        """
        page_id = self._generate_page_id()

        # LAYERINFO matches real device format exactly
        layer_info = [
            {"layerId": 3, "name": "Layer 3", "isBackgroundLayer": False, "isAllowAdd": False, "isCurrentLayer": False, "isVisible": True, "isDeleted": True, "isAllowUp": False, "isAllowDown": False},
            {"layerId": 2, "name": "Layer 2", "isBackgroundLayer": False, "isAllowAdd": False, "isCurrentLayer": False, "isVisible": True, "isDeleted": True, "isAllowUp": False, "isAllowDown": False},
            {"layerId": 1, "name": "Layer 1", "isBackgroundLayer": False, "isAllowAdd": False, "isCurrentLayer": False, "isVisible": True, "isDeleted": True, "isAllowUp": False, "isAllowDown": False},
            {"layerId": 0, "name": "Main Layer", "isBackgroundLayer": False, "isAllowAdd": False, "isCurrentLayer": True, "isVisible": True, "isDeleted": False, "isAllowUp": False, "isAllowDown": False},
            {"layerId": -1, "name": "Background Layer", "isBackgroundLayer": True, "isAllowAdd": True, "isCurrentLayer": False, "isVisible": True, "isDeleted": False, "isAllowUp": False, "isAllowDown": False},
        ]
        # Replace : with # in JSON (Supernote uses # as separator)
        layer_info_str = json.dumps(layer_info, separators=(',', ':')).replace(':', '#')

        # Tag order from real PNG template file
        tags = [
            f"<PAGESTYLE:user_{template_name}>",
            f"<PAGESTYLEMD5:{png_md5}>",
            f"<LAYERSEQ:MAINLAYER,BGLAYER>",
            f"<PAGEID:{page_id}>",
        ]

        # Layer addresses in order
        for layer_name in self.ALL_LAYER_NAMES:
            tags.append(f"<{layer_name}:{layer_addresses[layer_name]}>")

        # Remaining tags in exact order from real PNG template
        tags.extend([
            f"<TOTALPATH:0>",
            f"<THUMBNAILTYPE:0>",
            f"<RECOGNSTATUS:0>",
            f"<RECOGNTEXT:0>",
            f"<RECOGNFILE:0>",
            f"<LAYERINFO:{layer_info_str}>",
            f"<RECOGNTYPE:0>",
            f"<RECOGNFILESTATUS:0>",
            f"<RECOGNLANGUAGE:none>",
            f"<ORIENTATION:1000>",
            f"<PAGETEXTBOX:0>",
            f"<DISABLE:none>",
        ])

        return "".join(tags)

    def _build_png_footer_content(
        self,
        header_address: int,
        page_address: int,
        png_address: int,
        template_name: str,
        png_md5: str,
    ) -> str:
        """Build footer content for PNG template format.

        PNG template footers are simpler - no COVER_0, no PDFSTYLELIST,
        no STYLE_style_white_a5x2.

        STYLE entry format: STYLE_user_{template}{md5}:{address}
        (no underscore between template and md5, no size suffix)

        Args:
            header_address: Address of header block
            page_address: Address of page metadata block
            png_address: Address of PNG data (BGLAYER content)
            template_name: Template name
            png_md5: MD5 hash of PNG

        Returns:
            Footer content string
        """
        tags = [
            f"<PAGE1:{page_address}>",
            f"<DIRTY:0>",
            f"<FILE_FEATURE:{header_address}>",
            f"<STYLE_user_{template_name}{png_md5}:{png_address}>",
        ]

        return "".join(tags)

    def _build_header_content(
        self,
        pdf_name: str,
        num_pages: int,
        pdf_md5: str,
        pdf_size: int,
        file_id: str,
        realtime: bool = False,
    ) -> str:
        """Build header content (metadata tags).

        Args:
            pdf_name: Name of PDF file
            num_pages: Number of pages
            pdf_md5: MD5 hash of PDF
            pdf_size: Size of PDF in bytes
            file_id: Unique file ID
            realtime: Enable realtime handwriting recognition mode

        Returns:
            Header content string
        """
        # Get internal equipment code for device
        equipment = self.DEVICE_EQUIPMENT.get(self.device, "N5")

        # Realtime recognition settings
        recogn_type = "1" if realtime else "0"
        recogn_language = self.language if realtime else "none"

        # Tag order must match real device files exactly
        tags = [
            f"<MODULE_LABEL:none>",
            f"<FILE_TYPE:NOTE>",
            f"<APPLY_EQUIPMENT:{equipment}>",
            f"<FINALOPERATION_PAGE:{num_pages}>",
            f"<FINALOPERATION_LAYER:1>",
            f"<DEVICE_DPI:0>",
            f"<SOFT_DPI:0>",
            f"<FILE_PARSE_TYPE:0>",
            f"<RATTA_ETMD:0>",
            f"<APP_VERSION:0>",
            f"<FILE_ID:{file_id}>",
            f"<FILE_RECOGN_TYPE:{recogn_type}>",
            f"<FILE_RECOGN_LANGUAGE:{recogn_language}>",
            f"<PDFSTYLE:user_pdf_{pdf_name}_{num_pages}>",
            f"<PDFSTYLEMD5:{pdf_md5}_{pdf_size}>",
            f"<STYLEUSAGETYPE:2>",
            f"<HIGHLIGHTINFO:0>",
            f"<HORIZONTAL_CHECK:0>",
            f"<IS_OLD_APPLY_EQUIPMENT:1>",
            f"<ANTIALIASING_CONVERT:2>",
        ]

        return "".join(tags)

    def _build_layer_metadata(
        self,
        layer_name: str,
        bitmap_address: int,
    ) -> str:
        """Build layer metadata block.

        Args:
            layer_name: Name of the layer (MAINLAYER, BGLAYER)
            bitmap_address: Address of layer bitmap content (0 if none)

        Returns:
            Layer metadata string
        """
        # Both MAINLAYER and BGLAYER use NOTE type
        layer_type = "NOTE"

        tags = [
            f"<LAYERTYPE:{layer_type}>",
            f"<LAYERPROTOCOL:RATTA_RLE>",
            f"<LAYERNAME:{layer_name}>",
            f"<LAYERPATH:0>",
            f"<LAYERBITMAP:{bitmap_address}>",
            f"<LAYERVECTORGRAPH:0>",
            f"<LAYERRECOGN:0>",
        ]

        return "".join(tags)

    def _build_page_metadata(
        self,
        page_idx: int,
        pdf_name: str,
        page_md5: str,
        pdf_size: int,
        layer_addresses: dict,
    ) -> str:
        """Build page metadata block.

        Args:
            page_idx: Page index (0-based)
            pdf_name: Name of PDF file
            page_md5: MD5 hash of page
            pdf_size: Size of PDF
            layer_addresses: Dict of layer name to address (0 for unused layers)

        Returns:
            Page metadata string
        """
        page_num = page_idx + 1
        page_id = self._generate_page_id()

        # Layer info JSON (visibility settings) - matches real device format exactly
        # Note: layerId=-1 for Background Layer, unused layers have isDeleted=true
        layer_info = [
            {"layerId": 3, "name": "Layer 3", "isBackgroundLayer": False, "isAllowAdd": False, "isCurrentLayer": False, "isVisible": True, "isDeleted": True, "isAllowUp": False, "isAllowDown": False},
            {"layerId": 2, "name": "Layer 2", "isBackgroundLayer": False, "isAllowAdd": False, "isCurrentLayer": False, "isVisible": True, "isDeleted": True, "isAllowUp": False, "isAllowDown": False},
            {"layerId": 1, "name": "Layer 1", "isBackgroundLayer": False, "isAllowAdd": False, "isCurrentLayer": False, "isVisible": True, "isDeleted": True, "isAllowUp": False, "isAllowDown": False},
            {"layerId": 0, "name": "Main Layer", "isBackgroundLayer": False, "isAllowAdd": False, "isCurrentLayer": True, "isVisible": True, "isDeleted": False, "isAllowUp": False, "isAllowDown": False},
            {"layerId": -1, "name": "Background Layer", "isBackgroundLayer": True, "isAllowAdd": True, "isCurrentLayer": False, "isVisible": True, "isDeleted": False, "isAllowUp": False, "isAllowDown": False},
        ]
        # Replace : with # in JSON (Supernote uses # as separator in metadata)
        layer_info_str = json.dumps(layer_info, separators=(',', ':')).replace(':', '#')

        # Tag order must match real device files exactly
        tags = [
            f"<PAGESTYLE:user_pdf_{pdf_name}_{page_num}>",
            f"<PAGESTYLEMD5:{page_md5}_{pdf_size}>",
            f"<LAYERINFO:{layer_info_str}>",
            f"<LAYERSEQ:MAINLAYER,BGLAYER>",
        ]

        # Add all layer addresses in order (MAINLAYER, LAYER1, LAYER2, LAYER3, BGLAYER)
        for layer_name in self.ALL_LAYER_NAMES:
            tags.append(f"<{layer_name}:{layer_addresses[layer_name]}>")

        # Remaining tags in exact order from real files
        tags.extend([
            f"<TOTALPATH:0>",
            f"<THUMBNAILTYPE:0>",
            f"<RECOGNSTATUS:0>",
            f"<RECOGNTEXT:0>",
            f"<RECOGNFILE:0>",
            f"<PAGEID:{page_id}>",
            f"<RECOGNTYPE:0>",
            f"<RECOGNFILESTATUS:0>",
            f"<RECOGNLANGUAGE:none>",
            f"<EXTERNALLINKINFO:0>",
            f"<IDTABLE:0>",
            f"<ORIENTATION:1000>",
            f"<PAGETEXTBOX:0>",
            f"<DISABLE:none>",
        ])

        return "".join(tags)

    def _build_footer_content(
        self,
        header_address: int,
        page_addresses: List[int],
        png_addresses: List[int],
        pdf_name: str,
        page_md5s: List[str],
        pdf_size: int,
        pdfstylelist_address: int | None = None,
        style_white_address: int | None = None,
    ) -> str:
        """Build footer content.

        Args:
            header_address: Address of header block
            page_addresses: Addresses of page metadata blocks
            png_addresses: Addresses of PNG data for each page
            pdf_name: Name of PDF file
            page_md5s: MD5 hashes for each page
            pdf_size: Size of PDF
            pdfstylelist_address: Address of PDFSTYLELIST data block
            style_white_address: Address for default style RLE data

        Returns:
            Footer content string (no "tail" marker - real files don't have it)
        """
        tags = []

        # Page addresses
        for i, addr in enumerate(page_addresses, start=1):
            tags.append(f"<PAGE{i}:{addr}>")

        # Standard entries
        tags.append(f"<COVER_0:0>")
        tags.append(f"<DIRTY:0>")
        tags.append(f"<FILE_FEATURE:{header_address}>")

        # PDFSTYLELIST - points to PDFSTYLELIST data block
        if pdfstylelist_address is not None:
            tags.append(f"<PDFSTYLELIST:{pdfstylelist_address}>")

        # Default style entry - points to default RLE data
        if style_white_address is not None:
            tags.append(f"<STYLE_style_white_a5x2:{style_white_address}>")

        # Style entries for each page
        # Format: STYLE_{pagestyle}{pagestylemd5}: address
        # Note: No underscore between pagestyle and pagestylemd5
        # Where pagestyle = user_pdf_{name}_{pagenum}
        # And pagestylemd5 = {md5}_{size}
        for i, (page_md5, png_addr) in enumerate(zip(page_md5s, png_addresses), start=1):
            pagestyle = f"user_pdf_{pdf_name}_{i}"
            pagestylemd5 = f"{page_md5}_{pdf_size}"
            tags.append(f"<STYLE_{pagestyle}{pagestylemd5}:{png_addr}>")

        # No "tail" marker - real files don't have it
        return "".join(tags)

    def _generate_file_id(self) -> str:
        """Generate unique file ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]
        suffix = "".join(random.choices(string.ascii_letters + string.digits, k=15))
        return f"F{timestamp}{suffix}"

    def _generate_page_id(self) -> str:
        """Generate unique page ID (P + timestamp + random suffix)."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]
        suffix = "".join(random.choices(string.ascii_letters + string.digits, k=15))
        return f"P{timestamp}{suffix}"


def convert_pdf_to_note(
    pdf_path: str | Path,
    output_path: str | Path,
    device: str = "A5X2",
    language: str = "en_GB",
    realtime: bool = False,
) -> None:
    """Convert PDF to .note file.

    Args:
        pdf_path: Path to input PDF
        output_path: Path to output .note file
        device: Target device (A5X, A5X2/Manta, A6X, A6X2/Nomad)
        language: Recognition language (used when realtime=True)
        realtime: Enable realtime handwriting recognition mode
    """
    writer = NoteFileWriter(device=device, language=language)
    writer.convert_pdf_to_note(Path(pdf_path), Path(output_path), realtime=realtime)


def convert_png_to_note(
    png_path: str | Path,
    output_path: str | Path,
    device: str = "A5X2",
    template_name: str | None = None,
    language: str = "en_GB",
    realtime: bool = False,
) -> None:
    """Convert PNG template to .note file.

    This creates a .note file using the simpler PNG template format,
    which matches how the Supernote device creates notes from PNG
    templates in the MyStyle folder.

    Args:
        png_path: Path to input PNG template
        output_path: Path to output .note file
        device: Target device (A5X, A5X2/Manta, A6X, A6X2/Nomad)
        template_name: Template name (defaults to PNG filename)
        language: Recognition language (used when realtime=True)
        realtime: Enable realtime handwriting recognition mode
    """
    writer = NoteFileWriter(device=device, language=language)
    writer.convert_png_template_to_note(Path(png_path), Path(output_path), template_name, realtime=realtime)


def convert_markdown_to_note(
    markdown_path: str | Path,
    output_path: str | Path,
    device: str = "A5X2",
    language: str = "en_GB",
    realtime: bool = False,
    page_size: str = "A5",
    margin: str = "2cm",
    font_size: int = 11,
) -> None:
    """Convert Markdown file to .note file.

    This converts a Markdown file to a Supernote .note file by first
    converting to PDF using Pandoc, then converting the PDF to .note format.

    Requires Pandoc to be installed:
        Windows: choco install pandoc
        Mac: brew install pandoc
        Linux: apt install pandoc

    Args:
        markdown_path: Path to input Markdown file
        output_path: Path to output .note file
        device: Target device (A5X, A5X2/Manta, A6X, A6X2/Nomad)
        language: Recognition language (used when realtime=True)
        realtime: Enable realtime handwriting recognition mode
        page_size: PDF page size (A4, A5, A6, Letter)
        margin: Page margins (e.g., "2cm", "1in")
        font_size: Base font size in points
    """
    markdown_path = Path(markdown_path)
    output_path = Path(output_path)

    # Create temporary PDF file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
        tmp_pdf_path = Path(tmp_pdf.name)

    try:
        # Convert Markdown to PDF using Pandoc
        pandoc = PandocConverter(
            page_size=page_size,
            margin=margin,
            font_size=font_size,
        )
        pandoc.convert(markdown_path, tmp_pdf_path)

        # Convert PDF to .note
        writer = NoteFileWriter(device=device, language=language)
        writer.convert_pdf_to_note(tmp_pdf_path, output_path, realtime=realtime)

    finally:
        # Clean up temporary PDF file
        if tmp_pdf_path.exists():
            tmp_pdf_path.unlink()
