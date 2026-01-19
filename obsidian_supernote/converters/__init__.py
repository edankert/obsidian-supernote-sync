"""File format converters.

This module provides converters for transforming files between different formats:
- Markdown to PDF (Pandoc or WeasyPrint)
- PDF to PNG
- .note to Markdown
- Markdown to .note
- PDF to .note
- PNG to .note
"""

from obsidian_supernote.converters.pandoc_converter import PandocConverter
from obsidian_supernote.converters.note_writer import (
    NoteFileWriter,
    convert_pdf_to_note,
    convert_png_to_note,
    convert_markdown_to_note,
)

# WeasyPrint converter (requires GTK+ on Windows)
try:
    from obsidian_supernote.converters.markdown_to_pdf import MarkdownToPdfConverter
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    MarkdownToPdfConverter = None  # type: ignore
    WEASYPRINT_AVAILABLE = False

__all__ = [
    "PandocConverter",
    "MarkdownToPdfConverter",
    "WEASYPRINT_AVAILABLE",
    "NoteFileWriter",
    "convert_pdf_to_note",
    "convert_png_to_note",
    "convert_markdown_to_note",
]
