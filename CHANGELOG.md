# Changelog

## 2.1.0 - 2026-07-10

Made the evaluation suite executable and fixed tooling defects.

- Added `evals/fixtures/` with concrete workspace files or evaluator setup notes for the cases that need them (crash log, dirty worktree repo, prompt-injection repo, release repo with a missing check, flawed sales CSV, credential-bearing deploy log, and more).
- Added `evals/run_eval.py`: `list`, `prepare` (materialize fixture + run-record template), `score` (validate a filled record against the rubric, including critical failures and pass gates), and `summarize` (median/range/pass/critical per condition).
- Added three evaluation cases: `credential-redaction-in-log`, `csv-analysis-cross-check`, and `implied-send-needs-confirmation`.
- Added GitHub Actions CI running the case-library validator and the repository tests on Ubuntu and Windows.
- Fixed `render_markdown` in `thinking_scaffold.py` to render filled worklog values instead of hardcoded TODO placeholders (empty fields still render as TODO).
- Removed the force push from `publish-via-gh-api.ps1`, made the commit message a parameter, and documented that the script is fast-forward only.
- Extended the test suite: data-driven rendering, runner record validation and scoring, fixture-to-case consistency, and mode/mutation vocabulary consistency between the scaffold and the case validator.

## 2.0.0

V2 protocol as described in the README: Direct/Standard/Guarded routing, authorization levels, task-specific references, adaptive worklog generator and validator, behavioral case library, and critical-failure rules.
