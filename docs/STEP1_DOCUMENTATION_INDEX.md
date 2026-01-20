# Step 1 Documentation Index

## Complete Reference for Frontmatter Property Parsing Implementation

**Created:** 2026-01-20  
**Status:** Ready for development  
**Effort:** 2 weeks

---

## Documentation Files

### 1. **FRONTMATTER_PROPERTIES.md** (634 lines)
**Complete Technical Specification**

Detailed documentation of all 6 properties with:
- Full property specifications (type, valid values, defaults)
- Validation rules and error handling
- Workflow-specific examples
- Testing examples and scenarios
- Priority/conflict resolution rules
- Quick reference cheat sheet

**Use when:** Need to understand a specific property deeply or define validation rules

**Key Sections:**
- Property 1-6 detailed specifications
- Defaults summary table
- Validation rules
- Workflow-specific usage
- Testing examples
- Summary

**Location:** `docs/FRONTMATTER_PROPERTIES.md`

---

### 2. **STEP1_REQUIREMENTS.md** (541 lines)
**Implementation Roadmap**

Step-by-step implementation guide with:
- All 6 properties at a glance (table)
- User examples for each workflow
- What Step 1 must do (code examples)
- Files that need changes (with code structure)
- Complete implementation checklist (14 days)
- Unit tests required (with example code)
- Success criteria
- End-to-end flow example
- Dependencies and references

**Use when:** Implementing Step 1 or planning the work

**Key Sections:**
- 6 properties at-a-glance table
- User examples
- File changes needed
- 14-day implementation checklist
- Unit tests
- Success criteria
- End-to-end example

**Location:** `docs/STEP1_REQUIREMENTS.md`

---

### 3. **FRONTMATTER_VISUAL_GUIDE.md** (458 lines)
**Visual Reference & Quick Lookup**

Visual diagrams and tables with:
- All 6 properties in ASCII boxes
- Property relationships diagram
- Three usage scenarios with flow diagrams
- Validation rules & defaults table
- Workflow recommendations
- CLI precedence rules
- Copy-paste examples
- Testing checklist
- Summary table

**Use when:** Need quick visual reference or teaching others

**Key Sections:**
- 6 properties visual reference
- Dependencies & relationships
- Three usage scenarios
- Validation rules table
- Workflow recommendations
- CLI precedence diagram
- Testing checklist
- Summary table

**Location:** `docs/FRONTMATTER_VISUAL_GUIDE.md`

---

## Quick Navigation

### I need to...

**Understand what Step 1 is:**
→ Start with **STEP1_REQUIREMENTS.md** (2-page overview)

**See properties visually:**
→ **FRONTMATTER_VISUAL_GUIDE.md** (quick reference boxes and diagrams)

**Implement a specific property:**
→ **FRONTMATTER_PROPERTIES.md** (full specification)

**Start implementing Step 1:**
→ **STEP1_REQUIREMENTS.md** (checklist + timeline)

**Write validation code:**
→ **STEP1_REQUIREMENTS.md** (validation section)

**Write tests:**
→ **STEP1_REQUIREMENTS.md** (unit tests section)

**Show examples to team:**
→ **FRONTMATTER_VISUAL_GUIDE.md** (diagrams and examples)

**Quick reference card:**
→ **FRONTMATTER_VISUAL_GUIDE.md** (copy-paste examples)

---

## The 6 Properties Summary

| # | Property | Type | Default | Purpose |
|---|----------|------|---------|---------|
| 1 | `supernote_type` | string | `"standard"` | standard (sketching) vs realtime (text) |
| 2 | `supernote_linked_file` | string | None | Path to existing .note to update |
| 3 | `supernote_device` | string | `"A5X2"` | Target device (A5X, A5X2, A6X, A6X2) |
| 4 | `supernote_page_size` | string | `"A5"` | PDF page size (A4, A5, A6, Letter) |
| 5 | `supernote_realtime` | boolean | From type | Explicit realtime flag (overrides type) |
| 6 | `supernote_version` | integer | None | Version suffix when updating (_v2, _v3) |

