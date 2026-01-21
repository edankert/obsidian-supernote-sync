# Step 1: Frontmatter Property Parsing - Requirements Summary

**Phase 2 Implementation Step 1**
**Effort Estimate:** 1 week (5 working days) — simplified from 2 weeks with reduced properties
**Status:** Ready for development

---

## The 2 Frontmatter Properties - At a Glance

| # | Property | Type | Default | Required? | Purpose |
|---|----------|------|---------|-----------|---------|
| 1 | `supernote.type` | string | `"standard"` | No | Choose: standard (sketching) or realtime (text capture) |
| 2 | `supernote.file` | string | None | No (uncertain) | Path to existing .note to update instead of create new |

**Architectural Note:** Device type, page size, and versioning are **sync software configuration**, not note properties. Notes should be generic and device-agnostic.

---

## What Users Will Put in Their Markdown

### Example 1: Daily Notes (Realtime + Update)
```yaml
---
title: "Daily Notes 2026-01-20"
supernote.type: realtime
supernote.file: "Journal/2026-01-20.note"
---
```

### Example 2: Research Notes (Realtime + Update)
```yaml
---
title: "Deep Learning Paper"
supernote.type: realtime
supernote.file: "Reading/DeepLearning.note"
---
```

### Example 3: World Building (Standard, Optional Update)
```yaml
---
title: "Aragorn - Character Profile"
supernote.type: standard
supernote.file: "Characters/Aragorn.note"
---
```

### Example 4: Minimal (Uses Defaults)
```yaml
---
title: "My Note"
---
```

---

## What Step 1 Must Do

### Core Functionality

```
1. READ frontmatter from markdown file
   ↓
2. EXTRACT properties (2 total: type, file)
   ↓
3. VALIDATE each property
   ↓
4. APPLY defaults for missing properties
   ↓
5. PASS to converter functions
   ↓
6. LOG what's being used
```

### In Code Terms

```python
# 1. Read markdown file
with open("article.md") as f:
    content = f.read()

# 2. Extract frontmatter YAML
frontmatter = extract_frontmatter(content)
# Result: {"supernote.type": "realtime", "supernote.file": "..."}

# 3. Parse and validate properties
properties = parse_properties(frontmatter)
# Result: validated dict with defaults applied

# 4. Pass to converter
convert_markdown_to_note(
    "article.md",
    "article.note",
    note_type=properties.get("supernote.type", "standard"),
    update_file=properties.get("supernote.file"),
)
```

---

## Files That Need Changes

### 1. `obsidian_supernote/converters/markdown_to_pdf.py`

**Add these functions:**

```python
def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    # Reads between --- delimiters
    # Returns dict of properties

def parse_properties(frontmatter: dict) -> dict:
    """Parse and validate frontmatter properties."""
    # Validates supernote.type: "standard" or "realtime"
    # Validates supernote.file: path to .note (if specified)
    # Applies defaults for missing properties
    # Returns validated dict
```

**Modify:**
- `markdown_to_pdf()` - Read frontmatter, parse properties, pass to converter

---

### 2. `obsidian_supernote/converters/note_writer.py`

**Modify existing function to accept:**

```python
def convert_pdf_to_note(
    pdf_path: str,
    output_path: str,
    note_type: str = "standard",      # NEW - from supernote.type
    update_file: str = None,          # NEW - from supernote.file
) -> None:
    """Convert PDF to .note with property support."""
    # Use note_type for recognition flag
    # Use update_file to trigger update mode
```

---

### 3. `obsidian_supernote/cli.py`

**Modify command handlers:**

```python
@cli.command()
@click.argument('input_md', type=click.Path(exists=True))
@click.argument('output_note', type=click.Path(), required=False)
@click.option('--type', default=None, help='Override type: standard, realtime')
def md_to_note(input_md, output_note, type):
    """Convert markdown to .note (reads frontmatter properties)."""

    # 1. Read markdown file
    with open(input_md) as f:
        content = f.read()

    # 2. Extract and parse properties from frontmatter
    properties = extract_and_parse_frontmatter(content)

    # 3. CLI arguments OVERRIDE frontmatter if specified
    if type:
        properties['supernote.type'] = type

    # 4. Call converter with properties
    convert_markdown_to_note(input_md, output_note, **properties)

    click.echo(f"✓ Converted to {output_note}")
    click.echo(f"  Type: {properties['supernote.type']}")
```

