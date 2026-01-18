"""Convert Supernote .note files to Obsidian-compatible formats (PNG, Markdown)."""

from pathlib import Path
from typing import List, Optional
from datetime import datetime

from supernotelib import load_notebook
from supernotelib.converter import ImageConverter


class NoteToObsidianConverter:
    """Convert Supernote .note files to PNG images and Markdown.

    Uses supernotelib to parse .note files and render pages as images.
    """

    def __init__(self, note_path: Path):
        """Initialize converter with a .note file.

        Args:
            note_path: Path to Supernote .note file
        """
        self.note_path = Path(note_path)
        self.notebook = load_notebook(str(self.note_path))
        self.image_converter = ImageConverter(self.notebook)

    @property
    def page_count(self) -> int:
        """Get number of pages in the notebook."""
        return len(self.notebook.pages)

    @property
    def title(self) -> Optional[str]:
        """Get notebook title if available."""
        try:
            return self.notebook.get_title()
        except Exception:
            return None

    def convert_page_to_png(self, page_num: int, output_path: Path) -> Path:
        """Convert a single page to PNG.

        Args:
            page_num: Page number (0-indexed)
            output_path: Path to save PNG file

        Returns:
            Path to saved PNG file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        img = self.image_converter.convert(page_num)
        img.save(output_path, "PNG")

        return output_path

    def convert_all_pages_to_png(self, output_dir: Path) -> List[Path]:
        """Convert all pages to PNG images.

        Args:
            output_dir: Directory to save PNG files

        Returns:
            List of paths to saved PNG files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []
        stem = self.note_path.stem

        for page_num in range(self.page_count):
            output_path = output_dir / f"{stem}_page_{page_num + 1:02d}.png"
            self.convert_page_to_png(page_num, output_path)
            saved_files.append(output_path)

        return saved_files

    def convert_to_markdown(
        self,
        output_path: Path,
        image_dir: Optional[Path] = None,
        embed_images: bool = True,
    ) -> Path:
        """Convert .note file to Markdown with embedded/linked images.

        Args:
            output_path: Path to save Markdown file
            image_dir: Directory to save images (default: same as markdown)
            embed_images: If True, use Obsidian image embeds (![[image]])

        Returns:
            Path to saved Markdown file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if image_dir is None:
            image_dir = output_path.parent

        # Convert all pages to PNG
        png_files = self.convert_all_pages_to_png(image_dir)

        # Build markdown content
        md_content = self._build_markdown(png_files, embed_images)

        # Write markdown file
        output_path.write_text(md_content, encoding="utf-8")

        return output_path

    def _build_markdown(
        self,
        png_files: List[Path],
        embed_images: bool = True,
    ) -> str:
        """Build markdown content with frontmatter and image embeds.

        Args:
            png_files: List of PNG file paths
            embed_images: If True, use Obsidian image embeds

        Returns:
            Markdown content string
        """
        lines = []

        # YAML frontmatter
        title = self.title or self.note_path.stem
        now = datetime.now().strftime("%Y-%m-%d")

        lines.append("---")
        lines.append(f"title: \"{title}\"")
        lines.append(f"source: Supernote")
        lines.append(f"source_file: \"{self.note_path.name}\"")
        lines.append(f"pages: {self.page_count}")
        lines.append(f"imported: {now}")
        lines.append("---")
        lines.append("")

        # Title
        lines.append(f"# {title}")
        lines.append("")

        # Image embeds
        for i, png_path in enumerate(png_files, start=1):
            if embed_images:
                # Obsidian-style embed
                lines.append(f"## Page {i}")
                lines.append(f"![[{png_path.name}]]")
            else:
                # Standard markdown image
                lines.append(f"## Page {i}")
                lines.append(f"![Page {i}]({png_path.name})")
            lines.append("")

        return "\n".join(lines)


def convert_note_to_png(
    note_path: str | Path,
    output_dir: str | Path,
) -> List[Path]:
    """Convenience function to convert .note file to PNG images.

    Args:
        note_path: Path to .note file
        output_dir: Directory to save PNG files

    Returns:
        List of paths to saved PNG files
    """
    converter = NoteToObsidianConverter(Path(note_path))
    return converter.convert_all_pages_to_png(Path(output_dir))


def convert_note_to_markdown(
    note_path: str | Path,
    output_path: str | Path,
    image_dir: Optional[str | Path] = None,
) -> Path:
    """Convenience function to convert .note file to Markdown.

    Args:
        note_path: Path to .note file
        output_path: Path to save Markdown file
        image_dir: Optional directory for images

    Returns:
        Path to saved Markdown file
    """
    converter = NoteToObsidianConverter(Path(note_path))
    img_dir = Path(image_dir) if image_dir else None
    return converter.convert_to_markdown(Path(output_path), img_dir)
