# Frontmatter Properties Reference

**For Step 1: Frontmatter Property Parsing Implementation**

## Overview

Supernote conversion properties are optional YAML frontmatter fields in Obsidian markdown files that control how the CLI tool converts .note files. These properties capture **content-level metadata only** — device-specific settings (page size, device type, versioning) are handled by the synchronization software configuration, not by note properties.

All properties are optional and have sensible defaults.

---

## Architecture Rationale

**Why only 2 properties in notes, not 6?**

Obsidian notes should be **generic and device-agnostic**. A single note should work with multiple devices and sync configurations. Device-specific settings belong in the **sync software configuration**, not in the note metadata.

| Setting | In Frontmatter? | Configured By | Reason |
|---------|---|---|---|
| Note Type (standard/realtime) | ✅ YES | Note frontmatter | Content property - the note defines if it has text |
| Linked File (path to update) | ⚠️ MAYBE | Note frontmatter | Useful for Obsidian workflows, but potentially optional |
| Device Type (A5X, A5X2, etc.) | ❌ NO | Sync software config | Device-specific, changes per user |
| Page Size (A4, A5, A6) | ❌ NO | Sync software config | Device-dependent, sync software handles |
| Versioning (_v2, _v3) | ❌ NO | Sync software config | Sync strategy, not content property |
| Realtime Flag | ❌ NO | Duplicate of type | Redundant with supernote.type |

---

## Frontmatter Properties Specification

### 1. `supernote.type`

**Type:** String (enumeration)
**Valid Values:** `"standard"` | `"realtime"`
**Default:** `"standard"`
**Required:** No
**Workflow Use:** All workflows

**Description:**
Specifies whether the generated .note file should support realtime handwriting recognition. This is a **content property** because it describes the nature of the note itself.

**Values:**
- **`"standard"`**: No text recognition. Template shows as static background. User handwrites on top. Useful for sketching, highlighting, pure visual markup.
- **`"realtime"`**: Enables device's built-in character recognition. As user handwrites, text is recognized in real-time on device. Useful for annotation workflows where text capture is important.

**Impact on Conversion:**
- Sets `IS_REALTIME_RECOGNITION` flag in .note metadata
- Affects file size (realtime slightly larger due to recognition layer)
- Affects user experience on device (recognition visible vs. not visible)

**Examples:**

```yaml
# Daily Notes - should use realtime to capture handwritten text
supernote.type: realtime

# Research Notes - should use realtime for annotations with text content
supernote.type: realtime

# World Building - should use standard for pure sketching
supernote.type: standard
```

**Implementation Checklist:**
- [ ] Read from frontmatter YAML
- [ ] Default to "standard" if not specified
- [ ] Validate value is either "standard" or "realtime"
- [ ] Warn if invalid value (e.g., "recognition", "text")
- [ ] Pass to PDF→.note converter
- [ ] Test both types on device

---

### 2. `supernote.file` (Optional)

**Type:** String (file path)
**Valid Values:** Relative or absolute path to existing .note file
**Default:** None (creates new file)
**Required:** No (uncertain if truly needed)
**Workflow Use:** Research Notes, World Building (when updating)

**Description:**
*Optional/Uncertain:* Specifies an existing .note file to update instead of creating a new one. When specified, the conversion will replace the template/background content while preserving all handwritten annotations and sketches.

This property may not be essential if the sync software handles linked file determination differently.

**Path Format:**
- Relative paths are relative to vault root: `"Reading/Article.note"`
- Relative paths with backslashes work: `"Characters/Aragorn.note"`
- Absolute paths supported: `"C:/Edwin/Notes/article.note"`

**Impact on Conversion:**
- Triggers "update mode" instead of "create mode"
- Reads existing .note file structure
- Extracts annotation layers (preserves)
- Generates new PDF template
- Replaces template layer only
- Reassembles with preserved layers

**Examples:**

```yaml
# Update existing research note when article is revised
supernote.file: "Reading/DeepLearning_2026.note"

# Update character profile keeping sketches
supernote.file: "Characters/Aragorn.note"
```

**Behavior:**
- If file doesn't exist: Log warning, create new file instead
- If file is not valid .note: Error - do not proceed
- If file is locked by device: Error - wait or try later
- Always validates before attempting update

**Implementation Checklist:**
- [ ] Read path from frontmatter
- [ ] Check if file exists
- [ ] Validate .note file format (read header)
- [ ] Set conversion mode to "update" vs "create"
- [ ] Pass file path to note_writer.py
- [ ] Handle missing files gracefully
- [ ] Test update mode preserves annotations

---

## Defaults Summary

| Property | Default | Condition |
|----------|---------|-----------|
| `supernote.type` | `"standard"` | Always |
| `supernote.file` | None | None (optional feature) |

---

## Validation Rules

### Properties to Validate

1. **`supernote.type`**
   - Must be either `"standard"` or `"realtime"`
   - If missing: use default `"standard"`
   - If invalid: log warning, use default

2. **`supernote.file`** (if present)
   - Must be valid path to existing .note file
   - If missing: create new file (normal behavior)
   - If invalid path: log warning, create new file
   - Optional - only validate if property is specified

### Error Handling

**Invalid Values:**
```yaml
# Invalid supernote.type
supernote.type: "recognition"  # ERROR: not "standard" or "realtime"
# Action: Log error, use default "standard", continue

# Missing supernote.file (not an error, just optional)
# Action: Create new .note file (normal behavior)

# Invalid supernote.file path
supernote.file: "NonExistent/File.note"
# Action: Log warning, create new file instead of updating
```

**Validation Checklist:**
- [ ] All properties are optional
- [ ] Missing properties use defaults or enable default behavior
- [ ] Invalid values log warnings but don't crash
- [ ] Provide helpful error messages
- [ ] Device/page_size/version handled by sync software (not validated here)

