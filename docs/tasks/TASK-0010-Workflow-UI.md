---
type: "[[task]]"
id: TASK-0010
title: "Build Workflow and Conversion UI Components"
status: done
phase: 3B
owner: Edwin
created: 2026-01-24
updated: 2026-01-31
source:
  - "PLAN.md"
parent: "[[FEAT-0003-Web-Dashboard-MVP]]"
effort: L
depends:
  - "[[TASK-0009-React-Setup]]"
blocks: []
related: []
tests: []
---

# Build Workflow and Conversion UI Components

## Definition of Done
- [x] StatusBar component showing connection status
- [x] WorkflowCard component for workflow management
- [x] ConvertPanel for quick file conversion
- [x] ProgressIndicator for real-time progress display
- [x] File browser integration with native dialogs
- [x] Error boundary for graceful error handling

## Steps
- [x] Create StatusBar with WebSocket connection indicator
- [x] Create WorkflowCard with run button and status
- [x] Create ConvertPanel with conversion type selector
- [x] Add device selection dropdown
- [x] Integrate file browser buttons for path selection
- [x] Add ProgressIndicator component

## Notes
- Components use Tailwind for styling
- Real-time updates via WebSocket hook
- Native file dialogs via backend `/file-dialog` endpoint

## Evidence
- StatusBar: `web-dashboard/src/components/StatusBar.tsx`
- WorkflowCard: `web-dashboard/src/components/WorkflowCard.tsx`
- ConvertPanel: `web-dashboard/src/components/ConvertPanel.tsx`
- ProgressIndicator: `web-dashboard/src/components/ProgressIndicator.tsx`