---

## Implementation Timeline

```
Week 1 (Days 1-7)
├─ Days 1-3: Setup, Parsing, Unit Tests
├─ Days 4-6: Validation, Unit Tests
└─ Days 7: Integration start

Week 2 (Days 8-14)
├─ Days 8-10: Integration, CLI changes
├─ Days 11-12: Testing
├─ Days 13: Refinement
└─ Day 14: Final testing, user examples
```

**Total:** 2 weeks (10 working days)

---

## Files That Change

### 3 Python Files Need Modification

1. **obsidian_supernote/converters/markdown_to_pdf.py**
   - Add: `extract_frontmatter()` function
   - Add: `parse_properties()` function
   - Add: `validate_*()` functions
   - Modify: Main converter functions

2. **obsidian_supernote/converters/note_writer.py**
   - Modify: `convert_pdf_to_note()` - add property parameters
   - Modify: Metadata generation - use device property
   - Modify: Filename generation - use version property

3. **obsidian_supernote/cli.py**
   - Modify: `md_to_note()` command handler
   - Add: Frontmatter reading logic
   - Add: Property precedence logic (CLI > frontmatter > defaults)
   - Add: Output filename determination

### 3 New Test Files

1. **tests/test_frontmatter_parsing.py**
   - Test extraction, validation, defaults

2. **tests/test_frontmatter_cli_integration.py**
   - Test CLI reading and using properties

3. **tests/fixtures/** - Example markdown files with frontmatter

---

## Success Criteria

✅ **Parsing** - Extract all 6 properties from YAML
✅ **Validation** - Validate with helpful error messages
✅ **Integration** - Pass to converters correctly
✅ **Testing** - 80%+ code coverage
✅ **Documentation** - Code comments and docstrings

---

## Example: End-to-End Flow

**User creates markdown:**
```yaml
---
title: "Deep Learning Paper"
supernote_type: realtime
supernote_linked_file: "Reading/DeepLearning.note"
supernote_device: A5X2
---
# Content...
```

**User runs CLI:**
```bash
obsidian-supernote md-to-note paper.md
```

**Step 1 reads and processes:**
1. Extracts frontmatter YAML
2. Parses properties: realtime, A5X2, linked_file
3. Validates all values
4. Applies CLI overrides (none in this case)
5. Passes to converter with properties
6. CLI outputs:
   ```
   ✓ paper.md - Reading frontmatter
   ├─ supernote_type: realtime
   ├─ supernote_device: A5X2
   └─ supernote_linked_file: Reading/DeepLearning.note
   
   ✓ Updated Reading/DeepLearning.note
   ```

**Step 2-4 would then:**
- Generate PDF from markdown
- Read existing .note file
- Replace template layer
- Preserve annotation layers
- Output updated .note

---

## Cross-References

- **PLAN.md** - Overall Phase 2 implementation plan
- **FRONTMATTER_PROPERTIES.md** - Complete property specification
- **STEP1_REQUIREMENTS.md** - Implementation checklist
- **FRONTMATTER_VISUAL_GUIDE.md** - Visual reference guide
- **IMPLEMENTATION_STATUS.md** - Project status overview
- **README.md** - User documentation

---

## Next Steps After Step 1

1. ✅ Step 1: Frontmatter property parsing (THIS)
2. 🔄 Step 2: .note file update mode
3. 🔄 Step 3: Realtime recognition support
4. 🔄 Step 4: Configuration & documentation

---

## Questions?

For specific property details → **FRONTMATTER_PROPERTIES.md**
For implementation guidance → **STEP1_REQUIREMENTS.md**
For visual reference → **FRONTMATTER_VISUAL_GUIDE.md**
For overall plan → **PLAN.md**

---

**Created:** 2026-01-20
**Status:** Complete & Ready for Development
**Last Updated:** 2026-01-20

