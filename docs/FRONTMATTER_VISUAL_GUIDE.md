# Frontmatter Properties - Visual Guide

## The 6 Properties at a Glance

```
┌─────────────────────────────────────────────────────────────────────┐
│ SUPERNOTE CONVERSION PROPERTIES (Optional YAML in Markdown Header)  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1. supernote_type                                                   │
│     ├─ Purpose: Type of .note (sketching vs text capture)            │
│     ├─ Type: String ("standard" | "realtime")                        │
│     ├─ Default: "standard"                                           │
│     └─ Example: supernote_type: realtime                             │
│                                                                       │
│  2. supernote_linked_file                                            │
│     ├─ Purpose: Path to existing .note to update                     │
│     ├─ Type: String (file path)                                      │
│     ├─ Default: None (creates new .note)                             │
│     └─ Example: supernote_linked_file: "Reading/Article.note"        │
│                                                                       │
│  3. supernote_device                                                 │
│     ├─ Purpose: Target device model                                  │
│     ├─ Type: String ("A5X" | "A5X2" | "A6X" | "A6X2")              │
│     ├─ Default: "A5X2"                                               │
│     └─ Example: supernote_device: A5X2                               │
│                                                                       │
│  4. supernote_page_size                                              │
│     ├─ Purpose: PDF page size before conversion                      │
│     ├─ Type: String ("A4" | "A5" | "A6" | "Letter")                │
│     ├─ Default: "A5"                                                 │
│     └─ Example: supernote_page_size: A5                              │
│                                                                       │
│  5. supernote_realtime                                               │
│     ├─ Purpose: Explicit realtime flag (overrides supernote_type)   │
│     ├─ Type: Boolean (true | false)                                  │
│     ├─ Default: From supernote_type                                  │
│     └─ Example: supernote_realtime: true                             │
│                                                                       │
│  6. supernote_version                                                │
│     ├─ Purpose: Version suffix when updating (not overwriting)       │
│     ├─ Type: Integer (positive number)                               │
│     ├─ Default: None (overwrites original)                           │
│     └─ Example: supernote_version: 2                                 │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## How They Work Together

### Property Dependencies & Relationships

```
┌──────────────────────────────────────────────────────────────┐
│                    PROPERTY RELATIONSHIPS                     │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  supernote_type ─────┐                                        │
│                      ├─ Determines if text recognition enabled
│                      │  (realtime) or disabled (standard)     │
│  supernote_realtime ─┘  Explicit override if both specified  │
│                                                                │
│  supernote_device ──────┐                                     │
│  supernote_page_size ───┼─ PDF generation settings            │
│                         │  (resolution, layout)               │
│                         │                                      │
│  supernote_linked_file ──────┐                                │
│                              ├─ Triggers UPDATE mode           │
│  supernote_version ─────────┘  (replace template, keep       │
│                                 sketches, optionally version)  │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## Three Usage Scenarios

### Scenario 1: Create New .note (No Linked File)

```yaml
---
title: "My Article"
supernote_type: standard
supernote_device: A5X2
supernote_page_size: A5
---
Content...
```

**Flow:**
```
Read frontmatter
    ↓
Parse properties: type=standard, device=A5X2, page_size=A5
    ↓
Generate PDF (A5 page size, A5X2 resolution)
    ↓
Convert PDF to new .note (standard format)
    ↓
Output: article.note (NEW FILE)
```

---

### Scenario 2: Update Existing .note (With Linked File)

```yaml
---
title: "My Article"
supernote_type: standard
supernote_linked_file: "Reading/Article.note"
---
Updated content...
```

**Flow:**
```
Read frontmatter
    ↓
Parse properties: linked_file="Reading/Article.note"
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

### Scenario 3: Versioned Update (With Version Number)

```yaml
---
title: "Character Profile"
supernote_type: standard
supernote_linked_file: "Characters/Aragorn.note"
supernote_version: 2
---
Updated description...
```

**Flow:**
```
Read frontmatter
    ↓
Parse properties:
  linked_file="Characters/Aragorn.note"
  version=2
    ↓
Check if file exists: YES
    ↓
