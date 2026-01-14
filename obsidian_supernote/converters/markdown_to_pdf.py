"""Convert Markdown files to PDF optimized for Supernote devices."""

import re
from pathlib import Path
from typing import Optional
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


class MarkdownToPdfConverter:
    """Convert Markdown to PDF optimized for Supernote e-ink display."""

    # Supernote display dimensions (A5X: 1404x1872, A6X: 1404x1872)
    # PDF sizes optimized for e-ink readability
    PAGE_SIZES = {
        "A4": "210mm 297mm",
        "A5": "148mm 210mm",
        "A6": "105mm 148mm",
        "Letter": "8.5in 11in",
    }

    def __init__(self, page_size: str = "A5", dpi: int = 300):
        """Initialize the converter.

        Args:
            page_size: PDF page size (A4, A5, A6, Letter)
            dpi: Image resolution for quality
        """
        self.page_size = page_size
        self.dpi = dpi
        self.font_config = FontConfiguration()

    def convert(
        self, markdown_file: Path, output_pdf: Path, css_file: Optional[Path] = None
    ) -> None:
        """Convert a Markdown file to PDF.

        Args:
            markdown_file: Path to input markdown file
            output_pdf: Path to output PDF file
            css_file: Optional custom CSS file for styling
        """
        # Read markdown file
        markdown_content = markdown_file.read_text(encoding="utf-8")

        # Strip YAML frontmatter (Obsidian-style)
        markdown_content = self._strip_frontmatter(markdown_content)

        # Convert Obsidian wikilinks to regular markdown links
        markdown_content = self._convert_wikilinks(markdown_content)

        # Convert markdown to HTML
        html_content = self._markdown_to_html(markdown_content)

        # Wrap in HTML document with styling
        full_html = self._wrap_html(html_content, markdown_file.stem)

        # Apply CSS styling
        css = self._get_css(css_file)

        # Convert HTML to PDF using WeasyPrint
        html_doc = HTML(string=full_html, base_url=str(markdown_file.parent))
        html_doc.write_pdf(
            output_pdf,
            stylesheets=[CSS(string=css, font_config=self.font_config)],
            font_config=self.font_config,
        )

    def _strip_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from markdown content.

        Args:
            content: Markdown content with potential frontmatter

        Returns:
            Content without frontmatter
        """
        # Match YAML frontmatter (--- ... ---)
        pattern = r"^---\s*\n.*?\n---\s*\n"
        return re.sub(pattern, "", content, flags=re.DOTALL)

    def _convert_wikilinks(self, content: str) -> str:
        """Convert Obsidian wikilinks [[link]] to markdown links.

        Args:
            content: Markdown content with wikilinks

        Returns:
            Content with standard markdown links
        """
        # Convert [[Link]] to [Link](Link)
        content = re.sub(r"\[\[([^\]|]+)\]\]", r"[\1](\1)", content)

        # Convert [[Link|Display Text]] to [Display Text](Link)
        content = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"[\2](\1)", content)

        return content

    def _markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML.

        Args:
            markdown_content: Markdown text

        Returns:
            HTML content
        """
        md = markdown.Markdown(
            extensions=[
                "extra",  # Tables, fenced code, etc.
                "codehilite",  # Syntax highlighting
                "nl2br",  # Newline to <br>
                "sane_lists",  # Better list handling
                "toc",  # Table of contents
            ]
        )
        return md.convert(markdown_content)

    def _wrap_html(self, body_html: str, title: str) -> str:
        """Wrap HTML body in a complete HTML document.

        Args:
            body_html: HTML body content
            title: Document title

        Returns:
            Complete HTML document
        """
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
</head>
<body>
    {body_html}
</body>
</html>"""

    def _get_css(self, custom_css: Optional[Path] = None) -> str:
        """Get CSS styling for PDF.

        Args:
            custom_css: Optional path to custom CSS file

        Returns:
            CSS content as string
        """
        if custom_css and custom_css.exists():
            return custom_css.read_text(encoding="utf-8")

        # Default CSS optimized for e-ink display
        page_size = self.PAGE_SIZES.get(self.page_size, self.PAGE_SIZES["A5"])

        return f"""
@page {{
    size: {page_size};
    margin: 2cm 1.5cm;
}}

body {{
    font-family: "Georgia", "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #000000;
    background-color: #ffffff;
}}

/* Headings */
h1 {{
    font-size: 20pt;
    font-weight: bold;
    margin-top: 0.5em;
    margin-bottom: 0.3em;
    page-break-after: avoid;
}}

h2 {{
    font-size: 16pt;
    font-weight: bold;
    margin-top: 0.5em;
    margin-bottom: 0.3em;
    page-break-after: avoid;
}}

h3 {{
    font-size: 14pt;
    font-weight: bold;
    margin-top: 0.4em;
    margin-bottom: 0.2em;
    page-break-after: avoid;
}}

h4, h5, h6 {{
    font-size: 12pt;
    font-weight: bold;
    margin-top: 0.3em;
    margin-bottom: 0.2em;
    page-break-after: avoid;
}}

/* Paragraphs */
p {{
    margin-top: 0.3em;
    margin-bottom: 0.3em;
    text-align: left;
}}

/* Lists */
ul, ol {{
    margin-top: 0.3em;
    margin-bottom: 0.3em;
    padding-left: 2em;
}}

li {{
    margin-bottom: 0.2em;
}}

/* Code blocks */
pre {{
    background-color: #f5f5f5;
    border: 1px solid #cccccc;
    padding: 0.5em;
    overflow-x: auto;
    font-family: "Courier New", monospace;
    font-size: 9pt;
    line-height: 1.4;
}}

code {{
    font-family: "Courier New", monospace;
    font-size: 10pt;
    background-color: #f5f5f5;
    padding: 0.1em 0.3em;
}}

/* Tables */
table {{
    border-collapse: collapse;
    width: 100%;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}}

th, td {{
    border: 1px solid #000000;
    padding: 0.3em;
    text-align: left;
}}

th {{
    background-color: #e0e0e0;
    font-weight: bold;
}}

/* Blockquotes */
blockquote {{
    border-left: 3px solid #cccccc;
    margin-left: 0;
    padding-left: 1em;
    color: #333333;
    font-style: italic;
}}

/* Links */
a {{
    color: #000000;
    text-decoration: underline;
}}

/* Horizontal rules */
hr {{
    border: none;
    border-top: 1px solid #000000;
    margin: 1em 0;
}}

/* Images */
img {{
    max-width: 100%;
    height: auto;
}}

/* Page breaks */
.page-break {{
    page-break-after: always;
}}
"""


def convert_markdown_to_pdf(
    markdown_file: str | Path,
    output_pdf: str | Path,
    page_size: str = "A5",
    dpi: int = 300,
    css_file: Optional[str | Path] = None,
) -> None:
    """Convenience function to convert markdown to PDF.

    Args:
        markdown_file: Path to input markdown file
        output_pdf: Path to output PDF file
        page_size: PDF page size (A4, A5, A6, Letter)
        dpi: Image resolution
        css_file: Optional custom CSS file
    """
    converter = MarkdownToPdfConverter(page_size=page_size, dpi=dpi)
    converter.convert(
        Path(markdown_file),
        Path(output_pdf),
        Path(css_file) if css_file else None,
    )
