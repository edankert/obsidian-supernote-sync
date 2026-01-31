---
type: "[[test]]"
id: TST-0003
title: "Note parser test suite"
status: passing
owner: Edwin
created: 2026-01-19
updated: 2026-01-31
source:
  - "tests/test_note_parser.py"
scope: feature
kind: automated
level: unit
entrypoint: "pytest tests/test_note_parser.py -v"
requirements: []
features: []
issues: []
tasks: []
artifacts: []
evidence:
  - "4/6 tests passing"
last_run: "2026-01-31"
---

# Note Parser Test Suite

## Purpose
Verify that .note file parsing works correctly, including header parsing, PNG extraction, and ZIP archive handling.

## Test Coverage

- Header parsing tests
- PNG template extraction
- ZIP archive inspection (handwriting data)
- Metadata extraction

## How to Run
```bash
cd C:\Edwin\repos\obsidian-supernote-sync
venv\Scripts\activate
pytest tests/test_note_parser.py -v
```

## Evidence
Last run: 2026-01-31
- 4 tests passed
- 2 tests skipped (require test fixtures)
