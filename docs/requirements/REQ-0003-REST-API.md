---
type: "[[requirement]]"
id: REQ-0003
title: "REST API wrapping existing converters"
status: verified
owner: Edwin
created: 2026-01-24
updated: 2026-01-31
priority: high
scope: api
phase: 3
source:
  - "PLAN.md"
acceptance:
  - "All conversion functions accessible via HTTP endpoints"
  - "Real-time progress updates via WebSocket"
  - "Workflow management endpoints functional"
implements:
  - "[[FEAT-0002-Python-Backend-API]]"
verifies:
  - "curl http://localhost:8765/status"
tests: []
---

# REQ-0003: REST API for Converters

## Description
Provide a FastAPI-based REST API that wraps all existing converter functions for programmatic access.

## Acceptance Criteria

1. **HTTP endpoints** - All converters accessible via POST endpoints
2. **WebSocket progress** - Real-time progress updates during conversions
3. **Workflow management** - CRUD operations for workflows

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Health check, version, uptime |
| `/status/dependencies` | GET | Check Pandoc, supernotelib |
| `/convert/md-to-note` | POST | Markdown to .note |
| `/convert/note-to-md` | POST | .note to Markdown |
| `/convert/pdf-to-note` | POST | PDF to .note |
| `/convert/png-to-note` | POST | PNG to .note |
| `/convert/batch` | POST | Batch conversion |
| `/workflows` | GET | List workflows |
| `/workflows` | POST | Create workflow |
| `/workflows/{id}/run` | POST | Execute workflow |
| `/events` | WS | WebSocket events |

## Verification

```bash
# Start server
obsidian-supernote serve --port 8765

# Test health
curl http://localhost:8765/status

# Test conversion
curl -X POST http://localhost:8765/convert/md-to-note \
  -H "Content-Type: application/json" \
  -d '{"input_path": "test.md", "output_path": "test.note"}'
```

## Evidence
- Implementation: `obsidian_supernote/api/`
- Change: [[CHG-20260130-Phase3A-Backend-API]]
