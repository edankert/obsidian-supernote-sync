---
type: "[[workflow]]"
id: WF-0005
title: "API Server Workflow"
status: active
owner: Edwin
created: 2026-01-31
updated: 2026-01-31
source:
  - "docs/IMPLEMENTATION_STATUS.md"
entrypoints:
  - "obsidian-supernote serve"
  - "obsidian-supernote serve --port 8080"
  - "obsidian-supernote serve --reload"
  - "obsidian-supernote serve --dashboard web-dashboard/dist"
prereqs:
  - "Python venv activated"
  - "Dependencies installed"
  - "Web dashboard built (optional)"
inputs:
  - "Configuration (port, dashboard path)"
outputs:
  - "REST API at http://localhost:8765/"
  - "WebSocket at ws://localhost:8765/events"
  - "API docs at http://localhost:8765/docs"
related:
  - "[[FEAT-0002-Python-Backend-API]]"
  - "[[FEAT-0003-Web-Dashboard-MVP]]"
---

# API Server Workflow

## Purpose
Start the FastAPI backend server for REST API access and web dashboard hosting.

## Prerequisites
1. Python venv activated
2. Dependencies installed (`pip install -r requirements.txt`)
3. (Optional) Web dashboard built

## Start Server

### Basic
```bash
obsidian-supernote serve
```

### Custom Port
```bash
obsidian-supernote serve --port 8080
```

### Development Mode (Auto-reload)
```bash
obsidian-supernote serve --reload
```

### With Web Dashboard
```bash
# Build dashboard first
cd web-dashboard && npm install && npm run build && cd ..

# Start with dashboard
obsidian-supernote serve --dashboard web-dashboard/dist
```

## Endpoints

| URL | Description |
|-----|-------------|
| `http://localhost:8765/` | API root |
| `http://localhost:8765/docs` | Swagger UI |
| `http://localhost:8765/status` | Health check |
| `ws://localhost:8765/events` | WebSocket events |

## Test Endpoints
```bash
# Health check
curl http://localhost:8765/status

# List workflows
curl http://localhost:8765/workflows

# Check dependencies
curl http://localhost:8765/status/dependencies
```

## WebSocket Connection
Connect to `ws://localhost:8765/events` to receive real-time progress updates:
- `conversion_started`
- `conversion_progress`
- `conversion_complete`
- `conversion_error`
