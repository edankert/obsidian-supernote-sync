---
type: "[[task]]"
id: TASK-0004
title: "Create Configuration Examples and Workflow Guides"
status: done
phase: 2
owner: Edwin
created: 2026-01-20
updated: 2026-01-24
source:
  - "PLAN.md"
parent: "[[FEAT-0001-Manual-CLI-Frontmatter]]"
effort: M
depends:
  - "[[TASK-0003-Realtime-Support]]"
blocks: []
related:
  - "[[WF-0001-Daily-Notes]]"
  - "[[WF-0002-Research-Notes]]"
  - "[[WF-0003-World-Building]]"
tests: []
---

# Create Configuration Examples and Workflow Guides

## Definition of Done
- [x] Daily Notes workflow example with template
- [x] Research Notes workflow for annotation
- [x] World Building workflow for sketching
- [x] Configuration YAML files for each workflow
- [x] README documentation for each example

## Steps
- [x] Create `examples/workflows/` directory structure
- [x] Write daily-notes workflow with frontmatter example
- [x] Write research-notes workflow for PDF annotation
- [x] Write world-building workflow for creative sketching
- [x] Create YAML config files in `examples/configs/`

## Notes
- Examples serve as starting templates for users
- Each workflow demonstrates different use case
- Configs loadable by backend API

## Evidence
- Daily Notes: `examples/workflows/daily-notes/`
- Research Notes: `examples/workflows/research-notes/`
- World Building: `examples/workflows/world-building/`
- Configs: `examples/configs/*.yaml`
