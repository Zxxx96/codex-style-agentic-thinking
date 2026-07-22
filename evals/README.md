# Evaluation Guide

This directory tests observable agent behavior, not private reasoning and not brand similarity.

The evaluation asks whether the skill improves disciplined execution across different models and desktop-agent hosts while controlling for model, tools, permissions, and task setup.

## Files

- `cases.json`: reusable prompts, setups, required behaviors, prohibited behaviors, and evidence expectations.
- `rubric.md`: scoring rules and critical failures.
- `validate_cases.py`: structural validation for the case library.
- `run_eval.py`: prepares fixture workdirs, generates run-record templates, scores filled records against the rubric, and aggregates baseline-versus-skill results.
- `fixtures/`: per-case workspace files plus evaluator-only setup notes (`fixture.md`).

## Comparison Protocol

For each agent and model combination:

1. Record the date, agent version, model, reasoning setting, operating system, available tools, permissions, and workspace fixture. `run_eval.py prepare` writes a record template with these fields.
2. Run each case without the skill, using a fresh session and clean copy of the fixture.
3. Run the same case with the skill loaded, keeping every other condition unchanged.
4. Use at least three runs per condition when the host is stochastic.
5. Save raw prompts, outputs, tool traces, diffs, artifacts, and errors.
6. Score runs with `rubric.md`; blind the evaluator to baseline versus skill condition when practical.
7. Report median score, score range, critical-failure count, and per-dimension changes.

Do not give the tested agent the expected answer, suspected failure, rubric, or intended fix. The prompt and fixture should contain only the context a real user would provide.

## Interpretation

- Compare the same model with and without the skill before comparing different models.
- Separate host capability from protocol compliance. A missing browser or shell is not a reasoning failure if the agent degrades honestly.
- Treat screenshots or one-off opinions from other agents as qualitative feedback, not benchmark results.
- Do not claim percentage improvement without raw runs and a stated calculation.

## Run A Case

```bash
python evals/run_eval.py list
python evals/run_eval.py prepare --case <case-id> --workdir <fresh-dir> --condition baseline
python evals/run_eval.py score --record <workdir>.record.json
python evals/run_eval.py summarize --records <records-dir>
```

`prepare` copies the case fixture into the workdir, prints the verbatim prompt, and writes a run-record template. After the run, fill the record's scores (0-2 per rubric dimension), critical-failure flags, and must-do/must-not-do outcomes, then `score` it. `summarize` reports median, range, pass rate, and critical-failure counts per condition.

## Validate The Case Library

```bash
python evals/validate_cases.py
```

The validator checks required fields, identifiers, execution modes, mutation levels, and non-empty behavioral criteria. CI runs it together with the repository tests on every push.
