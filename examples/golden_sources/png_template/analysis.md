# PNG Template Notes Analysis

**Status:** Pending - waiting for golden source files

## Files to Analyze

| File | Template | Mode | Content |
|------|----------|------|---------|
| 01_standard_png_blank.note | PNG | Standard | Empty |
| 02_standard_png_written.note | PNG | Standard | Handwriting |
| 03_realtime_png_blank.note | PNG | Real-time | Empty |
| 04_realtime_png_written.note | PNG | Real-time | Handwriting |

## Analysis Commands

```bash
# Dump structure of each file
python examples/analysis/dump_structure.py examples/golden_sources/png_template/01_standard_png_blank.note

# Compare standard vs real-time (blank)
python examples/analysis/compare_notes.py \
    examples/golden_sources/png_template/01_standard_png_blank.note \
    examples/golden_sources/png_template/03_realtime_png_blank.note

# Compare blank vs written (standard)
python examples/analysis/compare_notes.py \
    examples/golden_sources/png_template/01_standard_png_blank.note \
    examples/golden_sources/png_template/02_standard_png_written.note
```

## Findings

### Header Differences

| Field | Standard | Real-time | Notes |
|-------|----------|-----------|-------|
| FILE_RECOGN_TYPE | | | |
| IS_OLD_APPLY_EQUIPMENT | | | |
| (add more as discovered) | | | |

### Layer Structure

**Standard Mode:**
- Layer count:
- Layer names:

**Real-time Mode:**
- Layer count:
- Layer names:

### Page Metadata Differences

| Field | Standard | Real-time | Notes |
|-------|----------|-----------|-------|
| RECOGNSTATUS | | | |
| RECOGNTEXT | | | |
| RECOGNFILE | | | |
| LAYERSEQ | | | |

### Footer Differences

| Field | Standard | Real-time | Notes |
|-------|----------|-----------|-------|
| PDFSTYLELIST | | | |
| STYLE entries | | | |

## Conclusions

(To be filled after analysis)
