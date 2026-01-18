#!/usr/bin/env python3
"""Dump complete structure of a Supernote .note file.

This script analyzes a .note file and outputs its complete structure,
including header, footer, page metadata, and layer information.

Usage:
    python dump_structure.py <note_file> [--output <file>] [--json]

Examples:
    python dump_structure.py golden_sources/png_template/01_standard_png_blank.note
    python dump_structure.py my_note.note --json > structure.json
    python dump_structure.py my_note.note --output analysis.txt
"""

import argparse
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any


def read_uint32_le(data: bytes, offset: int) -> int:
    """Read a little-endian uint32 from data at offset."""
    return struct.unpack("<I", data[offset : offset + 4])[0]


def parse_tags(content: str) -> dict[str, str]:
    """Parse <KEY:VALUE> tags into a dictionary."""
    tags = {}
    pattern = r"<([^:>]+):([^>]*)>"
    for match in re.finditer(pattern, content):
        key, value = match.groups()
        tags[key] = value
    return tags


def analyze_note_file(file_path: Path) -> dict[str, Any]:
    """Analyze a .note file and return its structure."""
    with open(file_path, "rb") as f:
        data = f.read()

    result = {
        "file": str(file_path),
        "size": len(data),
        "filetype": None,
        "signature": None,
        "header": {},
        "footer": {},
        "pages": [],
        "raw_sections": {},
    }

    # File type (bytes 0-3)
    result["filetype"] = data[0:4].decode("utf-8", errors="replace")

    # Signature (bytes 4-23)
    result["signature"] = data[4:24].decode("utf-8", errors="replace")

    # Footer address (last 4 bytes)
    footer_addr = read_uint32_le(data, len(data) - 4)
    result["footer_address"] = footer_addr

    # Read footer block
    footer_len = read_uint32_le(data, footer_addr)
    footer_content = data[footer_addr + 4 : footer_addr + 4 + footer_len].decode(
        "utf-8", errors="replace"
    )
    result["footer"]["length"] = footer_len
    result["footer"]["raw"] = footer_content
    result["footer"]["tags"] = parse_tags(footer_content)

    # Read header block (at offset 24)
    header_addr = 24
    header_len = read_uint32_le(data, header_addr)
    header_content = data[header_addr + 4 : header_addr + 4 + header_len].decode(
        "utf-8", errors="replace"
    )
    result["header"]["address"] = header_addr
    result["header"]["length"] = header_len
    result["header"]["raw"] = header_content
    result["header"]["tags"] = parse_tags(header_content)

    # Find and parse page metadata blocks
    page_num = 1
    while True:
        page_key = f"PAGE{page_num}"
        if page_key not in result["footer"]["tags"]:
            break

        page_addr = int(result["footer"]["tags"][page_key])
        page_len = read_uint32_le(data, page_addr)
        page_content = data[page_addr + 4 : page_addr + 4 + page_len].decode(
            "utf-8", errors="replace"
        )
        page_tags = parse_tags(page_content)

        page_info = {
            "number": page_num,
            "address": page_addr,
            "length": page_len,
            "raw": page_content,
            "tags": page_tags,
            "layers": [],
        }

        # Parse layer metadata for this page
        layer_names = ["MAINLAYER", "LAYER1", "LAYER2", "LAYER3", "BGLAYER"]
        for layer_name in layer_names:
            if layer_name in page_tags:
                layer_addr = int(page_tags[layer_name])
                if layer_addr > 0 and layer_addr < len(data) - 4:
                    try:
                        layer_len = read_uint32_le(data, layer_addr)
                        if layer_len > 0 and layer_len < 10000:  # Sanity check
                            layer_content = data[
                                layer_addr + 4 : layer_addr + 4 + layer_len
                            ].decode("utf-8", errors="replace")
                            layer_tags = parse_tags(layer_content)
                            page_info["layers"].append(
                                {
                                    "name": layer_name,
                                    "address": layer_addr,
                                    "length": layer_len,
                                    "raw": layer_content,
                                    "tags": layer_tags,
                                }
                            )
                    except (struct.error, UnicodeDecodeError):
                        page_info["layers"].append(
                            {
                                "name": layer_name,
                                "address": layer_addr,
                                "error": "Failed to parse",
                            }
                        )

        result["pages"].append(page_info)
        page_num += 1

    # Check for STYLE entries
    style_entries = {}
    for key, value in result["footer"]["tags"].items():
        if key.startswith("STYLE_"):
            style_entries[key] = value
    result["footer"]["style_entries"] = style_entries

    return result


