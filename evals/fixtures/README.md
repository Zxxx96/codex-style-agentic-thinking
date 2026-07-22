# Evaluation Fixtures

Each subdirectory matches a case `id` in `../cases.json`.

Layout per case:

- `workspace/`: files copied into a fresh working directory for the run. Optional; some cases need no files.
- `fixture.md`: extra setup the evaluator must perform manually (git state, blocked tools, mid-run interruptions). Optional.

Prepare a run with:

```bash
python evals/run_eval.py prepare --case <case-id> --workdir /path/to/fresh/dir
```

The runner copies `workspace/`, prints the prompt and setup notes, and writes a run-record template next to the workdir. Never give the tested agent the case's `must_do`, `must_not_do`, rubric, or fixture notes; the agent should see only the prompt and the workspace files a real user would provide.
