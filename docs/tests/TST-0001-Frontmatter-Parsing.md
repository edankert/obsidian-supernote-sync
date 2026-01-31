---
type: "[[test]]"
id: TST-0001
title: "Frontmatter parsing test suite"
status: passing
owner: Edwin
created: 2026-01-22
updated: 2026-01-31
source:
  - "tests/test_frontmatter_parsing.py"
scope: feature
kind: automated
level: unit
entrypoint: "pytest tests/test_frontmatter_parsing.py -v"
requirements:
  - "[[REQ-0001-Frontmatter-Parsing]]"
features:
  - "[[FEAT-0001-Manual-CLI-Frontmatter]]"
issues: []
tasks: []
artifacts: []
evidence:
  - "34 tests passing"
  - "92% code coverage"
last_run: "2026-01-31"
---

# Frontmatter Parsing Test Suite

## Purpose
Verify that YAML frontmatter is correctly extracted and parsed from markdown files, including `supernote.type` and `supernote.file` properties.

## Test Coverage

### TestFrontmatterExtraction
- `test_extract_valid_frontmatter` - Valid YAML frontmatter extraction
- `test_extract_no_frontmatter` - Handling markdown without frontmatter
- `test_extract_empty_frontmatter` - Empty frontmatter handling
- `test_extract_malformed_yaml` - Graceful handling of malformed YAML
- `test_extract_frontmatter_with_quotes` - Quoted values support

### TestFrontmatterPropertyParsing
- `test_parse_default_properties` - Default values when frontmatter is None
- `test_parse_realtime_type` - Parsing `supernote.type: realtime`
- `test_parse_standard_type` - Parsing `supernote.type: standard`
- `test_parse_invalid_type_uses_default` - Invalid type fallback
- `test_parse_file_property` - Parsing `supernote.file` property
- `test_parse_empty_file_property` - Empty file treated as None
- `test_parse_non_string_file_property` - Non-string file ignored

### TestWorkflowExamples
- `test_daily_notes_workflow` - Daily Notes workflow frontmatter
- `test_research_notes_workflow` - Research Notes workflow frontmatter
- `test_world_building_workflow` - World Building workflow frontmatter
- `test_minimal_frontmatter` - Minimal frontmatter with defaults

### TestNoteFileReferenceFormatting
- `test_format_relative_path_*` - Relative path formatting tests
- `test_format_uses_forward_slashes` - Cross-platform path handling

### TestFrontmatterFileReferenceUpdate
- `test_update_frontmatter_creates_new_frontmatter` - Creating new frontmatter
- `test_update_frontmatter_preserves_existing_properties` - Preserving properties
- `test_update_frontmatter_updates_existing_file_reference` - Updating reference

## How to Run
```bash
cd C:\Edwin\repos\obsidian-supernote-sync
venv\Scripts\activate
pytest tests/test_frontmatter_parsing.py -v
pytest tests/test_frontmatter_parsing.py --cov=obsidian_supernote.utils.frontmatter
```

## Evidence
Last run: 2026-01-31
- 34 tests passed
- 0 tests failed
- Coverage: 92%
