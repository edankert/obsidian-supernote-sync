---
type: "[[adr]]"
id: ADR-0002
title: "Use hybrid Obsidian Plugin + Python Backend + Web Dashboard"
status: accepted
owner: Edwin
created: 2026-01-24
updated: 2026-01-31
decision: "Implement hybrid architecture with Obsidian Plugin + FastAPI Backend + React Dashboard"
context: "Need both native Obsidian integration and complex UI capabilities"
alternatives:
  - "Pure Obsidian plugin (would require porting Python to TypeScript)"
  - "Electron app (separate from Obsidian)"
  - "CLI only"
consequences:
  - "100% reuse of existing Python converters"
  - "Native Obsidian integration for quick actions"
  - "Web dashboard for complex configuration"
  - "Requires running backend server"
supersedes: ""
superseded: ""
source:
  - "PLAN.md"
related:
  - "[[FEAT-0002-Python-Backend-API]]"
  - "[[FEAT-0003-Web-Dashboard-MVP]]"
  - "[[FEAT-0004-Obsidian-Plugin]]"
---

# ADR-0002: Hybrid UI Architecture

## Status
ACCEPTED

## Context
We need to provide a user-friendly interface for managing conversions and workflows. The existing converter code is in Python. Options include:

1. Pure Obsidian plugin (TypeScript)
2. Electron desktop app
3. Python GUI (Tkinter, PyQt)
4. Hybrid: Obsidian Plugin + Python Backend + Web Dashboard

## Decision
Implement hybrid architecture:
- **Obsidian Plugin** (TypeScript): Quick actions, commands, settings
- **Python Backend** (FastAPI): REST API wrapping converters, WebSocket
- **Web Dashboard** (React): Complex configuration, visual workflow builder

```
┌─────────────────────┐
│  Obsidian Plugin    │ ←─ Quick actions
│  (TypeScript)       │
└─────────┬───────────┘
          │ HTTP API
          ▼
┌─────────────────────┐
│  Python Backend     │ ←─ Converter logic
│  (FastAPI)          │
└─────────┬───────────┘
          │ Serves
          ▼
┌─────────────────────┐
│  Web Dashboard      │ ←─ Complex UI
│  (React)            │
└─────────────────────┘
```

## Rationale

### Pros
- **100% code reuse**: No need to port Python to TypeScript
- **Native integration**: Plugin feels native in Obsidian
- **Rich UI**: Web dashboard for complex features
- **Separation of concerns**: Each layer does one thing well

### Cons
- Requires running backend server
- More moving parts
- User must start server before using

## Alternatives Considered

### 1. Pure Obsidian Plugin
- Port all Python to TypeScript
- Rejected: Months of work, lose supernotelib

### 2. Electron App
- Separate desktop application
- Rejected: Not integrated with Obsidian

### 3. Python GUI
- Tkinter or PyQt interface
- Rejected: Separate from Obsidian workflow

## Consequences

### Positive
- Fast development (reuse existing code)
- Best of both worlds (native + rich UI)
- Future extensibility

### Negative
- Server dependency
- Complexity in deployment
- User education needed

## Implementation
- Phase 3A: Python Backend (FastAPI) ✅
- Phase 3B: Web Dashboard (React) ✅
- Phase 3C: Obsidian Plugin (in progress)
