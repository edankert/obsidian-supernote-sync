# Testing Notes - Real Supernote Files

**Date:** 2026-01-14
**Supernote Directory:** `C:\Users\Edwin Dankert\AppData\Roaming\com.ratta\supernote_partner\1002291834829889536\Supernote`

## Test Results

### Successful Parsing

#### 1. Cover.note ✓
```
File: C:\...\Supernote\Note\Cover.note
Size: 22.21 MB
Device: N6 (Nomad)
Format: 20230015
Template: None
PNG Images: 1 (1404x1872 pixels, 1.33 MB)
ZIP Archive: 0 KB
Status: PARSED SUCCESSFULLY
```

**Analysis:**
- Large file with embedded PNG image
- Nomad device file format
- No PDF template
- Successfully extracted PNG dimensions and metadata

#### 2. 20250102_205433.note ✓
```
File: C:\...\Supernote\Note\20250102_205433.note
Size: 0.69 MB
Device: N5
Format: 20230015
Template: None
PNG Images: 0
ZIP Archive: 0 KB
Status: PARSED (with caveats)
```

**Analysis:**
- Smaller file without PNG templates
- N5 device format
- File has data but ZIP extraction shows 0 KB (needs investigation)

#### 3. 20241004_120815.note ✓
```
File: C:\...\Supernote\Note\20241004_120815.note
Size: 0.58 MB
Device: A6X
Format: 20230015
Template: None
PNG Images: 0
ZIP Archive: 0 KB
Status: PARSED (with caveats)
```

**Analysis:**
- A6X device file
- Similar to previous - has data but ZIP not extracted

### Directory Structure Found

```
Supernote/
├── Document/           # PDF documents
├── EXPORT/            # Exported files
├── INBOX/             # Quick captures
├── MyStyle/           # PDF templates
├── Note/              # Main notes directory
│   ├── Personal/
│   │   ├── [01] 📥 Inbox/
│   │   ├── [02] 📆 Journal/
│   │   │   └── Daily Notes/
│   │   │       ├── 20241012.note
│   │   │       ├── 20241219.note
│   │   │       ├── 20241226.note
│   │   │       └── ...
│   ├── Cover.note
│   ├── 20241004_120815.note
│   └── 20250102_205433.note
└── SCREENSHOT/        # Screenshots
```

**Observations:**
- Organized folder structure with emojis in names
- Multiple device types (N5, N6/Nomad, A6X)
- Mix of timestamped and named files
- Hierarchical organization similar to Obsidian vault

## Issues Discovered

### 1. Windows Console Unicode Encoding ✓ FIXED
**Problem:** Unicode characters (✓, ✗, emojis) cause `UnicodeEncodeError: 'charmap' codec can't encode character`

**Solution:**
- Replaced Unicode symbols with simple text (SUCCESS, ERROR, OK)
- Still issues with emojis in file paths (Windows console limitation)

**Workaround:** Use paths without emojis for now, or implement proper Unicode console handling

### 2. ZIP Archive Extraction ⚠️ NEEDS INVESTIGATION
**Problem:** Files with handwriting show "0 KB" ZIP archive even though they have file size

**Possible causes:**
- Different .note file format for files without templates
- ZIP might not start with standard PK signature
- Data might be in different encoding/compression
- Our parser might be missing the ZIP data location

**Next steps:**
- Use supernotelib to compare results
- Examine binary structure of these files more carefully
- Check if ZIP is at different offset or has different format

### 3. Emoji Paths ⚠️ MINOR ISSUE
**Problem:** Paths with emojis (like `[02] 📆 Journal`) cause console encoding errors

**Workaround:**
- Convert emoji to ASCII when displaying paths
- Or use file IDs instead of full paths in output

## Parser Improvements Made

### Before
- Only handled files with PNG templates
- Failed on files without PNG or ZIP signatures
- Unicode characters caused crashes

### After
- Handles files with and without PNG templates
- Fallback header parsing using tag boundaries
- Removed problematic Unicode characters
- More robust error handling

## Devices Found

| Device Code | Device Name | Files Found |
|-------------|-------------|-------------|
| N5 | Supernote A5 | Yes |
| N6 | Supernote Nomad | Yes |
| A6X | Supernote A6X | Yes |

All devices use format version `20230015` (2023 format).

## Next Steps

### Immediate (High Priority)

1. **Fix ZIP Extraction**
   - Investigate why ZIP shows 0 KB for files without templates
   - Test with supernotelib to compare results
   - May need to handle different .note file variants

2. **Install Pandoc**
   - Required for PDF generation testing
   - Test markdown → PDF conversion with real Obsidian notes

3. **Test with Files That Have Templates**
   - Look in MyStyle folder for PDF templates
   - Find .note files that use templates
   - Test PNG extraction

### Medium Priority

4. **Implement Cloud Sync**
   - User prefers cloud-based sync
   - Need Supernote Cloud credentials
   - Use supernote-cloud-python or similar library

5. **Implement .note → Markdown Converter**
   - Extract handwriting as PNGs
   - Add OCR for text extraction (Tesseract or Gemini)
   - Generate markdown with embedded images

### Low Priority

6. **Handle Unicode Paths**
   - Properly handle emojis in file paths
   - Set up Unicode console encoding on Windows
   - Or sanitize paths for display

7. **Batch Processing**
   - Convert multiple .note files at once
   - Bulk export to Obsidian vault

## Test Commands Used

```bash
# Activate environment
cd C:\Edwin\OneDrive\dev\repos\obsidian-supernote-sync
venv\Scripts\activate

# Inspect a .note file
obsidian-supernote inspect "C:\Users\Edwin Dankert\...\Cover.note"

# Extract PNGs
obsidian-supernote inspect "C:\Users\Edwin Dankert\...\Cover.note" --save-images extracted/

# Find .note files
find "C:\Users\Edwin Dankert\...\Supernote\Note" -name "*.note" -type f
```

## Recommendations

### For Cloud Sync Implementation

1. **Use existing directory structure**
   - User already has Supernote Partner app syncing to local directory
   - Can monitor this directory for changes
   - Or implement cloud API for real-time sync

2. **Folder mapping**
   ```
   Supernote → Obsidian
   Note/Personal/[02] 📆 Journal/Daily Notes → 02 Journal/Daily Notes
   Note/Personal/[01] 📥 Inbox → 01 Inbox
   ```

3. **File naming**
   - Supernote uses timestamps: `20241219.note`
   - Obsidian uses: `2024-12-19.md`
   - Need conversion strategy

### For PDF Template Workflow

1. **MyStyle folder**
   - Store generated PDFs here
   - Supernote can apply as templates
   - User manually applies on device

2. **Naming convention**
   - Use Obsidian note title
   - Sanitize special characters
   - Keep under 50 characters

## Success Metrics

✓ Parser works with real Supernote files
✓ Multiple device formats supported
✓ PNG extraction working (for template files)
✓ Metadata extraction working
⚠️ ZIP extraction needs improvement
⚠️ Full handwriting extraction pending

## Questions for User

1. **Cloud Sync Credentials**
   - Do you have Supernote Cloud account?
   - Email and password for API access?

2. **Sync Scope**
   - Which folders to sync? (Daily Notes? Inbox? All?)
   - One-way or bi-directional?

3. **File Naming**
   - How to handle date formats (Supernote vs Obsidian)?
   - Keep original names or convert?

4. **Testing PDFs**
   - Which Obsidian notes to test converting first?
   - Any specific formatting requirements?

---

**Status:** Parser working, ready for next phase (Cloud Sync + .note→Markdown converter)
