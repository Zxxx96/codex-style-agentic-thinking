#!/usr/bin/env python3
"""Emit a Codex-style external reasoning scaffold.

Use for complex, ambiguous, high-stakes, or multi-step tasks. Do not use this
scaffold for trivial factual questions or single-step commands.

This does not produce hidden chain-of-thought. It prints an inspectable
workspace for facts, assumptions, unknowns, actions, verification, and risks.

Usage:
  python thinking_scaffold.py "compare three desktop agents"
  echo "fix the failing checkout test" | python thinking_scaffold.py
"""

import argparse
import sys


TEMPLATE = """# Codex-Style Work Scaffold

Use this scaffold only for non-trivial tasks. For simple questions, answer directly.

## Task
{problem}

## Classification
- Task type:
- Stakes / risk:
- Deadline:
- Reversibility:
- Done means:

## Context Checked
- Files / sources / tools inspected:
- Current state:
- Constraints:

## Evidence Ledger
- [fact] Confirmed:
- [inference] Reasonable inference:
- [assumption] Working assumption:
- [unknown] Missing information:

## Unknown Handling
| Unknown | Impact | Treatment | Action |
|---|---|---|---|
|  | high/medium/low | verify/negotiate/monitor/accept |  |

## Do Now / Needs Info
- Do now:
- Needs info:
- Won't do yet:

## Quality Gates
- Scope gate:
- Evidence needed:
- Mutation/external side-effect risk:
- Budget / stop rule:
- Trust boundaries:

## Options / Approach
- Option A:
- Option B:
- Status quo / no-op:

## Self-Refutation
- What would make the current conclusion wrong?
- Strongest counterexample:
- Assumption that would flip the answer:

## Action Plan
1.
2.
3.

## Verification
- Check to run:
- Expected evidence:
- Result:

## Deliverable
- Artifact / answer:
- Remaining risks:
"""


def read_problem(args: argparse.Namespace) -> str:
    if args.problem:
        return " ".join(args.problem).strip()
    piped = sys.stdin.read().strip()
    return piped or "(fill in the task or decision)"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Emit a Codex-style work scaffold for complex tasks."
    )
    parser.add_argument("problem", nargs="*", help="task or decision statement")
    args = parser.parse_args()
    print(TEMPLATE.format(problem=read_problem(args)))


if __name__ == "__main__":
    main()
