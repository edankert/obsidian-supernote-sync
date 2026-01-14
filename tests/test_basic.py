"""Basic tests to verify package structure."""

import obsidian_supernote


def test_version() -> None:
    """Test that version is defined."""
    assert obsidian_supernote.__version__
    assert isinstance(obsidian_supernote.__version__, str)


def test_author() -> None:
    """Test that author is defined."""
    assert obsidian_supernote.__author__ == "Edwin"
