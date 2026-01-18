# No Template Notes Analysis

**Status:** Pending - waiting for golden source files

## Files to Analyze

| File | Template | Mode | Content |
|------|----------|------|---------|
| 09_standard_none_blank.note | None | Standard | Empty |
| 10_standard_none_written.note | None | Standard | Handwriting |
| 11_realtime_none_written.note | None | Real-time | Handwriting |

## Analysis Commands

```bash
# Dump structure of each file
python examples/analysis/dump_structure.py examples/golden_sources/no_template/09_standard_none_blank.note

# Compare with PNG template version
python examples/analysis/compare_notes.py \
    examples/golden_sources/no_template/09_standard_none_blank.note \
    examples/golden_sources/png_template/01_standard_png_blank.note
```

## Findings

### Header Differences (no template vs with template)

| Field | No Template | With Template | Notes |
|-------|-------------|---------------|-------|
| PDFSTYLE | | | Expected: "none" or similar |
| PDFSTYLEMD5 | | | Expected: "0" or empty |
| STYLEUSAGETYPE | | | Expected: 0 |

### Default Style

**Question:** What built-in style is used when no template is selected?

Observed `STYLE_` entries:
```
(paste actual entries here)
```

### BGLAYER Structure

Without a template:
- Does BGLAYER have content?
- What is LAYERBITMAP value?

## Conclusions

(To be filled after analysis)
