---
type: "[[risk]]"
id: RISK-0001
title: ".note file corruption during update"
status: mitigating
owner: Edwin
created: 2026-01-20
updated: 2026-01-31
likelihood: low
impact: high
source:
  - "PLAN.md"
mitigation:
  - "Always work on copies first"
  - "Validate file structure before and after"
  - "Maintain backup of original"
  - "Extensive device testing"
mitigation_tasks: []
related: []
---

# RISK-0001: .note File Corruption

## Description
When updating an existing .note file, there is a risk of corrupting the file or losing handwriting data if the update process fails partway through.

## Likelihood: LOW
The .note format has been reverse-engineered and tested extensively. The update process reads all data before writing.

## Impact: HIGH
Corrupted .note files would result in lost handwriting annotations, which cannot be recovered.

## Mitigation Strategies

### 1. Work on Copies
- Never modify original file in place
- Create backup before update
- Only replace original after validation

### 2. Validation
- Validate .note structure before processing
- Validate output file opens correctly
- Check file size is reasonable

### 3. Testing
- Device-tested on Supernote Manta
- Integration tests for update workflow
- Edge case testing (empty annotations, many pages)

### 4. User Warning
- Recommend keeping Supernote Cloud backups enabled
- Document recovery procedures

## Current Status
- Mitigations implemented in code
- Device testing passed
- No corruption reports to date

## Contingency
If corruption occurs:
1. Restore from Supernote Cloud backup
2. Report issue with .note file for analysis
3. Fall back to PDF-only workflow
