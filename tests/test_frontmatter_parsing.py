"""Tests for frontmatter parsing functionality."""

import pytest
from pathlib import Path
from obsidian_supernote.utils.frontmatter import (
    FrontmatterProperties,
    extract_frontmatter,
    parse_frontmatter_properties,
    read_markdown_with_frontmatter,
    format_note_file_reference,
    update_frontmatter_file_reference,
)


class TestFrontmatterExtraction:
    """Test extracting YAML frontmatter from markdown content."""

    def test_extract_valid_frontmatter(self):
        """Test extracting valid YAML frontmatter."""
        content = """---
title: My Note
date: "2026-01-20"
supernote.type: realtime
---

# Content here
This is the actual note content.
"""
        frontmatter, remaining = extract_frontmatter(content)

        assert frontmatter is not None
        assert frontmatter["title"] == "My Note"
        assert frontmatter["date"] == "2026-01-20"
        assert frontmatter["supernote.type"] == "realtime"
        assert remaining.startswith("# Content here")

    def test_extract_no_frontmatter(self):
        """Test handling markdown without frontmatter."""
        content = """# My Note

This is just regular markdown content.
"""
        frontmatter, remaining = extract_frontmatter(content)

        assert frontmatter is None
        assert remaining == content

    def test_extract_empty_frontmatter(self):
        """Test handling empty frontmatter."""
        content = """---
---

# Content
"""
        frontmatter, remaining = extract_frontmatter(content)

        # Empty frontmatter should parse as None (no dict)
        assert frontmatter is None or frontmatter == {}
        assert "# Content" in remaining

    def test_extract_malformed_yaml(self):
        """Test handling malformed YAML in frontmatter."""
        content = """---
title: My Note
this is not valid yaml: [unclosed bracket
---

# Content
"""
        frontmatter, remaining = extract_frontmatter(content)

        # Should gracefully handle malformed YAML
        assert frontmatter is None
        assert content == remaining

    def test_extract_frontmatter_with_quotes(self):
        """Test extracting frontmatter with quoted values."""
        content = """---
title: "My Note Title"
supernote.file: "Journal/2026-01-20.note"
supernote.type: realtime
---

Content here
"""
        frontmatter, remaining = extract_frontmatter(content)

        assert frontmatter is not None
        assert frontmatter["title"] == "My Note Title"
        assert frontmatter["supernote.file"] == "Journal/2026-01-20.note"
        assert frontmatter["supernote.type"] == "realtime"


class TestFrontmatterPropertyParsing:
    """Test parsing Supernote properties from frontmatter."""

    def test_parse_default_properties(self):
        """Test default property values when frontmatter is None."""
        props = parse_frontmatter_properties(None, warn=False)

        assert props.supernote_type == "standard"
        assert props.supernote_file is None
        assert props.realtime is False

    def test_parse_realtime_type(self):
        """Test parsing realtime type."""
        frontmatter = {"supernote.type": "realtime"}
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_type == "realtime"
        assert props.realtime is True

    def test_parse_standard_type(self):
        """Test parsing standard type."""
        frontmatter = {"supernote.type": "standard"}
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_type == "standard"
        assert props.realtime is False

    def test_parse_invalid_type_uses_default(self):
        """Test that invalid type falls back to default."""
        frontmatter = {"supernote.type": "invalid_type"}
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_type == "standard"
        assert props.realtime is False

    def test_parse_file_property(self):
        """Test parsing supernote.file property."""
        frontmatter = {
            "supernote.type": "realtime",
            "supernote.file": "Journal/2026-01-20.note",
        }
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_type == "realtime"
        assert props.supernote_file == "Journal/2026-01-20.note"

    def test_parse_empty_file_property(self):
        """Test that empty file property is treated as None."""
        frontmatter = {"supernote.file": ""}
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_file is None

    def test_parse_non_string_file_property(self):
        """Test that non-string file property is ignored."""
        frontmatter = {"supernote.file": 123}
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_file is None

    def test_parse_all_properties(self):
        """Test parsing all properties together."""
        frontmatter = {
            "title": "Daily Notes",
            "supernote.type": "realtime",
            "supernote.file": "Journal/2026-01-20.note",
            "tags": ["daily", "journal"],
        }
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_type == "realtime"
        assert props.supernote_file == "Journal/2026-01-20.note"
        assert props.realtime is True
        assert "title" in props.raw_frontmatter
        assert "tags" in props.raw_frontmatter


