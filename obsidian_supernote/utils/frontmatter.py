"""Parse frontmatter properties from Obsidian markdown files."""

import re
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import os


class FrontmatterProperties:
    """Parsed frontmatter properties for Supernote conversion.

    Attributes:
        supernote_type: Type of .note file ("standard" or "realtime")
        supernote_file: Path to existing .note file to update (optional)
        raw_frontmatter: Raw YAML frontmatter dict (for debugging)
    """

    def __init__(
        self,
        supernote_type: str = "standard",
        supernote_file: Optional[str] = None,
        raw_frontmatter: Optional[Dict[str, Any]] = None,
    ):
        """Initialize frontmatter properties.

        Args:
            supernote_type: Type of .note file ("standard" or "realtime")
            supernote_file: Path to existing .note file to update
            raw_frontmatter: Raw YAML frontmatter for reference
        """
        self.supernote_type = supernote_type
        self.supernote_file = supernote_file
        self.raw_frontmatter = raw_frontmatter or {}

    @property
    def realtime(self) -> bool:
        """Convert supernote_type to realtime boolean.

        Returns:
            True if type is "realtime", False if "standard"
        """
        return self.supernote_type == "realtime"

    def get_absolute_file_path(self, markdown_path: Path) -> Optional[Path]:
        """Get absolute path to the .note file referenced in supernote.file.

        The supernote.file property uses [x.note] notation for relative paths.
        This resolves them relative to the markdown file's directory.

        Args:
            markdown_path: Path to the markdown file

        Returns:
            Absolute path to .note file, or None if supernote.file is not set
        """
        if self.supernote_file is None:
            return None

        # Strip brackets if present
        file_path = self.supernote_file.strip()
        if file_path.startswith('[') and file_path.endswith(']'):
            file_path = file_path[1:-1]

        # Convert to Path and resolve relative to markdown file
        note_path = Path(file_path)
        if not note_path.is_absolute():
            # Resolve relative to markdown file's directory
            note_path = (markdown_path.parent / note_path).resolve()

        return note_path

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"FrontmatterProperties(type={self.supernote_type!r}, "
            f"file={self.supernote_file!r})"
        )


def extract_frontmatter(markdown_content: str) -> tuple[Optional[Dict[str, Any]], str]:
    """Extract YAML frontmatter from markdown content.

    Obsidian frontmatter format:
    ---
    title: My Note
    supernote.type: realtime
    supernote.file: "Journal/2026-01-20.note"
    ---

    # Content starts here...

    Args:
        markdown_content: Full markdown file content

    Returns:
        Tuple of (frontmatter_dict, content_without_frontmatter)
        Returns (None, original_content) if no frontmatter found
    """
    # Match YAML frontmatter (--- ... ---)
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, markdown_content, flags=re.DOTALL)

    if not match:
        return None, markdown_content

    # Extract YAML content
    yaml_content = match.group(1)

    # Remove frontmatter from content
    content_without_frontmatter = markdown_content[match.end():]

    try:
        # Parse YAML
        frontmatter = yaml.safe_load(yaml_content)
        if not isinstance(frontmatter, dict):
            # Invalid YAML structure
            return None, markdown_content
        return frontmatter, content_without_frontmatter
    except yaml.YAMLError:
        # Failed to parse YAML - return original content
        return None, markdown_content


