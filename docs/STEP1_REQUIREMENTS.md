# Step 1: Frontmatter Property Parsing - Requirements Summary

**Phase 2 Implementation Step 1**
**Effort Estimate:** 2 weeks
**Status:** Ready for development

---

## The 6 Frontmatter Properties - At a Glance

| # | Property | Type | Default | Required? | Purpose |
|---|----------|------|---------|-----------|---------|
| 1 | `supernote_type` | string | `"standard"` | No | Choose: standard (sketching) or realtime (text capture) |
| 2 | `supernote_linked_file` | string | None | No | Path to existing .note to update instead of create new |
| 3 | `supernote_device` | string | `"A5X2"` | No | Target device: A5X, A5X2, A6X, A6X2 |
| 4 | `supernote_page_size` | string | `"A5"` | No | PDF page size: A4, A5, A6, Letter |
| 5 | `supernote_realtime` | boolean | From type | No | Explicit realtime flag (overrides supernote_type) |
| 6 | `supernote_version` | integer | None | No | Version suffix when updating (creates _v2, _v3, etc.) |

---

## What Users Will Put in Their Markdown

### Example 1: Daily Notes
```yaml
---
title: "Daily Notes 2026-01-20"
supernote_type: realtime
supernote_linked_file: "Journal/2026-01-20.note"
---
```

### Example 2: Research Notes
```yaml
---
title: "Deep Learning Paper"
supernote_type: realtime
supernote_linked_file: "Reading/DeepLearning.note"
---
```

### Example 3: World Building
```yaml
---
title: "Aragorn - Character Profile"
supernote_type: standard
supernote_device: A5X2
supernote_page_size: A5
supernote_linked_file: "Characters/Aragorn.note"
supernote_version: 2
---
```

---

## What Step 1 Must Do

### Core Functionality

```
1. READ frontmatter from markdown file
   ↓
2. EXTRACT properties (6 total)
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
# Result: {"supernote_type": "realtime", "supernote_linked_file": "..."}

# 3. Parse and validate properties
properties = parse_properties(frontmatter)
# Result: validated dict with defaults applied

# 4. Pass to converter
convert_markdown_to_note(
    "article.md",
    "article.note",
    note_type=properties.get("supernote_type", "standard"),
    update_existing=properties.get("supernote_linked_file"),
    device=properties.get("supernote_device", "A5X2"),
    page_size=properties.get("supernote_page_size", "A5"),
    realtime=properties.get("supernote_realtime"),
    version=properties.get("supernote_version"),
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
    # Validates supernote_type: "standard" or "realtime"
    # Validates supernote_device: A5X, A5X2, A6X, A6X2
    # Validates supernote_page_size: A4, A5, A6, Letter
    # Validates supernote_realtime: boolean
    # Validates supernote_version: positive integer
    # Applies defaults for missing properties
    # Returns validated dict

def get_property_with_default(properties: dict, key: str, default: any) -> any:
    """Get property with type-safe default."""
    # Handles missing properties gracefully
    # Logs what's being used
```

**Modify:**
- `convert_markdown_to_pdf()` - Accept properties as parameter
- `markdown_to_pdf()` - Read frontmatter, parse properties, pass to converter

---

### 2. `obsidian_supernote/converters/note_writer.py`

**Modify existing functions to accept:**

```python
def convert_pdf_to_note(
    pdf_path: str,
    output_path: str,
    device: str = "A5X2",           # NEW - from supernote_device
    note_type: str = "standard",    # NEW - from supernote_type
    realtime: bool = None,          # NEW - from supernote_realtime
    version: int = None,            # NEW - from supernote_version
    update_existing: str = None,    # NEW - from supernote_linked_file
    preserve_annotations: bool = True,
    preserve_layers: bool = True,
) -> None:
    """Convert PDF to .note with property support."""

    # Use device for resolution/metadata
    # Use note_type for recognition flag
    # Use realtime to override note_type
    # Use update_existing to trigger update mode
    # Use version to append to filename
```

---

### 3. `obsidian_supernote/cli.py`

**Modify command handlers:**

```python
@cli.command()
@click.argument('input_md', type=click.Path(exists=True))
@click.argument('output_note', type=click.Path(), required=False)
@click.option('--device', default=None, help='Override device: A5X, A5X2, A6X, A6X2')
@click.option('--page-size', default=None, help='Override page size: A4, A5, A6, Letter')
@click.option('--type', default=None, help='Override type: standard, realtime')
def md_to_note(input_md, output_note, device, page_size, type):
    """Convert markdown to .note (reads frontmatter properties)."""

    # 1. Read markdown file
    with open(input_md) as f:
        content = f.read()

    # 2. Extract and parse properties from frontmatter
    properties = extract_and_parse_frontmatter(content)

    # 3. CLI arguments OVERRIDE frontmatter if specified
    if device:
        properties['supernote_device'] = device
    if page_size:
        properties['supernote_page_size'] = page_size
    if type:
        properties['supernote_type'] = type

    # 4. Determine output filename
    output = output_note or determine_output_filename(
        input_md,
        properties.get('supernote_linked_file'),
        properties.get('supernote_version'),
    )

    # 5. Call converter with all properties
    convert_markdown_to_note(input_md, output, **properties)

    click.echo(f"✓ Converted to {output}")
    click.echo(f"  Device: {properties['supernote_device']}")
    click.echo(f"  Type: {properties['supernote_type']}")
    click.echo(f"  Realtime: {properties.get('supernote_realtime', False)}")
```

