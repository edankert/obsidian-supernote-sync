# Examples

This directory contains example files, templates, and tools for the obsidian-supernote sync project.

## Directory Structure

```
examples/
├── README.md                    # This file
├── config.example.yml           # Example configuration file
├── sample.md                    # Sample Markdown document
│
├── templates/                   # Input templates for note creation
│   ├── README.md
│   ├── blank_template.png       # 1404x1872 white PNG for Supernote
│   └── sample_document.pdf      # 2-page PDF for testing
│
├── golden_sources/              # Reference .note files from device
│   ├── README.md                # Detailed documentation
│   ├── png_template/            # PNG-based notes (01-04)
│   ├── pdf_template/            # PDF-based notes (05-08)
│   ├── no_template/             # Notes without template (09-11)
│   └── edge_cases/              # Multi-page, multi-layer (12-13)
│
├── generated/                   # Output from note_writer.py
│
├── analysis/                    # Analysis tools
│   ├── README.md
│   ├── dump_structure.py        # Dump .note file structure
│   ├── compare_notes.py         # Compare two .note files
│   └── check_golden_sources.py  # Check which files are present
│
├── pdf_to_note/                 # PDF to .note conversion example
│   ├── README.md
│   ├── sample_document.pdf
│   └── sample_document.note     # Generated (may not load on device yet)
│
└── note_export/                 # .note to Markdown export example
    ├── README.md
    ├── 20241004_120815.md
    ├── 20241004_120815_page_01.png
    └── 20241004_120815_page_02.png
```

## Workflows

### 1. Reverse Engineering .note Format

Create golden source files on Supernote to understand format variations:

```bash
# Check which golden sources are present
python examples/analysis/check_golden_sources.py

# Analyze a .note file structure
python examples/analysis/dump_structure.py path/to/note.note

# Compare two .note files
python examples/analysis/compare_notes.py file1.note file2.note
```

See `golden_sources/README.md` for detailed instructions.

### 2. Markdown to PDF to .note (Obsidian → Supernote)

Convert Obsidian notes to annotatable Supernote documents:

```bash
# Step 1: Convert Markdown to PDF
obsidian-supernote md-to-pdf sample.md sample.pdf

# Step 2: Convert PDF to .note
obsidian-supernote pdf-to-note sample.pdf sample.note

# Step 3: Copy .note to Supernote device
```

**Note:** Generated .note files currently work with supernotelib but may not load on the actual Supernote device. This is an active area of development.

### 3. .note to Markdown (Supernote → Obsidian)

Export Supernote handwritten notes to Obsidian:

```bash
# Convert .note to Markdown with embedded images
obsidian-supernote note-to-md input.note output.md

# Or export pages as PNG only
obsidian-supernote note-to-png input.note output_directory/
```

### 4. Inspect .note Files

Analyze the structure of a .note file:

```bash
# Using CLI tool
obsidian-supernote inspect input.note --save-images output_dir/

# Using analysis script (more detailed)
python examples/analysis/dump_structure.py input.note
```

## Templates

### blank_template.png
- **Dimensions:** 1404 x 1872 pixels (A5X native resolution)
- **Format:** PNG, RGB, white background
- **Usage:** Copy to Supernote's `MyStyle/` folder to use as custom template

### sample_document.pdf
- **Pages:** 2
- **Usage:** Copy to Supernote's `Document/` folder to use as PDF template

## Configuration

See `config.example.yml` for configuration options including:

- Obsidian vault path
- Supernote sync folder
- File naming patterns
- Sync preferences

## Golden Sources Test Matrix

| # | Name | Template | Mode | Purpose |
|---|------|----------|------|---------|
| 01 | standard_png_blank | PNG | Standard | Baseline PNG+Standard |
| 02 | standard_png_written | PNG | Standard | Stroke storage |
| 03 | realtime_png_blank | PNG | Real-time | Baseline PNG+Real-time |
| 04 | realtime_png_written | PNG | Real-time | Recognition data |
| 05 | standard_pdf_blank | PDF | Standard | Baseline PDF+Standard |
| 06 | standard_pdf_written | PDF | Standard | PDF stroke storage |
| 07 | realtime_pdf_blank | PDF | Real-time | Baseline PDF+Real-time |
| 08 | realtime_pdf_written | PDF | Real-time | PDF recognition |
| 09 | standard_none_blank | None | Standard | No template baseline |
| 10 | standard_none_written | None | Standard | Basic strokes |
| 11 | realtime_none_written | None | Real-time | Basic recognition |
| 12 | standard_multipage | None | Standard | Page structure |
| 13 | standard_multilayer | None | Standard | Layer structure |

See `golden_sources/README.md` for detailed creation instructions.
