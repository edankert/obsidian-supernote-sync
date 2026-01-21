# Frontmatter Properties - Visual Guide

## The 2 Properties at a Glance

```
┌──────────────────────────────────────────────────────────┐
│ SUPERNOTE CONVERSION PROPERTIES (Optional YAML Header)  │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  1. supernote.type                                        │
│     ├─ Purpose: Type of .note (sketching vs text)        │
│     ├─ Type: String ("standard" | "realtime")            │
│     ├─ Default: "standard"                               │
│     └─ Example: supernote.type: realtime                 │
│                                                            │
│  2. supernote.file (Optional/Uncertain)                  │
│     ├─ Purpose: Path to existing .note to update         │
│     ├─ Type: String (file path)                          │
│     ├─ Default: None (creates new .note)                 │
│     └─ Example: supernote.file: "Reading/Article.note"   │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

---

## Architecture: Why Only 2 Properties?

```
┌─────────────────────────────────────────────────────────┐
│ SEPARATION OF CONCERNS                                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│ ✅ IN FRONTMATTER (Content Properties)                 │
│ ├─ supernote.type      "standard" or "realtime"         │
│ └─ supernote.file      Path to existing .note           │
│                                                           │
│ ❌ NOT IN FRONTMATTER (Sync Software Config)            │
│ ├─ Device type         A5X2, A6X2, etc.                 │
│ ├─ Page size           A4, A5, A6, Letter                │
│ ├─ Versioning          _v2, _v3, etc.                    │
│ └─ Cloud sync settings Device, folder, frequency         │
│                                                           │
│ Why? Obsidian notes should be generic and              │
│      device-agnostic. Device-specific settings belong   │
│      in sync software configuration, not in notes.       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Three Usage Scenarios

### Scenario 1: Create New .note (Standard, No Linked File)

```yaml
---
title: "Character Profile"
supernote.type: standard
---
Content...
```

**Flow:**
```
Read frontmatter
    ↓
Parse properties: type=standard
    ↓
Generate PDF
    ↓
Convert PDF to new .note (standard format)
    ↓
Output: character.note (NEW FILE)
```

---

### Scenario 2: Update Existing .note (With Linked File)

```yaml
---
title: "Research Article"
supernote.type: realtime
supernote.file: "Reading/Article.note"
---
Updated content...
```

**Flow:**
```
Read frontmatter
    ↓
Parse properties: type=realtime, file="Reading/Article.note"
    ↓
Check if file exists: YES
    ↓
Extract annotation layers from existing .note (PRESERVE)
    ↓
Generate new PDF from updated content
    ↓
Replace template layer in .note
    ↓
Reassemble with preserved layers
    ↓
Output: Reading/Article.note (UPDATED)
        ↑
   Original annotations/sketches intact!
```

---

### Scenario 3: Minimal (Uses All Defaults)

```yaml
---
title: "My Note"
---
Content...
```

**Flow:**
```
Read frontmatter
    ↓
Properties: none specified
    ↓
Apply defaults: type=standard, no file
    ↓
Generate PDF
    ↓
Convert to new standard .note
    ↓
Output: note.note (NEW FILE)
```

---

## Property Validation Rules

```
┌──────────────────────────────────────────────────────┐
│ VALIDATION RULES & DEFAULTS                          │
├──────────────────────────────────────────────────────┤
│                                                        │
│ supernote.type:                                       │
│   Valid: "standard" or "realtime"                    │
│   Default: "standard"                                │
│   Invalid? → Warn, use default "standard"           │
│   Missing? → Use default "standard"                 │
│                                                        │
│ supernote.file:                                       │
│   Valid: Path to existing .note file                │
│   Default: None (creates new)                        │
│   Missing? → Create new .note (normal behavior)     │
│   Doesn't exist? → Warn, create new .note instead   │
│   Invalid? → Warn, create new .note instead         │
│                                                        │
└──────────────────────────────────────────────────────┘
```

---

## Workflow Property Recommendations

### Workflow 1: Daily Notes (Realtime + Update)

```
ALWAYS use:
  ✓ supernote.type: realtime
  ✓ supernote.file: "Journal/YYYYMMDD.note"

WHY?
- Daily notes capture handwritten text → need realtime
- Same file updated daily → use file property
```

