---
type: "[[adr]]"
id: ADR-0001
title: "Use YAML frontmatter for configuration"
status: accepted
owner: Edwin
created: 2026-01-20
updated: 2026-01-31
decision: "Use YAML frontmatter in markdown files for Supernote configuration"
context: "Need a way to configure .note conversion without separate config files"
alternatives:
  - "Separate config files per note"
  - "Global config only"
  - "CLI flags only"
consequences:
  - "No separate config files needed"
  - "Metadata travels with content"
  - "Obsidian-native approach"
  - "Requires parsing frontmatter"
supersedes: ""
superseded: ""
source:
  - "PLAN.md"
related:
  - "[[FEAT-0001-Manual-CLI-Frontmatter]]"
  - "[[REQ-0001-Frontmatter-Parsing]]"
---

# ADR-0001: YAML Frontmatter for Configuration

## Status
ACCEPTED

## Context
We need a way for users to configure how their markdown files are converted to .note format. Options include:
1. Separate config files per note
2. Global configuration only
3. CLI flags only
4. YAML frontmatter in markdown

## Decision
Use YAML frontmatter properties in markdown files for per-file configuration.

### Properties
```yaml
---
supernote.type: realtime  # or "standard"
supernote.file: "[output/file.note]"  # auto-managed
---
```

## Rationale

### Pros
- **No separate files**: Configuration lives with content
- **Obsidian-native**: Frontmatter is standard in Obsidian
- **Portable**: Metadata travels when files move
- **Simple**: Just two properties needed
- **Optional**: Graceful defaults when properties missing

### Cons
- Requires parsing frontmatter
- Users must learn property syntax
- Properties could be accidentally edited

## Alternatives Considered

### 1. Separate Config Files
- `.supernote.yaml` per note
- Rejected: Creates clutter, easy to lose sync

### 2. Global Config Only
- Single config file for all notes
- Rejected: No per-file customization

### 3. CLI Flags Only
- All options via command line
- Rejected: Must remember flags each time

## Consequences

### Positive
- Clean user experience
- Self-documenting notes
- Easy automation

### Negative
- Parsing overhead (minimal)
- Learning curve for properties

## Implementation
- `obsidian_supernote/utils/frontmatter.py`
- 34 tests, 92% coverage
