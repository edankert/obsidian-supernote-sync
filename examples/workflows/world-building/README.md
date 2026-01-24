# World Building Workflow

Sketch character designs, maps, and visual concepts on Supernote while maintaining connections with Obsidian worldbuilding notes.

## Overview

| Setting | Value |
|---------|-------|
| **Note Type** | `standard` |
| **Purpose** | Pure sketching without text recognition |
| **Best For** | Character designs, maps, diagrams, visual concepts |

## Quick Start

### 1. Create a Character Profile in Obsidian

```yaml
---
title: "Aragorn - Ranger King"
aliases: ["Strider", "Elessar"]
tags: [character, worldbuilding, fantasy]
created: 2026-01-15
supernote.type: standard
---

# Aragorn - Ranger King

## Basic Information
| Attribute | Value |
|-----------|-------|
| Full Name | Aragorn II |
| Age | 87 |
| Race | Dunedain |

## Physical Description
Tall and lean, weathered from years in the wild...

## Sketches
<!-- Draw character designs on Supernote -->
```

### 2. Convert to Supernote .note File

```bash
# Activate environment
cd c:\Edwin\repos\obsidian-supernote-sync
venv\Scripts\activate

# Convert to .note (standard mode for sketching)
obsidian-supernote md-to-note "Characters/aragorn.md" "output/Characters/aragorn.note"
```

### 3. Transfer to Supernote

```bash
copy "output\Characters\aragorn.note" "E:\Note\WorldBuilding\Characters\"
```

### 4. Sketch on Supernote

On your Supernote device:
- Open the note
- Draw character portraits, poses, costumes
- Sketch equipment and weapons
- Add visual reference notes
- Standard mode = pure drawing canvas

### 5. Import Sketches Back to Obsidian

```bash
# Export sketches as PNG images
obsidian-supernote note-to-md "E:\Note\WorldBuilding\Characters\aragorn.note" "Characters/aragorn-sketches.md"

# This creates:
# - aragorn-sketches.md
# - aragorn-sketches_page_01.png
# - aragorn-sketches_page_02.png
```

### 6. Embed Sketches in Original Note

In your Obsidian character file, add:
```markdown
## Sketches

![[aragorn-sketches_page_01.png]]
![[aragorn-sketches_page_02.png]]
```

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    OBSIDIAN                              │
│  1. Create character/location/item profile               │
│  2. Add descriptions, stats, relationships               │
│  3. Set supernote.type: standard                         │
└─────────────────────┬───────────────────────────────────┘
                      │ md-to-note
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    SUPERNOTE                             │
│  4. View profile on e-ink display                        │
│  5. Sketch visual designs                                │
│  6. Draw maps, diagrams, concepts                        │
│  7. Iterate on designs                                   │
└─────────────────────┬───────────────────────────────────┘
                      │ note-to-md
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    OBSIDIAN                              │
│  8. Import sketches as PNG images                        │
│  9. Embed in character/location notes                    │
│  10. Link across your world wiki                         │
└─────────────────────────────────────────────────────────┘
```

## File Structure

```
Your Obsidian Vault/
├── 03 Projects/
│   └── MyWorld/
│       ├── Characters/
│       │   ├── aragorn.md              # Character profile
│       │   ├── aragorn-sketches.md     # Imported sketches
│       │   └── assets/
│       │       ├── aragorn_page_01.png
│       │       └── aragorn_page_02.png
│       ├── Locations/
│       │   ├── rivendell.md
│       │   └── rivendell-map.md
│       └── Items/
│           └── anduril.md
└── output/
    └── worldbuilding/
        └── Characters/
            └── aragorn.note

Supernote Device/
└── Note/
    └── WorldBuilding/
        ├── Characters/
        │   └── aragorn.note            # With sketches
        └── Locations/
            └── rivendell.note
```

## Frontmatter Reference

| Property | Value | Description |
|----------|-------|-------------|
| `supernote.type` | `standard` | Pure sketching mode (no text recognition) |
| `supernote.file` | Auto-generated | Links to .note file |
| `aliases` | `["Name1", "Name2"]` | Alternative names for wikilinks |
| `tags` | `[character, worldbuilding]` | For organization |

## Why Standard Mode?

For world building, you typically:
- Draw visual designs (no text to recognize)
- Sketch maps and diagrams
- Create concept art
- Focus on visual expression

**Standard mode** keeps files smaller and avoids unnecessary text recognition processing.

Use **Realtime mode** only when you're adding substantial handwritten text that should be searchable.

## Sketching Tips

### Character Designs
- Start with basic profile info as header
- Draw multiple poses on separate pages
- Include costume/equipment details
- Add color notes in margins

### Maps
- Use grid templates for scale
- Label regions with simple text
- Draw terrain features consistently
- Leave space for legend/key

### Diagrams
- Family trees and relationship maps
- Magic system diagrams
- Technology schematics
- Timeline visualizations

## Batch Processing

For multiple character files:

```bash
# Convert all character files
for file in Characters/*.md; do
  obsidian-supernote md-to-note "$file" "output/Characters/$(basename ${file%.md}).note"
done

# Or use glob (future feature)
obsidian-supernote batch-convert "Characters/*.md" "output/Characters/"
```

## Troubleshooting

### Sketches look pixelated when imported

Increase DPI when converting:
```bash
obsidian-supernote note-to-md input.note output.md --dpi 300
```

### Want to update profile without losing sketches

The update mode preserves your handwritten content:
```bash
# Edit character profile in Obsidian
# Re-run conversion - sketches are preserved
obsidian-supernote md-to-note "Characters/aragorn.md" "output/Characters/aragorn.note"
```

### Organizing many world building files

Use folder structure that mirrors your Obsidian vault:
```bash
output/
├── Characters/
├── Locations/
├── Items/
├── Factions/
└── Maps/
```

## Example Files

- [character-template.md](character-template.md) - Blank character template
- [aragorn-example.md](aragorn-example.md) - Complete character example

## Configuration

See [world-building-config.yml](../../configs/world-building-config.yml) for sync configuration options.

## Best Practices

1. **Consistent structure** - Use templates for all characters, locations, items
2. **Mirror folders** - Keep Supernote folder structure matching Obsidian
3. **Version sketches** - Export sketches after each major revision
4. **Link everything** - Use `[[wikilinks]]` to connect your world wiki
5. **Tag for tracking** - Use tags like `needs-sketch`, `sketch-done`