Extract annotation layers (PRESERVE)
    ↓
Generate new PDF
    ↓
Append version: Aragorn.note → Aragorn_v2.note
    ↓
Reassemble with preserved layers
    ↓
Output: Characters/Aragorn_v2.note (NEW VERSIONED FILE)
        Characters/Aragorn.note (ORIGINAL UNCHANGED)
```

---

## Property Validation Rules

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION RULES & DEFAULTS                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ supernote_type:                                                  │
│   Valid: "standard" or "realtime"                               │
│   Default: "standard"                                            │
│   Invalid? → Warn, use default "standard"                       │
│   Missing? → Use default "standard"                             │
│                                                                   │
│ supernote_device:                                                │
│   Valid: A5X, A5X2, A6X, A6X2                                  │
│   Default: A5X2                                                  │
│   Invalid? → Warn, use default A5X2                             │
│   Missing? → Use default A5X2                                   │
│                                                                   │
│ supernote_page_size:                                             │
│   Valid: A4, A5, A6, Letter                                     │
│   Default: A5                                                    │
│   Invalid? → Warn, use default A5                               │
│   Missing? → Use default A5                                     │
│                                                                   │
│ supernote_linked_file:                                           │
│   Valid: Path to existing .note file                            │
│   Default: None (creates new)                                   │
│   Missing? → Create new .note (default behavior)                │
│   Doesn't exist? → Warn, create new .note instead               │
│   Invalid? → Warn, create new .note instead                     │
│                                                                   │
│ supernote_realtime:                                              │
│   Valid: true or false (boolean)                                │
│   Default: From supernote_type (realtime if type="realtime")   │
│   Invalid? → Warn, use type-based default                       │
│   Missing? → Use type-based default                             │
│                                                                   │
│ supernote_version:                                               │
│   Valid: Positive integer (1, 2, 3, ...)                        │
│   Default: None (overwrite original)                            │
│   Invalid? → Warn, overwrite original instead                   │
│   Missing? → Overwrite original (if linked_file specified)      │
│   0 or negative? → Warn, overwrite original instead             │
│   Only applies if supernote_linked_file specified               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Workflow Property Recommendations

### Workflow 1: Daily Notes (REALTIME + UPDATE)

```
ALWAYS use these properties:
  ✓ supernote_type: realtime
  ✓ supernote_linked_file: "Journal/YYYYMMDD.note"

OPTIONAL:
  • supernote_device: A5X2 (use default)
  • supernote_page_size: A5 (use default)
```

**Why:**
- Daily notes capture handwritten text → need realtime
- Same file updated daily → use linked_file
- No versioning (update same note daily)

---

### Workflow 2: Research Notes (REALTIME + UPDATE + Optional Version)

```
ALWAYS use these properties:
  ✓ supernote_type: realtime
  ✓ supernote_linked_file: "Reading/Topic.note"

OPTIONAL (for iteration):
  • supernote_version: 2 (if keeping multiple versions)
  • supernote_device: A5X2 (use default)
  • supernote_page_size: A5 (use default)
```

**Why:**
- Annotations include text highlights → need realtime
- Same article might be updated → use linked_file
- Option to version when revising significantly

---

### Workflow 3: World Building (STANDARD + Optional Update + Optional Version)

```
ALWAYS use these properties:
  ✓ supernote_type: standard
  ✓ supernote_device: A5X2
  ✓ supernote_page_size: A5

OPTIONAL (for updates):
  • supernote_linked_file: "Characters/Name.note"
  • supernote_version: 2 (if versioning iterations)
```

**Why:**
- Pure sketching/drawing → use standard (no text recognition)
- A5 page size optimal for character profiles
- Optional updates when character details change
- Optional versioning to track iterations

---

## CLI Behavior & Precedence

```
┌──────────────────────────────────────────────────────────────┐
│ PROPERTY PRECEDENCE (highest to lowest):                     │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  1. CLI Flags (highest priority)                             │
│     obsidian-supernote md-to-note file.md --device A6X       │
│     → Uses A6X (overrides frontmatter)                        │
│                                                                │
│  2. Frontmatter Properties (middle)                          │
│     ---                                                        │
│     supernote_device: A5X2                                   │
│     ---                                                        │
│     → Uses A5X2 (overrides defaults)                          │
│                                                                │
│  3. Default Values (lowest priority)                         │
│     (no CLI flag, no frontmatter property)                   │
│     → Uses default "A5X2"                                    │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

