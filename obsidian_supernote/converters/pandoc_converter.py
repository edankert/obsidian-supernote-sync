"""Convert Markdown files to PDF using Pandoc."""

import subprocess
import shutil
from pathlib import Path
from typing import Optional, List


class PandocConverter:
    """Convert Markdown to PDF using Pandoc.

    Pandoc is a universal document converter that many Obsidian users
    already have installed. It provides excellent markdown support and
    high-quality PDF output without requiring complex dependencies.

    Installation:
        Windows: choco install pandoc
        Mac: brew install pandoc
        Linux: apt install pandoc / dnf install pandoc
        Or download from: https://pandoc.org/installing.html
    """

    # Page sizes for PDF generation
    PAGE_SIZES = {
        "A4": "a4",
        "A5": "a5",
        "A6": "a6",
        "Letter": "letter",
    }

    def __init__(
        self,
        page_size: str = "A5",
        margin: str = "2cm",
        font_size: int = 11,
    ):
        """Initialize the Pandoc converter.

        Args:
            page_size: PDF page size (A4, A5, A6, Letter)
            margin: Page margins (e.g., "2cm", "1in")
            font_size: Base font size in points
        """
        self.page_size = page_size
        self.margin = margin
        self.font_size = font_size
        self._check_pandoc()

    def _check_pandoc(self) -> None:
        """Check if Pandoc is available."""
        if not shutil.which("pandoc"):
            raise RuntimeError(
                "Pandoc is not installed or not in PATH.\n"
                "Install from: https://pandoc.org/installing.html\n"
                "Windows: choco install pandoc\n"
                "Mac: brew install pandoc\n"
                "Linux: apt install pandoc"
            )

    def get_pandoc_version(self) -> str:
        """Get the installed Pandoc version.

        Returns:
            Version string (e.g., "3.1.11")
        """
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        # First line is like "pandoc 3.1.11"
        first_line = result.stdout.split("\n")[0]
        return first_line.split()[1] if len(first_line.split()) > 1 else "unknown"

    def convert(
        self,
        markdown_file: Path,
        output_pdf: Path,
        metadata_file: Optional[Path] = None,
        css_file: Optional[Path] = None,
        template_file: Optional[Path] = None,
    ) -> None:
        """Convert a Markdown file to PDF using Pandoc.

        Args:
            markdown_file: Path to input markdown file
            output_pdf: Path to output PDF file
            metadata_file: Optional YAML metadata file
            css_file: Optional CSS file for styling (via --css)
            template_file: Optional Pandoc template file
        """
        markdown_file = Path(markdown_file)
        output_pdf = Path(output_pdf)

        # Build Pandoc command
        cmd = self._build_command(
            markdown_file,
            output_pdf,
            metadata_file,
            css_file,
            template_file,
        )

        # Run Pandoc
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=markdown_file.parent,  # Run in source directory for relative paths
        )

        if result.returncode != 0:
            raise RuntimeError(f"Pandoc conversion failed:\n{result.stderr}")

    def _build_command(
        self,
        markdown_file: Path,
        output_pdf: Path,
        metadata_file: Optional[Path],
        css_file: Optional[Path],
        template_file: Optional[Path],
    ) -> List[str]:
        """Build the Pandoc command with all options.

        Args:
            markdown_file: Input markdown file
            output_pdf: Output PDF file
            metadata_file: Optional metadata file
            css_file: Optional CSS file
            template_file: Optional template file

        Returns:
            Command as list of strings
        """
        cmd = [
            "pandoc",
            str(markdown_file),
            "-o", str(output_pdf),
            "--from", "markdown+yaml_metadata_block+wikilinks_title_after_pipe",
            "--pdf-engine", "pdflatex",  # or xelatex for better Unicode support
            "-V", f"geometry:papersize={{{self.PAGE_SIZES.get(self.page_size, 'a5')}}}",
            "-V", f"geometry:margin={self.margin}",
            "-V", f"fontsize={self.font_size}pt",
            "--highlight-style", "tango",  # Syntax highlighting for code blocks
            "--table-of-contents",  # Add TOC
            "--toc-depth", "3",
            "--number-sections",  # Number headings
        ]

        # Add metadata file if provided
        if metadata_file and metadata_file.exists():
            cmd.extend(["--metadata-file", str(metadata_file)])

        # Add CSS file if provided (for HTML intermediate step)
        if css_file and css_file.exists():
            cmd.extend(["--css", str(css_file)])

        # Add template if provided
        if template_file and template_file.exists():
            cmd.extend(["--template", str(template_file)])

        # Additional Pandoc options for better output
        cmd.extend([
            "--standalone",  # Produce a standalone document
        ])

        return cmd

    def convert_with_options(
        self,
        markdown_file: Path,
        output_pdf: Path,
        **pandoc_options: str,
    ) -> None:
        """Convert with custom Pandoc options.

        Args:
            markdown_file: Input markdown file
            output_pdf: Output PDF file
            **pandoc_options: Additional Pandoc options as key-value pairs
                Example: pdf_engine="xelatex", highlight_style="pygments"
        """
        markdown_file = Path(markdown_file)
        output_pdf = Path(output_pdf)

        cmd = [
            "pandoc",
            str(markdown_file),
            "-o", str(output_pdf),
        ]

        # Add custom options
        for key, value in pandoc_options.items():
            # Convert Python parameter names to Pandoc flags
            # e.g., pdf_engine -> --pdf-engine
            flag = f"--{key.replace('_', '-')}"
            if value is True:
                cmd.append(flag)
            elif value is not False:
                cmd.extend([flag, str(value)])

        # Run Pandoc
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=markdown_file.parent,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Pandoc conversion failed:\n{result.stderr}")


def convert_markdown_to_pdf_pandoc(
    markdown_file: str | Path,
    output_pdf: str | Path,
    page_size: str = "A5",
    margin: str = "2cm",
    font_size: int = 11,
) -> None:
    """Convenience function to convert markdown to PDF using Pandoc.

    Args:
        markdown_file: Path to input markdown file
        output_pdf: Path to output PDF file
        page_size: PDF page size (A4, A5, A6, Letter)
        margin: Page margins
        font_size: Base font size in points
    """
    converter = PandocConverter(
        page_size=page_size,
        margin=margin,
        font_size=font_size,
    )
    converter.convert(Path(markdown_file), Path(output_pdf))
