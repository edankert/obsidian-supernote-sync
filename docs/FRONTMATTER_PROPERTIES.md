# Frontmatter Properties Reference

**For Step 1: Frontmatter Property Parsing Implementation**

## Overview

Supernote conversion properties are optional YAML frontmatter fields in Obsidian markdown files that control how the CLI tool converts and manages .note files. All properties are optional and have sensible defaults.

---

## Frontmatter Properties Specification

### 1. `supernote_type`

**Type:** String (enumeration)
**Valid Values:** `"standard"` | `"realtime"`
**Default:** `"standard"`
**Required:** No
**Workflow Use:** All workflows

**Description:**
Specifies whether the generated .note file should support realtime handwriting recognition.

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
supernote_type: realtime

# Research Notes - should use realtime for annotations with text content
supernote_type: realtime

# World Building - should use standard for pure sketching
supernote_type: standard
```

**Implementation Checklist:**
- [ ] Read from frontmatter YAML
- [ ] Default to "standard" if not specified
- [ ] Validate value is either "standard" or "realtime"
- [ ] Warn if invalid value (e.g., "recognition", "text")
- [ ] Pass to PDF→.note converter
- [ ] Test both types on device

---

### 2. `supernote_linked_file`

**Type:** String (file path)
**Valid Values:** Relative or absolute path to existing .note file
**Default:** None (creates new file)
**Required:** No
**Workflow Use:** Research Notes, World Building

**Description:**
Specifies an existing .note file to update instead of creating a new one. When specified, the conversion will replace the template/background content while preserving all handwritten annotations and sketches.

**Path Format:**
- Relative paths are relative to vault root: `"Reading/Article.note"`
- Relative paths with backslashes work: `"Characters/Aragorn.note"`
- Absolute paths supported: `"C:/Edwin/Notes/article.note"`
- Can be single file or pattern (Phase 3+)

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
supernote_linked_file: "Reading/DeepLearning_2026.note"

# Update character profile keeping sketches
supernote_linked_file: "Characters/Aragorn.note"

# Update with version suffix (see supernote_version)
supernote_linked_file: "Characters/Aragorn.note"
supernote_version: 2
# Result: Creates Characters/Aragorn_v2.note instead of updating original
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

### 3. `supernote_device`

**Type:** String (enumeration)
**Valid Values:** `"A5X"` | `"A5X2"` | `"A6X"` | `"A6X2"`
**Default:** `"A5X2"` (Manta - most common)
**Required:** No
**Workflow Use:** All workflows

**Description:**
Specifies which Supernote device this note is for. Different devices have different screen resolutions and optimal page sizes.

**Device Information:**
| Device | Model | Resolution | DPI | Page Size |
|--------|-------|------------|-----|-----------|
| A5X | - | 1404 x 1872 | 226 | A5 |
| A5X2 | Manta | 1920 x 2560 | 300 | A5 |
| A6X | - | 1404 x 1872 | 300 | A6 |
| A6X2 | Nomad | 1404 x 1872 | 300 | A6 |

**Impact on Conversion:**
- Determines optimal resolution for PDF rendering
- Sets device equipment code in .note metadata
- Affects DPI (affects text sharpness)
- Used for validation (page size appropriateness)

**Examples:**

```yaml
# For Manta (A5X2) - most common
supernote_device: A5X2

# For Nomad (A6X2)
supernote_device: A6X2

