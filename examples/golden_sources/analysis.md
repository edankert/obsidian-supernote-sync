# Golden Sources Analysis Results

**Analysis Date:** 2026-01-18 (Updated 2026-01-19)
**Firmware:** Chauvet 3.14.27 (signature SN_FILE_VER_20230015)
**Device:** Supernote Manta A5X2 (reports as "N5")
**Status:** ✅ RESOLVED - Both PNG and PDF converters working on device

## Summary of Findings

The comparison between real device-created files and our generated files revealed several critical differences. All issues have been resolved and device-tested.

## Critical Fixes Required

### 1. Device Equipment Name
| Field | Our Value | Real Value |
|-------|-----------|------------|
| APPLY_EQUIPMENT | A5X2 | N5 |

**Finding:** The Manta device identifies itself as "N5", not "A5X2".

### 2. Old Apply Equipment Flag
| Field | Our Value | Real Value |
|-------|-----------|------------|
| IS_OLD_APPLY_EQUIPMENT | 0 | 1 |

**Finding:** Real files always have this set to `1`.

### 3. Module Label
| Field | Our Value | Real Value |
|-------|-----------|------------|
| MODULE_LABEL | SNFILE_FEATURE | none |

**Finding:** Real files use `none` as the value.

### 4. BGLAYER Type
| Field | Our Value | Real Value |
|-------|-----------|------------|
| BGLAYER LAYERTYPE | MARK | NOTE |

**Finding:** BGLAYER uses `NOTE` as its type, not `MARK`.

### 5. Layer Count
| Condition | Our Approach | Real Approach |
|-----------|--------------|---------------|
| Layers per page | Always 5 | Only created layers |

**Finding:** Real files only include MAINLAYER and BGLAYER by default. LAYER1, LAYER2, LAYER3 only appear when actually used.

### 6. Missing Layer Metadata Fields
Real layer metadata includes these fields we don't generate:
- `LAYERPATH: 0`
- `LAYERVECTORGRAPH: 0`
- `LAYERRECOGN: 0`

### 7. Missing Page Metadata Fields
Real page metadata includes these fields we don't generate:
- `DISABLE: none`
- `PAGETEXTBOX: 0`

### 8. STYLE Entry Format

**PNG Template:**
```
STYLE_user_{templatename}{md5}:{address}
```
Example: `STYLE_user_blank_template_a5x21ef5ff7ca78996aa64761d41b26fe9c4:330`

Note: No underscore between template name and md5, no size suffix.

**PDF Template:**
```
STYLE_user_pdf_{filename}_{pagenum}{page_md5}_{pdfsize}:{address}
```
Example: `STYLE_user_pdf_sample_document_165213181db25ddd0778f1bdee2c0e949_155947:671`

Note: Page-specific md5, PDF file size suffix.

### 9. PDF-Specific Footer Entries
PDF-based notes include:
- `PDFSTYLELIST:{address}` - Address to some style list data
- `STYLE_style_white_a5x2:{address}` - Default/fallback style entry

### 10. PAGESTYLEMD5 Format

**PNG Template:** `{md5}` (no size suffix)
**PDF Template:** `{page_md5}_{pdf_size}`

## Standard vs Real-time Mode Differences

| Field | Standard Mode | Real-time Mode |
|-------|---------------|----------------|
| FILE_RECOGN_TYPE | 0 | 1 |
| FILE_RECOGN_LANGUAGE | none | en_GB |

Layer structure is the same in both modes when blank.

## File Structure Comparison

### PNG Template Notes (Blank)
- Size: ~21KB
- Layers: MAINLAYER, BGLAYER only
- Footer: No PDFSTYLELIST, no STYLE_style_white_a5x2

### PDF Template Notes (2 pages)
- Size: ~248KB
- Layers: MAINLAYER, BGLAYER per page
- Footer: Includes PDFSTYLELIST and STYLE_style_white_a5x2

### Multipage Notes (3 pages, PNG template)
- All pages share same STYLE entry (same template)
- Each page has unique PAGEID
- FILE_FEATURE points to different location (page 3 data?)

### Multilayer Notes
- All 5 layers present in LAYERSEQ when used
- LAYERSEQ order: LAYER3,LAYER2,LAYER1,MAINLAYER,BGLAYER
- LAYERINFO is base64 encoded JSON in this case

## Recommended Changes to note_writer.py

1. **Change APPLY_EQUIPMENT**: Use "N5" for Manta instead of "A5X2"
2. **Set IS_OLD_APPLY_EQUIPMENT**: Always use `1`
3. **Set MODULE_LABEL**: Use `none` instead of `SNFILE_FEATURE`
4. **Set BGLAYER LAYERTYPE**: Use `NOTE` instead of `MARK`
5. **Reduce layers**: Only create MAINLAYER and BGLAYER
6. **Add layer metadata fields**: LAYERPATH, LAYERVECTORGRAPH, LAYERRECOGN
7. **Add page metadata fields**: DISABLE, PAGETEXTBOX
8. **Fix STYLE entry format**: Remove underscore before md5
9. **Add PDF footer entries**: PDFSTYLELIST, STYLE_style_white_a5x2

## Device Equipment Mapping

| Commercial Name | Internal Code |
|-----------------|---------------|
| Manta (A5X2) | N5 |
| A5X | (unknown) |
| Nomad (A6X2) | (unknown) |
| A6X | (unknown) |

## Raw Data

See individual analysis dumps:
- `png_template/analysis.md` - PNG template specifics
- `pdf_template/analysis.md` - PDF template specifics
- `edge_cases/analysis.md` - Multipage/multilayer specifics

## Resolution Status

All fixes have been implemented and tested:

1. ✅ Updated note_writer.py with all fixes
2. ✅ Generated test files (PNG and PDF templates)
3. ✅ Tested with supernotelib - passes
4. ✅ Tested on Supernote Manta device - opens and allows writing

**Key Discovery:** The "tail" marker (4 bytes: `tail`) must appear after the footer content and before the footer address pointer. This was missing in our initial implementation.

## Implementation

Working converters are now available:

```python
from obsidian_supernote.converters.note_writer import convert_png_to_note, convert_pdf_to_note

# PNG template to .note
convert_png_to_note("template.png", "output.note", device="A5X2")

# PDF to .note
convert_pdf_to_note("document.pdf", "output.note", device="A5X2")
```
