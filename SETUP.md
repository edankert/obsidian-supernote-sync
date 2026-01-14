# Development Environment Setup

This document describes how the development environment was set up for the Obsidian-Supernote Sync Tool.

## Environment Details

- **Python Version:** 3.11.9
- **Operating System:** Windows
- **Project Location:** `C:\Edwin\OneDrive\dev\repos\obsidian-supernote-sync`
- **Virtual Environment:** `venv/`

## Initial Setup

### 1. Project Structure Created

```
obsidian-supernote-sync/
├── obsidian_supernote/        # Main Python package
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── converters/            # File format converters
│   │   └── __init__.py
│   ├── parsers/               # File format parsers
│   │   └── __init__.py
│   ├── sync/                  # Sync engine
│   │   └── __init__.py
│   └── utils/                 # Utilities
│       └── __init__.py
├── tests/                     # Test suite
│   └── test_basic.py
├── docs/                      # Documentation
├── examples/                  # Example configs
│   └── config.example.yml
├── requirements.txt           # Dependencies
├── pyproject.toml            # Project metadata
├── .gitignore                # Git ignore rules
├── .env.example              # Environment variables template
├── README.md                 # Project overview
└── SETUP.md                  # This file
```

### 2. Virtual Environment

Created and activated:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# or
venv\Scripts\activate.bat     # Windows CMD
```

### 3. Dependencies Installed

**Core dependencies:**
- `supernotelib` (0.6.4) - Supernote .note file library
- `Pillow` - Image processing
- `python-dotenv` - Environment variables
- `pyyaml` - YAML config files
- `weasyprint` - Markdown to PDF conversion
- `markdown` - Markdown parsing
- `rich` - Beautiful CLI output
- `click` - CLI framework
- `watchdog` - File monitoring
- `httpx` - HTTP client for cloud sync
- `aiofiles` - Async file I/O

**Development dependencies:**
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Code coverage
- `black` - Code formatting
- `ruff` - Linting
- `mypy` - Type checking
- `types-pyyaml` - Type stubs

### 4. Package Installation

Installed in editable mode:
```bash
pip install -e .
```

## Verification

### Tests Pass
```bash
pytest tests/test_basic.py -v
```
Output:
- ✅ test_version PASSED
- ✅ test_author PASSED

### CLI Works
```bash
obsidian-supernote --version
# Output: obsidian-supernote, version 0.1.0-alpha

obsidian-supernote --help
# Shows all available commands
```

## Available Commands

The CLI currently has these commands (all stubs, ready for implementation):

1. **md-to-pdf** - Convert Markdown to PDF for Supernote
2. **note-to-md** - Convert Supernote .note to Markdown
3. **sync** - Bi-directional sync (full sync engine)
4. **status** - Show sync status
5. **inspect** - Inspect .note file structure
6. **init** - Initialize configuration

## Next Steps

### Immediate Development Tasks

1. **Implement .note File Parser**
   - Create `obsidian_supernote/parsers/note_parser.py`
   - Use `supernotelib` to read .note files
   - Extract metadata, PNGs, and handwriting data
   - Test with real .note files from Supernote device

2. **Implement Markdown to PDF Converter**
   - Create `obsidian_supernote/converters/markdown_to_pdf.py`
   - Use `weasyprint` or `pandoc` for conversion
   - Optimize for Supernote display (A5/A6 size, e-ink friendly)
   - Add styling support

3. **Implement PDF to PNG Converter**
   - Create `obsidian_supernote/converters/pdf_to_png.py`
   - Convert PDF pages to 1920x2560 PNG images
   - Prepare for embedding in .note files

4. **Experimental: .note File Creator**
   - Create `obsidian_supernote/converters/note_creator.py`
   - Implement three-section .note file structure:
     - Binary header with metadata
     - Embedded PNG pages
     - ZIP archive with minimal handwriting data
   - Test on actual Supernote device

### Testing Requirements

Before testing on real device:
- [ ] Backup all existing .note files
- [ ] Test with disposable notes first
- [ ] Verify .note file integrity
- [ ] Test on Supernote device
- [ ] Verify can open, edit, save without corruption

## Important Notes

### Library Choice: supernotelib vs supernote-lite

**Issue:** The project documentation mentioned `supernote-lite`, but it requires Python >=3.13
**Solution:** Using `supernotelib` (version 0.6.4) instead, which works with Python 3.11+

`supernotelib` is the PyPI package for the `supernote-tool` project, which provides:
- .note file parsing
- Conversion to PNG, SVG, PDF, TXT
- Text extraction from recognition data
- All features needed for the project

### Pandoc Installation

**Note:** Pandoc is NOT a Python package. It must be installed separately:
- Download from: https://pandoc.org/installing.html
- Or use package manager: `choco install pandoc` (Windows)

Alternatively, use `weasyprint` which is a Python-native solution (already installed).

## Development Workflow

### Running Tests
```bash
pytest
pytest -v  # verbose
pytest --cov  # with coverage
```

### Code Formatting
```bash
black obsidian_supernote/
```

### Linting
```bash
ruff check obsidian_supernote/
```

### Type Checking
```bash
mypy obsidian_supernote/
```

## Configuration

1. Copy example files:
   ```bash
   cp .env.example .env
   cp examples/config.example.yml config.yml
   ```

2. Edit `.env` with your credentials and paths

3. Edit `config.yml` with your sync preferences

## Troubleshooting

### Virtual Environment Not Activating
- Windows CMD: Use `venv\Scripts\activate.bat`
- Windows PowerShell: Use `venv\Scripts\Activate.ps1`
- Git Bash: Use `source venv/Scripts/activate`

### Import Errors
- Ensure virtual environment is activated
- Reinstall in editable mode: `pip install -e .`

### Test Failures
- Check Python version: `python --version` (should be 3.10+)
- Verify dependencies: `pip list`

## Resources

- [supernotelib Documentation](https://github.com/jya-dev/supernote-tool)
- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)

---

**Setup Date:** 2025-01-14
**Python Version:** 3.11.9
**Status:** ✅ Development environment ready
