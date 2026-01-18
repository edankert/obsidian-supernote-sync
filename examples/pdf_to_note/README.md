# PDF to .note Conversion Example

This directory contains an example of PDF to Supernote .note file conversion.

## Files

- `sample_document.pdf` - A sample 2-page PDF document
- `sample_document.note` - The converted Supernote .note file

## How to Use

### Convert PDF to .note

```bash
obsidian-supernote pdf-to-note sample_document.pdf sample_document.note
```

### Options

- `--device` - Target Supernote device (A5X, A6X, Nomad, N5, N6). Default: A5X
- `--language` - Recognition language (en_GB, en_US, etc.). Default: en_GB
- `--dpi` - DPI for rendering PDF pages (higher = better quality). Default: 300

### Copy to Supernote

1. Connect your Supernote via USB or use Supernote Partner app
2. Copy the `.note` file to the `Note/` folder on your device
3. Open the file on your Supernote and start annotating!

## Workflow

1. **Create/Export PDF** - Use any application to create a PDF document
2. **Convert to .note** - Run `obsidian-supernote pdf-to-note` to convert
3. **Annotate on Supernote** - Add handwritten notes, highlights, etc.
4. **Export back** - Use `obsidian-supernote note-to-md` to export annotations
