# Pandoc Setup Guide

Pandoc is now the **default and recommended** PDF conversion engine for Obsidian-Supernote Sync. It's much easier to install than WeasyPrint and provides excellent markdown support.

## Why Pandoc?

- ✅ **Easy Installation** - Single binary, no complex dependencies
- ✅ **Obsidian-Friendly** - Many Obsidian users already have it
- ✅ **Excellent Markdown Support** - Tables, code blocks, wikilinks
- ✅ **Cross-Platform** - Works the same on Windows, Mac, Linux
- ✅ **Professional Output** - High-quality PDF generation
- ✅ **Customizable** - LaTeX templates, custom styling

WeasyPrint is still available as an alternative (use `--engine weasyprint`), but requires GTK+ libraries on Windows which are complex to set up.

## Installation

### Step 1: Install Pandoc

#### Windows

**Option 1: Using Chocolatey (Recommended)**
```powershell
choco install pandoc
```

**Option 2: Using Scoop**
```powershell
scoop install pandoc
```

**Option 3: Manual Install**
1. Download the installer from: https://pandoc.org/installing.html
2. Run the installer (`.msi` file)
3. Pandoc will be added to PATH automatically

### Step 2: Install PDF Engine (REQUIRED)

**Pandoc needs a PDF engine to generate PDFs.** MiKTeX is recommended for high-quality output.

#### Windows - Install MiKTeX

**Option 1: Using Chocolatey (Easiest)**
```powershell
choco install miktex
```

**Option 2: Manual Install**
1. Download from: https://miktex.org/download
2. Run the installer (Basic MiKTeX ~200MB)
3. During installation, select "Install missing packages on-the-fly: Yes"
4. **Important:** Restart your terminal after installation

**Verify MiKTeX installation:**
```powershell
pdflatex --version
```

You should see MiKTeX version information.

### macOS

**Using Homebrew:**
```bash
brew install pandoc
```

**Using MacPorts:**
```bash
sudo port install pandoc
```

### Linux

**Debian/Ubuntu:**
```bash
sudo apt install pandoc
```

**Fedora:**
```bash
sudo dnf install pandoc
```

**Arch Linux:**
```bash
sudo pacman -S pandoc
```

## Verification

After installation, verify Pandoc is working:

```bash
pandoc --version
```

You should see output like:
```
pandoc 3.1.11
...
```

## Usage

### Basic Conversion

```bash
obsidian-supernote md-to-pdf input.md output.pdf
```

Pandoc is the default engine, so you don't need to specify it.

### With Options

```bash
# Custom page size
obsidian-supernote md-to-pdf notes.md notes.pdf --page-size A6

# Custom margins
obsidian-supernote md-to-pdf notes.md notes.pdf --margin 3cm

# Custom font size
obsidian-supernote md-to-pdf notes.md notes.pdf --font-size 12

# All together
obsidian-supernote md-to-pdf notes.md notes.pdf --page-size A5 --margin 2cm --font-size 11
```

### Explicit Engine Selection

```bash
# Use Pandoc (default)
obsidian-supernote md-to-pdf input.md output.pdf --engine pandoc

# Use WeasyPrint (requires GTK+)
obsidian-supernote md-to-pdf input.md output.pdf --engine weasyprint
```

## Obsidian Integration

Many Obsidian users already have Pandoc installed for:
- Exporting notes to PDF
- Academic writing with citations
- Converting between markdown formats
- Publishing workflows

If you use Obsidian plugins like:
- Pandoc Plugin
- Obsidian Enhancing Export
- Better Export PDF

You likely already have Pandoc installed!

## Supported Features

Pandoc conversion supports:

### Markdown Elements
- ✅ Headings (H1-H6)
- ✅ Bold, italic, strikethrough
- ✅ Lists (ordered and unordered)
- ✅ Code blocks with syntax highlighting
- ✅ Inline code
- ✅ Tables
- ✅ Blockquotes
- ✅ Horizontal rules
- ✅ Links and images

### Obsidian-Specific
- ✅ YAML frontmatter (automatically processed)
- ✅ Wikilinks `[[link]]` (converted to regular links)
- ✅ Wikilinks with display text `[[link|text]]`

### PDF Features
- ✅ Table of contents (automatic)
- ✅ Section numbering
- ✅ Page numbers
- ✅ Syntax highlighting for code
- ✅ Customizable page sizes (A4, A5, A6, Letter)
- ✅ Adjustable margins and fonts

## Advanced Configuration

### Custom LaTeX Template

Create a custom Pandoc template for advanced formatting:

```bash
obsidian-supernote md-to-pdf notes.md notes.pdf --template custom.latex
```

### Using Metadata Files

Separate metadata from content:

```bash
obsidian-supernote md-to-pdf notes.md notes.pdf --metadata-file meta.yaml
```

## Troubleshooting

### "Pandoc is not installed" Error

**Solution:** Install Pandoc using one of the methods above.

Verify installation:
```bash
where pandoc        # Windows
which pandoc        # Mac/Linux
```

If installed but not found, add Pandoc to your PATH:
- Windows: Add Pandoc installation directory to System PATH
- Mac/Linux: Usually automatic with package managers

### LaTeX Errors

If you see LaTeX-related errors, ensure you have a LaTeX distribution:

**Windows:** MiKTeX or TeX Live
```powershell
choco install miktex
```

**Mac:**
```bash
brew install --cask mactex
```

**Linux:**
```bash
sudo apt install texlive-latex-base texlive-latex-extra
```

### Unicode/Font Issues

For better Unicode support, use XeLaTeX engine:

The tool uses `pdflatex` by default. For better Unicode support, you can modify the engine in future versions.

### Large File Performance

For very large markdown files (>1MB):
- Consider splitting into multiple files
- Remove unnecessary images
- Reduce image resolution

## Comparison: Pandoc vs WeasyPrint

| Feature | Pandoc | WeasyPrint |
|---------|--------|------------|
| Installation | ✅ Easy | ❌ Complex (needs GTK+) |
| Windows Support | ✅ Excellent | ⚠️ Requires setup |
| Markdown Support | ✅ Native | ⚠️ Via conversion |
| PDF Quality | ✅ Professional | ✅ Good |
| Customization | ✅ LaTeX templates | ✅ CSS styling |
| Performance | ✅ Fast | ✅ Fast |
| Obsidian Users | ✅ Often installed | ❌ Rarely installed |

**Recommendation:** Use Pandoc unless you have specific CSS requirements that WeasyPrint handles better.

## Resources

- [Pandoc Official Site](https://pandoc.org/)
- [Pandoc User Guide](https://pandoc.org/MANUAL.html)
- [Pandoc GitHub](https://github.com/jgm/pandoc)
- [Obsidian + Pandoc Workflows](https://forum.obsidian.md/t/pandoc-plugin/)

## Next Steps

After installing Pandoc:

1. **Test the conversion:**
   ```bash
   obsidian-supernote md-to-pdf examples/sample.md test_output.pdf
   ```

2. **Convert your Obsidian notes:**
   ```bash
   obsidian-supernote md-to-pdf "path/to/your/note.md" "output.pdf"
   ```

3. **Transfer to Supernote:**
   - Copy the generated PDF to your Supernote device
   - Open in Supernote and annotate!

---

**Last Updated:** 2026-01-14
