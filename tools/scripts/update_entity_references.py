#!/usr/bin/env python3
"""
update_entity_references.py — Update entity references across YAML

Purpose:
  Finds and updates entity_id references across configuration files after renames.

Usage:
  python3 tools/scripts/update_entity_references.py [args]

Safety:
  Review diffs before committing. Prefer dry-run/output mode if available.
"""

import argparse
import json
import re
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "appdaemon",
    "custom_components",
    "deps",
    "esphome",
    "image",
    "pyscript",
    "themes",
    "tts",
    "www",
    "zigbee2mqtt",
}

SKIP_FILES = {
    "ha_inventory.json",
    "entity_rename_map.json",
    "entity_rename_actions.json",
}

INCLUDE_EXTS = {".yaml", ".yml", ".json", ".txt", ".md"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Update entity_id references using a rename map.")
    parser.add_argument("--map", default="entity_rename_map.json", help="Path to rename map JSON")
    parser.add_argument("--root", default=".", help="Root directory to scan")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).resolve()
    mapping = json.loads(Path(args.map).read_text())

    if not mapping:
        return 0

    keys = sorted(mapping.keys(), key=len, reverse=True)
    pattern = re.compile(r"\b(" + "|".join(re.escape(k) for k in keys) + r")\b")

    touched = 0
    for path in root.rglob("*"):
        if path.is_dir():
            if path.name in SKIP_DIRS:
                continue
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix not in INCLUDE_EXTS:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue

        text = path.read_text()
        if not pattern.search(text):
            continue
        new_text = pattern.sub(lambda m: mapping[m.group(0)], text)
        if new_text != text:
            path.write_text(new_text)
            touched += 1

    print(f"Updated {touched} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