class TestFrontmatterPropertiesClass:
    """Test FrontmatterProperties class."""

    def test_properties_initialization(self):
        """Test initializing FrontmatterProperties."""
        props = FrontmatterProperties(
            supernote_type="realtime",
            supernote_file="test.note",
        )

        assert props.supernote_type == "realtime"
        assert props.supernote_file == "test.note"
        assert props.realtime is True

    def test_properties_defaults(self):
        """Test default values."""
        props = FrontmatterProperties()

        assert props.supernote_type == "standard"
        assert props.supernote_file is None
        assert props.realtime is False

    def test_properties_repr(self):
        """Test string representation."""
        props = FrontmatterProperties(
            supernote_type="realtime",
            supernote_file="test.note",
        )

        repr_str = repr(props)
        assert "realtime" in repr_str
        assert "test.note" in repr_str


class TestReadMarkdownWithFrontmatter:
    """Test reading markdown files with frontmatter."""

    def test_read_markdown_file(self, tmp_path):
        """Test reading a markdown file with frontmatter."""
        # Create test markdown file
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
title: Test Note
supernote.type: realtime
supernote.file: "Notes/test.note"
---

# Test Content

This is a test note.
""", encoding="utf-8")

        # Read and parse
        props, content = read_markdown_with_frontmatter(md_file, warn=False)

        assert props.supernote_type == "realtime"
        assert props.supernote_file == "Notes/test.note"
        assert props.realtime is True
        assert "# Test Content" in content
        assert "---" not in content

    def test_read_markdown_without_frontmatter(self, tmp_path):
        """Test reading markdown file without frontmatter."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""# Test Note

Just regular content.
""", encoding="utf-8")

        props, content = read_markdown_with_frontmatter(md_file, warn=False)

        assert props.supernote_type == "standard"
        assert props.supernote_file is None
        assert "# Test Note" in content


class TestWorkflowExamples:
    """Test real-world workflow examples from documentation."""

    def test_daily_notes_workflow(self):
        """Test Daily Notes workflow frontmatter."""
        content = """---
title: "Daily Notes 2026-01-20"
supernote.type: realtime
supernote.file: "Journal/2026-01-20.note"
---

# Today's Tasks
- [ ] Review code
- [ ] Write tests
"""
        frontmatter, _ = extract_frontmatter(content)
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_type == "realtime"
        assert props.supernote_file == "Journal/2026-01-20.note"
        assert props.realtime is True

    def test_research_notes_workflow(self):
        """Test Research Notes workflow frontmatter."""
        content = """---
title: "Deep Learning Paper"
supernote.type: realtime
supernote.file: "Reading/DeepLearning.note"
---

# Abstract
This paper presents...
"""
        frontmatter, _ = extract_frontmatter(content)
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_type == "realtime"
        assert props.supernote_file == "Reading/DeepLearning.note"

    def test_world_building_workflow(self):
        """Test World Building workflow frontmatter."""
        content = """---
title: "Aragorn - Character Profile"
supernote.type: standard
supernote.file: "Characters/Aragorn.note"
---

# Character Details
Name: Aragorn
"""
        frontmatter, _ = extract_frontmatter(content)
        props = parse_frontmatter_properties(frontmatter, warn=False)

        assert props.supernote_type == "standard"
        assert props.supernote_file == "Characters/Aragorn.note"
        assert props.realtime is False

    def test_minimal_frontmatter(self):
        """Test minimal frontmatter (no supernote properties)."""
        content = """---
title: "Simple Note"
---

# Content
Just a regular note.
"""
        frontmatter, _ = extract_frontmatter(content)
        props = parse_frontmatter_properties(frontmatter, warn=False)

        # Should use all defaults
        assert props.supernote_type == "standard"
        assert props.supernote_file is None
        assert props.realtime is False


class TestNoteFileReferenceFormatting:
    """Test formatting .note file references with [x.note] notation."""

    def test_format_relative_path_same_directory(self):
        """Test formatting when .note is in same directory as markdown."""
        markdown_path = Path("/vault/notes/daily.md")
        note_path = Path("/vault/notes/daily.note")

        result = format_note_file_reference(note_path, markdown_path)
        assert result == "[daily.note]"

    def test_format_relative_path_subdirectory(self):
        """Test formatting when .note is in subdirectory."""
        markdown_path = Path("/vault/daily.md")
        note_path = Path("/vault/output/daily.note")

        result = format_note_file_reference(note_path, markdown_path)
        assert result == "[output/daily.note]"

    def test_format_relative_path_parent_directory(self):
        """Test formatting when .note is in parent directory."""
        markdown_path = Path("/vault/notes/daily.md")
        note_path = Path("/vault/daily.note")

        result = format_note_file_reference(note_path, markdown_path)
        assert result == "[../daily.note]"

    def test_format_uses_forward_slashes(self):
        """Test that paths use forward slashes (cross-platform)."""
        markdown_path = Path("/vault/daily.md")
        note_path = Path("/vault/output/sub/daily.note")

        result = format_note_file_reference(note_path, markdown_path)
        assert "/" in result or result == "[daily.note]"
        assert "\\" not in result


class TestFrontmatterFileReferenceUpdate:
    """Test updating markdown files with .note file references."""

    def test_update_frontmatter_creates_new_frontmatter(self, tmp_path):
        """Test creating frontmatter when none exists."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""# My Note

