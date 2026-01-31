---
type: "[[requirement]]"
id: REQ-0002
title: "Update existing .note files preserving handwriting"
status: verified
owner: Edwin
created: 2026-01-20
updated: 2026-01-31
priority: high
scope: converters
phase: 2
source:
  - "PLAN.md"
acceptance:
  - "Can update existing .note files"
  - "Handwritten annotations preserved exactly"
  - "New template content displays correctly"
  - "Updated .note opens on device without errors"
implements:
  - "[[FEAT-0001-Manual-CLI-Frontmatter]]"
verifies:
  - "Manual device testing"
tests: []
---

# REQ-0002: .note File Update Mode

## Description
When reconverting a markdown file that already has an associated .note file, preserve all handwriting annotations while replacing the template/background content.

## Acceptance Criteria

1. **Update detection** - Automatically detect existing .note via `supernote.file` property
2. **Handwriting preserved** - All annotation layers (Layers 2-5) kept intact
3. **Template replaced** - Layer 1 (background) updated with new PDF content
4. **Device compatibility** - Updated .note opens correctly on Supernote device

## How It Works

### First Conversion
```bash
obsidian-supernote md-to-note daily.md output/daily.note
# Creates new .note file
# Markdown updated: supernote.file: "[output/daily.note]"
```

### After Handwriting Added
```bash
# Edit markdown, then reconvert
obsidian-supernote md-to-note daily.md output/daily.note

# Output:
# "Update mode: Found existing .note file"
# "Using UPDATE mode - preserving handwriting annotations"
# "Handwriting data: 45231 bytes, Has content: True"
# "Update complete - handwriting preserved!"
```

## Technical Implementation
- `NoteFileParser.get_zip_archive()` - Extracts handwriting ZIP data
- `NoteFileWriter.update_note_file()` - Orchestrates update workflow
- `NoteFileWriter._write_note_file_with_zip()` - Writes with preserved ZIP

## Verification
- Device-tested on Supernote Manta
- Handwriting visible after update
- No data corruption

## Evidence
- Implementation: `obsidian_supernote/converters/note_writer.py`
- Change: [[CHG-20260129-Step2-Update-Mode]]
