#!/usr/bin/env python3
"""Check which golden source files are present.

This script checks for the expected golden source .note files
and reports which are present and which are missing.

Usage:
    python check_golden_sources.py
"""

from pathlib import Path

# Expected golden source files
EXPECTED_FILES = {
    "png_template": [
        "01_standard_png_blank.note",
        "02_standard_png_written.note",
        "03_realtime_png_blank.note",
        "04_realtime_png_written.note",
    ],
    "pdf_template": [
        "05_standard_pdf_blank.note",
        "06_standard_pdf_written.note",
        "07_realtime_pdf_blank.note",
        "08_realtime_pdf_written.note",
    ],
    "no_template": [
        "09_standard_none_blank.note",
        "10_standard_none_written.note",
        "11_realtime_none_written.note",
    ],
    "edge_cases": [
        "12_standard_multipage.note",
        "13_standard_multilayer.note",
    ],
}


def main():
    # Find golden_sources directory relative to this script
    script_dir = Path(__file__).parent
    golden_sources_dir = script_dir.parent / "golden_sources"

    if not golden_sources_dir.exists():
        print(f"Error: Golden sources directory not found: {golden_sources_dir}")
        return

    print("=" * 60)
    print("GOLDEN SOURCES STATUS CHECK")
    print("=" * 60)
    print()

    total_expected = 0
    total_present = 0
    total_missing = 0

    for category, files in EXPECTED_FILES.items():
        category_dir = golden_sources_dir / category
        print(f"## {category.upper().replace('_', ' ')}")
        print(f"   Directory: {category_dir}")
        print()

        category_present = 0
        category_missing = 0

        for filename in files:
            file_path = category_dir / filename
            total_expected += 1

            if file_path.exists():
                size = file_path.stat().st_size
                size_str = f"{size:,} bytes" if size < 1024 * 1024 else f"{size / 1024 / 1024:.2f} MB"
                print(f"   [OK] {filename} ({size_str})")
                category_present += 1
                total_present += 1
            else:
                print(f"   [  ] {filename} (missing)")
                category_missing += 1
                total_missing += 1

        print()
        print(f"   Status: {category_present}/{len(files)} files present")
        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Total expected: {total_expected}")
    print(f"  Present:        {total_present}")
    print(f"  Missing:        {total_missing}")
    print()

    if total_missing == 0:
        print("  STATUS: All golden source files present!")
    else:
        print(f"  STATUS: {total_missing} files still needed")
        print()
        print("  Next steps:")
        print("  1. Create missing notes on Supernote device")
        print("  2. Sync via Supernote Partner app")
        print("  3. Copy .note files to golden_sources/ directories")

    # Check templates
    print()
    print("=" * 60)
    print("TEMPLATES STATUS")
    print("=" * 60)
    templates_dir = script_dir.parent / "templates"

    templates = [
        ("blank_template_a5x2.png", "PNG template for Manta (1920x2560)"),
        ("blank_template_a5x.png", "PNG template for A5X (1404x1872)"),
        ("sample_document.pdf", "PDF template for multi-page notes"),
    ]

    for filename, description in templates:
        file_path = templates_dir / filename
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  [OK] {filename} ({size:,} bytes)")
        else:
            print(f"  [  ] {filename} (missing) - {description}")


if __name__ == "__main__":
    main()
