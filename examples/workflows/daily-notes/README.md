# Daily Notes Workflow

Integrate handwritten daily notes from Supernote with your Obsidian daily notes.

## Overview

| Setting | Value |
|---------|-------|
| **Note Type** | `realtime` |
| **Purpose** | Capture handwritten text as searchable content |
| **Best For** | Journaling, quick notes, to-do lists, reflections |

## Quick Start

### 1. Create Your Daily Note in Obsidian

```yaml
---
title: "Daily Notes 2026-01-24"
date: 2026-01-24
supernote.type: realtime
---

# Daily Notes - 2026-01-24

## Morning Intentions
- [ ] Task 1
- [ ] Task 2

## Notes
<!-- Handwrite additional notes on Supernote -->
```

### 2. Convert to Supernote .note File

```bash
# Navigate to project
cd c:\Edwin\repos\obsidian-supernote-sync

# Activate virtual environment
venv\Scripts\activate

# Convert markdown to .note
obsidian-supernote md-to-note "path/to/2026-01-24.md" "output/20260124.note"
```

**Output:**
```
Reading markdown file: path/to/2026-01-24.md
Frontmatter properties:
  supernote.type: realtime
Converting to PDF...
Creating .note file...
Updating markdown with file reference...
Done! Created: output/20260124.note
```

### 3. Your Markdown is Auto-Updated

After conversion, your markdown file is updated with a file reference:

```yaml
---
title: "Daily Notes 2026-01-24"
date: 2026-01-24
supernote.type: realtime
supernote.file: "[output/20260124.note]"
---
```

### 4. Copy to Supernote

Copy the `.note` file to your Supernote device:

```bash
# USB method
copy "output\20260124.note" "E:\Note\Daily\"

# Or use Supernote Cloud (future feature)
```

### 5. Write on Supernote

- Open the note on your Supernote device
- Add handwritten notes, to-do items, reflections
- Realtime mode captures your handwriting as text

### 6. Update Workflow (Preserve Handwriting)

After editing your markdown in Obsidian and wanting to update the .note:

```bash
# Same command - automatically detects existing file
obsidian-supernote md-to-note "path/to/2026-01-24.md" "output/20260124.note"
```

**Output:**
```
Update mode: Found existing .note file
Extracting handwriting data...
Handwriting data: 45231 bytes, Has content: True
Preserving handwriting from 2 pages
Creating new template...
Update complete - handwriting preserved!
```

## File Structure

```
Your Obsidian Vault/
├── 02 Journal/
│   └── Daily Notes/
│       ├── 2026-01-24.md      # Your daily note
│       ├── 2026-01-25.md
│       └── ...
└── output/
    └── daily/
        ├── 20260124.note      # Supernote file
        └── 20260125.note

Supernote Device/
└── Note/
    └── Daily/
        ├── 20260124.note
        └── 20260125.note
```

## Frontmatter Reference

| Property | Value | Description |
|----------|-------|-------------|
| `supernote.type` | `realtime` | Enables handwriting recognition |
| `supernote.file` | Auto-generated | Links to .note file (auto-added after first conversion) |

## Troubleshooting

### Note doesn't open on device

1. Check device compatibility (A5X, A5X2, A6X, A6X2)
2. Ensure file is in `/Note/` folder on device
3. Try regenerating with correct device flag: `--device A5X2`

### Handwriting not preserved after update

1. Make sure you're converting to the same output path
2. Check that `supernote.file` property exists in frontmatter
3. The original .note file must exist at the specified path

### Text not being recognized

1. Confirm `supernote.type: realtime` in frontmatter
2. Realtime recognition happens on device, not during conversion
3. Text extraction from device recognition is a future feature

## Example Files

- [daily-note-template.md](daily-note-template.md) - Blank template
- [2026-01-24-example.md](2026-01-24-example.md) - Complete example

## Configuration

See [daily-notes-config.yml](../../configs/daily-notes-config.yml) for sync configuration options.

## Next Steps

1. Try the workflow with the example file
2. Create your own daily note template
3. Set up a daily routine for syncing
4. Wait for Phase 3 for automated sync
