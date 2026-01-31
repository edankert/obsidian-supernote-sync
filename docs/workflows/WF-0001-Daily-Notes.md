---
type: "[[workflow]]"
id: WF-0001
title: "Daily Notes Workflow"
status: active
owner: Edwin
created: 2026-01-24
updated: 2026-01-31
source:
  - "examples/workflows/daily-notes/README.md"
entrypoints:
  - "obsidian-supernote md-to-note daily.md output/daily.note"
prereqs:
  - "Pandoc installed"
  - "Python 3.10+"
  - "venv activated"
inputs:
  - "Markdown file with frontmatter"
outputs:
  - ".note file for Supernote device"
related:
  - "[[WF-0002-Research-Notes]]"
  - "[[WF-0003-World-Building]]"
---

# Daily Notes Workflow

## Purpose
Convert daily journal/to-do markdown files to Supernote .note format with realtime handwriting recognition enabled.

## When to Use
- Daily journaling and task lists
- Quick notes that should be searchable
- Any content where text recognition is valuable

## Prerequisites
1. Pandoc installed (`choco install pandoc`)
2. Python virtual environment activated
3. Dependencies installed (`pip install -r requirements.txt`)

## Steps

### 1. Create Markdown with Frontmatter
```markdown
---
title: "Daily Notes 2026-01-31"
supernote.type: realtime
---

# Today's Tasks
- [ ] Review code
- [ ] Write tests
```

### 2. Convert to .note
```bash
obsidian-supernote md-to-note daily.md output/daily.note
```

### 3. Transfer to Supernote
Copy the .note file to your Supernote device via USB or Supernote Cloud.

### 4. Annotate on Device
Write notes on your Supernote. The realtime mode enables handwriting recognition.

### 5. Update Workflow (Preserve Handwriting)
```bash
# Edit markdown in Obsidian
# Then reconvert - handwriting is preserved!
obsidian-supernote md-to-note daily.md output/daily.note
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Pandoc not found" | Install Pandoc: `choco install pandoc` |
| .note won't open | Check device compatibility (A5X, A5X2, A6X, A6X2) |
| Handwriting lost | Ensure `supernote.file` property is set |

## Links
- Guide: `examples/workflows/daily-notes/README.md`
- Template: `examples/workflows/daily-notes/daily-note-template.md`
- Example: `examples/workflows/daily-notes/2026-01-24-example.md`
