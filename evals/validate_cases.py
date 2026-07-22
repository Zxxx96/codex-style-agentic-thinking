#!/usr/bin/env python3
"""Validate the portable behavioral evaluation case library."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CASES_PATH = Path(__file__).with_name("cases.json")
REQUIRED_FIELDS = (
    "id",
    "title",
    "prompt",
    "setup",
    "skill_should_trigger",
    "expected_mode",
    "expected_mutation",
    "must_do",
    "must_not_do",
    "evidence_required",
    "expected_artifact",
)
MODES = {"direct", "standard", "guarded"}
MUTATIONS = {"read-only", "local", "external"}


def nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(isinstance(item, str) and item.strip() for item in value)
    if isinstance(value, bool):
        return True
    return value is not None


def validate_case(case: Any, index: int, seen: set[str]) -> list[str]:
    prefix = f"case[{index}]"
    if not isinstance(case, dict):
        return [f"{prefix} must be an object"]

    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in case or not nonempty(case[field]):
            errors.append(f"{prefix} missing non-empty field: {field}")

    case_id = case.get("id")
    if isinstance(case_id, str):
        if case_id in seen:
            errors.append(f"{prefix} duplicate id: {case_id}")
        seen.add(case_id)

    if case.get("expected_mode") not in MODES:
        errors.append(f"{prefix} expected_mode must be one of {sorted(MODES)}")
    if case.get("expected_mutation") not in MUTATIONS:
        errors.append(f"{prefix} expected_mutation must be one of {sorted(MUTATIONS)}")
    if case.get("expected_mutation") == "external" and case.get("expected_mode") != "guarded":
        errors.append(f"{prefix} external mutation requires guarded mode")
    if not isinstance(case.get("skill_should_trigger"), bool):
        errors.append(f"{prefix} skill_should_trigger must be boolean")
    return errors


def main() -> None:
    try:
        data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read {CASES_PATH}: {exc}", file=sys.stderr)
        raise SystemExit(1)

    errors: list[str] = []
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty list")
        cases = []

    seen: set[str] = set()
    for index, case in enumerate(cases):
        errors.extend(validate_case(case, index, seen))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Validated {len(cases)} evaluation cases.")


if __name__ == "__main__":
    main()
