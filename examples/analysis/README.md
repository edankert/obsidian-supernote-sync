# Analysis Tools

Scripts for analyzing and comparing Supernote .note files.

## Scripts

### dump_structure.py

Dumps the complete structure of a .note file, including:
- File header with all metadata tags
- Footer with page addresses and STYLE entries
- Page metadata for each page
- Layer metadata for each layer

**Usage:**
```bash
# Basic usage - output to terminal
python dump_structure.py path/to/note.note

# Save to file
python dump_structure.py path/to/note.note --output analysis.txt

# Output as JSON (for programmatic processing)
python dump_structure.py path/to/note.note --json > structure.json
```

**Example output:**
```
================================================================================
FILE ANALYSIS: my_note.note
================================================================================

## BASIC INFO
  Size: 129,500 bytes
  Filetype: note
  Signature: SN_FILE_VER_20230015
  Footer address: 129271

## HEADER
  Address: 24
  Length: 472 bytes
  Tags:
    APPLY_EQUIPMENT: A5X
    FILE_ID: F20260117121307842ysieok93NP6QPotl
    FILE_RECOGN_TYPE: 1
    ...
```

### compare_notes.py

Compares two .note files and highlights differences in:
- Header tags
- Footer tags (excluding addresses)
- Page metadata
- Layer structure

**Usage:**
```bash
# Basic comparison
python compare_notes.py file1.note file2.note

# Brief mode (just show which fields differ)
python compare_notes.py file1.note file2.note --brief

# JSON output
python compare_notes.py file1.note file2.note --json > diff.json
```

**Example output:**
```
================================================================================
NOTE FILE COMPARISON
================================================================================
File 1: standard_png_blank.note
File 2: realtime_png_blank.note

## SUMMARY
  page_count:
    File 1: 1
    File 2: 1

## DIFFERENCES (3 total)

  ### HEADER
    ~ FILE_RECOGN_TYPE:
        File 1: 0
        File 2: 1
    ~ IS_OLD_APPLY_EQUIPMENT:
        File 1: 0
        File 2: 1
```

### check_golden_sources.py

Checks which golden source files are present and which are missing.

**Usage:**
```bash
python check_golden_sources.py
```

## Workflow

1. **Create golden sources** on Supernote device
2. **Sync** via Supernote Partner app
3. **Copy** .note files to `golden_sources/` directories
4. **Analyze** each file:
   ```bash
   python dump_structure.py ../golden_sources/png_template/01_standard_png_blank.note
   ```
5. **Compare** pairs of files:
   ```bash
   python compare_notes.py \
       ../golden_sources/png_template/01_standard_png_blank.note \
       ../golden_sources/png_template/03_realtime_png_blank.note
   ```
6. **Document** findings in the appropriate `analysis.md` file
