#!/usr/bin/env python3
"""Required pre-release check: version.txt must match the newest changelog entry."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    version = (ROOT / "version.txt").read_text(encoding="utf-8").strip()
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"^## (\d+\.\d+\.\d+)", changelog, flags=re.MULTILINE)
    if not match:
        print("FAIL: no version heading found in CHANGELOG.md")
        return 1
    if match.group(1) != version:
        print(f"FAIL: version.txt is {version} but newest changelog entry is {match.group(1)}")
        return 1
    print(f"PASS: release check ok for {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
