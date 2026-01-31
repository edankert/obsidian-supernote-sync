---
type: "[[change]]"
id: CHG-20260128-Frontmatter
title: "Redesign frontmatter properties (simplified to 2)"
status: merged
owner: Edwin
created: 2026-01-28
updated: 2026-01-31
commit: "0c165a2"
pr: ""
impacts:
  - "obsidian_supernote/utils/frontmatter.py"
  - "Reduced from 6 to 2 properties"
issues: []
features:
  - "[[FEAT-0001-Manual-CLI-Frontmatter]]"
source:
  - "git log 0c165a2"
---

# CHG-20260128: Frontmatter Property Redesign

## Summary
Simplified frontmatter properties from 6 planned properties down to 2 essential ones.

## What Changed

### Before (Planned)
```yaml
supernote_type: realtime
supernote_linked_file: path/to/file.note
supernote_device: A5X2
supernote_page_size: A5
supernote_realtime: true
supernote_margins: 1cm
```

### After (Implemented)
```yaml
supernote.type: realtime  # or "standard"
supernote.file: "[output/file.note]"  # Auto-managed
```

## Why
- Simplicity: Most settings have good defaults
- Dot notation: Obsidian-friendly property naming
- Auto-managed: `supernote.file` is updated automatically
- Device setting via CLI flag (not per-file)

## Design Decisions
- Use dot notation (`supernote.type`) instead of underscores
- Use bracket notation (`[path.note]`) for file references
- Device defaults to A5X2/Manta, can override via `--device` flag
- Page size auto-calculated from device

## Evidence
- Commit: 0c165a2
- Decision: [[ADR-0001-Frontmatter-Approach]]
