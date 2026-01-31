---
type: "[[test]]"
id: TST-0004
title: "Markdown to PDF converter tests"
status: blocked
owner: Edwin
created: 2026-01-19
updated: 2026-01-31
source:
  - "tests/test_markdown_to_pdf.py"
scope: feature
kind: automated
level: integration
entrypoint: "pytest tests/test_markdown_to_pdf.py -v"
requirements: []
features: []
issues: []
tasks: []
artifacts: []
evidence:
  - "Skipped - requires GTK+ libraries for WeasyPrint"
last_run: "2026-01-31"
---

# Markdown to PDF Converter Tests

## Purpose
Verify that markdown files are correctly converted to PDF format using WeasyPrint.

## Status: BLOCKED

These tests require GTK+ libraries to be installed on Windows. See `docs/WEASYPRINT_SETUP.md` for setup instructions.

**Alternative:** Use Pandoc-based conversion instead (recommended).

## Test Coverage

- Page size conversion tests
- DPI settings tests
- CSS styling tests
- Obsidian markdown features (wikilinks, frontmatter stripping)

## How to Run
```bash
# Requires GTK+ libraries
cd C:\Edwin\repos\obsidian-supernote-sync
venv\Scripts\activate
pytest tests/test_markdown_to_pdf.py -v
```

## Workaround
Use Pandoc converter instead:
```bash
obsidian-supernote md-to-note input.md output.note
```

## Evidence
Last run: 2026-01-31
- 7 tests skipped (GTK+ not available)
