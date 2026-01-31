---
type: "[[task]]"
id: TASK-0012
title: "Implement Ribbon Button and Commands"
status: in-progress
phase: 3C
owner: Edwin
created: 2026-01-25
updated: 2026-01-31
source:
  - "PLAN.md"
parent: "[[FEAT-0004-Obsidian-Plugin]]"
effort: M
depends:
  - "[[TASK-0011-Plugin-Skeleton]]"
blocks: []
related: []
tests: []
---

# Implement Ribbon Button and Commands

## Definition of Done
- [x] Custom Supernote ribbon icon (SVG)
- [x] Basic commands registered
- [ ] "Convert to Supernote" command with active file
- [ ] "Open Dashboard" command to launch web UI
- [ ] "Check Connection" command to test backend
- [ ] "Sync All" command for batch conversion
- [ ] File context menu integration
- [ ] Status bar showing connection status

## Steps
- [x] Create custom SVG icon for ribbon
- [x] Register ribbon button with click handler
- [x] Add commands to command palette
- [ ] Implement convert command with file detection
- [ ] Implement dashboard launch (open in browser)
- [ ] Implement connection check with notification
- [ ] Add file menu item "Convert to Supernote"
- [ ] Create status bar item showing API status

## Notes
- Ribbon icon should be distinctive Supernote-style
- Commands available via Ctrl+P command palette
- File context menu appears on right-click in file explorer
- Status bar shows green/red connection indicator

## Remaining Work
- Full command implementations
- Status bar integration
- File context menu
- Error handling and user notifications
