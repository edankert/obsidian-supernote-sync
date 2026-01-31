---
type: "[[risk]]"
id: RISK-0002
title: "Data loss from sync conflicts"
status: open
owner: Edwin
created: 2026-01-20
updated: 2026-01-31
likelihood: medium
impact: high
source:
  - "PLAN.md"
mitigation:
  - "Version history maintained"
  - "User always sees options"
  - "Conflict resolution with AI suggestions"
mitigation_tasks: []
related:
  - "[[FEAT-0006-Cloud-Integration]]"
---

# RISK-0002: Data Loss from Sync Conflicts

## Description
When both markdown and .note files are edited simultaneously (e.g., user edits markdown while also annotating on device), a sync operation could overwrite changes from one side.

## Likelihood: MEDIUM
Common scenario when user forgets they have uncommitted changes on either side.

## Impact: HIGH
Lost edits (either markdown content or handwriting) are difficult or impossible to recover.

## Mitigation Strategies

### 1. Version History
- Keep previous versions of .note files
- Track modification timestamps
- Enable rollback to previous state

### 2. User-Guided Resolution
- Never auto-destructive actions
- Show user what will be overwritten
- Offer merge options where possible

### 3. Conflict Detection
- Check timestamps before sync
- Warn if both sides modified since last sync
- Option to create conflict copies

### 4. AI-Assisted Merge (Future)
- Intelligent merging of text changes
- Preserve handwriting while updating template
- Suggest resolution strategies

## Current Status
- **Phase 2**: Manual workflow, user controls timing
- **Phase 4**: Will implement conflict detection and resolution

## Contingency
- Supernote Cloud backup for handwriting recovery
- Git history for markdown recovery
