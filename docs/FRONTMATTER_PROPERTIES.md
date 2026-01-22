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

### 2. `supernote.file` (Auto-Managed)

**Type:** String (file path with [x.note] notation)
**Valid Values:** `"[relative/path/file.note]"` notation
**Default:** None (auto-set after first conversion)
**Required:** No (automatically managed by CLI)
**Workflow Use:** All workflows (auto-updated)

**Description:**
**Automatically managed property** that links a markdown file to its generated .note file. After the first conversion, the CLI automatically adds/updates this property in the markdown frontmatter with a reference to the created .note file.

**Path Format - [x.note] Notation:**
The CLI uses bracketed notation to indicate relative paths from the markdown file:
- Same directory: `"[daily.note]"`
- Subdirectory: `"[output/daily.note]"`
- Parent directory: `"[../daily.note]"`
- Cross-platform: Always uses forward slashes `/`

**Automatic Update Workflow:**
1. User creates markdown without `supernote.file`
2. User runs: `obsidian-supernote md-to-note daily.md output/daily.note`
3. CLI creates `output/daily.note` **and** updates `daily.md` frontmatter:
   ```yaml
   supernote.file: "[output/daily.note]"
   ```
4. Future: Edit markdown and re-run conversion → updates existing .note (preserves handwriting)

**Impact on Conversion:**
- First conversion: Creates new .note file, auto-updates markdown
- Future conversions (when implemented): Updates .note file, preserves annotations
- Can disable auto-update with: `--no-update-markdown` flag

**Note:** Update mode (preserving handwriting while replacing template) is planned for future implementation.

**Examples (Auto-Generated):**

```yaml
# After first conversion, CLI automatically adds:
supernote.file: "[output/daily.note]"

# Subdirectory example (auto-generated):
supernote.file: "[Reading/DeepLearning_2026.note]"

# Parent directory example (auto-generated):
supernote.file: "[../notes/Aragorn.note]"
```

**Current Behavior (v0.2.0-alpha):**
- ✅ Auto-updates markdown after conversion
- ✅ Uses [x.note] notation for relative paths
- ✅ Preserves existing frontmatter properties
- ⏳ Update mode (preserving handwriting): Planned for future release

**Implementation Checklist:**
- [x] Read path from frontmatter
- [x] Auto-update markdown with file reference
- [x] Use [x.note] bracket notation
- [x] Handle relative and absolute paths
- [x] Preserve existing frontmatter
- [ ] Implement update mode (preserve annotations)
- [ ] Test update mode preserves handwriting

---

## Defaults Summary

| Property | Default | Behavior |
|----------|---------|----------|
| `supernote.type` | `"standard"` | Used if not specified in frontmatter |
| `supernote.file` | Auto-generated | Set automatically after first conversion |

---

## Validation Rules

### Properties to Validate

1. **`supernote.type`**
   - Must be either `"standard"` or `"realtime"`
   - If missing: use default `"standard"`
   - If invalid: log warning, use default

2. **`supernote.file`** (if present)
   - Auto-managed by CLI (normally don't edit manually)
   - Uses [x.note] bracket notation for relative paths
   - If missing: normal (first conversion hasn't happened yet)
   - If present: indicates linked .note file exists
   - Future: Will trigger update mode instead of create mode

### Error Handling

**Invalid Values:**
```yaml
# Invalid supernote.type
supernote.type: "recognition"  # ERROR: not "standard" or "realtime"
# Action: Log warning, use default "standard", continue

# Missing supernote.file (not an error - normal for first conversion)
# Action: Create new .note file, auto-update markdown with reference

# Manually edited supernote.file (future: will trigger update mode)
supernote.file: "[Reading/Article.note]"
# Current: Logged as info, update mode not yet implemented
# Future: Will update existing .note file instead of creating new
```

**Validation Checklist:**
- [ ] All properties are optional
- [ ] Missing properties use defaults or enable default behavior
- [ ] Invalid values log warnings but don't crash
- [ ] Provide helpful error messages
- [ ] Device/page_size/version handled by sync software (not validated here)

---

## Implementation Summary

### Properties Implemented (2 total)

1. ✅ `supernote.type` - Type of note (standard/realtime) — **CONTENT PROPERTY** ✅ COMPLETE
2. ✅ `supernote.file` - Path to linked .note file — **AUTO-MANAGED** ✅ COMPLETE

### Code Changes Completed

**File: `obsidian_supernote/utils/frontmatter.py`** ✅ CREATED
- [x] Add frontmatter parsing (YAML extraction)
- [x] Add property validation functions
- [x] Create property defaults configuration
- [x] Add [x.note] notation support
- [x] Auto-update markdown with file reference

**File: `obsidian_supernote/converters/note_writer.py`** ✅ UPDATED
- [x] Handle `supernote.type` parameter
- [x] Handle `supernote.file` parameter (parse and log)
- [x] Auto-update markdown after conversion
- [ ] Implement update mode (preserve annotations) - FUTURE

**File: `obsidian_supernote/cli.py`** ✅ UPDATED
- [x] Added `md-to-note` command
- [x] Read markdown file and extract frontmatter
- [x] Pass properties to converter functions
- [x] Show which properties are being used
- [x] Added `--no-update-markdown` flag

**Tests Completed:** ✅ 34/34 PASSING
- [x] Parse valid YAML frontmatter
- [x] Handle missing properties (use defaults)
- [x] Validate property values
- [x] Warn on invalid values
- [x] Examples from each workflow
- [x] Test [x.note] notation
- [x] Test markdown auto-update
- [x] Test path resolution

---

## Workflow-Specific Property Usage

### Workflow 1: Daily Notes (Realtime + Auto-Update)

**User Creates:**
```yaml
---
title: "Daily Notes 2026-01-20"
created: 2026-01-20
supernote.type: realtime
---
```

**After CLI Conversion (Auto-Updated):**
```yaml
---
title: "Daily Notes 2026-01-20"
created: 2026-01-20
supernote.type: realtime
supernote.file: "[Journal/2026-01-20.note]"
---
```

**Properties Used:** `supernote.type` (user-set), `supernote.file` (auto-added)
**Expected:** Realtime note created, markdown auto-updated with file reference

---

### Workflow 2: Research Notes (Realtime + Auto-Update)

**User Creates:**
```yaml
---
title: "Deep Learning Advances in 2026"
author: "LeCun & Hinton"
tags: [research, ai, to-supernote]
supernote.type: realtime
---
```

**After CLI Conversion (Auto-Updated):**
```yaml
---
title: "Deep Learning Advances in 2026"
author: "LeCun & Hinton"
tags: [research, ai, to-supernote]
supernote.type: realtime
supernote.file: "[Reading/DeepLearning_2026.note]"
---
```

**Properties Used:** `supernote.type` (user-set), `supernote.file` (auto-added)
**Expected:** Realtime note created, markdown auto-updated with file reference

---

### Workflow 3: World Building (Standard + Auto-Update)

**User Creates:**
```yaml
---
title: "Aragorn - Ranger King"
aliases: ["Strider"]
tags: [characters, worldbuilding, fantasy]
created: 2026-01-10
supernote.type: standard
---
```

**After CLI Conversion (Auto-Updated):**
```yaml
---
title: "Aragorn - Ranger King"
aliases: ["Strider"]
tags: [characters, worldbuilding, fantasy]
created: 2026-01-10
supernote.type: standard
supernote.file: "[Characters/Aragorn.note]"
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

