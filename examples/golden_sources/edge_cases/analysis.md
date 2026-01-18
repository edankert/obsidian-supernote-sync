# Edge Cases Analysis

**Status:** Pending - waiting for golden source files

## Files to Analyze

| File | Description |
|------|-------------|
| 12_standard_multipage.note | Note with 3+ pages added manually |
| 13_standard_multilayer.note | Note with content on LAYER1 and LAYER2 |

## Analysis Commands

```bash
# Dump multipage structure
python examples/analysis/dump_structure.py examples/golden_sources/edge_cases/12_standard_multipage.note

# Dump multilayer structure
python examples/analysis/dump_structure.py examples/golden_sources/edge_cases/13_standard_multilayer.note
```

## Multipage Analysis

### Footer Structure

How are multiple pages addressed in the footer?

```
<PAGE1:address1>
<PAGE2:address2>
<PAGE3:address3>
...
```

### Page Metadata

Are there differences in page metadata for pages 2, 3, etc.?

| Field | Page 1 | Page 2 | Page 3 |
|-------|--------|--------|--------|
| PAGEID | | | |
| PAGESTYLE | | | |

## Multilayer Analysis

### Layer Metadata

When multiple layers have content:

| Layer | Has Content | LAYERBITMAP | LAYERTYPE |
|-------|-------------|-------------|-----------|
| MAINLAYER | | | |
| LAYER1 | | | |
| LAYER2 | | | |
| LAYER3 | | | |
| BGLAYER | | | |

### LAYERSEQ

What is LAYERSEQ value when multiple layers are used?

Expected format: `MAINLAYER,LAYER1,LAYER2,BGLAYER` (order of visible layers?)

## Conclusions

(To be filled after analysis)
