# WeasyPrint Setup for Windows

WeasyPrint requires GTK+ libraries to be installed on Windows. This is a known requirement for PDF generation.

## Windows Installation

### Option 1: Using MSYS2 (Recommended)

1. Install MSYS2 from https://www.msys2.org/
2. Open MSYS2 terminal and run:
   ```bash
   pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-pango
   ```
3. Add MSYS2 bin directory to your PATH:
   - Default location: `C:\msys64\mingw64\bin`

### Option 2: GTK+ for Windows

1. Download GTK+ bundle from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Install GTK+ runtime
3. Add GTK+ bin directory to your PATH

### Option 3: Use Alternative Converter (Coming Soon)

We plan to add support for alternative converters that don't require system libraries:
- reportlab (Pure Python)
- Pandoc (external tool)

## Verification

Test if WeasyPrint works:

```bash
python -c "from weasyprint import HTML; print('WeasyPrint works!')"
```

## Troubleshooting

If you get "cannot load library" errors:

1. Check that GTK+ is installed
2. Verify PATH includes GTK+ bin directory
3. Restart your terminal/IDE
4. Try reinstalling weasyprint: `pip install --force-reinstall weasyprint`

## Alternative: Use Pandoc

For now, you can also use Pandoc for markdown to PDF conversion:

1. Install Pandoc: https://pandoc.org/installing.html
2. Or with chocolatey: `choco install pandoc`
3. Use command line: `pandoc input.md -o output.pdf`

We'll add Pandoc integration as an alternative converter option.
