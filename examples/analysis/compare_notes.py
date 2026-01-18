#!/usr/bin/env python3
"""Compare two Supernote .note files and highlight differences.

This script analyzes two .note files and shows what's different between them,
which is useful for understanding how different note types vary.

Usage:
    python compare_notes.py <file1> <file2> [--json] [--brief]

Examples:
    python compare_notes.py standard.note realtime.note
    python compare_notes.py file1.note file2.note --brief
    python compare_notes.py file1.note file2.note --json > diff.json
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


def extract_note_info(file_path: Path) -> dict[str, Any]:
    """Extract key information from a .note file."""
    with open(file_path, "rb") as f:
        data = f.read()

    result = {
        "file": str(file_path.name),
        "size": len(data),
        "filetype": data[0:4].decode("utf-8", errors="replace"),
        "signature": data[4:24].decode("utf-8", errors="replace"),
        "header_tags": {},
        "footer_tags": {},
        "page_count": 0,
        "pages": [],
    }

    # Footer address and content
    footer_addr = read_uint32_le(data, len(data) - 4)
    footer_len = read_uint32_le(data, footer_addr)
    footer_content = data[footer_addr + 4 : footer_addr + 4 + footer_len].decode(
        "utf-8", errors="replace"
    )
    result["footer_tags"] = parse_tags(footer_content)

    # Header content
    header_len = read_uint32_le(data, 24)
    header_content = data[28 : 28 + header_len].decode("utf-8", errors="replace")
    result["header_tags"] = parse_tags(header_content)

    # Count pages and extract page info
    page_num = 1
    while f"PAGE{page_num}" in result["footer_tags"]:
        page_addr = int(result["footer_tags"][f"PAGE{page_num}"])
        page_len = read_uint32_le(data, page_addr)
        page_content = data[page_addr + 4 : page_addr + 4 + page_len].decode(
            "utf-8", errors="replace"
        )
        page_tags = parse_tags(page_content)

        # Get layer info
        layers = {}
        for layer_name in ["MAINLAYER", "LAYER1", "LAYER2", "LAYER3", "BGLAYER"]:
            if layer_name in page_tags:
                layer_addr = int(page_tags[layer_name])
                if layer_addr > 0 and layer_addr < len(data) - 4:
                    try:
                        layer_len = read_uint32_le(data, layer_addr)
                        if layer_len > 0 and layer_len < 10000:
                            layer_content = data[
                                layer_addr + 4 : layer_addr + 4 + layer_len
                            ].decode("utf-8", errors="replace")
                            layers[layer_name] = parse_tags(layer_content)
                    except (struct.error, UnicodeDecodeError):
                        pass

        result["pages"].append(
            {
                "number": page_num,
                "tags": page_tags,
                "layers": layers,
            }
        )
        page_num += 1

    result["page_count"] = page_num - 1
    return result


def compare_dicts(
    dict1: dict, dict2: dict, name: str
) -> list[dict[str, Any]]:
    """Compare two dictionaries and return differences."""
    diffs = []
    all_keys = set(dict1.keys()) | set(dict2.keys())

    for key in sorted(all_keys):
        val1 = dict1.get(key)
        val2 = dict2.get(key)

        if val1 is None:
            diffs.append(
                {
                    "type": "added",
                    "section": name,
                    "key": key,
                    "file1": None,
                    "file2": val2,
                }
            )
        elif val2 is None:
            diffs.append(
                {
                    "type": "removed",
                    "section": name,
                    "key": key,
                    "file1": val1,
                    "file2": None,
                }
            )
        elif val1 != val2:
            diffs.append(
                {
                    "type": "changed",
                    "section": name,
                    "key": key,
                    "file1": val1,
                    "file2": val2,
                }
            )

    return diffs


def compare_notes(file1: Path, file2: Path) -> dict[str, Any]:
    """Compare two .note files and return differences."""
    info1 = extract_note_info(file1)
    info2 = extract_note_info(file2)

    result = {
        "file1": info1["file"],
        "file2": info2["file"],
        "summary": {},
        "differences": [],
    }

    # Basic info comparison
    if info1["size"] != info2["size"]:
        result["summary"]["size"] = {"file1": info1["size"], "file2": info2["size"]}
    if info1["signature"] != info2["signature"]:
        result["summary"]["signature"] = {
            "file1": info1["signature"],
            "file2": info2["signature"],
        }
    if info1["page_count"] != info2["page_count"]:
        result["summary"]["page_count"] = {
            "file1": info1["page_count"],
            "file2": info2["page_count"],
        }

    # Compare headers
    header_diffs = compare_dicts(info1["header_tags"], info2["header_tags"], "header")
    result["differences"].extend(header_diffs)

    # Compare footers (excluding PAGE addresses which will always differ)
    footer1 = {k: v for k, v in info1["footer_tags"].items() if not k.startswith("PAGE")}
    footer2 = {k: v for k, v in info2["footer_tags"].items() if not k.startswith("PAGE")}
    footer_diffs = compare_dicts(footer1, footer2, "footer")
    result["differences"].extend(footer_diffs)

    # Compare first page (if both have at least one page)
    if info1["pages"] and info2["pages"]:
        # Compare page tags (excluding layer addresses)
        page1_tags = {
            k: v
            for k, v in info1["pages"][0]["tags"].items()
            if k not in ["MAINLAYER", "LAYER1", "LAYER2", "LAYER3", "BGLAYER", "PAGEID"]
        }
        page2_tags = {
            k: v
            for k, v in info2["pages"][0]["tags"].items()
            if k not in ["MAINLAYER", "LAYER1", "LAYER2", "LAYER3", "BGLAYER", "PAGEID"]
        }
        page_diffs = compare_dicts(page1_tags, page2_tags, "page1")
        result["differences"].extend(page_diffs)

        # Compare layer structure
        layers1 = set(info1["pages"][0]["layers"].keys())
        layers2 = set(info2["pages"][0]["layers"].keys())
        if layers1 != layers2:
            result["summary"]["layers"] = {
                "file1": sorted(layers1),
                "file2": sorted(layers2),
            }

        # Compare layer tags for common layers
        for layer_name in layers1 & layers2:
            layer1_tags = info1["pages"][0]["layers"][layer_name]
            layer2_tags = info2["pages"][0]["layers"][layer_name]
            layer_diffs = compare_dicts(
                layer1_tags, layer2_tags, f"layer_{layer_name}"
            )
            result["differences"].extend(layer_diffs)

    return result


def format_output(result: dict[str, Any], brief: bool = False) -> str:
    """Format comparison result for display."""
    lines = []
    lines.append("=" * 80)
    lines.append("NOTE FILE COMPARISON")
    lines.append("=" * 80)
    lines.append(f"File 1: {result['file1']}")
    lines.append(f"File 2: {result['file2']}")
    lines.append("")

    # Summary
    if result["summary"]:
        lines.append("## SUMMARY")
        for key, values in result["summary"].items():
            lines.append(f"  {key}:")
            lines.append(f"    File 1: {values['file1']}")
            lines.append(f"    File 2: {values['file2']}")
        lines.append("")

    # Differences
    if result["differences"]:
        lines.append(f"## DIFFERENCES ({len(result['differences'])} total)")
        lines.append("")

        # Group by section
        by_section = {}
        for diff in result["differences"]:
            section = diff["section"]
            if section not in by_section:
                by_section[section] = []
            by_section[section].append(diff)

        for section, diffs in sorted(by_section.items()):
            lines.append(f"  ### {section.upper()}")
            for diff in diffs:
                key = diff["key"]
                if diff["type"] == "added":
                    lines.append(f"    + {key}: {diff['file2']}")
                elif diff["type"] == "removed":
                    lines.append(f"    - {key}: {diff['file1']}")
                else:  # changed
                    if brief:
                        lines.append(f"    ~ {key}: (changed)")
                    else:
                        val1 = diff["file1"]
                        val2 = diff["file2"]
                        # Truncate long values
                        if len(str(val1)) > 40:
                            val1 = str(val1)[:37] + "..."
                        if len(str(val2)) > 40:
                            val2 = str(val2)[:37] + "..."
                        lines.append(f"    ~ {key}:")
                        lines.append(f"        File 1: {val1}")
                        lines.append(f"        File 2: {val2}")
            lines.append("")
    else:
        lines.append("## NO DIFFERENCES FOUND")
        lines.append("  The files have identical structure (metadata may differ)")

    # Key findings summary
    lines.append("## KEY FINDINGS")

    # Check for recognition mode differences
    header_diffs = [d for d in result["differences"] if d["section"] == "header"]
    recogn_type = next(
        (d for d in header_diffs if d["key"] == "FILE_RECOGN_TYPE"), None
    )
    if recogn_type:
        lines.append(f"  - FILE_RECOGN_TYPE differs: {recogn_type['file1']} vs {recogn_type['file2']}")

    # Check for layer differences
    if "layers" in result["summary"]:
        lines.append(
            f"  - Layer count differs: {len(result['summary']['layers']['file1'])} vs {len(result['summary']['layers']['file2'])}"
        )

    # Check for STYLE entries
    style_diffs = [
        d for d in result["differences"] if d["key"].startswith("STYLE_")
    ]
    if style_diffs:
        lines.append(f"  - {len(style_diffs)} STYLE entry differences found")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Compare two Supernote .note files"
    )
    parser.add_argument("file1", type=Path, help="First .note file")
    parser.add_argument("file2", type=Path, help="Second .note file")
    parser.add_argument(
        "--json", "-j", action="store_true", help="Output as JSON"
    )
    parser.add_argument(
        "--brief", "-b", action="store_true", help="Brief output (don't show values)"
    )

    args = parser.parse_args()

    for f in [args.file1, args.file2]:
        if not f.exists():
            print(f"Error: File not found: {f}", file=sys.stderr)
            sys.exit(1)

    try:
        result = compare_notes(args.file1, args.file2)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result, brief=args.brief))

    except Exception as e:
        print(f"Error comparing files: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
