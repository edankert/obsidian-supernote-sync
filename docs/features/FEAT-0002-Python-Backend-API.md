---
type: "[[feature]]"
id: FEAT-0002
title: "Phase 3A: Python Backend API (FastAPI)"
status: done
phase: 3
owner: Edwin
created: 2026-01-24
updated: 2026-01-24
source:
  - "PLAN.md"
  - "docs/IMPLEMENTATION_STATUS.md"
goal: "Create FastAPI server wrapping existing converters with REST API and WebSocket support"
requirements:
  - "[[REQ-0003-REST-API]]"
tasks:
  - "[[TASK-0005-FastAPI-Server]]"
  - "[[TASK-0006-Conversion-Endpoints]]"
  - "[[TASK-0007-WebSocket-Support]]"
  - "[[TASK-0008-Workflow-Endpoints]]"
release: "v0.3.0-alpha"
related:
  - "[[FEAT-0001-Manual-CLI-Frontmatter]]"
  - "[[FEAT-0003-Web-Dashboard-MVP]]"
tests: []
---

# Phase 3A: Python Backend API (FastAPI)

## Goal
Create FastAPI server wrapping existing converters with REST API and WebSocket support for real-time progress updates.

## Scope

**In Scope:**
- FastAPI server with CORS and static file serving
- REST API endpoints for all conversions
- WebSocket for real-time progress updates
- Workflow management endpoints
- YAML-based workflow loading

**Out of Scope:**
- Web dashboard UI (Phase 3B)
- Obsidian plugin (Phase 3C)
- Authentication/authorization

## Acceptance
- All conversion functions accessible via HTTP endpoints
- Real-time progress updates via WebSocket
- Workflow management endpoints functional
- Server starts via `obsidian-supernote serve` command

## Evidence

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Health check and version info |
| `/status/dependencies` | GET | Check Pandoc, supernotelib, Pillow |
| `/convert/md-to-note` | POST | Convert markdown to .note |
| `/convert/note-to-md` | POST | Export .note to markdown |
| `/convert/pdf-to-note` | POST | Convert PDF to .note |
| `/convert/png-to-note` | POST | Convert PNG to .note |
| `/convert/batch` | POST | Batch conversion |
| `/workflows` | GET/POST | Workflow management |
| `/workflows/{id}/run` | POST | Execute workflow |
| `/events` | WS | Real-time progress updates |

### WebSocket Events
- `conversion_started`, `conversion_progress`, `conversion_complete`, `conversion_error`
- `batch_started`, `batch_progress`, `batch_complete`
- `workflow_started`, `workflow_step`, `workflow_complete`, `workflow_error`

## Links
- Requirements: [[REQ-0003-REST-API]]
- Implementation: `obsidian_supernote/api/`
- CLI command: `obsidian-supernote serve --port 8765`