def format_output(result: dict[str, Any], as_json: bool = False) -> str:
    """Format the analysis result for output."""
    if as_json:
        return json.dumps(result, indent=2, ensure_ascii=False)

    lines = []
    lines.append("=" * 80)
    lines.append(f"FILE ANALYSIS: {result['file']}")
    lines.append("=" * 80)
    lines.append("")

    # Basic info
    lines.append("## BASIC INFO")
    lines.append(f"  Size: {result['size']:,} bytes")
    lines.append(f"  Filetype: {result['filetype']}")
    lines.append(f"  Signature: {result['signature']}")
    lines.append(f"  Footer address: {result['footer_address']}")
    lines.append("")

    # Header
    lines.append("## HEADER")
    lines.append(f"  Address: {result['header']['address']}")
    lines.append(f"  Length: {result['header']['length']} bytes")
    lines.append("  Tags:")
    for key, value in sorted(result["header"]["tags"].items()):
        # Truncate long values
        display_value = value if len(value) < 60 else value[:57] + "..."
        lines.append(f"    {key}: {display_value}")
    lines.append("")

    # Footer
    lines.append("## FOOTER")
    lines.append(f"  Length: {result['footer']['length']} bytes")
    lines.append("  Tags:")
    for key, value in sorted(result["footer"]["tags"].items()):
        if not key.startswith("STYLE_"):  # Show STYLE entries separately
            lines.append(f"    {key}: {value}")
    lines.append("")

    # STYLE entries
    if result["footer"]["style_entries"]:
        lines.append("## STYLE ENTRIES")
        for key, value in sorted(result["footer"]["style_entries"].items()):
            lines.append(f"    {key}: {value}")
        lines.append("")

    # Pages
    lines.append(f"## PAGES ({len(result['pages'])} total)")
    for page in result["pages"]:
        lines.append(f"\n  ### Page {page['number']}")
        lines.append(f"    Address: {page['address']}")
        lines.append(f"    Length: {page['length']} bytes")
        lines.append("    Tags:")
        for key, value in sorted(page["tags"].items()):
            if key not in ["MAINLAYER", "LAYER1", "LAYER2", "LAYER3", "BGLAYER"]:
                display_value = value if len(value) < 50 else value[:47] + "..."
                lines.append(f"      {key}: {display_value}")

        lines.append("    Layers:")
        for layer in page["layers"]:
            if "error" in layer:
                lines.append(f"      {layer['name']}: {layer['error']}")
            else:
                lines.append(
                    f"      {layer['name']}: addr={layer['address']}, len={layer['length']}"
                )
                for lkey, lvalue in layer["tags"].items():
                    lines.append(f"        {lkey}: {lvalue}")
    lines.append("")

    # Raw footer content (useful for debugging)
    lines.append("## RAW FOOTER CONTENT")
    raw_footer = result["footer"]["raw"]
    # Split on tag boundaries for readability
    formatted = raw_footer.replace("><", ">\n<")
    for line in formatted.split("\n"):
        lines.append(f"  {line}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Dump complete structure of a Supernote .note file"
    )
    parser.add_argument("note_file", type=Path, help="Path to .note file")
    parser.add_argument("--output", "-o", type=Path, help="Output file (default: stdout)")
    parser.add_argument(
        "--json", "-j", action="store_true", help="Output as JSON"
    )

    args = parser.parse_args()

    if not args.note_file.exists():
        print(f"Error: File not found: {args.note_file}", file=sys.stderr)
        sys.exit(1)

    try:
        result = analyze_note_file(args.note_file)
        output = format_output(result, as_json=args.json)

        if args.output:
            args.output.write_text(output, encoding="utf-8")
            print(f"Output written to: {args.output}")
        else:
            print(output)

    except Exception as e:
        print(f"Error analyzing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
