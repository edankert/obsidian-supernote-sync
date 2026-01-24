# Implementation Plan: Obsidian-Supernote Sync Tool

**Last Updated:** 2026-01-24
**Status:** Phase 2 Complete - Starting Phase 3 (Hybrid UI Architecture)
**Current Phase:** Manual CLI Complete → Hybrid UI (Plugin + Backend + Dashboard)

## Overview

This document outlines the implementation plan for the Obsidian-Supernote Sync tool, structured around three distinct user workflows (Daily Notes, Research Notes, World Building) with progressive automation levels (Manual → Semi-Automated → Full Automation).

### End State Vision

**Goal:** Bi-directional synchronization between Obsidian and Supernote with intelligent automation:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MANUAL (Phase 2)                              │
│  User: Run CLI commands, control timing, review each sync      │
│  Tool: Convert formats, preserve annotations, track state       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              SEMI-AUTOMATED (Phase 3)                            │
│  User: Tag files, run periodic sync, handle conflicts           │
│  Tool: Monitor folders, auto-convert, detect changes            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│               FULLY AUTOMATED (Phase 4+)                         │
│  User: Just edit/annotate, sync happens seamlessly             │
│  Tool: Continuous monitoring, auto-sync, intelligent merging    │
└─────────────────────────────────────────────────────────────────┘
```

## Current State (As of 2026-01-20)

### ✅ Completed

**Core Converters:**
- Markdown → PDF (via Pandoc/WeasyPrint)
- PDF → .note (device-tested on Manta)
- PNG → .note (device-tested on Manta)
- Markdown → .note (via PDF pipeline)
- .note → PNG (via supernotelib)
- .note → Markdown (via supernotelib + custom converter)

**Architecture:**
- Cloud-based sync strategy (Supernote Cloud API)
- Device recognition-based text extraction (no external OCR needed)
- Three user workflows defined with detailed specifications
- Three automation levels per workflow with configuration examples

**Documentation:**
- Comprehensive PRD with workflows and use cases
- Technical requirements specification
- Feature dependency matrix
- Migration paths and examples

### ✅ Recently Completed

- Step 1: Frontmatter property parsing (34 tests, 92% coverage)
- Step 2: .note file update mode (preserves handwriting)
- Step 3: Realtime recognition support
- Step 4: Configuration examples & documentation

### ❌ Not Started (Phase 3)

- File watching/monitoring system
- Batch operations
- Change detection (MD5 hashing)
- Sync database (SQLite)
- Sync engine with conflict resolution
- Cloud API integration
- GUI interface

## Phase 2: Manual CLI with Frontmatter Support (6-8 weeks)

**Goal:** Enable users to control .note type and updates via frontmatter properties, with manual CLI commands.

### Step 1: Frontmatter Property Parsing (2 weeks)

**Objective:** CLI reads and respects frontmatter properties for conversion control.

**Tasks:**
- [ ] **1.1:** Update markdown parsing to extract frontmatter properties
  - File: `obsidian_supernote/converters/markdown_to_pdf.py`
  - Properties to read: `supernote_type`, `supernote_linked_file`, `supernote_device`, `supernote_page_size`, `supernote_realtime`
  - Fallback to defaults if properties missing

- [ ] **1.2:** Implement `supernote_type` handling
  - Read `supernote_type` property from frontmatter
  - Options: "standard", "realtime" (default: "standard")
  - Pass to .note conversion pipeline

- [ ] **1.3:** Implement `supernote_linked_file` detection
  - Read `supernote_linked_file` property
  - Determine if updating existing .note or creating new
  - Set conversion mode flag

- [ ] **1.4:** Add device-specific property handling
  - Read `supernote_device` (A5X, A5X2, A6X, A6X2)
  - Read `supernote_page_size` (A4, A5, A6, Letter)
  - Read `supernote_realtime` (true/false)
  - Apply to converter settings

- [ ] **1.5:** Update CLI commands to auto-detect properties
  - `md-to-note` command reads frontmatter automatically
  - CLI flags override frontmatter if specified
  - Log which properties are being used

- [ ] **1.6:** Add frontmatter property validation
  - Validate property values are valid options
  - Warn if invalid values found
  - Use defaults for missing properties

**Success Criteria:**
- ✅ CLI reads frontmatter properties from markdown
- ✅ Properties override default settings
- ✅ Properties are optional (graceful fallback)
- ✅ Validation prevents invalid configurations

**Example Test:**
```markdown
---
title: "Article"
supernote_type: realtime
supernote_device: A5X2
---
```
Command: `obsidian-supernote md-to-note article.md article.note`
Result: Creates realtime note for A5X2 device

---

### Step 2: .note File Update Mode (3-4 weeks)

**Objective:** CLI can update existing .note files while preserving handwritten annotations.

**Tasks:**
- [ ] **2.1:** Implement layer detection in .note files
  - File: `obsidian_supernote/converters/note_writer.py`
  - Read .note file structure (already partially done)
  - Identify template layer (Layer 1) vs annotation layers (Layers 2-5)
  - Extract layer boundaries and metadata

- [ ] **2.2:** Extract annotation layers from .note
  - Read Layers 2-5 as separate binary data
  - Store layer metadata (offsets, sizes, types)
  - Save to temporary files for reassembly

- [ ] **2.3:** Implement template replacement logic
  - Generate new PDF from updated markdown
  - Render PDF to appropriate dimensions
  - Replace Layer 1 (template) with new content
  - Update template metadata (sizes, MD5s, IDs)

- [ ] **2.4:** Implement layer reassembly
  - Combine new Layer 1 with preserved Layers 2-5
  - Recalculate file offsets and positions
  - Update footer metadata with new calculations
  - Maintain layer type and metadata integrity

- [ ] **2.5:** Add update mode to CLI
  - New flag: `--update-existing` or auto-detect from `supernote_linked_file`
  - New flag: `--preserve-annotations` (default: true)
  - Validate existing .note file format before updating
  - Error handling if .note file is corrupted

- [ ] **2.6:** Implement dimension change handling
  - Handle case where new PDF has different page size
  - Adjust layer offsets if needed
  - Test with various page size transitions
  - Warn user if significant resize needed

- [ ] **2.7:** Validate updated .note file integrity
  - Test that updated .note opens on device
  - Verify all layers are readable
  - Verify handwritten content is intact
  - Check file size is reasonable

**Success Criteria:**
- ✅ Can update existing .note files
- ✅ Handwritten annotations preserved exactly
- ✅ New template content displays correctly
- ✅ Updated .note opens on device without errors
- ✅ File size remains reasonable

**Example Test:**
```bash
# Create initial .note with article
obsidian-supernote md-to-note article.md article.note

