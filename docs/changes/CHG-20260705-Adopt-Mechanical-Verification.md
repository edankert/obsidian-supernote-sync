---
type: "[[change]]"
id: CHG-20260705-Adopt-Mechanical-Verification
aliases: ["CHG-20260705-Adopt-Mechanical-Verification"]
title: "Adopt mechanical verification from project-os template"
status: merged
owner: Edwin
created: 2026-07-05
updated: 2026-07-05
commit: ""
pr: ""
impacts:
  - "tools/scripts/"
  - "tools/adapters/claude-code/"
  - "tools/skills/"
  - "tools/instructions/"
  - "docs/__templates__/"
  - ".github/workflows/"
  - ".claude/settings.json"
issues: []
features: []
reviewed_by: ""
review_date: ""
review_verdict: ""
source:
  - "project-os template sync (baseline 77b4d5e -> HEAD)"
---

# CHG-20260705: Adopt Mechanical Verification

## Summary
Synced the "mechanical verification" change set from the canonical project-os template. Core documentation invariants move from convention to mechanism: a deterministic validator (`tools/scripts/validate-docs.py` + `validate-docs.sh`) checks snapshot-filesystem agreement, frontmatter/status consistency, counter integrity, link-graph integrity, and the verification invariant (no terminal status without passing linked tests). The Claude Code verification gate becomes a blocking PreToolUse hook (`verification-gate.py` behind `verification-gate.sh`) that denies edits setting `done`/`closed`/`verified` while linked `TST-*` notes are not `passing`. The validator is enforced at git pre-commit (installed via `tools/scripts/install-git-hooks.sh`) and in CI (`.github/workflows/validate-docs.yml`). Two new skills were added: `independent-review` (different-model review of new/updated `TST-*`/`CHG-*` notes, recorded via `reviewed_by` frontmatter) and `docs-audit` (periodic full-scope consistency audit run to quiescence). Instructions (HOOKS, QUALITY, TESTING, SYNCING, LIFECYCLE), affected skills (issue-intake, snapshot-sync, backlog-grooming, close-out, release-prep), templates (test, change, SCHEMAS), the claude-code adapter (hooks.json, ADAPTER.md, close-out-check.sh), and `sync-project-os.sh` were updated to the current template versions; all matched the pre-change template baseline, so no hand-merges were needed. `.claude/settings.json` hooks were regenerated from the new `hooks.json` and the git pre-commit hook was installed.

## Impact
- Documentation drift now fails at edit time (blocking hook), commit time (pre-commit), and in CI, instead of relying on agent discipline.
- `CLAUDE.md` skill list gains Independent review and Docs audit entries.
- Test and change templates gain `reviewed_by`/`review_date`/`review_verdict` fields; test template gains adequacy/`mutation_score` fields (see SCHEMAS.md).

## Drift Fixed During Sync
- `SNAPSHOT.yaml` items.tasks.TASK-0012 `file` key pointed at `docs/features/FEAT-0004-Obsidian-Plugin.md`; corrected to `docs/tasks/TASK-0012-Ribbon-Commands.md`.
- `docs/tasks/TASK-0012-Ribbon-Commands.md` frontmatter status was `in-progress`, which is not a valid task status; aligned to the snapshot's `doing`.
- Validator result: 3 errors before fixes, 0 after (`validate-docs: OK`).

## Documentation Coverage (All Types Considered)
- features: not-applicable
- requirements: not-applicable
- tasks: updated (TASK-0012 status drift fix)
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new (this note)
- snapshot: updated

## Follow-ups
- [ ] Run `tools/skills/docs-audit/SKILL.md` once to establish a clean audit baseline.
- [ ] Use `tools/skills/independent-review/SKILL.md` on future TST-*/CHG-* notes.
