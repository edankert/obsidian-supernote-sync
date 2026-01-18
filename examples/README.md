# Examples

This directory contains example files demonstrating the obsidian-supernote sync tool capabilities.

## Directory Structure

```
examples/
├── config.example.yml     # Example configuration file
├── sample.md              # Sample Markdown document for PDF conversion
├── pdf_to_note/           # PDF to .note conversion example
│   ├── sample_document.pdf
│   ├── sample_document.note
│   └── README.md
└── note_export/           # .note to Markdown export example
    ├── 20241004_120815.md
    ├── 20241004_120815_page_01.png
    ├── 20241004_120815_page_02.png
    └── README.md
```

## Workflows

### 1. Markdown to PDF to .note (Obsidian → Supernote)

Convert Obsidian notes to annotatable Supernote documents:

```bash
# Step 1: Convert Markdown to PDF
obsidian-supernote md-to-pdf sample.md sample.pdf

# Step 2: Convert PDF to .note
obsidian-supernote pdf-to-note sample.pdf sample.note

# Step 3: Copy .note to Supernote device
```

### 2. .note to Markdown (Supernote → Obsidian)

Export Supernote handwritten notes to Obsidian:

```bash
# Convert .note to Markdown with embedded images
obsidian-supernote note-to-md input.note output.md

# Or export pages as PNG only
obsidian-supernote note-to-png input.note output_directory/
```

### 3. Inspect .note Files

Analyze the structure of a .note file:

```bash
obsidian-supernote inspect input.note --save-images output_dir/
```

## Configuration

See `config.example.yml` for configuration options including:

- Obsidian vault path
- Supernote sync folder
- File naming patterns
- Sync preferences
