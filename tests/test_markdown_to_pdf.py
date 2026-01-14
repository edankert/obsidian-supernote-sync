"""Tests for Markdown to PDF converter."""

import pytest
from pathlib import Path

# Try to import weasyprint, skip tests if not available
try:
    from obsidian_supernote.converters.markdown_to_pdf import MarkdownToPdfConverter
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False
    MarkdownToPdfConverter = None  # type: ignore


requires_weasyprint = pytest.mark.skipif(
    not WEASYPRINT_AVAILABLE,
    reason="WeasyPrint requires GTK+ libraries. See docs/WEASYPRINT_SETUP.md"
)


@pytest.fixture
def sample_markdown(tmp_path: Path) -> Path:
    """Create a sample markdown file for testing."""
    md_file = tmp_path / "test.md"
    content = """---
title: Test Document
date: 2026-01-14
---

# Test Document

This is a test markdown file with **bold** and *italic* text.

## Lists

- Item 1
- Item 2
- Item 3

## Code

```python
def hello():
    print("Hello, World!")
```

## Links

This is a [[wikilink]] and a [regular link](https://example.com).
"""
    md_file.write_text(content, encoding="utf-8")
    return md_file


@requires_weasyprint
def test_converter_initialization() -> None:
    """Test that converter can be initialized."""
    converter = MarkdownToPdfConverter(page_size="A5", dpi=300)
    assert converter.page_size == "A5"
    assert converter.dpi == 300


@requires_weasyprint
def test_strip_frontmatter() -> None:
    """Test YAML frontmatter removal."""
    converter = MarkdownToPdfConverter()

    content_with_fm = """---
title: Test
date: 2026-01-14
---

# Content"""

    result = converter._strip_frontmatter(content_with_fm)
    assert "---" not in result
    assert "title:" not in result
    assert "# Content" in result


@requires_weasyprint
def test_convert_wikilinks() -> None:
    """Test Obsidian wikilink conversion."""
    converter = MarkdownToPdfConverter()

    # Simple wikilink
    content = "This is a [[link]] here."
    result = converter._convert_wikilinks(content)
    assert "[[link]]" not in result
    assert "[link](link)" in result

    # Wikilink with display text
    content = "This is [[link|display text]] here."
    result = converter._convert_wikilinks(content)
    assert "[[link|display text]]" not in result
    assert "[display text](link)" in result


@requires_weasyprint
def test_markdown_to_html() -> None:
    """Test markdown to HTML conversion."""
    converter = MarkdownToPdfConverter()

    markdown_content = """# Heading

**Bold** and *italic* text.

- List item 1
- List item 2
"""

    html = converter._markdown_to_html(markdown_content)
    assert "<h1>Heading</h1>" in html
    assert "<strong>Bold</strong>" in html
    assert "<em>italic</em>" in html
    assert "<li>List item 1</li>" in html


@requires_weasyprint
def test_convert_markdown_file(sample_markdown: Path, tmp_path: Path) -> None:
    """Test full markdown to PDF conversion."""
    converter = MarkdownToPdfConverter(page_size="A5")
    output_pdf = tmp_path / "output.pdf"

    # Convert
    converter.convert(sample_markdown, output_pdf)

    # Check output exists
    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0

    # Check it's a PDF (starts with %PDF)
    with open(output_pdf, "rb") as f:
        header = f.read(4)
        assert header == b"%PDF"


@requires_weasyprint
def test_page_sizes() -> None:
    """Test different page size configurations."""
    for page_size in ["A4", "A5", "A6", "Letter"]:
        converter = MarkdownToPdfConverter(page_size=page_size)
        assert converter.page_size == page_size
        # Check that page size is in CSS
        css = converter._get_css()
        assert page_size in css or converter.PAGE_SIZES[page_size] in css


def test_weasyprint_availability() -> None:
    """Test that indicates if WeasyPrint is available."""
    if not WEASYPRINT_AVAILABLE:
        pytest.skip("WeasyPrint not available - see docs/WEASYPRINT_SETUP.md")
    else:
        assert MarkdownToPdfConverter is not None
