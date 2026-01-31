---
type: "[[workflow]]"
id: WF-0003
title: "World Building Workflow"
status: active
owner: Edwin
created: 2026-01-24
updated: 2026-01-31
source:
  - "examples/workflows/world-building/README.md"
entrypoints:
  - "obsidian-supernote md-to-note character.md output/character.note"
prereqs:
  - "Pandoc installed"
  - "Python 3.10+"
inputs:
  - "Character/world template markdown"
outputs:
  - ".note file in standard mode (sketching)"
related:
  - "[[WF-0001-Daily-Notes]]"
  - "[[WF-0002-Research-Notes]]"
---

# World Building Workflow

## Purpose
Convert character profiles, world maps, and creative sketches to Supernote .note format in standard (sketching) mode.

## When to Use
- Character profile sketches
- World maps and diagrams
- Any creative visual work
- Content where text recognition is NOT needed

## Prerequisites
1. Pandoc installed
2. Python virtual environment activated

## Steps

### 1. Create Markdown with Frontmatter
```markdown
---
title: "Aragorn - Character Profile"
supernote.type: standard
---

# Character Details
Name: Aragorn
Class: Ranger

# Sketch Area
(Leave space for drawings)
```

### 2. Convert to .note
```bash
obsidian-supernote md-to-note character.md output/character.note
```

### 3. Sketch on Device
Draw character portraits, maps, or diagrams on your Supernote.

## Standard vs Realtime

| Mode | Use Case |
|------|----------|
| `standard` | Sketching, drawing, visual work |
| `realtime` | Text annotations, notes, searchable content |

## Links
- Guide: `examples/workflows/world-building/README.md`
- Template: `examples/workflows/world-building/character-template.md`
