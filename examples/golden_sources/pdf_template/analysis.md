# PDF Template Notes Analysis

**Status:** Pending - waiting for golden source files

## Files to Analyze

| File | Template | Mode | Content |
|------|----------|------|---------|
| 05_standard_pdf_blank.note | PDF | Standard | Empty |
| 06_standard_pdf_written.note | PDF | Standard | Handwriting |
| 07_realtime_pdf_blank.note | PDF | Real-time | Empty |
| 08_realtime_pdf_written.note | PDF | Real-time | Handwriting |

## Analysis Commands

```bash
# Dump structure of each file
python examples/analysis/dump_structure.py examples/golden_sources/pdf_template/05_standard_pdf_blank.note

# Compare standard vs real-time (blank)
python examples/analysis/compare_notes.py \
    examples/golden_sources/pdf_template/05_standard_pdf_blank.note \
    examples/golden_sources/pdf_template/07_realtime_pdf_blank.note

# Compare PNG vs PDF template (standard, blank)
python examples/analysis/compare_notes.py \
    examples/golden_sources/png_template/01_standard_png_blank.note \
    examples/golden_sources/pdf_template/05_standard_pdf_blank.note
```

## Findings

### Header Differences (vs PNG template)

| Field | PNG Template | PDF Template | Notes |
|-------|--------------|--------------|-------|
| PDFSTYLE | | | |
| PDFSTYLEMD5 | | | |
| STYLEUSAGETYPE | | | |

### STYLE Entries in Footer

**Key Question:** What is the exact format of STYLE entries for PDF templates?

Current understanding:
```
<STYLE_{pagestyle}{pagestylemd5}:{png_address}>
```

Observed in real files:
```
(paste actual STYLE entries here after analysis)
```

### PDFSTYLELIST Mystery

**What is PDFSTYLELIST?**
- Observed value in real file: 494
- Hypothesis: (to be determined)

### Page Structure

| Aspect | PNG Template | PDF Template |
|--------|--------------|--------------|
| Pages | 1 | Multiple (from PDF) |
| PAGESTYLE format | | |
| PAGESTYLEMD5 format | | |

## Conclusions

(To be filled after analysis)
