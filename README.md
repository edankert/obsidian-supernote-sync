# Obsidian-Supernote Sync Tool

A bi-directional synchronization tool between Obsidian vault and Supernote device for seamless handwritten and digital note management.

## Project Status

**Current Phase:** Phase 1 Complete - Core Converters Working
**Version:** 0.2.0-alpha

## Features

### Working ✅

- **Markdown → .note**: Convert Obsidian markdown directly to Supernote .note files (via Pandoc)
- **Markdown → PDF**: Convert Obsidian markdown to Supernote-optimized PDFs (via Pandoc)
- **PDF → .note**: Convert PDFs to annotatable Supernote .note files (device-tested)
- **PNG → .note**: Convert PNG templates to .note files (device-tested)
- **.note → PNG**: Extract pages as PNG images (via supernotelib)
- **.note → Markdown**: Export handwritten notes to Obsidian markdown

### Planned

- Bi-directional sync with conflict detection
- Cloud-based sync support with automatic change detection
- Intelligent change detection using MD5 hashing
- Text extraction from Supernote's built-in handwriting recognition (via supernotelib)

## Quick Start

### Prerequisites

- Python 3.10 or higher
- **Pandoc** (for markdown to PDF conversion) - [Installation Guide](docs/PANDOC_SETUP.md)
- Supernote device (A5X, A6X, or Nomad)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd obsidian-supernote-sync

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Convert markdown to PDF for Supernote
python -m obsidian_supernote.cli md-to-pdf input.md output.pdf

# Convert Supernote note to markdown
python -m obsidian_supernote.cli note-to-md input.note output.md

# Full sync (coming soon)
python -m obsidian_supernote.cli sync --config config.yml
```

## Project Structure

```
obsidian-supernote-sync/
├── obsidian_supernote/       # Main package
│   ├── converters/           # File conversion modules
│   ├── sync/                 # Sync engine
│   ├── parsers/              # File format parsers
│   └── cli.py               # Command-line interface
├── tests/                    # Unit and integration tests
├── docs/                     # Documentation
├── examples/                 # Example files and configs
└── requirements.txt          # Python dependencies
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project uses:
- `black` for code formatting
- `ruff` for linting
- `mypy` for type checking

```bash
# Format code
black obsidian_supernote/

# Run linter
ruff check obsidian_supernote/

# Type checking
mypy obsidian_supernote/
```

## Documentation

For detailed documentation, see:
- [Project Roadmap](docs/ROADMAP.md) - Development phases and goals
- [Implementation Status](docs/IMPLEMENTATION_STATUS.md) - Current feature status
- [Pandoc Setup](docs/PANDOC_SETUP.md) - Installing Pandoc for PDF conversion
- [Testing Notes](docs/TESTING_NOTES.md) - Testing documentation

## Related Projects

- [supernote-tool](https://github.com/jya-dev/supernote-tool) - Core library for .note parsing (supernotelib)
- [supernote-lite](https://github.com/allenporter/supernote-lite) - Alternative lighter toolkit
- [supernote-to-obsidian](https://github.com/heyScully/supernote-to-obsidian) - One-way sync inspiration

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## Acknowledgments

- MyScript for the iink SDK used in Supernote devices
- Allen Porter for supernote-lite library
- Supernote community for reverse engineering efforts
