# .note to Markdown Export Example

This directory contains an example of Supernote .note file export to Obsidian-compatible Markdown.

## Files

- `20241004_120815.md` - Markdown file with YAML frontmatter and image embeds
- `20241004_120815_page_01.png` - Rendered page 1 as PNG image
- `20241004_120815_page_02.png` - Rendered page 2 as PNG image

## How to Use

### Convert .note to Markdown

```bash
obsidian-supernote note-to-md input.note output.md
```

### Convert .note to PNG only

```bash
obsidian-supernote note-to-png input.note output_directory/
```

### Options

- `--image-dir` - Directory for images (default: same as markdown file)
- `--embed/--no-embed` - Use Obsidian image embeds (![[image]]) or standard markdown

## Output Format

The generated Markdown includes:

```yaml
---
title: "Note Title"
source: Supernote
source_file: "original.note"
pages: 2
imported: 2024-01-15
---

# Note Title

## Page 1
![[note_page_01.png]]

## Page 2
![[note_page_02.png]]
```

## Integration with Obsidian

1. Export your .note files to your Obsidian vault
2. Images are automatically embedded using Obsidian's `![[]]` syntax
3. YAML frontmatter provides metadata for search and organization
