---
type: "[[risk]]"
id: RISK-0003
title: "Cloud API dependency for sync"
status: open
owner: Edwin
created: 2026-01-20
updated: 2026-01-31
likelihood: medium
impact: medium
source:
  - "PLAN.md"
mitigation:
  - "Local sync as fallback"
  - "Cache locally during connectivity issues"
  - "Graceful degradation"
mitigation_tasks: []
related:
  - "[[FEAT-0006-Cloud-Integration]]"
---

# RISK-0003: Cloud API Dependency

## Description
Phase 4 cloud sync depends on Supernote Cloud API availability and compatibility. API changes or downtime could break sync functionality.

## Likelihood: MEDIUM
- Third-party API, not under our control
- API may change without notice
- Regional availability varies

## Impact: MEDIUM
- Users can fall back to USB sync
- Existing local features still work
- Inconvenience rather than data loss

## Mitigation Strategies

### 1. Local Sync Fallback
- USB sync always available
- Local file watching for automation
- No cloud dependency for core features

### 2. Caching
- Cache data locally during sync
- Retry logic for transient failures
- Queue operations during downtime

### 3. Graceful Degradation
- Detect API unavailability
- Switch to local-only mode automatically
- Notify user of reduced functionality

### 4. API Abstraction
- Abstract cloud operations behind interface
- Support multiple sync backends if needed
- Easy to adapt to API changes

## Current Status
- **Phase 2-3**: No cloud dependency, local only
- **Phase 4**: Will implement with mitigations

## Contingency
- Document manual USB sync workflow
- Community-driven API compatibility updates
