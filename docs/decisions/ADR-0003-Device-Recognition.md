---
type: "[[adr]]"
id: ADR-0003
title: "Use Supernote device-based text recognition"
status: accepted
owner: Edwin
created: 2026-01-20
updated: 2026-01-31
decision: "Use Supernote's built-in recognition (realtime notes) instead of external OCR"
context: "Need text extraction from handwritten notes"
alternatives:
  - "External OCR service (Google Cloud Vision, AWS Textract)"
  - "Local OCR (Tesseract)"
  - "No text extraction"
consequences:
  - "More accurate for Supernote handwriting"
  - "No API costs"
  - "Data stays on device"
  - "Only works for realtime notes"
supersedes: ""
superseded: ""
source:
  - "PLAN.md"
related:
  - "[[FEAT-0001-Manual-CLI-Frontmatter]]"
---

# ADR-0003: Device-Based Text Recognition

## Status
ACCEPTED

## Context
Users want to extract text from their handwritten notes on Supernote. Options include:

1. External OCR services (Google Cloud Vision, AWS Textract)
2. Local OCR (Tesseract)
3. Supernote's built-in recognition
4. No text extraction

## Decision
Use Supernote's built-in realtime handwriting recognition:
- Create .note files with `supernote.type: realtime`
- Device performs recognition as user writes
- supernotelib extracts recognized text from .note files

## Rationale

### Pros
- **More accurate**: Optimized for Supernote pen/screen
- **No API costs**: Free, unlimited usage
- **Privacy**: Data stays on device
- **Already exists**: Just need to enable it

### Cons
- Only works for realtime notes
- User must choose realtime mode in advance
- Can't retroactively recognize standard notes

## Alternatives Considered

### 1. External OCR
- Google Cloud Vision, AWS Textract
- Rejected: Costs money, privacy concerns, less accurate for handwriting

### 2. Local OCR (Tesseract)
- Open-source, runs locally
- Rejected: Poor handwriting recognition, complex setup

### 3. No Text Extraction
- Export as images only
- Rejected: Users want searchable content

## Consequences

### Positive
- Simple implementation
- Great recognition quality
- No external dependencies

### Negative
- Must choose realtime mode upfront
- Standard notes remain image-only
- Depends on supernotelib extraction support

## Implementation
- `supernote.type: realtime` frontmatter property
- `IS_REALTIME_RECOGNITION: 1` in .note metadata
- supernotelib extracts recognized text

## Usage
```yaml
---
supernote.type: realtime  # Enable recognition
---
```

For sketching (no recognition):
```yaml
---
supernote.type: standard
---
```