---

## Implementation Checklist

### Phase 1: Setup & Parsing (Days 1-3)

- [ ] Create `FRONTMATTER_PROPERTIES.md` (specification) ✅ DONE
- [ ] Create unit test file: `tests/test_frontmatter_parsing.py`
- [ ] Create test fixtures with example markdown files
- [ ] Implement `extract_frontmatter()` function
  - [ ] Parse YAML between `---` delimiters
  - [ ] Handle missing/empty frontmatter
  - [ ] Return dict of properties
- [ ] Write tests for extraction

### Phase 2: Validation (Days 4-6)

- [ ] Implement `parse_properties()` function
- [ ] Add validators for each property:
  - [ ] `validate_supernote_type()` - must be "standard" or "realtime"
  - [ ] `validate_supernote_device()` - must be A5X, A5X2, A6X, A6X2
  - [ ] `validate_supernote_page_size()` - must be A4, A5, A6, Letter
  - [ ] `validate_supernote_realtime()` - must be boolean
  - [ ] `validate_supernote_version()` - must be positive integer
  - [ ] `validate_supernote_linked_file()` - must be valid path
- [ ] Handle invalid values (log warning, use default)
- [ ] Write tests for validation

### Phase 3: Integration (Days 7-10)

- [ ] Modify `markdown_to_pdf.py`:
  - [ ] Add property extraction to converter
  - [ ] Pass properties to PDF generation
- [ ] Modify `note_writer.py`:
  - [ ] Add device parameter
  - [ ] Add note_type parameter
  - [ ] Add realtime parameter
  - [ ] Add version parameter
  - [ ] Add update_existing parameter
- [ ] Modify `cli.py`:
  - [ ] Read frontmatter in command handlers
  - [ ] Parse properties
  - [ ] Apply CLI overrides
  - [ ] Determine output filename with versioning
  - [ ] Pass to converters
- [ ] Write integration tests

### Phase 4: Testing & Refinement (Days 11-14)

- [ ] Test with workflow examples:
  - [ ] Daily Notes example
  - [ ] Research Notes example
  - [ ] World Building example
- [ ] Test property precedence:
  - [ ] Frontmatter overrides defaults
  - [ ] CLI overrides frontmatter
  - [ ] Invalid values handled gracefully
- [ ] Test edge cases:
  - [ ] Missing frontmatter (use all defaults)
  - [ ] Empty frontmatter
  - [ ] Partial properties (some specified, some default)
  - [ ] Invalid device name
  - [ ] Non-existent linked file
  - [ ] Negative version number
- [ ] User testing:
  - [ ] Create example markdown files for each workflow
  - [ ] Run conversions
  - [ ] Verify properties are respected
  - [ ] Test on device

---

## Unit Tests Required

### Test: Property Extraction

```python
def test_extract_frontmatter_basic():
    """Extract simple frontmatter."""
    content = """---
title: Test
supernote_type: realtime
---
Body"""
    result = extract_frontmatter(content)
    assert result['title'] == 'Test'
    assert result['supernote_type'] == 'realtime'

def test_extract_frontmatter_no_frontmatter():
    """Handle markdown without frontmatter."""
    content = "# Just content\nNo frontmatter here"
    result = extract_frontmatter(content)
    assert result == {}

def test_extract_frontmatter_multiple_lines():
    """Extract multi-line properties."""
    content = """---
supernote_linked_file: "Path/To/File.note"
supernote_version: 2
---
"""
    result = extract_frontmatter(content)
    assert result['supernote_linked_file'] == "Path/To/File.note"
    assert result['supernote_version'] == 2
```

### Test: Property Validation

```python
def test_validate_supernote_type_valid():
    """Accept valid types."""
    assert validate_supernote_type("standard") == "standard"
    assert validate_supernote_type("realtime") == "realtime"

def test_validate_supernote_type_invalid():
    """Reject invalid types."""
    with pytest.raises(ValueError):
        validate_supernote_type("recognition")

def test_validate_supernote_type_default():
    """Use default for missing."""
    assert validate_supernote_type(None) == "standard"

def test_validate_supernote_device_valid():
    """Accept valid devices."""
    for device in ["A5X", "A5X2", "A6X", "A6X2"]:
        assert validate_supernote_device(device) == device

def test_validate_supernote_device_invalid():
    """Reject invalid devices."""
    with pytest.raises(ValueError):
        validate_supernote_device("A5")

def test_parse_properties_all_valid():
    """Parse complete valid properties."""
    properties = {
        "supernote_type": "realtime",
        "supernote_device": "A5X2",
        "supernote_page_size": "A5",
        "supernote_linked_file": "Path/To/File.note",
        "supernote_realtime": True,
        "supernote_version": 2,
    }
    result = parse_properties(properties)
    assert result["supernote_type"] == "realtime"
    assert result["supernote_device"] == "A5X2"
    # ... etc
```

