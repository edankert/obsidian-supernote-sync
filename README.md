# Obsidian-Supernote Sync Tool

A bi-directional synchronization tool between Obsidian vault and Supernote device for seamless handwritten and digital note management.

## Project Status

**Current Phase:** Phase 3B Complete - Ready for Phase 3C (Obsidian Plugin)
**Version:** 0.3.0-alpha

### Phase 3 Progress

- ✅ **Phase 3A**: Python Backend API (FastAPI with WebSocket support)
- ✅ **Phase 3B**: Web Dashboard MVP (React + Tailwind)
- ⏳ **Phase 3C**: Obsidian Plugin (next)
- ⏳ **Phase 3D**: Visual Workflow Builder (planned)

## Features

### Working ✅

- **Markdown → .note**: Convert Obsidian markdown directly to Supernote .note files (via Pandoc)
  - ✅ Frontmatter support for `supernote.type` (standard/realtime)
  - ✅ Auto-updates markdown with `supernote.file` reference
  - ✅ **Update mode** - preserves handwriting when reconverting
- **Markdown → PDF**: Convert Obsidian markdown to Supernote-optimized PDFs
- **PDF → .note**: Convert PDFs to annotatable .note files (device-tested)
- **PNG → .note**: Convert PNG templates to .note files (device-tested)
- **.note → PNG**: Extract pages as PNG images
- **.note → Markdown**: Export handwritten notes to Obsidian

### Planned (Phase 3+)

- File watching and automatic sync
- Bi-directional sync with conflict detection
- Cloud-based sync via Supernote Cloud API
- Batch processing operations

## Quick Start

### Prerequisites

- Python 3.10 or higher
- **Pandoc** (for markdown to PDF) - [Installation Guide](docs/PANDOC_SETUP.md)
- Supernote device (A5X, A5X2/Manta, A6X, A6X2/Nomad)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd obsidian-supernote-sync

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Convert markdown to .note (recommended)
obsidian-supernote md-to-note input.md output.note

# Convert .note to markdown with images
obsidian-supernote note-to-md input.note output.md

# Other commands
obsidian-supernote md-to-pdf input.md output.pdf
obsidian-supernote pdf-to-note input.pdf output.note
obsidian-supernote inspect input.note
```

### API Server & Web Dashboard

Start the backend API server for the web dashboard and automation:

```bash
# Start the API server
obsidian-supernote serve

# With custom port
obsidian-supernote serve --port 8080

# Development mode with auto-reload
obsidian-supernote serve --reload
```

The server provides:
- **REST API** at `http://localhost:8765/` - All conversion endpoints
- **API Docs** at `http://localhost:8765/docs` - Interactive Swagger UI
- **WebSocket** at `ws://localhost:8765/events` - Real-time progress updates

To use the web dashboard:

```bash
# Build the dashboard (first time only)
cd web-dashboard && npm install && npm run build && cd ..

# Start server with dashboard
obsidian-supernote serve --dashboard web-dashboard/dist
```

## Workflow Guides

Choose the workflow that matches your use case:

| Workflow | Note Type | Best For | Guide |
|----------|-----------|----------|-------|
| **Daily Notes** | `realtime` | Journaling, to-do lists, quick notes | [Guide](examples/workflows/daily-notes/) |
| **Research Notes** | `realtime` | Article annotations, study materials | [Guide](examples/workflows/research-notes/) |
| **World Building** | `standard` | Sketches, maps, character designs | [Guide](examples/workflows/world-building/) |

### Note Types Explained

- **`realtime`**: Enables Supernote's handwriting recognition. Use when capturing text that should be searchable.
- **`standard`**: Pure sketching mode. Use for visual work without text recognition.

## Frontmatter Properties

Add these optional properties to your markdown files:

```yaml
---
title: "My Note"
supernote.type: realtime  # or "standard" (default)
---
```

After conversion, the markdown is automatically updated:

```yaml
---
title: "My Note"
supernote.type: realtime
supernote.file: "[output/my-note.note]"  # Auto-added
---
```

## Update Workflow (Preserve Handwriting)

The killer feature: update your markdown content without losing handwritten annotations!

```bash
# 1. First conversion - creates .note file
obsidian-supernote md-to-note daily.md output/daily.note

# 2. Write on Supernote device (add handwriting)

# 3. Edit markdown in Obsidian (update text content)

# 4. Reconvert - handwriting is preserved!
obsidian-supernote md-to-note daily.md output/daily.note

# Output:
# "Update mode: Found existing .note file"
# "Preserving handwriting from 2 pages"
# "Update complete - handwriting preserved!"
```

## Project Structure

```
obsidian-supernote-sync/
├── obsidian_supernote/       # Main package
│   ├── converters/           # File conversion modules
│   ├── parsers/              # File format parsers
│   ├── sync/                 # Sync engine (Phase 3)
│   ├── utils/                # Utilities (frontmatter parsing)
│   └── cli.py                # Command-line interface
├── examples/
│   ├── workflows/            # Step-by-step workflow guides
│   ├── configs/              # Configuration examples
│   └── templates/            # PNG/PDF templates
├── tests/                    # Unit and integration tests
├── docs/                     # Documentation
└── requirements.txt          # Python dependencies
```

## Development

### Running Tests

```bash
pytest tests/
pytest --cov  # With coverage
```

### Code Style

```bash
black obsidian_supernote/     # Format code
ruff check obsidian_supernote/ # Lint
mypy obsidian_supernote/       # Type check
```

## Documentation

- [Workflow Guides](examples/workflows/) - Step-by-step usage guides
- [Project Roadmap](docs/ROADMAP.md) - Development phases and goals
- [Implementation Status](docs/IMPLEMENTATION_STATUS.md) - Current feature status
- [Frontmatter Properties](docs/FRONTMATTER_PROPERTIES.md) - Frontmatter reference
- [Pandoc Setup](docs/PANDOC_SETUP.md) - Installing Pandoc

## Supported Devices

| Device | Model | Resolution | Status |
|--------|-------|------------|--------|
| A5X2 | Manta | 1920 x 2560 | ✅ Tested |
| A5X | - | 1404 x 1872 | ✅ Supported |
| A6X2 | Nomad | 1404 x 1872 | ✅ Supported |
| A6X | - | 1404 x 1872 | ✅ Supported |

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
