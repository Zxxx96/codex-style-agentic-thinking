#!/usr/bin/env python3
"""Generate or validate a task-specific external work scaffold.

The scaffold records observable work state: scope, evidence, authorization,
actions, verification, and risks. It does not produce hidden chain-of-thought.

Examples:
  python thinking_scaffold.py --type debug --risk standard "fix login test"
  python thinking_scaffold.py --type decision --risk guarded --format json "choose vendor"
  python thinking_scaffold.py --check worklog.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


TASK_TYPES = (
    "general",
    "code",
    "debug",
    "review",
    "research",
    "decision",
    "document",
    "external",
)
MODES = ("direct", "standard", "guarded")
AUTO_MODE = {
    "general": "standard",
    "code": "standard",
    "debug": "standard",
    "review": "standard",
    "research": "standard",
    "decision": "guarded",
    "document": "standard",
    "external": "guarded",
}


def read_problem(parts: list[str]) -> str:
    if parts:
        return " ".join(parts).strip()
    piped = sys.stdin.read().strip()
    return piped or "(fill in the task)"


def resolve_mode(task_type: str, risk: str) -> str:
    return AUTO_MODE[task_type] if risk == "auto" else risk


def task_specific_fields(task_type: str) -> dict[str, Any]:
    fields: dict[str, dict[str, Any]] = {
        "general": {
            "approach": [],
            "decision_points": [],
        },
        "code": {
            "expected_behavior": "",
            "relevant_files": [],
            "existing_pattern": "",
            "test_plan": [],
        },
        "debug": {
            "observed_failure": "",
            "reproduction": "",
            "hypotheses": [],
            "next_discriminating_check": "",
            "fix_scope": "",
        },
        "review": {
            "review_scope": "",
            "findings": [],
            "test_gaps": [],
            "residual_risk": "",
        },
        "research": {
            "question": "",
            "criteria": [],
            "source_budget": "",
            "sources": [],
            "disagreements": [],
        },
        "decision": {
            "decision": "",
            "deadline": "",
            "reversibility": "",
            "criteria": [],
            "options": [],
            "unknown_treatments": [],
            "countercase": "",
            "fallback_rule": "",
        },
        "document": {
            "source_material": [],
            "output_format": "",
            "layout_constraints": [],
            "render_or_readback_check": "",
        },
        "external": {
            "action": "",
            "target": "",
            "payload": "",
            "visibility": "",
            "reversibility": "",
            "privacy_check": "",
            "destination_evidence": "",
        },
    }
    return fields[task_type]


def build_worklog(problem: str, task_type: str, mode: str) -> dict[str, Any]:
    return {
        "schema_version": "2.0",
        "task": {
            "statement": problem,
            "type": task_type,
            "mode": mode,
            "done_condition": "",
        },
        "scope": {
            "in_scope": [],
            "out_of_scope": [],
            "constraints": [],
        },
        "context": {
            "checked": [],
            "facts": [],
            "inferences": [],
            "assumptions": [],
            "unknowns": [],
        },
        "authorization": {
            "requested_action": "",
            "mutation_level": "read-only",
            "allowed_scope": [],
            "confirmation_required": False,
            "confirmation_evidence": "",
            "sensitive_data_notes": "",
        },
        "plan": {
            "do_now": [],
            "needs_information": [],
            "not_authorized_yet": [],
            "stop_rule": "",
        },
        "task_specific": task_specific_fields(task_type),
        "verification": {
            "claim": "",
            "checks": [],
            "results": [],
            "scope_covered": "",
            "not_verified_reason": "",
        },
        "deliverable": {
            "result": "",
            "artifacts": [],
            "remaining_risks": [],
            "next_action": "",
        },
    }


def display_value(value: Any) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "TODO"
    return str(value) if value else "TODO"


def title_from_key(key: str) -> str:
    return key.replace("_", " ").capitalize()


def render_section(title: str, data: dict[str, Any], keys: tuple[str, ...]) -> list[str]:
    lines = [f"## {title}"]
    lines.extend(f"- {title_from_key(key)}: {display_value(data[key])}" for key in keys)
    lines.append("")
    return lines


def render_markdown(worklog: dict[str, Any]) -> str:
    task = worklog["task"]
    if task["mode"] == "direct":
        return "\n".join(
            [
                "# Direct Work Note",
                "",
                f"- Task: {task['statement']}",
                f"- Type: {task['type']}",
                "- Answer or action: TODO",
                "- Evidence needed for unstable claims: TODO or none",
                "- Result: TODO",
                "",
            ]
        )

    lines = [
        "# Codex-Style Worklog",
        "",
        "Record observable evidence and actions, not private chain-of-thought.",
        "",
        "## Task",
        f"- Statement: {task['statement']}",
        f"- Type: {task['type']}",
        f"- Mode: {task['mode']}",
        f"- Done condition: {display_value(task['done_condition'])}",
        "",
    ]
    lines.extend(
        render_section("Scope", worklog["scope"], ("in_scope", "out_of_scope", "constraints"))
    )
    lines.extend(
        render_section(
            "Context And Evidence",
            worklog["context"],
            ("checked", "facts", "inferences", "assumptions", "unknowns"),
        )
    )
    lines.extend(
        render_section(
            "Authorization",
            worklog["authorization"],
            (
                "requested_action",
                "mutation_level",
                "allowed_scope",
                "confirmation_required",
                "sensitive_data_notes",
            ),
        )
    )
    lines.extend(
        render_section(
            "Work Split",
            worklog["plan"],
            ("do_now", "needs_information", "not_authorized_yet", "stop_rule"),
        )
    )
    lines.append(f"## {title_from_key(task['type'])} Details")
    for key, value in worklog["task_specific"].items():
        lines.append(f"- {title_from_key(key)}: {display_value(value)}")

    if task["mode"] == "guarded":
        lines.extend(
            [
                "",
                "## Guarded Gates",
                "- Authorization evidence: TODO",
                "- Privacy / credential check: TODO",
                "- Rollback, fallback, or handoff: TODO",
                "- External destination check: TODO or not applicable",
            ]
        )

    verification = worklog["verification"]
    deliverable = worklog["deliverable"]
    lines.extend(
        [
            "",
            "## Verification",
            f"- Intended claim: {display_value(verification['claim'])}",
            f"- Checks: {display_value(verification['checks'])}",
            f"- Observed results: {display_value(verification['results'])}",
            f"- Scope covered: {display_value(verification['scope_covered'])}",
            f"- Not-verified reason: {display_value(verification['not_verified_reason'])}",
            "",
            "## Deliverable",
            f"- Result: {display_value(deliverable['result'])}",
            f"- Artifacts: {display_value(deliverable['artifacts'])}",
            f"- Remaining risks: {display_value(deliverable['remaining_risks'])}",
            f"- Next action: {display_value(deliverable['next_action'])}",
            "",
        ]
    )
    return "\n".join(lines)


def get_path(data: dict[str, Any], dotted: str) -> Any:
    value: Any = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def is_filled(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return len(value) > 0
    return True


def validate_worklog(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read valid JSON: {exc}"]

    errors: list[str] = []
    if data.get("schema_version") != "2.0":
        errors.append("schema_version must be 2.0")

    required = (
        "task.statement",
        "task.type",
        "task.mode",
        "task.done_condition",
        "scope.in_scope",
        "context.checked",
        "plan.do_now",
        "plan.stop_rule",
        "authorization.requested_action",
        "authorization.allowed_scope",
        "verification.claim",
        "deliverable.result",
    )
    for field in required:
        if not is_filled(get_path(data, field)):
            errors.append(f"missing required field: {field}")

    task_type = get_path(data, "task.type")
    mode = get_path(data, "task.mode")
    mutation_level = get_path(data, "authorization.mutation_level")
    if task_type not in TASK_TYPES:
        errors.append(f"task.type must be one of: {', '.join(TASK_TYPES)}")
    if mode not in MODES:
        errors.append(f"task.mode must be one of: {', '.join(MODES)}")
    if mutation_level not in ("read-only", "local", "external"):
        errors.append("authorization.mutation_level must be read-only, local, or external")

    checks = get_path(data, "verification.checks")
    results = get_path(data, "verification.results")
    no_verify = get_path(data, "verification.not_verified_reason")
    if mode in ("standard", "guarded") and not (
        is_filled(checks) and is_filled(results)
    ) and not is_filled(no_verify):
        errors.append(
            "standard/guarded work needs verification checks and results, "
            "or an explicit not_verified_reason"
        )

    confirmation_required = get_path(data, "authorization.confirmation_required")
    confirmation_evidence = get_path(data, "authorization.confirmation_evidence")
    if confirmation_required and not is_filled(confirmation_evidence):
        errors.append("confirmation_required is true but confirmation_evidence is empty")

    if mutation_level == "external" and mode != "guarded":
        errors.append("external mutation requires guarded mode")

    return errors


def write_output(content: str, output: str | None) -> None:
    if output:
        Path(output).write_text(content, encoding="utf-8")
    else:
        print(content)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate or validate a Codex-style external worklog."
    )
    parser.add_argument("problem", nargs="*", help="task or decision statement")
    parser.add_argument("--type", choices=TASK_TYPES, default="general")
    parser.add_argument(
        "--risk",
        choices=("auto",) + MODES,
        default="auto",
        help="execution mode; auto chooses from task type",
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", help="optional output file")
    parser.add_argument("--check", metavar="JSON_FILE", help="validate a filled JSON worklog")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.check:
        errors = validate_worklog(Path(args.check))
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            raise SystemExit(1)
        print("Worklog is valid.")
        return

    problem = read_problem(args.problem)
    mode = resolve_mode(args.type, args.risk)
    worklog = build_worklog(problem, args.type, mode)
    if args.format == "json":
        content = json.dumps(worklog, indent=2, ensure_ascii=False) + "\n"
    else:
        content = render_markdown(worklog)
    write_output(content, args.output)


if __name__ == "__main__":
    main()