### Test: CLI Integration

```python
def test_cli_reads_frontmatter():
    """CLI reads and uses frontmatter properties."""
    # Create temp markdown with frontmatter
    temp_md = """---
supernote_type: realtime
supernote_device: A6X2
---
# Content
"""
    # Run CLI command
    # Verify it used realtime and A6X2
    # Verify output note reflects these properties

def test_cli_overrides_frontmatter():
    """CLI flags override frontmatter."""
    # Create markdown with supernote_device: A5X2
    # Run: cli.md_to_note(file, device="A6X")
    # Verify it used A6X (CLI override)

def test_cli_uses_defaults():
    """CLI uses defaults for missing properties."""
    # Create markdown with no supernote properties
    # Run: cli.md_to_note(file)
    # Verify defaults: standard, A5X2, A5 page size
```

---

## Success Criteria for Step 1

✅ **Parsing:**
- [x] Extract frontmatter YAML from markdown
- [x] Handle missing/empty frontmatter gracefully
- [x] Extract all 6 properties (if present)

✅ **Validation:**
- [x] Validate supernote_type values
- [x] Validate supernote_device values
- [x] Validate supernote_page_size values
- [x] Validate supernote_realtime boolean
- [x] Validate supernote_version integer
- [x] Log helpful warnings for invalid values
- [x] Use defaults for missing properties

✅ **Integration:**
- [x] CLI reads frontmatter automatically
- [x] Properties override defaults
- [x] CLI flags override frontmatter
- [x] Pass properties to converters
- [x] Output filename respects version property

✅ **Testing:**
- [x] 80%+ coverage of parsing code
- [x] Test all 6 properties
- [x] Test valid and invalid values
- [x] Test defaults
- [x] Test precedence (defaults < frontmatter < CLI)
- [x] Integration test with real markdown files

✅ **Documentation:**
- [x] Properties documented in FRONTMATTER_PROPERTIES.md ✅ DONE
- [x] Examples for each workflow ✅ DONE
- [x] Code comments explaining logic
- [x] User guide in README

---

## Example: End-to-End Step 1 Flow

### User creates markdown with frontmatter:
```yaml
---
title: "Deep Learning Paper"
supernote_type: realtime
supernote_linked_file: "Reading/DeepLearning.note"
supernote_device: A5X2
supernote_page_size: A5
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
   - supernote_type: "realtime" ✓
   - supernote_linked_file: "Reading/DeepLearning.note" ✓
   - supernote_device: "A5X2" ✓
   - supernote_page_size: "A5" ✓
   - supernote_realtime: (default from type = True)
   - supernote_version: (default = None)
4. Logs:
   ```
   ✓ Paper.md - reading frontmatter properties
   ├─ supernote_type: realtime
   ├─ supernote_device: A5X2
   ├─ supernote_page_size: A5
   ├─ supernote_linked_file: Reading/DeepLearning.note
   ├─ supernote_realtime: true (from type)
   └─ supernote_version: none (create new)
   ```
5. Calls converter:
   ```python
   convert_markdown_to_note(
       "paper.md",
       "paper.note",
       note_type="realtime",
       device="A5X2",
       page_size="A5",
       update_existing="Reading/DeepLearning.note",
       realtime=True,
       version=None,
   )
   ```

### Result:
- Reads existing "Reading/DeepLearning.note"
- Generates new PDF from markdown
- Replaces template layer
- Preserves annotation layers
- Enables realtime character recognition
- Outputs to "Reading/DeepLearning.note" (updated)

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
- ✅ [FRONTMATTER_PROPERTIES.md](./FRONTMATTER_PROPERTIES.md) - Complete property specification
- ✅ [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md) - Current project status
- 📋 README.md - User documentation (will update after Step 1)

---

## Next Steps After Step 1

After Step 1 is complete and tested:
1. Move to Step 2: .note File Update Mode
2. Reuse frontmatter parsing from Step 1
3. Use supernote_linked_file and supernote_version

---

## Summary

**Step 1 delivers:**
- ✅ Frontmatter property parsing (6 properties)
- ✅ Property validation with defaults
- ✅ Integration with CLI and converters
- ✅ Foundation for Steps 2-4

**Effort:** 2 weeks (10 working days)
**Complexity:** Medium (parsing + validation + integration)
**Risk:** Low (self-contained, well-specified)

---

Created: 2026-01-20
Status: Ready for development

