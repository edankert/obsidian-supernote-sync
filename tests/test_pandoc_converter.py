"""Tests for Pandoc-based markdown to PDF converter."""

import pytest
import shutil
from pathlib import Path
from obsidian_supernote.converters.pandoc_converter import PandocConverter


# Check if Pandoc is available
PANDOC_AVAILABLE = shutil.which("pandoc") is not None

requires_pandoc = pytest.mark.skipif(
    not PANDOC_AVAILABLE,
    reason="Pandoc not installed. Install from https://pandoc.org/installing.html"
)


@pytest.fixture
def sample_markdown(tmp_path: Path) -> Path:
    """Create a sample markdown file for testing."""
    md_file = tmp_path / "test.md"
    content = """---
title: Test Document
date: 2026-01-14
author: Test User
---

# Test Document

This is a test markdown file for Pandoc conversion.

## Features

- **Bold text**
- *Italic text*
- `Code inline`

### Code Blocks

```python
def hello():
    print("Hello, Supernote!")
```

### Lists

1. First item
2. Second item
3. Third item

### Tables

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| A        | B        | C        |
| 1        | 2        | 3        |

### Links

Visit [Supernote](https://supernote.com) for more information.

## Conclusion

This should convert nicely to PDF.
"""
    md_file.write_text(content, encoding="utf-8")
    return md_file


def test_pandoc_availability() -> None:
    """Test that indicates if Pandoc is available."""
    if not PANDOC_AVAILABLE:
        pytest.skip("Pandoc not available")
    else:
        # Test we can get version
        converter = PandocConverter()
        version = converter.get_pandoc_version()
        assert version
        assert len(version) > 0


@requires_pandoc
def test_converter_initialization() -> None:
    """Test that Pandoc converter can be initialized."""
    converter = PandocConverter(page_size="A5", margin="2cm", font_size=11)
    assert converter.page_size == "A5"
    assert converter.margin == "2cm"
    assert converter.font_size == 11


@requires_pandoc
def test_convert_markdown_file(sample_markdown: Path, tmp_path: Path) -> None:
    """Test full markdown to PDF conversion with Pandoc."""
    converter = PandocConverter(page_size="A5")
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


@requires_pandoc
def test_page_sizes(sample_markdown: Path, tmp_path: Path) -> None:
    """Test different page size configurations."""
    for page_size in ["A4", "A5", "A6", "Letter"]:
        converter = PandocConverter(page_size=page_size)
        output_pdf = tmp_path / f"output_{page_size}.pdf"

        converter.convert(sample_markdown, output_pdf)

        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0


@requires_pandoc
def test_build_command(sample_markdown: Path, tmp_path: Path) -> None:
    """Test that Pandoc command is built correctly."""
    converter = PandocConverter(page_size="A5", margin="1.5cm", font_size=12)
    output_pdf = tmp_path / "output.pdf"

    cmd = converter._build_command(sample_markdown, output_pdf, None, None, None)

    # Check essential components
    assert "pandoc" in cmd
    assert str(sample_markdown) in cmd
    assert "-o" in cmd
    assert str(output_pdf) in cmd
    assert any("a5" in str(arg) for arg in cmd)  # Page size
    assert any("1.5cm" in str(arg) for arg in cmd)  # Margin
    assert any("12pt" in str(arg) for arg in cmd)  # Font size


@requires_pandoc
def test_convert_with_margins(sample_markdown: Path, tmp_path: Path) -> None:
    """Test conversion with custom margins."""
    converter = PandocConverter(page_size="A5", margin="3cm")
    output_pdf = tmp_path / "output.pdf"

    converter.convert(sample_markdown, output_pdf)

    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0


@requires_pandoc
def test_convert_with_font_size(sample_markdown: Path, tmp_path: Path) -> None:
    """Test conversion with custom font size."""
    converter = PandocConverter(page_size="A5", font_size=14)
    output_pdf = tmp_path / "output.pdf"

    converter.convert(sample_markdown, output_pdf)

    assert output_pdf.exists()
    # Larger font should generally mean larger file
    assert output_pdf.stat().st_size > 0


def test_no_pandoc_raises_error() -> None:
    """Test that missing Pandoc raises appropriate error."""
    if PANDOC_AVAILABLE:
        pytest.skip("Pandoc is available, cannot test error case")

    with pytest.raises(RuntimeError) as exc_info:
        PandocConverter()

    assert "Pandoc is not installed" in str(exc_info.value)


@requires_pandoc
def test_pandoc_version_format() -> None:
    """Test that Pandoc version is in expected format."""
    converter = PandocConverter()
    version = converter.get_pandoc_version()

    # Version should be like "3.1.11" or similar
    parts = version.split(".")
    assert len(parts) >= 2
    assert parts[0].isdigit()
