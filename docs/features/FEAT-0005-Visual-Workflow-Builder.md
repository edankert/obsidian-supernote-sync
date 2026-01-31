---
type: "[[feature]]"
id: FEAT-0005
title: "Phase 3D: Visual Workflow Builder"
status: planned
phase: 3
owner: unassigned
created: 2026-01-31
updated: 2026-01-31
source:
  - "PLAN.md"
goal: "Implement drag-and-drop workflow designer with React Flow"
requirements:
  - "[[REQ-0006-Visual-Workflow-Builder]]"
tasks: []
release: ""
related:
  - "[[FEAT-0003-Web-Dashboard-MVP]]"
tests: []
---

# Phase 3D: Visual Workflow Builder

## Goal
Implement drag-and-drop workflow designer with React Flow for creating custom sync workflows.

## Scope

**In Scope:**
- React Flow integration for drag-and-drop
- Building blocks library:
  - Source blocks: Folder watch, single file, tag filter
  - Transform blocks: MD→Note, Note→MD, PDF→Note
  - Output blocks: Save to folder, update frontmatter
- Connection validation
- YAML export/import
- Template library

**Out of Scope:**
- Scheduled execution (Phase 4)
- Cloud triggers (Phase 4)

## Acceptance
- Users can drag-and-drop blocks to create workflows
- Connections validate input/output compatibility
- Workflows can be saved and loaded as YAML
- Template library provides starting points

## Tasks (Planned)
- [ ] 3D.1: Implement drag-and-drop designer with React Flow
- [ ] 3D.2: Create building blocks (source, transform, output)
- [ ] 3D.3: Add workflow save/load functionality

## Links
- Requirements: [[REQ-0006-Visual-Workflow-Builder]]
- Web dashboard: [[FEAT-0003-Web-Dashboard-MVP]]
