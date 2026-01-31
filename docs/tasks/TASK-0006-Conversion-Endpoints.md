---
type: "[[task]]"
id: TASK-0006
title: "Implement Conversion REST Endpoints"
status: done
phase: 3A
owner: Edwin
created: 2026-01-24
updated: 2026-01-24
source:
  - "PLAN.md"
parent: "[[FEAT-0002-Python-Backend-API]]"
effort: L
depends:
  - "[[TASK-0005-FastAPI-Server]]"
blocks: []
related: []
tests: []
---

# Implement Conversion REST Endpoints

## Definition of Done
- [x] POST `/convert/md-to-note` - Markdown to .note conversion
- [x] POST `/convert/note-to-md` - .note to Markdown export
- [x] POST `/convert/pdf-to-note` - PDF to .note conversion
- [x] POST `/convert/png-to-note` - PNG to .note conversion
- [x] POST `/convert/batch` - Batch conversion endpoint
- [x] Proper error handling and validation

## Steps
- [x] Create `routes/convert.py` module
- [x] Wrap existing converters with HTTP endpoints
- [x] Add request/response models with Pydantic
- [x] Implement batch conversion logic
- [x] Add input validation and error responses

## Notes
- All endpoints accept JSON with file paths
- Batch endpoint processes multiple files
- Returns conversion result with output path

## Evidence
- Implementation: `obsidian_supernote/api/routes/convert.py`
- Endpoints: `/convert/md-to-note`, `/convert/note-to-md`, etc.
