from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "codex-style-agentic-thinking"
EVALS_DIR = REPO_ROOT / "evals"
SCAFFOLD_PATH = SKILL_ROOT / "scripts" / "thinking_scaffold.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scaffold = load_module("thinking_scaffold", SCAFFOLD_PATH)
run_eval = load_module("run_eval", EVALS_DIR / "run_eval.py")
validate_cases = load_module("validate_cases", EVALS_DIR / "validate_cases.py")


class ScaffoldTests(unittest.TestCase):
    def test_auto_mode_routing(self) -> None:
        self.assertEqual(scaffold.resolve_mode("debug", "auto"), "standard")
        self.assertEqual(scaffold.resolve_mode("decision", "auto"), "guarded")
        self.assertEqual(scaffold.resolve_mode("external", "auto"), "guarded")

    def test_direct_markdown_stays_minimal(self) -> None:
        worklog = scaffold.build_worklog("explain git status", "general", "direct")
        markdown = scaffold.render_markdown(worklog)
        self.assertIn("# Direct Work Note", markdown)
        self.assertNotIn("## Guarded Gates", markdown)
        self.assertNotIn("## Context And Evidence", markdown)

    def test_render_markdown_uses_filled_values(self) -> None:
        worklog = scaffold.build_worklog("fix failure", "debug", "standard")
        worklog["task"]["done_condition"] = "targeted test passes"
        worklog["scope"]["in_scope"] = ["login module"]
        worklog["verification"]["claim"] = "verified login behavior"
        worklog["deliverable"]["result"] = "scoped fix"
        markdown = scaffold.render_markdown(worklog)
        self.assertIn("- Done condition: targeted test passes", markdown)
        self.assertIn("- In scope: login module", markdown)
        self.assertIn("- Intended claim: verified login behavior", markdown)
        self.assertIn("- Result: scoped fix", markdown)
        self.assertIn("- Out of scope: TODO", markdown)

    def test_task_specific_fields_change_by_type(self) -> None:
        debug = scaffold.build_worklog("fix failure", "debug", "standard")
        decision = scaffold.build_worklog("choose vendor", "decision", "guarded")
        self.assertIn("observed_failure", debug["task_specific"])
        self.assertNotIn("options", debug["task_specific"])
        self.assertIn("options", decision["task_specific"])
        self.assertIn("countercase", decision["task_specific"])

    def test_validator_accepts_filled_standard_worklog(self) -> None:
        worklog = scaffold.build_worklog("fix failure", "debug", "standard")
        worklog["task"]["done_condition"] = "targeted test passes"
        worklog["scope"]["in_scope"] = ["login module"]
        worklog["context"]["checked"] = ["failing test", "login module"]
        worklog["authorization"]["requested_action"] = "fix the test"
        worklog["authorization"]["mutation_level"] = "local"
        worklog["authorization"]["allowed_scope"] = ["login module"]
        worklog["plan"]["do_now"] = ["reproduce", "patch", "retest"]
        worklog["plan"]["stop_rule"] = "targeted test passes or blocker is evidenced"
        worklog["verification"]["claim"] = "verified login behavior"
        worklog["verification"]["checks"] = ["targeted login test"]
        worklog["verification"]["results"] = ["passed"]
        worklog["deliverable"]["result"] = "scoped fix"

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "worklog.json"
            path.write_text(json.dumps(worklog), encoding="utf-8")
            self.assertEqual(scaffold.validate_worklog(path), [])

    def test_validator_rejects_unverified_standard_worklog(self) -> None:
        worklog = scaffold.build_worklog("fix failure", "debug", "standard")
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "worklog.json"
            path.write_text(json.dumps(worklog), encoding="utf-8")
            errors = scaffold.validate_worklog(path)
        self.assertTrue(any("done_condition" in error for error in errors))
        self.assertTrue(any("needs verification" in error for error in errors))


class SkillIntegrityTests(unittest.TestCase):
    def test_skill_references_exist(self) -> None:
        instruction_files = [SKILL_ROOT / "SKILL.md", *SKILL_ROOT.glob("references/*.md")]
        references = []
        for instruction_file in instruction_files:
            text = instruction_file.read_text(encoding="utf-8")
            references.extend(re.findall(r"`((?:references|scripts)/[^`]+)`", text))
        self.assertGreater(len(references), 0)
        missing = [relative for relative in references if not (SKILL_ROOT / relative).exists()]
        self.assertEqual(missing, [])

    def test_openai_prompt_invokes_exact_skill_name(self) -> None:
        metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$codex-style-agentic-thinking", metadata)

    def test_eval_case_library_has_expected_coverage(self) -> None:
        data = json.loads((REPO_ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        cases = data["cases"]
        self.assertGreaterEqual(len(cases), 14)
        self.assertTrue(any(not case["skill_should_trigger"] for case in cases))
        self.assertTrue(any(case["expected_mutation"] == "external" for case in cases))
        self.assertTrue(any(case["expected_mode"] == "guarded" for case in cases))

    def test_mode_and_mutation_vocabulary_consistent(self) -> None:
        self.assertEqual(set(scaffold.MODES), validate_cases.MODES)
        self.assertEqual({"read-only", "local", "external"}, validate_cases.MUTATIONS)


class EvalRunnerTests(unittest.TestCase):
    def test_case_library_passes_structural_validation(self) -> None:
        data = json.loads((EVALS_DIR / "cases.json").read_text(encoding="utf-8"))
        seen: set[str] = set()
        errors = []
        for index, case in enumerate(data["cases"]):
            errors.extend(validate_cases.validate_case(case, index, seen))
        self.assertEqual(errors, [])

    def test_fixture_directories_match_case_ids(self) -> None:
        case_ids = set(run_eval.load_cases())
        fixtures_dir = EVALS_DIR / "fixtures"
        fixture_dirs = {path.name for path in fixtures_dir.iterdir() if path.is_dir()}
        self.assertEqual(sorted(fixture_dirs - case_ids), [])
        self.assertGreaterEqual(len(fixture_dirs), 8)

    def test_record_validation_and_scoring(self) -> None:
        record = run_eval.build_record("dirty-worktree-code-fix", "skill")
        self.assertTrue(run_eval.validate_record(record))

        record["date"] = "2026-07-10"
        record["agent"] = "test-agent"
        record["model"] = "test-model"
        record["trace_path"] = "traces/run1.txt"
        record["scores"] = {dimension: 2 for dimension in run_eval.DIMENSIONS}
        record["must_do_satisfied"] = True
        record["must_not_do_satisfied"] = True
        self.assertEqual(run_eval.validate_record(record), [])

        result = run_eval.evaluate_record(record)
        self.assertTrue(result["passed"])
        self.assertEqual(result["total"], 14)

        record["critical_failures"]["credential_or_secret_exposed"] = True
        result = run_eval.evaluate_record(record)
        self.assertFalse(result["passed"])

    def test_low_gate_dimension_fails_even_with_high_total(self) -> None:
        record = run_eval.build_record("dirty-worktree-code-fix", "skill")
        record["date"] = "2026-07-10"
        record["agent"] = "test-agent"
        record["model"] = "test-model"
        record["trace_path"] = "traces/run2.txt"
        record["scores"] = {dimension: 2 for dimension in run_eval.DIMENSIONS}
        record["scores"]["verification_and_claim_strength"] = 0
        record["must_do_satisfied"] = True
        record["must_not_do_satisfied"] = True
        result = run_eval.evaluate_record(record)
        self.assertFalse(result["passed"])


if __name__ == "__main__":
    unittest.main()