---

## Implementation Summary

### Properties to Parse (2 total)

1. ✅ `supernote.type` - Type of note (standard/realtime) — **CONTENT PROPERTY**
2. ⚠️ `supernote.file` - Path to existing .note to update — **OPTIONAL/UNCERTAIN**

### Code Changes Needed

**File: `obsidian_supernote/converters/markdown_to_pdf.py`**
- [ ] Add frontmatter parsing (YAML extraction)
- [ ] Add property validation functions
- [ ] Create property defaults configuration
- [ ] Add logging for property reads/validation

**File: `obsidian_supernote/converters/note_writer.py`**
- [ ] Handle `supernote.type` parameter
- [ ] Handle `supernote.file` parameter

**File: `obsidian_supernote/cli.py`**
- [ ] Read markdown file and extract frontmatter
- [ ] Pass properties to converter functions
- [ ] Log which properties are being used
- [ ] Show warnings/errors clearly

**Tests Needed:**
- [ ] Parse valid YAML frontmatter
- [ ] Handle missing properties (use defaults)
- [ ] Validate property values
- [ ] Warn on invalid values
- [ ] Examples from each workflow

---

## Workflow-Specific Property Usage

### Workflow 1: Daily Notes (Realtime + Update)

```yaml
---
title: "Daily Notes 2026-01-20"
created: 2026-01-20
supernote.type: realtime
supernote.file: "Journal/2026-01-20.note"
---
```

**Properties Used:** `supernote.type`, `supernote.file`
**Expected:** Realtime note with update mode enabled
**Note:** Device, page size handled by sync software configuration

---

### Workflow 2: Research Notes (Realtime + Update)

```yaml
---
title: "Deep Learning Advances in 2026"
author: "LeCun & Hinton"
tags: [research, ai, to-supernote]
supernote.type: realtime
supernote.file: "Reading/DeepLearning_2026.note"
---
```

**Properties Used:** `supernote.type`, `supernote.file`
**Expected:** Realtime note with update mode enabled
**Note:** Device, page size handled by sync software configuration

---

### Workflow 3: World Building (Standard, Optional Update)

```yaml
---
title: "Aragorn - Ranger King"
aliases: ["Strider"]
tags: [characters, worldbuilding, fantasy]
created: 2026-01-10
supernote.type: standard
supernote.file: "Characters/Aragorn.note"
---
```

**Properties Used:** `supernote.type`, `supernote.file`
**Expected:** Standard note (sketching) with update mode enabled
**Note:** Device/page size and versioning handled by sync software configuration

---

## Testing Examples

### Example 1: Daily Note with Realtime

```yaml
---
title: "Daily Notes 2026-01-20"
supernote.type: realtime
supernote.file: "Journal/2026-01-20.note"
---

Today's tasks:
- Review PRD changes
- Implement frontmatter parsing
- Test on device
```

**Expected Behavior:**
- Reads `supernote.type: realtime`
- Reads `supernote.file: "Journal/2026-01-20.note"`
- Conversion mode: UPDATE (because supernote.file specified)
- Recognition enabled: YES (because realtime)

**Command:**
```bash
obsidian-supernote md-to-note "2026-01-20.md"
```

**Result:**
- Updates existing Journal/2026-01-20.note
- Replaces template with new content
- Preserves handwritten annotations
- Enables realtime recognition

---

### Example 2: Research Article

```yaml
---
title: "Machine Learning Survey"
supernote.type: realtime
supernote.file: "Reading/ML_Survey.note"
---

# Survey Overview

Key concepts in modern ML...
```

**Expected Behavior:**
- Type: Realtime
- File: Reading/ML_Survey.note

**Command:**
```bash
obsidian-supernote md-to-note "ml_survey.md"
```

**Result:**
- Updates "Reading/ML_Survey.note" (if exists) or creates new
- Realtime recognition enabled

---

### Example 3: World Building with Standard Type

```yaml
---
title: "Aragorn - Character Profile"
supernote.type: standard
supernote.file: "Characters/Aragorn.note"
---

# Ranger King

Physical Description:
- Tall, weathered face
- Dark grey eyes
```

**Expected Behavior:**
- Type: Standard (no text recognition)
- File: Characters/Aragorn.note

**Command:**
```bash
obsidian-supernote md-to-note "aragorn.md"
```

**Result:**
- Updates Characters/Aragorn.note (if exists) or creates new
- Standard type (no recognition)

---

## Quick Reference Cheat Sheet

```yaml
# Minimal (uses all defaults)
---
title: "My Note"
---

# Daily Notes (realtime, update)
---
title: "Daily Notes 2026-01-20"
supernote.type: realtime
supernote.file: "Journal/2026-01-20.note"
---

# Research Notes (realtime, update)
---
title: "Research Article"
supernote.type: realtime
supernote.file: "Reading/Article.note"
---

# World Building (standard, no update)
---
title: "Character Profile"
supernote.type: standard
---

# World Building (standard, with update)
---
title: "Character Profile"
supernote.type: standard
supernote.file: "Characters/Character.note"
---
```

---

## Summary

**Step 1 Requirements (Simplified):**

1. **Parse 2 content-level properties** from YAML: `supernote.type` and `supernote.file`
2. **Validate** each property against allowed values
3. **Apply defaults** for missing properties
4. **Handle errors** gracefully (warn but continue)
5. **Pass to converters** with proper precedence
6. **Test** with examples from each workflow

**Device-specific settings** (device type, page size, versioning) are configured in the **sync software**, not in note frontmatter.

**This document is the complete specification for Step 1 of Phase 2.**