# For older A5X
supernote_device: A5X
```

**Implementation Checklist:**
- [ ] Read device from frontmatter
- [ ] Default to "A5X2" if not specified
- [ ] Validate device is one of four valid options
- [ ] Warn if invalid device specified
- [ ] Look up DPI and resolution for device
- [ ] Pass to PDF→.note converter
- [ ] Use in .note metadata generation

---

### 4. `supernote_page_size`

**Type:** String (enumeration)
**Valid Values:** `"A4"` | `"A5"` | `"A6"` | `"Letter"`
**Default:** `"A5"` (most common)
**Required:** No
**Workflow Use:** All workflows, especially World Building (uses A5)

**Description:**
Specifies the page size for PDF generation before conversion to .note. This affects the layout and text size in the final .note file.

**Page Size Information:**
| Size | Width | Height | Use Case |
|------|-------|--------|----------|
| A4 | 210mm | 297mm | Large documents, detailed layouts |
| A5 | 148mm | 210mm | Default, good for character profiles |
| A6 | 105mm | 148mm | Small, compact notes |
| Letter | 8.5" | 11" | US standard |

**Impact on Conversion:**
- Controls PDF page dimensions
- Affects font size relative to page
- Affects how content is laid out
- Should match device's viewing preference

**Examples:**

```yaml
# Character profiles - use A5 for compact view
supernote_page_size: A5

# Detailed research articles - use A4 for more space
supernote_page_size: A4

# Small notes - use A6
supernote_page_size: A6

# US users - use Letter
supernote_page_size: Letter
```

**Implementation Checklist:**
- [ ] Read page size from frontmatter
- [ ] Default to "A5" if not specified
- [ ] Validate page size is one of four valid options
- [ ] Warn if invalid size specified
- [ ] Pass to Markdown→PDF converter
- [ ] Validate against device (warn if mismatched)

---

### 5. `supernote_realtime`

**Type:** Boolean
**Valid Values:** `true` | `false`
**Default:** Depends on `supernote_type` (realtime=true if type is "realtime", false otherwise)
**Required:** No
**Workflow Use:** Research Notes, Daily Notes

**Description:**
Explicitly controls whether realtime character recognition is enabled. Redundant with `supernote_type` but provided for clarity when mixing standard/realtime.

**Impact on Conversion:**
- Redundant with `supernote_type: realtime`
- If both specified, this overrides `supernote_type`
- Sets recognition metadata in .note file

**Examples:**

```yaml
# Explicit realtime setting
supernote_realtime: true

# This is equivalent to:
supernote_type: realtime
```

**Implementation Checklist:**
- [ ] Read realtime boolean from frontmatter
- [ ] If both supernote_type and supernote_realtime specified, supernote_realtime wins
- [ ] Validate value is boolean (true/false)
- [ ] Warn if non-boolean value (e.g., "yes", "enabled")
- [ ] Pass to converter as recognition flag

---

### 6. `supernote_version`

**Type:** Integer
**Valid Values:** Any positive integer (1, 2, 3, ...)
**Default:** None (overwrites original)
**Required:** No (only used with `supernote_linked_file`)
**Workflow Use:** Research Notes, World Building (multi-iteration scenarios)

**Description:**
When updating an existing .note file, optionally create a versioned copy instead of overwriting. The version number is appended to the filename.

**Behavior:**
- Only applies when `supernote_linked_file` is specified
- Ignored if no linked file (creates new file normally)
- Appends `_v{number}` to filename before `.note` extension
- Preserves original file untouched

**Examples:**

```yaml
supernote_linked_file: "Characters/Aragorn.note"
supernote_version: 2
# Result: Creates "Characters/Aragorn_v2.note"
# Original "Characters/Aragorn.note" unchanged

