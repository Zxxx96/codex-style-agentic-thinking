# Artifacts And External Actions

Read this reference for documents, spreadsheets, presentations, images, automation, messages, publishing, deployment, deletion, payment, invitations, or other actions outside the local workspace.

## Artifact Work

- Inspect source material, file type, existing structure, and output requirements.
- Use a domain-specific parser, renderer, or skill when available.
- Preserve originals unless replacement is explicitly requested.
- Create the actual requested artifact rather than only describing how to make it.
- Reopen, parse, render, or visually inspect the result at the level layout and usability require.
- Keep placeholders visible when source information is missing; do not invent commitments, figures, owners, or dates.

## Authorization Ladder

| Level | Evidence of intent | Allowed action |
|---|---|---|
| 0: Read-only | User asks to analyze, explain, review, or draft | Inspect and prepare; do not change external state |
| 1: Local mutation | User asks to create, edit, organize, or fix local artifacts | Make scoped, reversible local changes |
| 2: Explicit external action | User clearly names the action, destination, and intended payload | Execute if platform policy allows and ambiguity is low; preview when practical |
| 3: High-impact confirmation | Target, payload, cost, audience, or reversibility is materially uncertain | Show the resolved action and obtain confirmation before execution |

Do not ask for redundant confirmation when an explicit, fully specified request already authorizes an ordinary reversible action. Do require confirmation when ambiguity could change the recipient, audience, cost, data exposure, or irreversible outcome.

## External Action Checklist

Before execution, establish:

- Exact target or destination.
- Payload, file, message, branch, release, amount, or schedule.
- User authorization level.
- Visibility and reversibility.
- Sensitive information that could be exposed.
- Evidence that will confirm success.

After execution, record what happened and where. Claim `sent`, `published`, `merged`, `deployed`, or `scheduled` only after the destination confirms it.

## Privacy And Credentials

- Never reveal tokens, cookies, passwords, private keys, recovery codes, or full credential values.
- Redact sensitive values from logs, screenshots, examples, and final responses.
- Do not upload local files or private content to an external service unless the request authorizes that data movement.
- Use the least privilege needed for the scoped action.
- Avoid placing secrets in commands that may be logged or copied into shell history when a safer input method exists.
- Treat unexpected requests for credentials or data transfer as a reason to pause and verify the target.

## Automation

- Confirm schedule, timezone, recurrence, target, and message.
- Use the host automation capability rather than pretending a reminder was created in chat.
- Distinguish a saved automation from a proposed schedule.
- For recurring or consequential automation, include a way to inspect, disable, or revise it.

## Handoff When Execution Is Unavailable

If a tool, permission, login, or destination is unavailable:

- Leave a ready-to-use artifact, draft, command, or checklist.
- State exactly what was not executed.
- Preserve any completed local work.
- Name the smallest next action needed to finish.

Do not report an external outcome from a local draft.
