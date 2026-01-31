---
type: "[[workflow]]"
id: WF-0004
title: "Development Workflow"
status: active
owner: Edwin
created: 2026-01-31
updated: 2026-01-31
source:
  - "README.md"
  - "SETUP.md"
entrypoints:
  - "pytest tests/"
  - "black obsidian_supernote/"
  - "ruff check obsidian_supernote/"
  - "mypy obsidian_supernote/"
prereqs:
  - "Python 3.10+"
  - "venv activated"
  - "Dev dependencies installed"
inputs:
  - "Source code changes"
outputs:
  - "Test results"
  - "Formatted code"
  - "Lint/type check results"
related:
  - "[[WF-0005-API-Server]]"
---

# Development Workflow

## Purpose
Run tests, format code, and check for linting/type errors during development.

## Prerequisites
1. Python 3.10+ installed
2. Virtual environment created and activated
3. Dev dependencies installed

## Setup
```bash
cd C:\Edwin\repos\obsidian-supernote-sync
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Commands

### Run Tests
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov

# Run specific test file
pytest tests/test_frontmatter_parsing.py -v
```

### Format Code
```bash
black obsidian_supernote/
```

### Lint Code
```bash
ruff check obsidian_supernote/
```

### Type Check
```bash
mypy obsidian_supernote/
```

### Full Check
```bash
black obsidian_supernote/ && ruff check obsidian_supernote/ && mypy obsidian_supernote/ && pytest tests/
```

## Code Quality Targets
- Test coverage: 80%+
- Black formatting: enforced
- Ruff: no errors
- mypy: no errors (strict mode planned)