supernote_linked_file: "Reading/Article.note"
supernote_version: 3
# Result: Creates "Reading/Article_v3.note"
```

**Use Cases:**
- **Iteration tracking**: Keep versions as character evolves
- **Comparison**: Side-by-side comparison of different versions
- **Recovery**: Original always available if needed
- **History**: Track multiple sketching sessions

**Implementation Checklist:**
- [ ] Read version number from frontmatter
- [ ] Only apply if `supernote_linked_file` is specified
- [ ] Validate version is positive integer
- [ ] Warn if version is 0 or negative
- [ ] Append `_v{number}` to output filename
- [ ] Don't overwrite if version specified
- [ ] Test filename generation

---

## Defaults Summary

| Property | Default | Condition |
|----------|---------|-----------|
| `supernote_type` | `"standard"` | Always |
| `supernote_linked_file` | None | None |
| `supernote_device` | `"A5X2"` | Always |
| `supernote_page_size` | `"A5"` | Always |
| `supernote_realtime` | From `supernote_type` | If not specified |
| `supernote_version` | None | Only if `supernote_linked_file` present |

---

## Validation Rules

### Priority & Conflicts

1. **Frontmatter properties take precedence over CLI flags**
   ```bash
   # Command: --device A6X2
   # Frontmatter: supernote_device: A5X2
   # Result: Uses A5X2 (frontmatter wins)
   ```

2. **supernote_realtime overrides supernote_type**
   ```yaml
   supernote_type: standard
   supernote_realtime: true
   # Result: Uses realtime (explicit supernote_realtime wins)
   ```

3. **supernote_version only applies with supernote_linked_file**
   ```yaml
   supernote_version: 2
   # (no supernote_linked_file)
   # Result: Ignored, creates new file normally
   ```

### Error Handling

**Invalid Values:**
```yaml
# Invalid supernote_type
supernote_type: "recognition"  # ERROR: not "standard" or "realtime"
# Action: Log error, use default "standard", continue

# Invalid device
supernote_device: "A5"  # ERROR: not one of four valid devices
# Action: Log error, use default "A5X2", continue

# Non-boolean realtime
supernote_realtime: yes  # ERROR: not boolean true/false
# Action: Log error, interpret as string, skip, use type-based default
```

**Missing Files:**
```yaml
supernote_linked_file: "NonExistent/File.note"
# Action: Log warning, create new file instead of updating
```

**Validation Checklist:**
- [ ] All properties are optional
- [ ] Missing properties use defaults
- [ ] Invalid values log warnings but don't crash
- [ ] Frontmatter properties override CLI flags
- [ ] Provide helpful error messages

---

## Implementation Summary

### Properties to Parse (6 total)

1. ✅ `supernote_type` - Type of note (standard/realtime)
2. ✅ `supernote_linked_file` - Path to existing .note to update
3. ✅ `supernote_device` - Device type (A5X, A5X2, A6X, A6X2)
4. ✅ `supernote_page_size` - Page size (A4, A5, A6, Letter)
5. ✅ `supernote_realtime` - Explicit realtime flag (boolean)
6. ✅ `supernote_version` - Version suffix for updates (integer)

### Code Changes Needed

**File: `obsidian_supernote/converters/markdown_to_pdf.py`**
- [ ] Add frontmatter parsing (YAML extraction)
- [ ] Add property validation functions
- [ ] Create property defaults configuration
- [ ] Add logging for property reads/validation

**File: `obsidian_supernote/converters/note_writer.py`**
- [ ] Handle `supernote_type` parameter
- [ ] Handle `supernote_realtime` parameter
- [ ] Handle `supernote_device` parameter
- [ ] Handle `supernote_version` in filename generation

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
- [ ] Property precedence (frontmatter > CLI)
- [ ] Examples from each workflow

---

## Workflow-Specific Property Usage

### Workflow 1: Daily Notes (Level 1: Manual)

```yaml
---
title: "Daily Notes 2026-01-20"
created: 2026-01-20
supernote_type: realtime           # Capture handwritten text
supernote_linked_file: "Journal/2026-01-20.note"  # Update daily note
---
```

**Properties Used:** `supernote_type`, `supernote_linked_file`
**Expected:** Realtime note, update mode enabled

---

### Workflow 2: Research Notes (Level 1: Manual)

```yaml
---
title: "Deep Learning Advances in 2026"
author: "LeCun & Hinton"
date: 2026-01-15
tags: [research, ai, to-supernote]
supernote_type: realtime              # Annotations with text recognition
supernote_linked_file: "Reading/DeepLearning_2026.note"  # Update if exists
---
```

**Properties Used:** `supernote_type`, `supernote_linked_file`
**Expected:** Realtime note, update mode enabled

---

### Workflow 3: World Building (Level 1: Manual)

```yaml
---
title: "Aragorn - Ranger King"
aliases: ["Strider"]
tags: [characters, worldbuilding, fantasy]
created: 2026-01-10
supernote_type: standard              # Standard (sketching, not text)
supernote_device: A5X2
supernote_page_size: A5               # Smaller for profiles
supernote_linked_file: "Characters/Aragorn.note"  # Update if exists
supernote_version: 2                  # Create v2 instead of overwriting
---
```

**Properties Used:** All six properties
**Expected:** Standard note, A5 page size, A5X2 device, update to v2

---

## Testing Examples

### Example 1: Daily Note with Realtime

```yaml
---
title: "Daily Notes 2026-01-20"
supernote_type: realtime
supernote_linked_file: "Journal/2026-01-20.note"
---

