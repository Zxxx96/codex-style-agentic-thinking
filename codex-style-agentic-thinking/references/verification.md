# Verification Before Completion

Load this reference before claiming that a complex task is done, fixed, complete, or ready.

## Verification Ladder

Use the highest rung that is practical for the task:

1. **Read-back check**: Reopen or inspect the artifact you created.
2. **Static check**: Lint, parse, schema-check, validate frontmatter, or search for placeholders.
3. **Unit check**: Run the smallest test or command that exercises the changed behavior.
4. **Integration check**: Run the relevant workflow end to end.
5. **Visual check**: Screenshot, render, or inspect output when appearance matters.
6. **User-facing check**: Confirm the deliverable exists where promised and is usable.

## Completion Questions

Before final response, answer internally:

- Did the requested artifact or behavior actually get created?
- Did I verify with a tool, source, or file read?
- Did verification cover the risky part of the task?
- Did I avoid changing unrelated state?
- Are any assumptions or unverified parts important enough to mention?
- Is the final answer about the latest user request?

## Evidence Language

Use precise claims:

- "I ran X and it passed."
- "I inspected Y and found no TODO placeholders."
- "I created Z at [path]."
- "I could not verify X because Y."

Avoid vague claims:

- "Should work."
- "Looks good" without saying what was checked.
- "Done" when tests or artifacts were not inspected.

## Claim Strength

Match the claim to the evidence:

| Evidence | Allowed claim |
|---|---|
| No verification | "Drafted", "prepared", "proposed", or "not verified" |
| File reopened or source inspected | "Created" or "updated" |
| Targeted command/test passed | "Verified for [specific behavior]" |
| End-to-end workflow passed | "Validated end to end" |
| External side effect completed | "Sent/published/merged" only if explicitly requested and confirmed |

If the check is partial, say what it covers and what it does not cover.

## If Verification Fails

- Do not claim success.
- Capture the exact failure.
- Decide whether to fix, narrow scope, or report the blocker.
- If fixing, repeat the verification command after the fix.

After two failed attempts with the same blocker, stop and reassess. Do not keep retrying without new evidence or a changed hypothesis.

## Final Response Shape

For implementation or file work:

```text
Done: [what changed]
Files: [links]
Verified: [commands/checks]
Notes: [unverified risks or next steps]
```

For research or analysis:

```text
Answer: [concise conclusion]
Evidence: [sources or observed facts]
Confidence: [high/medium/low and why]
Gaps: [what remains uncertain]
```