This is content without frontmatter.
""", encoding="utf-8")

        note_file = tmp_path / "test.note"

        # Update the frontmatter
        update_frontmatter_file_reference(md_file, note_file)

        # Read back and verify
        updated_content = md_file.read_text(encoding="utf-8")
        assert "---" in updated_content
        assert "supernote.file:" in updated_content
        assert "[test.note]" in updated_content
        assert "# My Note" in updated_content

    def test_update_frontmatter_preserves_existing_properties(self, tmp_path):
        """Test that existing frontmatter properties are preserved."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
title: "My Daily Note"
date: "2026-01-22"
tags:
  - daily
  - journal
supernote.type: realtime
---

# Content here
""", encoding="utf-8")

        note_file = tmp_path / "test.note"

        # Update the frontmatter
        update_frontmatter_file_reference(md_file, note_file)

        # Read back and parse
        updated_content = md_file.read_text(encoding="utf-8")
        frontmatter, _ = extract_frontmatter(updated_content)

        assert frontmatter is not None
        assert frontmatter["title"] == "My Daily Note"
        assert frontmatter["date"] == "2026-01-22"
        assert frontmatter["tags"] == ["daily", "journal"]
        assert frontmatter["supernote.type"] == "realtime"
        assert frontmatter["supernote.file"] == "[test.note]"

    def test_update_frontmatter_updates_existing_file_reference(self, tmp_path):
        """Test updating an existing supernote.file property."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
title: "My Note"
supernote.file: "[old-file.note]"
---

# Content
""", encoding="utf-8")

        note_file = tmp_path / "new-file.note"

        # Update the frontmatter
        update_frontmatter_file_reference(md_file, note_file)

        # Read back and verify
        frontmatter, _ = extract_frontmatter(md_file.read_text(encoding="utf-8"))

        assert frontmatter["supernote.file"] == "[new-file.note]"
        assert frontmatter["title"] == "My Note"

    def test_update_frontmatter_with_relative_path(self, tmp_path):
        """Test updating frontmatter with .note in subdirectory."""
        md_file = tmp_path / "daily.md"
        md_file.write_text("# Daily Note", encoding="utf-8")

        output_dir = tmp_path / "output"
        output_dir.mkdir()
        note_file = output_dir / "daily.note"

        # Update the frontmatter
        update_frontmatter_file_reference(md_file, note_file)

        # Read back and verify
        frontmatter, _ = extract_frontmatter(md_file.read_text(encoding="utf-8"))

        assert frontmatter["supernote.file"] == "[output/daily.note]"


class TestFrontmatterPropertiesPathResolution:
    """Test resolving [x.note] notation to absolute paths."""

    def test_get_absolute_path_with_brackets(self, tmp_path):
        """Test resolving path with brackets notation."""
        md_file = tmp_path / "test.md"
        note_file = tmp_path / "output" / "test.note"

        props = FrontmatterProperties(supernote_file="[output/test.note]")
        absolute_path = props.get_absolute_file_path(md_file)

        assert absolute_path is not None
        assert absolute_path.name == "test.note"
        assert "output" in str(absolute_path)

    def test_get_absolute_path_without_brackets(self, tmp_path):
        """Test resolving path without brackets."""
        md_file = tmp_path / "test.md"

        props = FrontmatterProperties(supernote_file="output/test.note")
        absolute_path = props.get_absolute_file_path(md_file)

        assert absolute_path is not None
        assert absolute_path.name == "test.note"

    def test_get_absolute_path_returns_none_when_no_file(self):
        """Test that None is returned when supernote.file is not set."""
        md_file = Path("/vault/test.md")

        props = FrontmatterProperties(supernote_file=None)
        absolute_path = props.get_absolute_file_path(md_file)

        assert absolute_path is None

    def test_get_absolute_path_resolves_relative_to_markdown(self, tmp_path):
        """Test that paths are resolved relative to markdown file location."""
        notes_dir = tmp_path / "notes"
        notes_dir.mkdir()
        md_file = notes_dir / "test.md"

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        props = FrontmatterProperties(supernote_file="[../output/test.note]")
        absolute_path = props.get_absolute_file_path(md_file)

        assert absolute_path is not None
        assert absolute_path.parent.name == "output"
        assert absolute_path.name == "test.note"
