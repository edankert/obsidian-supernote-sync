---
type: "[[test]]"
id: TST-0002
title: "Basic package structure tests"
status: passing
owner: Edwin
created: 2026-01-19
updated: 2026-01-31
source:
  - "tests/test_basic.py"
scope: system
kind: automated
level: unit
entrypoint: "pytest tests/test_basic.py -v"
requirements: []
features: []
issues: []
tasks: []
artifacts: []
evidence:
  - "2 tests passing"
last_run: "2026-01-31"
---

# Basic Package Structure Tests

## Purpose
Verify that the obsidian_supernote package is properly structured with version and author metadata.

## Test Coverage

- `test_version` - Verify `__version__` is defined and is a string
- `test_author` - Verify `__author__` equals "Edwin"

## How to Run
```bash
cd C:\Edwin\repos\obsidian-supernote-sync
venv\Scripts\activate
pytest tests/test_basic.py -v
```

## Evidence
Last run: 2026-01-31
- 2 tests passed
- 0 tests failed