Today's tasks:
- Review PRD changes
- Implement frontmatter parsing
- Test on device
```

**Expected Behavior:**
- Reads `supernote_type: realtime`
- Reads `supernote_linked_file: "Journal/2026-01-20.note"`
- Device: A5X2 (default)
- Page size: A5 (default)
- Conversion mode: UPDATE (because supernote_linked_file specified)
- Recognition enabled: YES (because realtime)

**Command:**
```bash
obsidian-supernote md-to-note "2026-01-20.md" "2026-01-20.note"
```

**Result:**
- Updates existing Journal/2026-01-20.note
- Replaces template with new content
- Preserves handwritten annotations
- Enables realtime recognition

---

### Example 2: Research Article with Version

```yaml
---
title: "Machine Learning Survey"
supernote_type: realtime
supernote_device: A5X
supernote_page_size: A4
supernote_linked_file: "Reading/ML_Survey.note"
supernote_version: 3
---

# Survey Overview

Key concepts in modern ML...
```

**Expected Behavior:**
- Device: A5X (specified)
- Page size: A4 (specified)
- Realtime: YES
- Version: 3 (creates v3 instead of overwriting)

**Command:**
```bash
obsidian-supernote md-to-note "ml_survey.md"
```

**Result:**
- Creates "Reading/ML_Survey_v3.note" (new file, doesn't overwrite original)
- Uses A5X device settings
- Uses A4 page size
- Realtime recognition enabled

---

### Example 3: World Building with All Properties

```yaml
---
title: "Aragorn - Character Profile"
supernote_type: standard
supernote_device: A5X2
supernote_page_size: A5
supernote_linked_file: "Characters/Aragorn.note"
supernote_version: 2
---

# Ranger King

Physical Description:
- Tall, weathered face
- Dark grey eyes
```

**Expected Behavior:**
- Type: Standard (no text recognition)
- Device: A5X2 (Manta)
- Page size: A5 (compact)
- Update to: Characters/Aragorn_v2.note
- Preserve original sketches

**Command:**
```bash
obsidian-supernote md-to-note "aragorn.md"
```

**Result:**
- Creates Characters/Aragorn_v2.note
- Profile displayed on A5 page size
- Original Aragorn.note unchanged
- All original sketches preserved
- New description visible in v2

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
supernote_type: realtime
supernote_linked_file: "Journal/2026-01-20.note"
---

# Research Notes (realtime, update)
---
title: "Research Article"
supernote_type: realtime
supernote_linked_file: "Reading/Article.note"
---

# World Building (standard, version)
---
title: "Character"
supernote_type: standard
supernote_page_size: A5
supernote_linked_file: "Characters/Character.note"
supernote_version: 2
---

# Complex (all properties)
---
title: "Complete Example"
supernote_type: realtime
supernote_device: A5X2
supernote_page_size: A5
supernote_linked_file: "Path/To/File.note"
supernote_realtime: true
supernote_version: 2
---
```

---

## Summary

**Step 1 Requirements:**

1. **Parse 6 frontmatter properties** from YAML
2. **Validate** each property against allowed values
3. **Apply defaults** for missing properties
4. **Handle errors** gracefully (warn but continue)
5. **Pass to converters** with proper precedence
6. **Test** with examples from each workflow

**This document is the complete specification for Step 1 of Phase 2.**

