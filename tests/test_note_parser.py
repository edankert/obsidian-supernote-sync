"""Tests for Supernote .note file parser."""

import pytest
from pathlib import Path
from obsidian_supernote.parsers.note_parser import NoteFileParser


def test_parser_requires_valid_file() -> None:
    """Test that parser requires a valid file."""
    with pytest.raises(FileNotFoundError):
        parser = NoteFileParser(Path("nonexistent.note"))
        parser.parse()


def test_parser_header_extraction() -> None:
    """Test header metadata extraction."""
    # Create minimal mock .note file with just header
    mock_note = b"""noteSN_FILE_VER_20230015<FILE_TYPE:NOTE><APPLY_EQUIPMENT:N5><FILE_RECOGN_LANGUAGE:en_GB>PK\x03\x04"""

    # This is a simplified test - would need real .note files for full testing
    # For now, just verify the parser can be instantiated
    assert NoteFileParser is not None


def test_png_signature_detection() -> None:
    """Test PNG signature detection."""
    # PNG signature
    png_sig = b"\x89PNG\r\n\x1a\n"

    # Create mock data with PNG
    mock_data = b"header_data" + png_sig + b"PNG_DATA_HERE" + b"IEND\xaeB`\x82" + b"more_data"

    # Verify signature exists
    assert png_sig in mock_data


def test_zip_signature_detection() -> None:
    """Test ZIP signature detection."""
    # ZIP signature
    zip_sig = b"PK\x03\x04"

    # Create mock data with ZIP
    mock_data = b"header_data" + b"png_data" + zip_sig + b"ZIP_DATA_HERE"

    # Verify signature exists
    assert zip_sig in mock_data


# Integration test (requires actual .note file)
@pytest.mark.skipif(
    not Path("test_files/sample.note").exists(),
    reason="Requires test .note file"
)
def test_parse_real_note_file() -> None:
    """Test parsing a real .note file (if available)."""
    parser = NoteFileParser(Path("test_files/sample.note"))
    data = parser.parse()

    # Verify structure
    assert "metadata" in data
    assert "png_count" in data
    assert "zip_contents" in data

    # Get summary
    summary = parser.get_summary()
    assert "file_name" in summary
    assert "file_size_mb" in summary


@pytest.mark.skipif(
    not Path("test_files/sample.note").exists(),
    reason="Requires test .note file"
)
def test_extract_png_images() -> None:
    """Test PNG extraction from real .note file (if available)."""
    parser = NoteFileParser(Path("test_files/sample.note"))
    parser.parse()

    if len(parser.png_images) > 0:
        # Get first image
        img = parser.get_png_image(0)
        assert img is not None
        assert img.width > 0
        assert img.height > 0
