# Workflow Examples

Ready-to-use templates and step-by-step guides for three common use cases.

## Quick Reference

| Workflow | Note Type | Best For |
|----------|-----------|----------|
| [Daily Notes](daily-notes/) | `realtime` | Journaling, to-do lists, quick notes |
| [Research Notes](research-notes/) | `realtime` | Article annotations, study materials |
| [World Building](world-building/) | `standard` | Sketches, maps, character designs |

## Choosing the Right Note Type

### Realtime Mode (`supernote.type: realtime`)

Use when you want to **capture handwritten text** as searchable content.

- Supernote recognizes your handwriting in real-time
- Text is extractable via supernotelib
- Slightly larger file size
- Best for: notes, annotations, margin comments

### Standard Mode (`supernote.type: standard`)

Use when you're **primarily sketching or drawing**.

- Pure canvas for visual work
- No text recognition processing
- Smaller file size
- Best for: sketches, diagrams, maps, visual designs

## Workflow Directories

```
workflows/
├── README.md                           # This file
├── daily-notes/
│   ├── README.md                       # Step-by-step guide
│   ├── daily-note-template.md          # Blank template
│   └── 2026-01-24-example.md           # Complete example
├── research-notes/
│   ├── README.md                       # Step-by-step guide
│   ├── research-article-template.md    # Blank template
│   └── machine-learning-survey-example.md
└── world-building/
    ├── README.md                       # Step-by-step guide
    ├── character-template.md           # Blank template
    └── aragorn-example.md              # Complete example
```

## Getting Started

### 1. Choose Your Workflow

Pick the workflow that matches your use case from the table above.

### 2. Copy a Template

```bash
# Daily notes
cp examples/workflows/daily-notes/daily-note-template.md "Your Vault/Daily Notes/"

# Research notes
cp examples/workflows/research-notes/research-article-template.md "Your Vault/Reading/"

# World building
cp examples/workflows/world-building/character-template.md "Your Vault/Characters/"
```

### 3. Add Your Content

Fill in the template with your content. The frontmatter is pre-configured with the correct `supernote.type`.

### 4. Convert and Sync

```bash
# Activate environment
cd c:\Edwin\repos\obsidian-supernote-sync
venv\Scripts\activate

# Convert your file
obsidian-supernote md-to-note "your-file.md" "output/your-file.note"

# Copy to Supernote
copy "output\your-file.note" "E:\Note\YourFolder\"
```

### 5. Use on Supernote

- Write/sketch on your Supernote device
- Sync back when ready
- Your markdown is auto-updated with the file reference

## Configuration Files

Pre-configured YAML files for each workflow:

- [daily-notes-config.yml](../configs/daily-notes-config.yml)
- [research-notes-config.yml](../configs/research-notes-config.yml)
- [world-building-config.yml](../configs/world-building-config.yml)

These will be used by the sync engine (Phase 3) for automated workflows.

## Common Commands

```bash
# Convert markdown to .note
obsidian-supernote md-to-note input.md output.note

# Convert .note to markdown (with images)
obsidian-supernote note-to-md input.note output.md

# Inspect a .note file
obsidian-supernote inspect input.note

# Help
obsidian-supernote --help
```

## Frontmatter Quick Reference

```yaml
# Daily Notes / Research Notes (text capture)
---
title: "Your Title"
supernote.type: realtime
---

# World Building (sketching)
---
title: "Your Title"
supernote.type: standard
---

# After conversion (auto-added)
---
title: "Your Title"
supernote.type: realtime
supernote.file: "[output/your-file.note]"
---
```

## Next Steps

1. Try one of the example files
2. Create your own templates
3. Establish a sync routine
4. Wait for Phase 3 automated sync features