**Example:**
```bash
# File has: supernote_device: A5X
# Command: --device A6X
# Result: Uses A6X (CLI wins)

# File has: supernote_device: A5X
# Command: (no --device flag)
# Result: Uses A5X (frontmatter)

# File has: (no device property)
# Command: (no --device flag)
# Result: Uses A5X2 (default)
```

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────┐
│ COPY-PASTE EXAMPLES FOR EACH WORKFLOW                │
├──────────────────────────────────────────────────────┤
│                                                        │
│ Daily Notes:                                          │
│ ───────────                                           │
│ ---                                                    │
│ title: "Daily Notes 2026-01-20"                      │
│ supernote_type: realtime                             │
│ supernote_linked_file: "Journal/2026-01-20.note"     │
│ ---                                                    │
│                                                        │
│ Research Notes:                                       │
│ ───────────────                                       │
│ ---                                                    │
│ title: "Article Title"                               │
│ supernote_type: realtime                             │
│ supernote_linked_file: "Reading/Article.note"        │
│ ---                                                    │
│                                                        │
│ World Building:                                       │
│ ───────────────                                       │
│ ---                                                    │
│ title: "Character Name"                              │
│ supernote_type: standard                             │
│ supernote_device: A5X2                               │
│ supernote_page_size: A5                              │
│ supernote_linked_file: "Characters/Name.note"        │
│ supernote_version: 2                                 │
│ ---                                                    │
│                                                        │
└──────────────────────────────────────────────────────┘
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
        {"supernote_type": "realtime", "supernote_linked_file": "..."}

STEP 3: Validate each property
        ↓
        [Check types, allowed values, ranges]

STEP 4: Apply defaults
        ↓
        [Add default values for missing properties]

STEP 5: Apply CLI overrides
        ↓
        [If --device flag passed, override supernote_device]

STEP 6: Pass to converter
        ↓
        [Convert markdown with all properties]

OUTPUT: .note file with properties respected
```

---

## Testing Checklist

```
✓ Parse frontmatter YAML
  ├─ With all 6 properties
  ├─ With some properties missing
  ├─ With no properties (use all defaults)
  └─ With invalid YAML (handle gracefully)

✓ Validate each property
  ├─ supernote_type: test "standard" and "realtime"
  ├─ supernote_device: test all 4 devices
  ├─ supernote_page_size: test all 4 sizes
  ├─ supernote_realtime: test boolean true/false
  ├─ supernote_version: test positive integers
  └─ supernote_linked_file: test valid/invalid paths

✓ Handle invalid values
  ├─ Invalid device name → warn, use default
  ├─ Non-existent file → warn, create new
  ├─ Negative version → warn, ignore
  └─ Non-boolean realtime → warn, use default

✓ Precedence rules
  ├─ CLI flags override frontmatter
  ├─ Frontmatter overrides defaults
  ├─ Defaults apply when missing
  └─ supernote_realtime overrides supernote_type

✓ Integration
  ├─ CLI reads frontmatter automatically
  ├─ Properties passed to converters
  ├─ Output respects all properties
  └─ Error messages are helpful
```

---

## Summary Table

| Need | Solution | Property |
|------|----------|----------|
| Create .note for Manta device | Use A5X2 device specs | `supernote_device: A5X2` |
| Smaller character profile layout | Use A5 page size | `supernote_page_size: A5` |
| Capture handwritten text | Enable recognition | `supernote_type: realtime` |
| Update existing .note | Specify linked file | `supernote_linked_file: "..."` |
| Keep multiple versions | Add version number | `supernote_version: 2` |
| Override frontmatter | Use CLI flag | `--device A6X` |

---

**This visual guide makes Step 1 crystal clear. Ready to implement!**

