---
type: skill
id: SKILL-CLOSE-OUT
status: active
owner: group:maintainers
created: 2026-01-27
updated: 2026-01-27
tags: [skills, closeout]
---

# Skill: Close-out

## When to use
- At the end of an implementation task or when an issue is resolved.

## Inputs
- Completed task/issue/feature IDs.

## Outputs
- Updated statuses, optional change note, and cleaned focus.

## Checklist
1. Update notes:
   - task `status: done` (and `updated`)
   - issue `status: fixed/closed` if resolved
   - feature progress if milestones were reached
2. Update `../../../SNAPSHOT.yaml`:
   - set the same statuses
   - update relationships if new tasks/issues/risks were created
   - clear or move `focus` to the next task
   - update `metrics`
3. If user-facing behavior/paths/contracts changed:
   - create `../../../docs/changes/CHG-YYYYMMDD-Short-Description.md`
   - link it to `issues`/`features` in note + snapshot
4. Run a risk scan if the change introduces new hazards.
5. Apply verification gating:
   - ensure required `TST-*` are `status: passing` before setting task `done`, issue `closed`, or requirement `verified`.