# [User annotates on device]

# Update article.md with new content
# Re-run conversion with update flag
obsidian-supernote md-to-note article.md article.note --update-existing

# Result: article.note has new content + original annotations
```

---

### Step 3: Realtime Handwriting Recognition Support (1-2 weeks)

**Objective:** .note files support realtime handwriting recognition for text capture.

**Tasks:**
- [ ] **3.1:** Add realtime parameter to PDF→.note conversion
  - File: `obsidian_supernote/converters/note_writer.py`
  - Parameter: `realtime=True/False`
  - Default to reading from `supernote_type` frontmatter property

- [ ] **3.2:** Implement realtime metadata generation
  - Set `IS_REALTIME_RECOGNITION: 1` in .note metadata
  - Enable recognition layer in .note structure
  - Configure for device's character recognition

- [ ] **3.3:** Test realtime note creation
  - Create test .note with realtime enabled
  - Create test .note with realtime disabled
  - Verify on device that recognition works
  - Compare file size and structure

- [ ] **3.4:** Document realtime vs standard behavior
  - When to use realtime (annotations with text)
  - When to use standard (pure sketching)
  - Performance and file size implications

**Success Criteria:**
- ✅ Realtime notes created correctly
- ✅ Device recognizes handwriting in realtime notes
- ✅ Standard notes work as before
- ✅ User can choose via frontmatter property

**Example Test:**
```yaml
---
supernote_type: realtime  # Enable character recognition
---
```
Result: Created note shows text recognition as user writes on device

---

### Step 4: Configuration Examples & Documentation ✅ COMPLETE

**Objective:** Provide ready-to-use configuration examples for all workflows and automation levels.

**Tasks:**
- [x] **4.1:** Create example frontmatter templates
  - ✅ Daily Notes template and example (`examples/workflows/daily-notes/`)
  - ✅ Research Notes template and example (`examples/workflows/research-notes/`)
  - ✅ World Building template and example (`examples/workflows/world-building/`)

- [x] **4.2:** Create workflow configuration files
  - ✅ `examples/configs/daily-notes-config.yml`
  - ✅ `examples/configs/research-notes-config.yml`
  - ✅ `examples/configs/world-building-config.yml`

- [x] **4.3:** Create step-by-step workflow guides
  - ✅ README for each workflow with step-by-step instructions
  - ✅ Before/after examples included
  - ✅ Troubleshooting tips in each guide

- [x] **4.4:** Update main README
  - ✅ Quick start with frontmatter properties
  - ✅ Workflow guides table with links
  - ✅ Feature status updates

**Success Criteria:**
- ✅ Users can copy-paste examples
- ✅ Examples are self-documented
- ✅ Works without modification
- ✅ Clear instructions for customization

**Completed:** 2026-01-24

---

### Phase 2 Testing Strategy

**Unit Tests:**
- [ ] Frontmatter property parsing
- [ ] Property validation
- [ ] Layer extraction from .note files
- [ ] Layer reassembly logic
- [ ] Realtime metadata generation

**Integration Tests:**
- [ ] End-to-end: markdown → realtime .note
- [ ] End-to-end: update existing .note
- [ ] End-to-end: standard vs realtime comparison
- [ ] Device testing on physical Supernote

**User Acceptance Testing:**
- [ ] Daily Notes workflow (Manual Level 1)
- [ ] Research Notes workflow (Manual Level 1)
- [ ] World Building workflow (Manual Level 1)

---

## Phase 3: Hybrid UI Architecture (10-14 weeks)

**Goal:** Create a user-friendly interface for managing conversions and workflows via a hybrid Obsidian Plugin + Python Backend + Web Dashboard architecture.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN PLUGIN (TypeScript)                  │
│  - Ribbon icon, commands, status bar                            │
│  - Quick actions: Convert current file, Sync All                │
│  - Settings tab for backend URL and defaults                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP API
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 PYTHON BACKEND (FastAPI Server)                  │
│  - REST API wrapping existing converters (100% reuse)           │
│  - Workflow execution engine                                    │
│  - WebSocket for real-time progress updates                     │
│  - Serves web dashboard static files                            │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Serves static files
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 WEB DASHBOARD (React SPA)                        │
│  - Visual workflow designer (drag-and-drop)                     │
│  - Pre-defined workflow templates                               │
│  - Configuration panels for devices, folders                    │
│  - Sync history and status display                              │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 3A: Python Backend API (2-3 weeks)

- [ ] **3A.1:** Create FastAPI server structure
  - File: `obsidian_supernote/api/server.py`
  - Basic server setup with CORS, static file serving
  - Health check endpoint `/status`

- [ ] **3A.2:** Implement conversion endpoints
  - File: `obsidian_supernote/api/routes/convert.py`
  - `POST /convert/md-to-note` - Single file conversion
  - `POST /convert/note-to-md` - Export .note file
  - `POST /batch/convert` - Batch conversion

- [ ] **3A.3:** Add WebSocket support
  - File: `obsidian_supernote/api/websocket.py`
  - Real-time progress updates during conversion
  - Connection management for multiple clients

- [ ] **3A.4:** Implement workflow endpoints
  - File: `obsidian_supernote/api/routes/workflows.py`
  - `GET /workflows` - List saved workflows
  - `POST /workflows` - Create/update workflow
  - `POST /workflows/{id}/run` - Execute workflow

- [ ] **3A.5:** Add workflow storage
  - File: `obsidian_supernote/workflows/storage.py`
  - YAML-based workflow definitions
  - SQLite for sync state tracking

### Phase 3B: Web Dashboard MVP (2-3 weeks)

- [ ] **3B.1:** Set up React project with Vite
  - Directory: `web-dashboard/`
  - TypeScript, Tailwind CSS, shadcn/ui

- [ ] **3B.2:** Create pre-defined workflow UI
  - Select from Daily Notes, Research, World Building
  - Configure source/output folders
  - Run workflow with progress display

- [ ] **3B.3:** Add configuration panels
  - Device selection (A5X, A5X2/Manta, etc.)
  - Folder mappings
  - Conversion options

- [ ] **3B.4:** Implement sync status display
  - Recent conversions list
  - File mapping viewer
  - Error/warning display

### Phase 3C: Obsidian Plugin (2-3 weeks)

- [ ] **3C.1:** Set up TypeScript plugin skeleton
  - Directory: `obsidian-plugin/`
  - manifest.json, main.ts structure

- [ ] **3C.2:** Implement ribbon button and commands
  - `Convert to Supernote` - Convert current file
  - `Open Dashboard` - Open web dashboard
  - `Sync All` - Execute default workflow

- [ ] **3C.3:** Create settings tab
  - Backend URL configuration
  - Default device selection
  - Workflow selection

- [ ] **3C.4:** Add sidebar status view
  - Connection status
  - Pending files count
  - Last sync time

### Phase 3D: Visual Workflow Builder (3-4 weeks)

- [ ] **3D.1:** Implement drag-and-drop designer
  - React Flow integration
  - Block library (source, transform, output)
  - Connection validation

- [ ] **3D.2:** Create building blocks
  - Source blocks: Folder watch, single file, tag filter
  - Transform blocks: MD→Note, Note→MD, PDF→Note
  - Output blocks: Save to folder, update frontmatter

- [ ] **3D.3:** Add workflow save/load
  - YAML export/import
  - Template library
  - Share workflows

---

## Phase 4+: Advanced Features & Cloud Integration

**Goal:** Extended features including cloud sync and automation.

### Key Features

- [ ] **Cloud API integration**
  - Supernote Cloud API connection
  - Direct cloud sync without USB
  - Real-time change notifications

- [ ] **Scheduled workflows**
  - Cron-like scheduling
  - Folder watching with debounce
  - Background execution

- [ ] **Conflict resolution**
  - Detect simultaneous edits
  - Intelligent merge strategies
  - User-guided resolution options

- [ ] **Advanced workflow features**
  - Conditional logic blocks
  - Variables and templates
  - Webhook triggers

---

## Architecture Decisions

### 1. Frontmatter Properties Approach
- **Decision:** Use YAML frontmatter in markdown files
- **Rationale:** No separate config files, metadata travels with content, Obsidian-native
- **Tradeoffs:** Requires parsing, optional fields need good defaults

### 2. Hybrid UI Architecture (Phase 3)
- **Decision:** Obsidian Plugin + Python Backend (FastAPI) + Web Dashboard (React)
- **Rationale:**
  - 100% reuse of existing Python converters (no port to TypeScript)
  - Native Obsidian integration for quick actions
  - Web dashboard for complex configuration and visual workflow building
  - Separation of concerns: Plugin is lightweight, backend does heavy lifting
- **Tradeoffs:** Requires running backend server, more moving parts

### 3. Device-Based Text Recognition
- **Decision:** Use Supernote's built-in recognition (realtime notes) instead of external OCR
- **Rationale:** More accurate, no API costs, data stays on device, supernotelib extracts it
- **Tradeoffs:** Only works for realtime notes, depends on device implementation

### 4. Three Workflows Approach
- **Decision:** Define three distinct workflows with pre-defined templates
- **Rationale:** Users have different needs, templates provide quick start
- **Tradeoffs:** Custom workflows need visual builder (Phase 3D)

### 5. Manual UI-Driven Operations
- **Decision:** Replace background automation with user-triggered actions
- **Rationale:** Users want visibility and control over sync operations
- **Tradeoffs:** Slightly more user interaction required

---

## Dependencies & Prerequisites

### Core Dependencies
- Python 3.10+ (for async features)
- supernotelib (0.6.4+) - .note file handling
- Pandoc - Markdown to PDF conversion
- Pillow - Image processing
- PyYAML - Configuration parsing

### Optional Dependencies
- Supernote Cloud API credentials
- SQLite 3 (usually included with Python)
- watchdog - File system monitoring (Phase 3+)

### System Requirements
- Windows (primary), Linux/macOS support planned
- 500MB+ free disk space
- Internet connection for cloud sync
- Supernote device (A5X, A5X2/Manta, A6X, A6X2/Nomad)

---

## Success Metrics

### Phase 2 Success
- ✅ Users can control .note type via frontmatter
- ✅ Users can update existing .note files
- ✅ All three workflows work at Manual level
- ✅ Device testing successful for all converters
- ✅ 80%+ unit test coverage for new code

### Phase 3 Success
- ✅ Folder monitoring works reliably
- ✅ Batch operations 10x faster than manual
- ✅ Change detection accurate (MD5 hashing)
- ✅ Sync database tracks state correctly
- ✅ No data loss in any scenario tested

### Phase 4 Success
- ✅ Cloud sync works with low latency
- ✅ Conflicts resolved automatically (>80% of cases)
- ✅ Intelligent merging preserves both sides
- ✅ Background service stable 24/7
- ✅ User testing shows intuitive experience

---

## Risk Mitigation

### Risk 1: .note File Corruption During Update
**Mitigation:**
- Always work on copies first
- Validate file structure before and after
- Maintain backup of original
- Extensive device testing

### Risk 2: Data Loss from Conflicts
**Mitigation:**
- Version history maintained
- Timestamps preserved
- User always sees options (not auto-destructive)
- Conflict resolution with AI suggestions

### Risk 3: Cloud API Dependency
**Mitigation:**
- Work toward local sync as fallback
- Cache locally during connectivity issues
- Graceful degradation
- Alternative sync methods in future

### Risk 4: Performance Issues with Large Vaults
**Mitigation:**
- Implement selective sync
- Batch processing optimization
- Background task scheduling
- Monitor resource usage

---

## Implementation Timeline (Estimates)

| Phase | Feature | Effort | Timeline |
|-------|---------|--------|----------|
| 2 | Frontmatter properties | 2 weeks | ✅ Complete |
| 2 | .note update mode | 3-4 weeks | ✅ Complete |
| 2 | Realtime support | 1-2 weeks | ✅ Complete |
| 2 | Testing & docs | 1 week | ✅ Complete |
| 3A | Python Backend API | 2-3 weeks | In Progress |
| 3B | Web Dashboard MVP | 2-3 weeks | Planned |
| 3C | Obsidian Plugin | 2-3 weeks | Planned |
| 3D | Visual Workflow Builder | 3-4 weeks | Planned |
| 4+ | Cloud integration | 3-4 weeks | Future |
| 4+ | Advanced workflows | 3-4 weeks | Future |

**Total Phase 2:** ✅ Complete
**Total Phase 3:** 10-14 weeks
**Total Phase 4+:** 6+ weeks

---

## Getting Started

### To Implement Phase 2:

1. **Set up development environment**
   ```bash
   cd obsidian-supernote-sync
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Add dev dependencies
   ```

2. **Review specification documents**
   - PRD: `C:\Edwin\Notes Vault\03 Projects\Obsidian-Supernote Sync\Obsidian-Supernote Sync Tool.md`
   - Technical specs in this plan

3. **Start with Step 1: Frontmatter parsing**
   - Create unit tests first
   - Implement frontmatter extraction
   - Test with example markdown files

4. **Iterate through steps sequentially**
   - Complete one step before moving to next
   - Test thoroughly at each stage
   - Commit changes with descriptive messages

5. **Test on device frequently**
   - Don't wait until the end
   - Device behavior is critical
   - Early feedback prevents rework

---

## Next Steps (Immediate)

1. **Review this plan** with team/stakeholders
2. **Assign Phase 2 work** to developer(s)
3. **Set up development environment**
4. **Begin Step 1:** Frontmatter property parsing
5. **Create unit tests** before implementation
6. **Weekly check-ins** to track progress

---

## Contact & Questions

For questions about this plan:
- See PRD for detailed workflows: `C:\Edwin\Notes Vault\03 Projects\Obsidian-Supernote Sync\Obsidian-Supernote Sync Tool.md`
- See ROADMAP.md for project status
- See IMPLEMENTATION_STATUS.md for current feature status

---

**Plan Created:** 2026-01-20
**Last Updated:** 2026-01-20
**Status:** Ready for Phase 2 Development
