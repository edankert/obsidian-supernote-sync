# Obsidian-Supernote Sync Roadmap

**Last Updated:** 2026-01-18
**Status:** Phase 1 - Fixing .note Generation

## End Goal

Bi-directional sync between Obsidian and Supernote:

```
┌─────────────────┐                      ┌─────────────────┐
│    OBSIDIAN     │                      │   SUPERNOTE     │
│                 │                      │                 │
│  Markdown notes │  ───────────────►    │  .note files    │
│  with text      │  (annotate on device)│  with handwriting│
│                 │                      │                 │
│  Markdown +     │  ◄───────────────    │  Handwritten    │
│  embedded PNGs  │  (review in Obsidian)│  annotations    │
└─────────────────┘                      └─────────────────┘
```

### Use Cases

1. **Obsidian → Supernote**: Convert markdown notes to annotatable .note files
   - Daily notes for handwritten additions
   - Documents for review and markup
   - Templates for repeated workflows

2. **Supernote → Obsidian**: Import handwritten notes as markdown
   - Meeting notes with embedded page images
   - Sketches and diagrams
   - Handwritten journal entries

## Current State

| Component | Status | Notes |
|-----------|--------|-------|
| Markdown → PDF | ✅ Working | Via Pandoc + MiKTeX |
| PDF → .note | ⚠️ Partial | supernotelib reads it, device rejects as "corrupted" |
| .note → PNG | ✅ Working | Via supernotelib |
| .note → Markdown | ✅ Working | Via supernotelib + note_to_obsidian.py |
| Golden sources | ✅ Complete | 10 reference files from Manta device |

## Phases

### Phase 1: Fix .note Generation (Current)

**Goal:** Generate .note files that the Supernote device accepts

#### Step 1.1: Analyze Golden Sources

Compare real device files with generated files to identify differences:

```bash
cd C:\Edwin\repos\obsidian-supernote-sync

# Dump a real PNG-template note
python examples/analysis/dump_structure.py \
    examples/golden_sources/png_template/standard_png_blank.note

# Dump a real PDF-template note
python examples/analysis/dump_structure.py \
    examples/golden_sources/pdf_template/standard_pdf_blank.note

# Compare real vs generated PDF-based files
python examples/analysis/compare_notes.py \
    examples/golden_sources/pdf_template/standard_pdf_blank.note \
    examples/pdf_to_note/sample_document.note
```

#### Step 1.2: Identify Format Differences

Known suspects from initial analysis:

| Field | Generated | Real File | Action |
|-------|-----------|-----------|--------|
| PDFSTYLELIST | Missing | Present (e.g., 494) | Investigate purpose |
| IS_OLD_APPLY_EQUIPMENT | 0 | 1 | Test with 1 |
| STYLE_style_white_a5x2 | Missing | Present | Add default style |

#### Step 1.3: Update note_writer.py

Fix the format based on analysis findings:
- File: `obsidian_supernote/converters/note_writer.py`
- Test after each change with supernotelib first, then device

#### Step 1.4: Device Testing

1. Generate test .note file
2. Copy to Supernote via Partner app or USB
3. Attempt to open on device
4. If fails, compare with working file and iterate

### Phase 2: Complete Conversion Pipeline

**Goal:** Reliable end-to-end conversion in both directions

#### Step 2.1: Obsidian → Supernote Workflow

```bash
# Convert markdown to PDF
obsidian-supernote md-to-pdf "My Note.md" "My Note.pdf"

# Convert PDF to .note
obsidian-supernote pdf-to-note "My Note.pdf" "My Note.note"

# Copy to Supernote device
cp "My Note.note" /path/to/supernote/Note/
```

#### Step 2.2: Supernote → Obsidian Workflow

```bash
# Convert .note to markdown with embedded images
obsidian-supernote note-to-md "Handwritten.note" "Handwritten.md"

# Output structure:
# Handwritten.md
# Handwritten_page_01.png
# Handwritten_page_02.png
```

#### Step 2.3: CLI Improvements

- Add `--device` flag for device-specific settings
- Add `--output-dir` for batch processing
- Add progress indicators for large files

### Phase 3: Automated Sync

**Goal:** Automatic synchronization without manual commands

#### Step 3.1: File Watching

- Monitor Obsidian vault for markdown changes
- Monitor Supernote sync folder for .note changes
- Auto-convert on file changes

#### Step 3.2: Sync Engine

```yaml
# config.yml
sync:
  obsidian_vault: "C:/Edwin/Notes Vault"
  supernote_folder: "C:/Users/Edwin/Supernote/Note"

  # Folders to sync
  mappings:
    - obsidian: "02 Journal/Daily Notes"
      supernote: "Personal/[02] Journal/Daily Notes"
      direction: bidirectional

    - obsidian: "03 Projects"
      supernote: "Work/[03] Projects"
      direction: obsidian_to_supernote
```

#### Step 3.3: Conflict Resolution

- Detect when both sides have changes
- Options: keep newest, keep both, manual merge
- Track sync state in SQLite database

#### Step 3.4: Cloud Integration (Optional)

- Integrate with Supernote Cloud API
- Sync without USB connection
- Real-time sync when online

## File Structure

```
obsidian-supernote-sync/
├── obsidian_supernote/
│   ├── cli.py                    # Command-line interface
│   ├── converters/
│   │   ├── markdown_to_pdf.py    # MD → PDF
│   │   ├── pandoc_converter.py   # Pandoc integration
│   │   ├── note_writer.py        # PDF → .note (needs fixing)
│   │   └── note_to_obsidian.py   # .note → MD
│   ├── parsers/
│   │   └── note_parser.py        # .note file parsing
│   └── sync/
│       ├── sync_engine.py        # (Phase 3)
│       └── state_tracker.py      # (Phase 3)
├── examples/
│   ├── templates/                # PNG/PDF templates
│   ├── golden_sources/           # Reference .note files
│   └── analysis/                 # Analysis scripts
└── docs/
    ├── ROADMAP.md                # This file
    └── IMPLEMENTATION_STATUS.md  # Detailed status
```

## Device Support

| Device | Model | Resolution | DPI | Status |
|--------|-------|------------|-----|--------|
| A5X2 | Manta | 1920 x 2560 | 300 | Primary target |
| A5X | - | 1404 x 1872 | 226 | Supported |
| A6X2 | Nomad | 1404 x 1872 | 300 | Supported |
| A6X | - | 1404 x 1872 | 300 | Supported |

## References

- [.note File Format Analysis](../../Notes%20Vault/03%20Projects/Obsidian-Supernote%20Sync/Obsidian-Supernote%20Sync%20-%20.note%20File%20Format%20Analysis.md)
- [supernotelib GitHub](https://github.com/jya-dev/supernote-tool)
- [Golden Sources README](../examples/golden_sources/README.md)

## Contributing

1. Run analysis scripts to understand current state
2. Make changes to note_writer.py
3. Test with supernotelib: `python -c "import supernotelib; nb = supernotelib.load_notebook('test.note'); print(nb)"`
4. Test on actual device
5. Document findings in analysis.md files
