---
type: "[[workflow]]"
id: WF-0002
title: "Research Notes Workflow"
status: active
owner: Edwin
created: 2026-01-24
updated: 2026-01-31
source:
  - "examples/workflows/research-notes/README.md"
entrypoints:
  - "obsidian-supernote md-to-note research.md output/research.note"
prereqs:
  - "Pandoc installed"
  - "Python 3.10+"
inputs:
  - "Research article markdown"
outputs:
  - ".note file with realtime recognition"
related:
  - "[[WF-0001-Daily-Notes]]"
  - "[[WF-0003-World-Building]]"
---

# Research Notes Workflow

## Purpose
Convert research articles and study materials to Supernote .note format for annotation with handwriting recognition.

## When to Use
- Reading and annotating research papers
- Study materials with highlights and notes
- Any content requiring text annotations

## Prerequisites
1. Pandoc installed
2. Python virtual environment activated

## Steps

### 1. Create Markdown with Frontmatter
```markdown
---
title: "Deep Learning Paper"
supernote.type: realtime
---

# Abstract
This paper presents a novel approach to...

# Key Findings
- Finding 1
- Finding 2
```

### 2. Convert to .note
```bash
obsidian-supernote md-to-note research.md output/research.note
```

### 3. Annotate and Return
Annotate on device, then export handwriting back to Obsidian:
```bash
obsidian-supernote note-to-md output/research.note annotated/research.md
```

## Links
- Guide: `examples/workflows/research-notes/README.md`
- Template: `examples/workflows/research-notes/research-article-template.md`
