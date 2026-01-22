"""Utility functions and helpers.

This module provides common utilities:
- File system operations
- Hash calculation
- Configuration loading
- Logging setup
- Frontmatter parsing for Obsidian markdown files
"""

from obsidian_supernote.utils.frontmatter import (
    FrontmatterProperties,
    extract_frontmatter,
    parse_frontmatter_properties,
    read_markdown_with_frontmatter,
    format_note_file_reference,
    update_frontmatter_file_reference,
)

__all__ = [
    "FrontmatterProperties",
    "extract_frontmatter",
    "parse_frontmatter_properties",
    "read_markdown_with_frontmatter",
    "format_note_file_reference",
    "update_frontmatter_file_reference",
]
