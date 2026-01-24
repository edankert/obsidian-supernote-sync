# Research Notes Workflow

Annotate research articles and study materials on Supernote, then import annotations back to Obsidian.

## Overview

| Setting | Value |
|---------|-------|
| **Note Type** | `realtime` |
| **Purpose** | Capture annotations, highlights, and margin notes as text |
| **Best For** | Academic papers, articles, study materials, book notes |

## Quick Start

### 1. Prepare Your Research Article in Obsidian

```yaml
---
title: "Attention Is All You Need - Transformer Architecture"
author: "Vaswani et al."
date: 2026-01-20
tags: [research, ai, to-supernote]
supernote.type: realtime
---

# Transformer Architecture

## Summary
The Transformer architecture introduces self-attention...

## Key Points
1. Self-Attention Mechanism
2. Multi-Head Attention
3. Positional Encoding

## Annotations
<!-- Handwrite margin notes and highlights on Supernote -->
```

### 2. Convert to Supernote .note File

```bash
# Activate environment
cd c:\Edwin\repos\obsidian-supernote-sync
venv\Scripts\activate

# Convert article to .note
obsidian-supernote md-to-note "Reading/transformer-paper.md" "output/transformer-paper.note"
```

### 3. Transfer to Supernote

```bash
# Copy to device
copy "output\transformer-paper.note" "E:\Note\Reading\"
```

### 4. Annotate on Supernote

On your Supernote device:
- Open the note in `/Note/Reading/`
- Highlight key passages
- Write margin notes
- Add questions and comments
- Realtime mode captures your annotations as text

### 5. Update After More Research

When you add more content to your Obsidian note:

```bash
# Edit transformer-paper.md in Obsidian (add new sections, insights)

# Re-run conversion - preserves your handwritten annotations
obsidian-supernote md-to-note "Reading/transformer-paper.md" "output/transformer-paper.note"
```

### 6. Import Annotations Back (Future Feature)

```bash
# Future: Import handwritten annotations as images + text
obsidian-supernote note-to-md "E:\Note\Reading\transformer-paper.note" "Reading/transformer-paper-annotated.md"
```

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    OBSIDIAN                              │
│  1. Create research article with key points             │
│  2. Add frontmatter: supernote.type: realtime           │
└─────────────────────┬───────────────────────────────────┘
                      │ md-to-note
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    SUPERNOTE                             │
│  3. Read article on e-ink display                        │
│  4. Highlight important passages                         │
│  5. Write margin notes and questions                     │
│  6. Realtime captures annotations as text                │
└─────────────────────┬───────────────────────────────────┘
                      │ note-to-md (future)
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    OBSIDIAN                              │
│  7. View annotations as images                           │
│  8. Search through recognized text                       │
│  9. Link to related notes                                │
└─────────────────────────────────────────────────────────┘
```

## File Structure

```
Your Obsidian Vault/
├── 02 Reading/
│   ├── transformer-paper.md           # Original article
│   ├── machine-learning-survey.md
│   └── assets/
│       └── annotations/               # Imported annotation images
│           ├── transformer_page_01.png
│           └── transformer_page_02.png
└── output/
    └── reading/
        ├── transformer-paper.note
        └── machine-learning-survey.note

Supernote Device/
└── Note/
    └── Reading/
        ├── transformer-paper.note      # Annotated on device
        └── machine-learning-survey.note
```

## Frontmatter Reference

| Property | Value | Description |
|----------|-------|-------------|
| `supernote.type` | `realtime` | Captures annotation text |
| `supernote.file` | Auto-generated | Links to .note file |
| `tags` | `[to-supernote]` | Optional: mark for export |

## Annotation Tips

### Effective Highlighting
- Use pen tool for underlining key concepts
- Circle important terms or equations
- Draw arrows to connect related ideas

### Margin Notes
- Write questions in margins
- Note connections to other papers
- Add brief summaries per section

### Symbols to Use
- `?` - Questions to research further
- `!` - Important insight
- `*` - Key concept
- `→` - Connection to other notes

## Troubleshooting

### Article too long for single page

The conversion creates multi-page .note files automatically. Each page of your markdown becomes a page in the .note file.

### Annotations not preserved on update

1. Verify `supernote.file` exists in your markdown frontmatter
2. Make sure you're outputting to the same file path
3. Check that the original .note file hasn't been moved or deleted

### Want to keep original and annotated versions

Use different output paths:
```bash
# Original (for clean reading)
obsidian-supernote md-to-note article.md output/article-clean.note

# After annotation, keep as separate file
# Copy annotated version from device with different name
copy "E:\Note\Reading\article.note" "output\article-annotated.note"
```

## Example Files

- [research-article-template.md](research-article-template.md) - Blank template
- [machine-learning-survey-example.md](machine-learning-survey-example.md) - Complete example

## Configuration

See [research-notes-config.yml](../../configs/research-notes-config.yml) for sync configuration options.

## Best Practices

1. **Use consistent frontmatter** - Always include `supernote.type: realtime`
2. **Tag for export** - Use `to-supernote` tag to mark articles for conversion
3. **Regular sync** - Sync annotations back to Obsidian weekly
4. **Link notes** - Connect annotated articles using `[[wikilinks]]`
5. **Archive completed** - Move fully-annotated articles to an archive folder