---

## Implementation Checklist

### Phase 1: Setup & Parsing (Days 1-2)

- [ ] Create unit test file: `tests/test_frontmatter_parsing.py`
- [ ] Create test fixtures with example markdown files
- [ ] Implement `extract_frontmatter()` function
  - [ ] Parse YAML between `---` delimiters
  - [ ] Handle missing/empty frontmatter
  - [ ] Return dict of properties
- [ ] Write tests for extraction

### Phase 2: Validation (Days 3-4)

- [ ] Implement `parse_properties()` function
- [ ] Add validators:
  - [ ] `validate_supernote_type()` - must be "standard" or "realtime"
  - [ ] `validate_supernote_file()` - must be valid path (if specified)
- [ ] Handle invalid values (log warning, use default)
- [ ] Write tests for validation

### Phase 3: Integration (Days 5-6)

- [ ] Modify `markdown_to_pdf.py`:
  - [ ] Add property extraction to converter
  - [ ] Pass properties to PDF generation
- [ ] Modify `note_writer.py`:
  - [ ] Add note_type parameter
  - [ ] Add update_file parameter
- [ ] Modify `cli.py`:
  - [ ] Read frontmatter in command handlers
  - [ ] Parse properties
  - [ ] Apply CLI overrides
  - [ ] Pass to converters
- [ ] Write integration tests

### Phase 4: Testing & Refinement (Days 7-10)

- [ ] Test with workflow examples:
  - [ ] Daily Notes example
  - [ ] Research Notes example
  - [ ] World Building example
- [ ] Test property validation:
  - [ ] Valid values accepted
  - [ ] Invalid values handled gracefully
  - [ ] Defaults applied
- [ ] Test edge cases:
  - [ ] Missing frontmatter (use all defaults)
  - [ ] Empty frontmatter
  - [ ] Partial properties (some specified, some default)
  - [ ] Invalid type value
  - [ ] Non-existent file path
- [ ] User testing:
  - [ ] Create example markdown files for each workflow
  - [ ] Run conversions
  - [ ] Verify properties are respected

---

## Unit Tests Required

### Test: Property Extraction

```python
def test_extract_frontmatter_basic():
    """Extract simple frontmatter."""
    content = """---
title: Test
supernote.type: realtime
---
Body"""
    result = extract_frontmatter(content)
    assert result['title'] == 'Test'
    assert result['supernote.type'] == 'realtime'

def test_extract_frontmatter_no_frontmatter():
    """Handle markdown without frontmatter."""
    content = "# Just content\nNo frontmatter here"
    result = extract_frontmatter(content)
    assert result == {}

def test_extract_frontmatter_with_file():
    """Extract file property."""
    content = """---
supernote.file: "Path/To/File.note"
---
"""
    result = extract_frontmatter(content)
    assert result['supernote.file'] == "Path/To/File.note"
```

### Test: Property Validation

```python
def test_validate_type_valid():
    """Accept valid types."""
    assert validate_type("standard") == "standard"
    assert validate_type("realtime") == "realtime"

def test_validate_type_invalid():
    """Reject invalid types."""
    with pytest.raises(ValueError):
        validate_type("recognition")

def test_validate_type_default():
    """Use default for missing."""
    assert validate_type(None) == "standard"

def test_parse_properties_minimal():
    """Parse minimal valid properties."""
    properties = {"supernote.type": "realtime"}
    result = parse_properties(properties)
    assert result["supernote.type"] == "realtime"
    assert result.get("supernote.file") is None

def test_parse_properties_all_valid():
    """Parse complete valid properties."""
    properties = {
        "supernote.type": "standard",
        "supernote.file": "Path/To/File.note",
    }
    result = parse_properties(properties)
    assert result["supernote.type"] == "standard"
    assert result["supernote.file"] == "Path/To/File.note"
```

### Test: CLI Integration

