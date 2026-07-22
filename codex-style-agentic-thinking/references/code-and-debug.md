# Code, Debugging, And Review Work

Read this reference for code changes, bug diagnosis, reviews, refactors, UI work, tests, and release preparation.

## Establish Mutation Intent

- `Explain`, `review`, and `diagnose` are read-only unless the user also requests a fix.
- `Fix`, `add`, `change`, `refactor`, and `build` authorize scoped local edits.
- `Prepare a release` authorizes local version or notes work, not tagging or publishing.
- If intent is mixed, investigate first and isolate the exact mutation that needs approval.

## Inspect Before Editing

- Check repository status and preserve unrelated user changes.
- Inspect the relevant structure, code path, tests, configuration, and local conventions.
- Search for existing helpers before adding dependencies or abstractions.
- Define the expected behavior and narrowest useful verification.

Do not clean, reset, reformat, or refactor unrelated files to make the workspace look tidy.

## Code Change Loop

1. Locate the owning module and existing pattern.
2. State or infer the smallest behavior change that satisfies the request.
3. Edit within that boundary.
4. Add or update focused tests when behavior changes.
5. Run the narrowest meaningful check first.
6. Expand verification only when shared behavior or blast radius warrants it.
7. Inspect the final diff for accidental scope.

For behavior-preserving refactors, establish a before/after checkpoint. If useful tests do not exist, add characterization coverage before moving code.

## Debugging Loop

1. Reproduce or directly observe the failure.
2. Identify the first relevant application frame, state transition, or bad value.
3. Form one concrete hypothesis tied to evidence.
4. Run a narrow experiment that could disprove it.
5. Fix the cause rather than only masking the symptom.
6. Re-run the failing case and a nearby regression check.

If reproduction is impossible, label the cause as a hypothesis and provide the next discriminating check. Do not turn a plausible explanation into a confirmed root cause.

## Failure Protocol

After a failed command or patch:

- Record the exact error or observed behavior.
- Name the assumption that failed.
- Change the next attempt materially.
- Stop only when the blocker remains unchanged, no new evidence is available, and no safe alternative can advance the task.

Attempt count alone is not a stop rule.

## Review Protocol

- Lead with actionable findings ordered by severity.
- Tie each finding to a file, line, log, test gap, or user-visible behavior.
- Prioritize correctness, security, data loss, regressions, performance, and missing tests.
- Do not modify code during a review unless the user also asks for changes.
- If no findings remain, say so and name residual risk or untested areas.

## UI And Visual Work

- Follow the existing design system and interaction patterns.
- Check relevant desktop and mobile dimensions.
- Verify overflow, overlap, loading, empty, error, and disabled states where they matter.
- Use screenshots, rendering, or browser checks for visual claims.

## Release Preparation

- Read version files, changelog conventions, recent commits, and current git state.
- Draft notes from actual changes rather than memory.
- Run release-relevant validation.
- Do not tag, publish, merge, or deploy unless explicitly requested and authorized.

## Completion Evidence

Report:

- What behavior changed or what cause was found.
- Which files changed, if any.
- Which checks ran and their exact scope.
- What remains unverified.

Passing lint does not prove runtime behavior. A unit test does not prove an end-to-end workflow. Match the claim to the check.
