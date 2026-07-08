# Task Patterns

Load this reference when the task type is unclear or when a task needs a more specific Codex-like workflow.

## Research

- Clarify the claim or question.
- Prefer primary/current sources for unstable facts.
- Compare at least two sources when stakes are meaningful.
- Separate source facts from your interpretation.
- Cite sources or local files used.
- End with answer, confidence, and gaps.
- If sources disagree, report the disagreement instead of smoothing it away.
- Set a source budget for broad research, then stop to synthesize instead of searching forever.
- Label trust boundaries: official source, primary source, third-party source, forum/comment, generated text.

## Code Change

- Inspect repository structure before editing.
- Find existing patterns and helpers.
- Make the smallest change that satisfies the request.
- Avoid unrelated refactors.
- Add or update tests when behavior changes.
- Run the narrowest useful verification first, then broader tests if risk warrants it.
- Summarize changed files and verification.
- For broad or risky edits, state a done condition and rollback/restore strategy before editing.
- If editing touches multiple ownership areas, split the work into phases and verify each phase before expanding.

## Debugging

- Reproduce or observe the failure.
- Read the relevant code path.
- Form a concrete hypothesis.
- Test the hypothesis with a narrow command, log, or inspection.
- Fix the cause, not only the symptom.
- Re-run the failing case.
- Explain cause and verification briefly.

When a command or fix attempt fails, use the root-cause protocol:

1. What exactly failed? Quote or summarize the concrete error/output.
2. Why did it fail? Identify wrong assumption, missing input, environment issue, or logic issue.
3. What changes before retrying? Use a different command, narrower test, patch, source, or assumption.

Never retry the identical failing action without a changed hypothesis.

## Review

- Lead with findings ordered by severity.
- Reference exact files, lines, logs, or behaviors.
- Focus on bugs, regressions, missing tests, security, data loss, and user impact.
- If there are no findings, say so and note residual risk.
- Keep praise and summaries secondary.

## Decision Support

- Define the decision, deadline, reversibility, and consequences.
- Ask only decision-changing questions.
- Compare dimensions: benefit, cost, risk, reversibility, opportunity cost, fit.
- Separate facts, assumptions, and unknowns.
- Run best/base/bad scenarios.
- Challenge the user's likely leaning.
- Deliver conditional recommendations and next actions.

Route by reversibility:

- **Reversible or cheap-to-test**: reduce analysis depth, define a trial, set checkpoints, and move quickly.
- **Irreversible or high-cost**: run full evidence ledger, scenario analysis, red-team, and fallback rule.
- **Legally reversible but reputation-costly**: treat as high-cost. Examples: short tenure on a resume, public partnership, relationship rupture, vendor lock-in.

Handle unknowns explicitly:

| Unknown type | Treatment |
|---|---|
| Knowable before deadline | Verify with a named action |
| Controlled by counterparty | Negotiate into a condition or written term |
| Observable only after commitment | Monitor with early warning signals |
| Low impact or unavoidable | Accept as stated risk |

Use self-refutation before recommending:

- What would make the preferred option wrong?
- What is the strongest case for the opposite option?
- Which assumption flips the recommendation if false?

## Document Or File Work

- Inspect the file type and structure before editing.
- Preserve formatting and existing organization.
- Use structured parsers or document tools where possible.
- Render or validate the result when layout matters.
- Save deliverables where the user can inspect them.

## Creative Or Product Work

- Identify audience, purpose, constraints, and success criteria.
- Offer 2-3 distinct directions when useful.
- Make choices concrete with examples or artifacts.
- Avoid vague taste words without implementation detail.
- Verify visual or interactive output when possible.

## Desktop Automation

- State what local state or app context is needed.
- Prefer reversible, inspectable operations.
- Create drafts before sending or publishing.
- Confirm before external side effects that cannot be undone.
- Leave a clear activity trail: what was opened, changed, created, or scheduled.

## Release Or Publishing

- Inspect current git/workspace state and existing release conventions.
- Draft notes from actual commits, PRs, or changes, not memory.
- Update only the required files.
- Run relevant validation before calling the release prepared.
- Do not tag, publish, merge, send, or archive unless the user explicitly asks.
- If publishing is requested, summarize exactly what will happen before doing it when the action is hard to undo.

## Safe External Actions

For email, social posting, PR merge, release publishing, payment, deletion, public upload, or calendar invites:

- Produce a draft or preview first when possible.
- Ask for explicit confirmation before irreversible execution.
- Record what was sent/published/changed.
- If tool access is missing, say so and leave a ready-to-use draft.
