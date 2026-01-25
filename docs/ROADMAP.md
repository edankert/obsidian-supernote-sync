# Obsidian-Supernote Sync Roadmap

**Last Updated:** 2026-01-24
**Status:** Phase 3A Complete - Ready for Phase 3B (Web Dashboard)
**PRD Location:** `C:\Edwin\Notes Vault\03 Projects\Obsidian-Supernote Sync\Obsidian-Supernote Sync Tool.md`

## Recent Additions (2026-01-24)

- ✅ **Phase 3A COMPLETE:** Python Backend API
  - ✅ FastAPI server with REST endpoints for all conversions
  - ✅ WebSocket support for real-time progress updates
  - ✅ Workflow management and execution
  - ✅ `obsidian-supernote serve` CLI command
  - ✅ Pre-defined workflows loaded from `examples/configs/`

## Previous Completions

- ✅ **Step 1:** Frontmatter property parsing (34 tests, 92% coverage)
- ✅ **Step 2:** .note file update mode (preserves handwriting)
- ✅ **Step 3:** Realtime note type support
- ✅ **Step 4:** Configuration examples & documentation

## Phase Mapping

| PRD Phase | Project Phase | Status |
|-----------|---------------|--------|
| Phase 1: Research & Discovery | - | ✅ Complete |
| Phase 2: Decision & Planning | - | ✅ Complete |
| Phase 2.5: .note Format Research | Phase 1: Fix .note Generation | ✅ Complete |
| Phase 3: Prototype Development | Phase 2: Manual CLI Complete | ✅ Complete |
| Phase 4: Testing & Refinement | Phase 3A: Python Backend API | ✅ Complete |
| Phase 5: Production & Enhancement | Phase 3B-D: UI & Workflow Builder | ⏳ Next |

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

#### Step 1: Frontmatter Property Parsing ✅ COMPLETE (2026-01-22)

**Implemented:**
```bash
# Convert markdown directly to .note with frontmatter support
obsidian-supernote md-to-note "My Note.md" "output/My Note.note"

# Markdown is automatically updated with file reference:
# supernote.file: "[output/My Note.note]"
```

**Features:**
- ✅ Parse `supernote.type` (standard/realtime) from frontmatter
- ✅ Auto-update markdown with `supernote.file` using [x.note] notation
- ✅ New `md-to-note` CLI command
- ✅ 34 tests, 92% coverage

#### Step 2: .note File Update Mode ✅ COMPLETE (2026-01-22)

**Implemented:**
- ✅ Read existing .note file when `supernote.file` is present
- ✅ Extract and preserve annotation layers (ZIP archive)
- ✅ Replace template/background only
- ✅ Maintain handwriting and sketches
- ✅ Automatic update mode detection
- ✅ Graceful fallback when no handwriting exists

#### Step 2.1: Obsidian → Supernote Workflow (Alternative)

```bash
# Two-step workflow (if md-to-note not used)
obsidian-supernote md-to-pdf "My Note.md" "My Note.pdf"
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

#### Step 4: Configuration Examples & Documentation ✅ COMPLETE (2026-01-24)

**Implemented:**
- ✅ Workflow guides with step-by-step instructions
  - `examples/workflows/daily-notes/README.md`
  - `examples/workflows/research-notes/README.md`
  - `examples/workflows/world-building/README.md`
- ✅ Example templates and complete examples
  - Templates for each workflow
  - Filled-in examples showing real usage
- ✅ Configuration files for future sync engine
  - `examples/configs/daily-notes-config.yml`
  - `examples/configs/research-notes-config.yml`
  - `examples/configs/world-building-config.yml`
- ✅ Updated main README with workflow table

### Phase 3: Hybrid UI Architecture (Phase 3A Complete)

**Goal:** User-friendly interface via Obsidian Plugin + Python Backend + Web Dashboard

#### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN PLUGIN (TypeScript)                  │
│  Ribbon icon, commands, sidebar status view                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP API
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 PYTHON BACKEND (FastAPI) ✅ COMPLETE             │
│  REST API, WebSocket progress, serves web dashboard              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 WEB DASHBOARD (React)                            │
│  Visual workflow designer, pre-defined templates, config         │
└─────────────────────────────────────────────────────────────────┘
```

