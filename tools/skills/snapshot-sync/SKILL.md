---
type: skill
id: SKILL-SNAPSHOT-SYNC
status: active
owner: group:maintainers
created: 2026-01-27
updated: 2026-01-27
tags: [skills, snapshot]
---

# Skill: Snapshot sync

## When to use
- After any work that changes statuses/relationships.
- When you suspect drift between `../../../SNAPSHOT.yaml` and the notes.

## Inputs
- `../../../SNAPSHOT.yaml`
- The affected notes under `../../../docs/`

## Outputs
- A consistent snapshot and notes (IDs, statuses, relationships aligned).

## Checklist
1. Validate `../../../SNAPSHOT.yaml` invariants (see `../../instructions/SNAPSHOT.md`).
2. For each modified item:
   - ensure `items.<type>.<ID>.file` exists
   - ensure note frontmatter `id` matches `<ID>`
   - ensure note frontmatter `status` matches snapshot `status`
3. Check relationship consistency:
   - task `parent` ↔ feature/issue lists
   - issue ↔ feature links
4. If `claimed_by` exists, ensure it is intentional and not stale (update or clear).
5. Update `metrics` counts in the snapshot.
