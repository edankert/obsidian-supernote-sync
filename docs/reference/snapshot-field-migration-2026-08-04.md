---
type: "[[reference]]"
id: REFERENCE-SNAPSHOT-FIELD-MIGRATION
title: "Snapshot field migration record: values replaced when title/goal became derived"
status: active
owner: user:edwin
created: 2026-08-04
updated: 2026-08-04
scope: "project"
source: ["FEAT-0022", "TASK-0084", "ADR-0018"]
related: []
---

# Snapshot field migration record

Every `title:`/`goal:` value **obsidian-supernote-sync**'s `SNAPSHOT.yaml` carried before ADR-0018 made those
fields derived, where it differed from the note that now supplies it. Includes entries
later removed by retention, so this is the complete replaced set, not just the survivors.

Reconstructed from `7b9aa24c~1` after the first pass wrote an incomplete record: the rollout
re-ran the recorder *after* migrating, when there was no drift left to capture.

1 value(s) replaced.

## TASK-0012 (`title`)

- **was:** Implement ribbon button and commands
- **now:** Implement Ribbon Button and Commands

