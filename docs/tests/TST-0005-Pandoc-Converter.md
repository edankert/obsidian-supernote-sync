---
type: "[[test]]"
id: TST-0005
title: "Pandoc converter test suite"
status: passing
owner: Edwin
created: 2026-01-20
updated: 2026-01-31
source:
  - "tests/test_pandoc_converter.py"
scope: feature
kind: automated
level: integration
entrypoint: "pytest tests/test_pandoc_converter.py -v"
requirements: []
features: []
issues: []
tasks: []
artifacts: []
evidence:
  - "Tests passing"
last_run: "2026-01-31"
---

# Pandoc Converter Test Suite

## Purpose
Verify that markdown files are correctly converted to PDF using Pandoc, which is the recommended conversion method.

## Prerequisites
- Pandoc installed (`choco install pandoc` on Windows)
- LaTeX distribution (MiKTeX or TeX Live) for PDF generation

## Test Coverage

- Basic markdown to PDF conversion
- Custom page size handling
- Margin and font size configuration
- Frontmatter stripping

## How to Run
```bash
cd C:\Edwin\repos\obsidian-supernote-sync
venv\Scripts\activate
pytest tests/test_pandoc_converter.py -v
```

## Evidence
Last run: 2026-01-31
- Tests passing
