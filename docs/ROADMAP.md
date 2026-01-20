# Obsidian-Supernote Sync Roadmap

**Last Updated:** 2026-01-20
**Status:** Phase 3 In Progress - Core Converters Complete, Workflow Automation Planned
**PRD Location:** `C:\Edwin\Notes Vault\03 Projects\Obsidian-Supernote Sync\Obsidian-Supernote Sync Tool.md`

## Recent Additions (2026-01-20)

- ✨ Frontmatter properties for .note type control (`supernote_type`, `supernote_linked_file`)
- ✨ .note file update mode (replace template while preserving annotations/sketches)
- ✨ Realtime note type support for annotation workflows (Research Notes)
- ✨ Progressive automation levels for each workflow (Manual → Semi-Auto → Full Automation)

## Phase Mapping

| PRD Phase | Project Phase | Status |
|-----------|---------------|--------|
| Phase 1: Research & Discovery | - | ✅ Complete |
| Phase 2: Decision & Planning | - | ✅ Complete |
| Phase 2.5: .note Format Research | Phase 1: Fix .note Generation | ✅ Complete |
| Phase 3: Prototype Development | Phase 2: Complete Conversion Pipeline | 🔄 In Progress |
| Phase 4: Testing & Refinement | - | Upcoming |
| Phase 5: Production & Enhancement | Phase 3: Automated Sync | Planned |

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
| Markdown → .note | ✅ Working | Via Pandoc → PDF → .note pipeline |
| PDF → .note | ✅ Working | Device-tested, opens and allows writing |
| PNG → .note | ✅ Working | Device-tested, opens and allows writing |
| .note → PNG | ✅ Working | Via supernotelib |
| .note → Markdown | ✅ Working | Via supernotelib + note_to_obsidian.py |
| Golden sources | ✅ Complete | 10 reference files from Manta device |

## Phases

### PRD Phases 1-2.5: Research & .note Generation ✅ COMPLETE

**Goal:** Understand .note format and generate files that the Supernote device accepts

**Completed 2026-01-19** - Full .note format reverse-engineered. PNG, PDF, and Markdown converters working on device.

#### Key Discoveries

| Issue | Solution |
|-------|----------|
| Device equipment code | Use `N5` for Manta (not `A5X2`) |
| IS_OLD_APPLY_EQUIPMENT | Must be `1` |
| MODULE_LABEL | Use `none` (not `SNFILE_FEATURE`) |
| BGLAYER LAYERTYPE | Use `NOTE` (not `MARK`) |
| Missing "tail" marker | Add `tail` (4 bytes) after footer content |
| Layer count | All 5 layers must be referenced (unused = address 0) |
| LAYERINFO format | Uses `#` instead of `:` as JSON separator |

#### Converter Functions

**PNG Template Converter:**
```python
from obsidian_supernote.converters.note_writer import convert_png_to_note
convert_png_to_note("template.png", "output.note", device="A5X2")
```

**PDF Template Converter:**
```python
from obsidian_supernote.converters.note_writer import convert_pdf_to_note
convert_pdf_to_note("document.pdf", "output.note", device="A5X2")
```

**Markdown Converter:**
```python
from obsidian_supernote.converters.note_writer import convert_markdown_to_note
convert_markdown_to_note("document.md", "output.note", device="A5X2")

# With realtime handwriting recognition
convert_markdown_to_note("document.md", "output.note", realtime=True)

# With custom page settings
convert_markdown_to_note("document.md", "output.note", page_size="A5", margin="2cm", font_size=11)
```

### PRD Phase 3: Prototype Development (IN PROGRESS)

**Goal:** Reliable end-to-end conversion in both directions + sync state tracking

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

### PRD Phases 4-5: Testing, Refinement & Automated Sync (PLANNED)

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