def parse_frontmatter_properties(
    frontmatter: Optional[Dict[str, Any]],
    warn: bool = True,
) -> FrontmatterProperties:
    """Parse Supernote properties from frontmatter dict.

    Extracts and validates:
    - supernote.type: "standard" (default) or "realtime"
    - supernote.file: Optional path to .note file to update

    Args:
        frontmatter: Parsed YAML frontmatter dict (or None)
        warn: Whether to print warnings for invalid values

    Returns:
        FrontmatterProperties with validated values and defaults
    """
    if frontmatter is None:
        frontmatter = {}

    # Extract supernote.type (default: "standard")
    supernote_type = frontmatter.get("supernote.type", "standard")

    # Validate supernote_type
    valid_types = ["standard", "realtime"]
    if supernote_type not in valid_types:
        if warn:
            print(
                f"Warning: Invalid supernote.type '{supernote_type}'. "
                f"Valid values: {valid_types}. Using default: 'standard'"
            )
        supernote_type = "standard"

    # Extract supernote.file (optional)
    supernote_file = frontmatter.get("supernote.file")

    # Validate supernote_file if present
    if supernote_file is not None:
        if not isinstance(supernote_file, str):
            if warn:
                print(
                    f"Warning: supernote.file must be a string, got {type(supernote_file).__name__}. "
                    f"Ignoring value."
                )
            supernote_file = None
        elif supernote_file.strip() == "":
            # Empty string is same as None
            supernote_file = None

    return FrontmatterProperties(
        supernote_type=supernote_type,
        supernote_file=supernote_file,
        raw_frontmatter=frontmatter,
    )


def read_markdown_with_frontmatter(
    markdown_path: Path,
    warn: bool = True,
) -> tuple[FrontmatterProperties, str]:
    """Read markdown file and extract frontmatter properties.

    Convenience function that combines file reading, extraction, and parsing.

    Args:
        markdown_path: Path to markdown file
        warn: Whether to print warnings for invalid values

    Returns:
        Tuple of (FrontmatterProperties, content_without_frontmatter)

    Example:
        >>> props, content = read_markdown_with_frontmatter(Path("note.md"))
        >>> print(f"Type: {props.supernote_type}, Realtime: {props.realtime}")
        Type: realtime, Realtime: True
    """
    # Read markdown file
    markdown_content = markdown_path.read_text(encoding="utf-8")

    # Extract frontmatter
    frontmatter, content = extract_frontmatter(markdown_content)

    # Parse properties
    properties = parse_frontmatter_properties(frontmatter, warn=warn)

    return properties, content


def format_note_file_reference(note_path: Path, markdown_path: Path) -> str:
    """Format .note file path as [x.note] notation relative to markdown file.

    Args:
        note_path: Absolute path to .note file
        markdown_path: Absolute path to markdown file

    Returns:
        Formatted reference like "[output/daily-note.note]"

    Example:
        >>> format_note_file_reference(
        ...     Path("/vault/output/note.note"),
        ...     Path("/vault/daily.md")
        ... )
        '[output/note.note]'
    """
    # Get relative path from markdown file to note file
    try:
        # Try to compute relative path
        rel_path = os.path.relpath(note_path, markdown_path.parent)
        # Normalize path separators to forward slashes (cross-platform)
        rel_path = rel_path.replace('\\', '/')
        return f"[{rel_path}]"
    except ValueError:
        # Different drives on Windows - use absolute path
        abs_path = str(note_path).replace('\\', '/')
        return f"[{abs_path}]"


def update_frontmatter_file_reference(
    markdown_path: Path,
    note_path: Path,
) -> None:
    """Update the supernote.file property in markdown frontmatter.

    Adds or updates the supernote.file property with a reference to the
    created .note file. Uses [x.note] notation for relative paths.

    If no frontmatter exists, creates it with just the supernote.file property.
    If frontmatter exists, updates supernote.file while preserving other properties.

    Args:
        markdown_path: Path to markdown file to update
        note_path: Path to .note file to reference

    Example:
        After calling this function, the markdown file will have:
        ---
        title: My Note
        supernote.file: "[output/my-note.note]"
        ---
    """
    # Read current content
    markdown_content = markdown_path.read_text(encoding="utf-8")

    # Extract existing frontmatter
    frontmatter, content = extract_frontmatter(markdown_content)

    # Create or update frontmatter dict
    if frontmatter is None:
        frontmatter = {}

    # Format the file reference
    file_reference = format_note_file_reference(note_path, markdown_path)

    # Update the supernote.file property
    frontmatter["supernote.file"] = file_reference

    # Convert frontmatter back to YAML
    yaml_content = yaml.safe_dump(
        frontmatter,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )

    # Rebuild markdown with updated frontmatter
    new_content = f"---\n{yaml_content}---\n\n{content}"

    # Write back to file
    markdown_path.write_text(new_content, encoding="utf-8")
