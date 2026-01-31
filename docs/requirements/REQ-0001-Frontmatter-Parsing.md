---
type: "[[requirement]]"
id: REQ-0001
title: "CLI reads and respects frontmatter properties"
status: verified
owner: Edwin
created: 2026-01-20
updated: 2026-01-31
priority: high
scope: converters
phase: 2
source:
  - "PLAN.md"
  - "docs/STEP1_REQUIREMENTS.md"
acceptance:
  - "CLI reads frontmatter properties from markdown"
  - "Properties override default settings"
  - "Properties are optional with graceful fallback"
  - "Validation prevents invalid configurations"
implements:
  - "[[FEAT-0001-Manual-CLI-Frontmatter]]"
verifies:
  - "tests/test_frontmatter_parsing.py"
tests:
  - "[[TST-0001-Frontmatter-Parsing]]"
---

# REQ-0001: Frontmatter Property Parsing

## Description
The CLI must read and respect YAML frontmatter properties in markdown files for controlling .note conversion.

## Properties

| Property | Values | Default | Description |
|----------|--------|---------|-------------|
| `supernote.type` | `standard`, `realtime` | `standard` | Note type for handwriting recognition |
| `supernote.file` | `[path/to/file.note]` | None | Auto-managed reference to generated .note |

## Acceptance Criteria

1. **CLI reads frontmatter** - `md-to-note` command automatically reads frontmatter
2. **Properties override defaults** - Frontmatter values take precedence
3. **Optional properties** - Missing properties use sensible defaults
4. **Validation** - Invalid values trigger warnings, fallback to defaults

## Verification

### Automated Tests
- `pytest tests/test_frontmatter_parsing.py -v`
- 34 tests, 92% coverage

### Manual Verification
```bash
# Test realtime property
echo "---\nsupernote.type: realtime\n---\n# Test" > test.md
obsidian-supernote md-to-note test.md test.note
# Verify .note has realtime recognition enabled
```

## Evidence
- Test suite: [[TST-0001-Frontmatter-Parsing]]
- Implementation: `obsidian_supernote/utils/frontmatter.py`
