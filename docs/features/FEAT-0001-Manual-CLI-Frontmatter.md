---
type: "[[feature]]"
id: FEAT-0001
title: "Phase 2: Manual CLI with Frontmatter Support"
status: done
phase: 2
owner: Edwin
created: 2026-01-20
updated: 2026-01-24
source:
  - "PLAN.md"
  - "docs/IMPLEMENTATION_STATUS.md"
goal: "Enable users to control .note type and updates via frontmatter properties with manual CLI commands"
requirements:
  - "[[REQ-0001-Frontmatter-Parsing]]"
  - "[[REQ-0002-Update-Mode]]"
tasks:
  - "[[TASK-0001-Frontmatter-Parsing]]"
  - "[[TASK-0002-Update-Mode]]"
  - "[[TASK-0003-Realtime-Support]]"
  - "[[TASK-0004-Configuration-Examples]]"
release: "v0.2.0-alpha"
related:
  - "[[FEAT-0002-Python-Backend-API]]"
tests:
  - "[[TST-0001-Frontmatter-Parsing]]"
---

# Phase 2: Manual CLI with Frontmatter Support

## Goal
Enable users to control .note type and updates via frontmatter properties, with manual CLI commands for all conversions.

## Scope

**In Scope:**
- Frontmatter property parsing (`supernote.type`, `supernote.file`)
- .note file update mode preserving handwriting
- Realtime handwriting recognition support
- Configuration examples and workflow guides

**Out of Scope:**
- File watching/monitoring
- Batch operations
- GUI interface

## Acceptance
- CLI reads frontmatter properties from markdown
- Properties override default settings
- Properties are optional (graceful fallback)
- Validation prevents invalid configurations
- Can update existing .note files
- Handwritten annotations preserved exactly
- New template content displays correctly
- Updated .note opens on device without errors

## Evidence

### Completed Steps
1. **Step 1: Frontmatter Property Parsing** - 34 tests, 92% coverage
2. **Step 2: .note File Update Mode** - Preserves handwriting when reconverting
3. **Step 3: Realtime Recognition Support** - `supernote.type: realtime` enables recognition
4. **Step 4: Configuration Examples** - Workflow guides in `examples/workflows/`

### Test Results
- `pytest tests/test_frontmatter_parsing.py -v` - 34 tests passing

## Links
- Requirements: [[REQ-0001-Frontmatter-Parsing]], [[REQ-0002-Update-Mode]]
- Tasks: [[TASK-0001-Frontmatter-Parsing]], [[TASK-0002-Update-Mode]], [[TASK-0003-Realtime-Support]], [[TASK-0004-Configuration-Examples]]
- Implementation: `obsidian_supernote/utils/frontmatter.py`, `obsidian_supernote/converters/note_writer.py`
- Documentation: `docs/FRONTMATTER_PROPERTIES.md`, `examples/workflows/`
