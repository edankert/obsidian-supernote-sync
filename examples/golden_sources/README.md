# Golden Sources for .note Format Reverse Engineering

**Created:** 2026-01-18
**Purpose:** Systematic analysis of Supernote .note file format variations

## Overview

This directory contains reference .note files created directly on a Supernote device to serve as "golden sources" for reverse engineering the file format. By creating notes with different configurations and comparing their binary structures, we can understand the exact format requirements.

## Background

The Supernote supports two note creation modes:

### Standard Mode
- Supports **multiple layers** (MAINLAYER, LAYER1, LAYER2, LAYER3, BGLAYER)
- Handwriting stored as vector strokes (RATTA_RLE encoding)
- No automatic text recognition during writing
- Recognition can be triggered manually after writing

### Real-Time Recognition Mode
- **Single layer only** (no multi-layer support)
- Handwriting converted to machine-readable text in real-time
- Recognition data stored in note metadata
- Uses MyScript iink technology

### Template Types
- **PNG Template**: Single-page custom background image (device-specific resolution)
  - A5X2 (Manta): 1920 x 2560 pixels
  - A5X/A6X: 1404 x 1872 pixels
- **PDF Template**: Multi-page document, each page becomes a template

**Note:** Supernote requires a template for all notes - there is no "no template" option.

## Test Matrix

| # | Filename | Template | Mode | Content | Key Questions |
|---|----------|----------|------|---------|---------------|
| 01 | `standard_png_blank.note` | PNG | Standard | Empty | Baseline for PNG+Standard |
| 02 | `standard_png_written.note` | PNG | Standard | Handwriting | How are strokes stored? |
| 03 | `realtime_png_blank.note` | PNG | Real-time | Empty | Baseline for PNG+Real-time |
| 04 | `realtime_png_written.note` | PNG | Real-time | Handwriting | Where is recognized text? |
| 05 | `standard_pdf_blank.note` | PDF | Standard | Empty | Baseline for PDF+Standard |
| 06 | `standard_pdf_written.note` | PDF | Standard | Handwriting | Compare with PNG version |
| 07 | `realtime_pdf_blank.note` | PDF | Real-time | Empty | Baseline for PDF+Real-time |
| 08 | `realtime_pdf_written.note` | PDF | Real-time | Handwriting | Recognition + PDF combo |
| 09 | `standard_multipage.note` | PNG | Standard | Multi-page | Page addressing structure |
| 10 | `standard_multilayer.note` | PNG | Standard | Multi-layer | Layer structure when used |

## Key Research Questions

### 1. Header Differences
- Does `FILE_RECOGN_TYPE` indicate standard (0) vs real-time (1)?
- What other header fields change between modes?

### 2. Layer Structure
- How many layer metadata blocks in real-time mode?
- Is BGLAYER structure different?

### 3. Recognition Data Storage
- Where is recognized text stored? (`RECOGNTEXT`? `RECOGNFILE`?)
- What format is the recognition data?

### 4. Footer Mysteries
- What is `PDFSTYLELIST` and how is it calculated?
- Why do some files have `IS_OLD_APPLY_EQUIPMENT:1` and others `0`?
- What determines the `STYLE_style_white_a5x2` entry?

### 5. Template Handling
- How does the device validate PNG dimensions?
- What happens if PNG size doesn't match device resolution?
- Does A5X2 (1920x2560) use different format than A5X (1404x1872)?

## Directory Structure

```
golden_sources/
├── README.md                    # This file
│
├── png_template/                # PNG-based notes
│   ├── standard_png_blank.note
│   ├── standard_png_written.note
│   ├── realtime_png_blank.note
│   ├── realtime_png_written.note
│   └── analysis.md              # Findings from comparison
│
├── pdf_template/                # PDF-based notes
│   ├── standard_pdf_blank.note
│   ├── standard_pdf_written.note
│   ├── realtime_pdf_blank.note
│   ├── realtime_pdf_written.note
│   └── analysis.md
│
└── edge_cases/                  # Additional test cases
    ├── standard_multipage.note
    ├── standard_multilayer.note
    └── analysis.md
```

## How to Create Golden Sources

### Prerequisites
1. Supernote device (A5X2/Manta, A5X, A6X2/Nomad, A6X)
2. Appropriate `blank_template_*.png` copied to device's `MyStyle/` folder:
   - A5X2 (Manta): Use `blank_template_a5x2.png` (1920x2560)
   - A5X/A6X: Use `blank_template_a5x.png` (1404x1872)
3. `sample_document.pdf` copied to device's `Document/` folder

### Steps for Each Note

#### PNG Template Notes (01-04)
1. Open Note app on Supernote
2. Create new note
3. Select "Template" → Choose `blank_template.png` from MyStyle
4. For Standard mode: Keep default settings
5. For Real-time mode: Enable real-time recognition in settings
6. For "written" variants: Write "Hello World" on the page
7. Save and name according to test matrix
8. Sync via Supernote Partner app

#### PDF Template Notes (05-08)
1. Create new note with PNG template
2. Go to note settings → "Change Template"
3. Select `sample_document.pdf` from Documents
4. This converts the note to use PDF pages as templates
5. For Standard/Real-time: Set mode before writing
6. For "written" variants: Write on first page
7. Save and sync

#### Edge Cases (09-10)
1. **Multipage**: Create note with PNG template, add 3+ pages manually
2. **Multilayer**: Create note with PNG template, use Layer menu to draw on LAYER1 and LAYER2

### After Syncing
1. Copy .note files from Supernote Partner sync folder:
   `C:\Users\{user}\AppData\Roaming\com.ratta\supernote_partner\...\Supernote\Note\`
2. Place in appropriate subdirectory under `golden_sources/`
3. Run analysis scripts to compare

## Analysis Tools

### dump_structure.py
Dumps complete structure of a .note file:
```bash
python examples/analysis/dump_structure.py golden_sources/png_template/01_standard_png_blank.note
```

### compare_notes.py
Compares two .note files and highlights differences:
```bash
python examples/analysis/compare_notes.py \
    golden_sources/png_template/01_standard_png_blank.note \
    golden_sources/png_template/03_realtime_png_blank.note
```

## Expected Findings

Based on initial research, we expect to find:

| Field | Standard Mode | Real-Time Mode |
|-------|---------------|----------------|
| FILE_RECOGN_TYPE | 0 or 1? | 1? |
| Layer count | 5 | 1 or 2? |
| RECOGNTEXT | 0 | Actual text? |
| RECOGNFILE | 0 | File reference? |
| RECOGNSTATUS | 0 | 1? |

## Status

- [x] Templates created and copied to device
- [x] PNG template notes created (01-04)
- [x] PDF template notes created (05-08)
- [x] Edge case notes created (09-10)
- [x] All files synced and copied to golden_sources/
- [ ] Analysis complete

## References

- [.note File Format Analysis](../../../Notes%20Vault/03%20Projects/Obsidian-Supernote%20Sync/Obsidian-Supernote%20Sync%20-%20.note%20File%20Format%20Analysis.md)
- [supernotelib source code](../../venv/Lib/site-packages/supernotelib/)
- [Supernote Tool GitHub](https://github.com/jya-dev/supernote-tool)