```python
def test_cli_reads_frontmatter():
    """CLI reads and uses frontmatter properties."""
    # Create temp markdown with frontmatter
    temp_md = """---
supernote.type: realtime
supernote.file: "Test.note"
---
# Content
"""
    # Run CLI command
    # Verify it used realtime and file path

def test_cli_uses_defaults():
    """CLI uses defaults for missing properties."""
    # Create markdown with no supernote properties
    # Run: cli.md_to_note(file)
    # Verify defaults: standard type, no file
```

---

## Success Criteria for Step 1

✅ **Parsing:**
- [ ] Extract frontmatter YAML from markdown
- [ ] Handle missing/empty frontmatter gracefully
- [ ] Extract both properties (if present)

✅ **Validation:**
- [ ] Validate supernote.type values
- [ ] Validate supernote.file values (if specified)
- [ ] Log helpful warnings for invalid values
- [ ] Use defaults for missing properties

✅ **Integration:**
- [ ] CLI reads frontmatter automatically
- [ ] Properties override defaults
- [ ] CLI flags override frontmatter
- [ ] Pass properties to converters

✅ **Testing:**
- [ ] 80%+ coverage of parsing code
- [ ] Test both properties
- [ ] Test valid and invalid values
- [ ] Test defaults
- [ ] Integration test with real markdown files

✅ **Documentation:**
- [ ] Properties documented in FRONTMATTER_PROPERTIES.md
- [ ] Examples for each workflow
- [ ] Code comments explaining logic

---

## Example: End-to-End Step 1 Flow

### User creates markdown with frontmatter:
```yaml
---
title: "Deep Learning Paper"
supernote.type: realtime
supernote.file: "Reading/DeepLearning.note"
---

# Abstract
...
```

### User runs CLI:
```bash
obsidian-supernote md-to-note "paper.md"
```

### Step 1 Code:
1. Reads `paper.md`
2. Extracts frontmatter YAML
3. Parses and validates:
   - supernote.type: "realtime" ✓
   - supernote.file: "Reading/DeepLearning.note" ✓
4. Logs:
   ```
   ✓ Paper.md - reading frontmatter properties
   ├─ supernote.type: realtime
   └─ supernote.file: Reading/DeepLearning.note
   ```
5. Calls converter:
   ```python
   convert_markdown_to_note(
       "paper.md",
       "paper.note",
       note_type="realtime",
       update_file="Reading/DeepLearning.note",
   )
   ```

### Result:
- Reads existing "Reading/DeepLearning.note"
- Generates new PDF from markdown
- Replaces template layer
- Preserves annotation layers
- Enables realtime character recognition
- Outputs to "Reading/DeepLearning.note" (updated)

**Note:** Device type, page size, and versioning are configured in sync software, not here.

---

## Dependencies

### Existing:
- PyYAML (for YAML parsing) - already in requirements.txt
- Click (for CLI) - already in requirements.txt
- Python 3.10+ - already required

### Need to Check:
- [ ] PyYAML version supports reading frontmatter
- [ ] All imports available

---

## Reference Documents

- ✅ [PLAN.md](../PLAN.md) - Overall implementation plan
- ✅ [FRONTMATTER_PROPERTIES.md](./FRONTMATTER_PROPERTIES.md) - Complete property specification (2 properties)
- 📋 README.md - User documentation (will update after Step 1)

---

## Next Steps After Step 1

After Step 1 is complete and tested:
1. Implement sync software configuration for device/page_size/versioning
2. Build .note update mode (using supernote.file)
3. Integrate with cloud sync workflow

---

## Summary

**Step 1 delivers (Simplified):**
- ✅ Frontmatter property parsing (2 content-level properties)
- ✅ Property validation with defaults
- ✅ Integration with CLI and converters
- ✅ Foundation for downstream features

**Effort:** 1 week (5 working days) — significantly simplified with only 2 properties
**Complexity:** Low (straightforward parsing + validation)
**Risk:** Very low (self-contained, well-specified)

**Separation of Concerns:**
- **Note properties:** What type of note (standard/realtime), optional linked file
- **Sync software:** Device type, page size, versioning strategy, cloud sync settings

---

Created: 2026-01-20 (Updated: 2026-01-20)
Status: Ready for development