**Example:**
```yaml
---
title: "Daily Notes 2026-01-20"
supernote.type: realtime
supernote.file: "Journal/2026-01-20.note"
---
```

---

### Workflow 2: Research Notes (Realtime + Optional Update)

```
ALWAYS use:
  ✓ supernote.type: realtime

OPTIONAL:
  • supernote.file: "Reading/Article.note" (if updating)

WHY?
- Annotations include text highlights → need realtime
- May update if article is revised → optional file
```

**Example:**
```yaml
---
title: "Research Article"
supernote.type: realtime
supernote.file: "Reading/Article.note"
---
```

---

### Workflow 3: World Building (Standard, Optional Update)

```
ALWAYS use:
  ✓ supernote.type: standard

OPTIONAL:
  • supernote.file: "Characters/Name.note" (if updating)

WHY?
- Pure sketching/drawing → use standard
- May update character profiles → optional file
```

**Example:**
```yaml
---
title: "Aragorn - Character Profile"
supernote.type: standard
supernote.file: "Characters/Aragorn.note"
---
```

---

## What Step 1 Code Must Do

```
INPUT: Markdown file with frontmatter
        ↓

STEP 1: Extract YAML frontmatter
        ↓
        [Extract text between --- delimiters]

STEP 2: Parse into dictionary
        ↓
        {"supernote.type": "realtime", "supernote.file": "..."}

STEP 3: Validate each property
        ↓
        [Check types, allowed values]

STEP 4: Apply defaults
        ↓
        [Add default values for missing properties]

STEP 5: Pass to converter
        ↓
        [Convert markdown with all properties]

OUTPUT: .note file with properties respected
```

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────┐
│ COPY-PASTE EXAMPLES FOR EACH WORKFLOW            │
├──────────────────────────────────────────────────┤
│                                                   │
│ Daily Notes (realtime + update):                │
│ ──────────────────────────────────              │
│ ---                                              │
│ title: "Daily Notes 2026-01-20"                 │
│ supernote.type: realtime                        │
│ supernote.file: "Journal/2026-01-20.note"      │
│ ---                                              │
│                                                   │
│ Research Notes (realtime + optional update):    │
│ ────────────────────────────────────────────    │
│ ---                                              │
│ title: "Article Title"                          │
│ supernote.type: realtime                        │
│ supernote.file: "Reading/Article.note"         │
│ ---                                              │
│                                                   │
│ World Building (standard + optional update):    │
│ ──────────────────────────────────────────     │
│ ---                                              │
│ title: "Character Name"                         │
│ supernote.type: standard                        │
│ supernote.file: "Characters/Name.note"         │
│ ---                                              │
│                                                   │
│ Minimal (defaults):                             │
│ ──────────────────                              │
│ ---                                              │
│ title: "My Note"                                │
│ ---                                              │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

## Testing Checklist

```
✓ Parse frontmatter YAML
  ├─ With both properties
  ├─ With one property missing
  ├─ With no properties (use all defaults)
  └─ With invalid YAML (handle gracefully)

✓ Validate each property
  ├─ supernote.type: test "standard" and "realtime"
  ├─ supernote.file: test valid/invalid paths
  └─ Missing properties: apply defaults

✓ Handle invalid values
  ├─ Invalid type name → warn, use default
  ├─ Non-existent file → warn, create new
  └─ Provide helpful error messages

✓ Integration
  ├─ CLI reads frontmatter automatically
  ├─ Properties passed to converters
  ├─ Output respects all properties
  └─ Error messages are helpful
```

---

## Summary Table

| Need | Solution | Property | Example |
|------|----------|----------|---------|
| Capture handwritten text | Enable recognition | `supernote.type: realtime` | Daily notes |
| Update existing .note | Specify linked file | `supernote.file: "..."` | Article revisions |
| Sketching without text | No recognition | `supernote.type: standard` | World building |
| Create new .note | Omit file property | (not specified) | Default behavior |
| Device/page size | Sync software config | (not in notes) | Device settings |
| Versioning strategy | Sync software config | (not in notes) | Sync software |

---

**This visual guide makes Step 1 crystal clear. Ready to implement!**

