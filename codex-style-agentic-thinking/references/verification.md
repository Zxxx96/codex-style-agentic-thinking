# Verification Before Completion

Read this reference before claiming that a complex task is done, fixed, complete, ready, sent, published, or otherwise successful.

## Start From The Claim

Write the intended claim in concrete terms, then choose evidence that could actually prove it.

Examples:

- `The file exists` requires a file or read-back check.
- `The parser handles quoted CSV fields` requires a behavior test, not only lint.
- `The page looks correct on mobile` requires rendering or screenshots at relevant dimensions.
- `The message was sent` requires confirmation from the destination, not a local draft.
- `This is the best current option` requires current sources, criteria, and stated uncertainty.

## Verification Ladder

Use the highest practical rung required by risk and claim scope:

1. **Existence check**: confirm the promised file, record, branch, message, or output exists.
2. **Read-back check**: reopen or inspect the created or changed artifact.
3. **Static check**: parse, lint, type-check, validate schema/frontmatter, or search for placeholders.
4. **Targeted behavior check**: exercise the changed behavior with the narrowest useful test.
5. **Integration check**: run the relevant workflow across components.
6. **Visual check**: render, screenshot, or inspect layout and interaction.
7. **Destination check**: confirm an external action where it was supposed to occur.

More checks do not automatically mean stronger evidence. Choose checks that cover the risky claim.

## Claim Strength

| Evidence observed | Allowed claim |
|---|---|
| No verification | `Drafted`, `prepared`, `proposed`, or `not verified` |
| Existence/read-back check | `Created` or `updated` |
| Targeted command or test passed | `Verified for [specific behavior]` |
| Relevant end-to-end workflow passed | `Validated end to end for [scope]` |
| Destination confirms external action | `Sent`, `published`, `merged`, or `deployed` |

If verification is partial, state what it covers and what it does not.

## Evidence Record

For each material completion claim, record:

```text
Claim:
Check performed:
Observed result:
Scope covered:
Remaining gap:
```

Do not copy a successful command or result from an example. Report only output actually observed in the current task.

## Task-Specific Checks

### Code

- Inspect the final diff.
- Run the failing or changed behavior test.
- Add a nearby regression or broader check when blast radius warrants it.
- Distinguish lint/type success from runtime success.

### Research And Decisions

- Cite or name sources checked.
- State dates or freshness limits for unstable facts.
- Separate sourced facts from interpretation.
- Report confidence, disagreement, and decision-changing gaps.

### Documents And Visual Artifacts

- Confirm file existence and format.
- Reopen or parse content.
- Render or visually inspect when layout matters.
- Check for overflow, broken links, missing assets, and placeholders.

### External Actions

- Confirm target, payload, authorization, and destination result.
- Record identifiers, URL, recipient, schedule, or branch when safe and useful.
- Do not equate a prepared local artifact with successful external execution.

## When Verification Fails

- Do not preserve the original success claim.
- Capture the exact failure.
- Decide whether to fix, narrow the claim, change the approach, or leave a handoff.
- Re-run the relevant check after a fix.
- Stop when the same blocker remains, no new evidence is available, and no safe alternative remains.

Attempt count alone is not evidence that a task is blocked.

## Final Response Shape

For implementation or artifact work:

```text
Outcome: [what changed or was created]
Artifacts: [inspectable paths or destinations]
Verified: [checks and observed results]
Gaps: [unverified risk or next action]
```

For research or analysis:

```text
Answer: [concise conclusion]
Evidence: [sources or observed facts]
Confidence: [level and reason]
Gaps: [what remains uncertain]
```
