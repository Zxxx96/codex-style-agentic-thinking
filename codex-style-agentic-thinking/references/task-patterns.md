# Task Routing

Read this reference when a request spans several task families or the correct execution mode is unclear.

## Route By Dominant Risk

| Task family | Typical intent | Default mode | Load | Minimum completion evidence |
|---|---|---|---|---|
| Simple answer | Explain or answer a stable question | Direct | None | A direct, bounded answer |
| Code or UI change | Modify local behavior | Standard | `references/code-and-debug.md` | Diff/read-back plus a targeted check |
| Debugging | Diagnose, then optionally fix | Standard | `references/code-and-debug.md` | Reproduction or observed failure; re-check after a fix |
| Review | Find risks without changing state | Standard, read-only | `references/code-and-debug.md` | Findings tied to files, lines, logs, or behavior |
| Current research | Establish fresh external facts | Standard | `references/research-and-decisions.md` | Sources, freshness, confidence, and gaps |
| High-stakes decision | Recommend under uncertainty | Guarded | `references/research-and-decisions.md` | Criteria, unknown treatment, countercase, next actions |
| Document or media artifact | Create a usable file | Standard | `references/artifacts-and-external-actions.md` | File read-back, parse, render, or visual inspection |
| External action | Send, publish, merge, deploy, delete, or pay | Guarded | `references/artifacts-and-external-actions.md` and `references/quality-gates.md` | Authorization plus confirmation from the destination |

Raise the mode when the action is destructive, public, security-sensitive, expensive, reputation-costly, or difficult to reverse. Lower it when a reversible trial or narrow experiment contains the risk.

## Route Mixed Tasks In Stages

Split a mixed request into stages with separate done conditions and mutation authority. Common sequences include:

```text
research -> decision -> local implementation -> verification -> optional publication
diagnosis -> proposed fix -> authorized edit -> regression check
source inspection -> artifact creation -> render/read-back -> optional send
```

Completing one stage does not authorize the next. A request to prepare release notes does not authorize publishing a release. A request to diagnose a failure does not authorize editing the code.

## Resolve Competing Signals

Use this order:

1. Explicit user outcome and constraints.
2. Actual state observed through files, tools, or sources.
3. Existing project or organizational conventions.
4. Reversible assumptions needed to continue.

If a specialized skill is available, use its domain procedure and retain this protocol for scope, authorization, state protection, failure handling, and verification.

## Avoid Process Theater

- Do not print the routing decision unless it helps the user.
- Do not force every task through every gate.
- Do not create an artifact when a short answer is the useful deliverable.
- Do not ask questions that cannot change the next action.
- Do not claim stronger confidence merely because more steps were performed.
