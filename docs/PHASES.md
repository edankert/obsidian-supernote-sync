---
type: registry
id: PHASES
title: "Phase Registry"
updated: 2026-01-31
---

# Phase Registry

This document is the **semantic source of truth** for the project's development phases. It maps phase numbers to specific technical and business milestones, enabling machine-filtering, automated progress tracking, and dashboard grouping.

## How Phases Work

- **Property**: `phase` (Integer 1–N, optional)
- **Location**: YAML frontmatter of features, tasks, requirements, and issues
- **Purpose**: Groups related work into cohesive delivery milestones

## Phase Definitions

| Phase | Name | Description | Key Deliverables | Status |
|-------|------|-------------|------------------|--------|
| 1 | Foundation | Core converters and parser | Note parser, MD→PDF, PDF→Note, PNG→Note | Done |
| 2 | Manual CLI | Frontmatter support and update mode | Frontmatter parsing, annotation preservation, realtime support | Done |
| 3A | Backend API | FastAPI server with REST endpoints | REST API, WebSocket events, workflow management | Done |
| 3B | Web Dashboard | React + Tailwind dashboard MVP | Workflow UI, conversion panel, status display | Done |
| 3C | Obsidian Plugin | Native Obsidian integration | Ribbon, commands, settings, status bar | In Progress |
| 3D | Workflow Builder | Visual drag-and-drop workflow designer | React Flow, block library, custom workflows | Planned |
| 4 | Cloud Integration | Supernote Cloud API and sync | Cloud API client, file watching, conflict resolution | Planned |
| 5 | Production | Launch readiness | Documentation, packaging, store assets | Planned |

## Phase Details

### Phase 1: Foundation (Done)
Core conversion infrastructure and file parsing.
- **Feature**: Core converters (pre-existing)
- **Deliverables**: Note parser, all conversion pipelines
- **Release**: v0.1.0-alpha

### Phase 2: Manual CLI (Done)
User control via frontmatter with CLI commands.
- **Feature**: [[FEAT-0001-Manual-CLI-Frontmatter]]
- **Deliverables**: Frontmatter parsing, update mode, realtime support
- **Release**: v0.2.0-alpha

### Phase 3A: Backend API (Done)
FastAPI server wrapping converters.
- **Feature**: [[FEAT-0002-Python-Backend-API]]
- **Deliverables**: REST API, WebSocket, workflow endpoints
- **Release**: v0.3.0-alpha

### Phase 3B: Web Dashboard (Done)
React dashboard for workflow management.
- **Feature**: [[FEAT-0003-Web-Dashboard-MVP]]
- **Deliverables**: Workflow cards, convert panel, status bar
- **Release**: v0.3.0-alpha

### Phase 3C: Obsidian Plugin (In Progress)
Native Obsidian plugin integration.
- **Feature**: [[FEAT-0004-Obsidian-Plugin]]
- **Deliverables**: Ribbon button, commands, settings tab, status bar
- **Release**: v0.4.0-alpha

### Phase 3D: Visual Workflow Builder (Planned)
Drag-and-drop workflow designer.
- **Feature**: [[FEAT-0005-Visual-Workflow-Builder]]
- **Deliverables**: React Flow canvas, block library, save/load
- **Release**: v0.5.0-alpha

### Phase 4: Cloud Integration (Planned)
Supernote Cloud API and automatic sync.
- **Feature**: [[FEAT-0006-Cloud-Integration]]
- **Deliverables**: Cloud API client, file watching, conflict resolution
- **Release**: v1.0.0

### Phase 5: Production (Planned)
Launch preparation and polish.
- **Deliverables**: Documentation, packaging, community plugin submission
- **Release**: v1.0.0

## Usage

### In Frontmatter

```yaml
---
type: "[[task]]"
id: TASK-0042
phase: 3C
status: doing
parent: "[[FEAT-0004]]"
---
```

### Filtering by Phase

Use the `phase` property in Obsidian bases or queries to:
- Group items by delivery milestone
- Track progress within a phase
- Identify scope creep (items without phases)

### Phase Inheritance

- **Features** define the phase for a body of work
- **Tasks** inherit phase from their parent feature (or override explicitly)
- **Requirements** and **Issues** can specify phase when relevant to milestone planning

## Operational Rules for LLMs

When executing work, the LLM must:

1. **Verify phase alignment**: Check the `phase` property in the task/feature frontmatter before starting work.
2. **Consult this registry**: Understand the broader context and boundaries of the current phase.
3. **Prevent phase bleeding**: Do not introduce implementations from future phases prematurely.
   - Example: Don't build Phase 4 cloud sync while working on a Phase 3C plugin task.
4. **Flag scope concerns**: If a task requires future-phase dependencies, document it and discuss before proceeding.

## Phase Progression

Phases are generally sequential but may overlap:
- **Active phase**: Phase 3C (Obsidian Plugin)
- **Maintenance phases**: Phases 1-3B may receive bug fixes
- **Blocked phases**: Phase 4+ awaiting dependencies

---

*This file is part of the Project OS documentation system. See [docs/INDEX.md](INDEX.md) for overview.*
