"""File format parsers.

This module provides parsers for reading and understanding different file formats:
- .note file parser (Supernote native format)
- PDF template parser
- Markdown frontmatter parser
"""

from obsidian_supernote.parsers.note_parser import NoteFileParser

__all__ = [
    "NoteFileParser",
]