#### Phase 3A: Python Backend API (✅ Complete)

```bash
# Start backend server
obsidian-supernote serve --port 8765

# API Endpoints:
# GET  /status                - Health check and version
# GET  /status/dependencies   - Check Pandoc, supernotelib, Pillow
# POST /convert/md-to-note    - Convert markdown to .note
# POST /convert/note-to-md    - Export .note to markdown
# POST /convert/pdf-to-note   - Convert PDF to .note
# POST /convert/png-to-note   - Convert PNG to .note
# POST /convert/batch         - Batch conversion
# GET  /workflows             - List saved workflows
# POST /workflows/{id}/run    - Execute workflow
# WS   /events                - Real-time progress updates
```

**Files Created:**
- `obsidian_supernote/api/server.py` - FastAPI app + WebSocket endpoint
- `obsidian_supernote/api/websocket.py` - ConnectionManager + ProgressReporter
- `obsidian_supernote/api/routes/convert.py` - Conversion endpoints
- `obsidian_supernote/api/routes/workflows.py` - Workflow management
- `obsidian_supernote/api/routes/status.py` - Health/status endpoints

#### Phase 3B: Web Dashboard MVP (✅ Complete)

- ✅ React + Vite + Tailwind CSS project setup
- ✅ Pre-defined workflow selection UI
- ✅ Quick Convert panel for manual conversions
- ✅ Sync status display with WebSocket integration
- ✅ Integration testing with backend
- ✅ Error boundary for graceful error handling

**Files Created:**
- `web-dashboard/src/App.tsx` - Main dashboard component
- `web-dashboard/src/components/` - StatusBar, WorkflowCard, ConvertPanel, ProgressIndicator, ErrorBoundary
- `web-dashboard/src/hooks/` - useWebSocket, useApi hooks
- `web-dashboard/src/api/client.ts` - API client for backend communication
- `web-dashboard/src/types/index.ts` - TypeScript type definitions

#### Phase 3C: Obsidian Plugin (Planned)

- Ribbon button for quick actions
- Commands: Convert, Open Dashboard, Sync All
- Settings tab for backend URL
- Sidebar status view

#### Phase 3D: Visual Workflow Builder (Planned)

- Drag-and-drop workflow designer
- Building blocks: source, transform, output
- Save/load custom workflows
- Template library

## File Structure

```
obsidian-supernote-sync/
├── obsidian_supernote/
│   ├── cli.py                    # Command-line interface
│   ├── converters/
│   │   ├── markdown_to_pdf.py    # MD → PDF
│   │   ├── pandoc_converter.py   # Pandoc integration
│   │   ├── note_writer.py        # PDF → .note
│   │   └── note_to_obsidian.py   # .note → MD
│   ├── parsers/
│   │   └── note_parser.py        # .note file parsing
│   ├── api/                      # NEW: FastAPI backend (Phase 3A)
│   │   ├── server.py             # FastAPI app
│   │   ├── routes/
│   │   │   ├── convert.py        # Conversion endpoints
│   │   │   ├── workflows.py      # Workflow management
│   │   │   └── status.py         # Health/status
│   │   └── websocket.py          # Real-time events
│   └── workflows/                # NEW: Workflow engine (Phase 3A)
│       ├── engine.py             # Workflow executor
│       └── storage.py            # YAML/SQLite storage
├── web-dashboard/                # NEW: React app (Phase 3B)
│   ├── src/
│   └── package.json
├── obsidian-plugin/              # NEW: TypeScript plugin (Phase 3C)
│   ├── src/
│   └── manifest.json
├── examples/
│   ├── workflows/                # Pre-defined workflow guides
│   ├── templates/                # PNG/PDF templates
│   └── golden_sources/           # Reference .note files
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
