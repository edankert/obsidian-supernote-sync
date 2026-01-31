---
type: "[[task]]"
id: TASK-0002
title: "Implement .note File Update Mode"
status: done
phase: 2
owner: Edwin
created: 2026-01-20
updated: 2026-01-24
source:
  - "PLAN.md"
parent: "[[FEAT-0001-Manual-CLI-Frontmatter]]"
effort: L
depends:
  - "[[TASK-0001-Frontmatter-Parsing]]"
blocks:
  - "[[TASK-0003-Realtime-Support]]"
related: []
tests: []
---

# Implement .note File Update Mode

## Definition of Done
- [x] Detect existing .note file from `supernote.file` property
- [x] Extract annotation layers from existing .note (ZIP archive)
- [x] Replace only template content, preserve handwriting
- [x] Reassemble .note file with preserved layers
- [x] Updated file opens correctly on device

## Steps
- [x] Implement .note ZIP archive extraction
- [x] Identify template vs annotation layers
- [x] Create layer preservation logic in note_writer.py
- [x] Add update detection in CLI flow
- [x] Test on physical Supernote device

## Notes
- .note files are ZIP archives with layered content
- Annotation layers contain handwritten content
- Template layer contains the PDF/PNG background
- Device-tested on Supernote Manta (A5X2)

## Evidence
- Implementation: `obsidian_supernote/converters/note_writer.py`
- Documentation: `docs/STEP2_SUMMARY.md`
