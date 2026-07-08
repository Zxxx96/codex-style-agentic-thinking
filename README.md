# Codex-Style Agentic Thinking

A portable skill that turns chatty AI agents into disciplined desktop collaborators.

It helps agents work in a context-first, tool-aware, verification-driven, and artifact-oriented way.

This is an independent community project. It is not affiliated with, endorsed by, or maintained by OpenAI.

## What It Does

`codex-style-agentic-thinking` packages a visible agent workflow into a reusable skill. It does not expose hidden chain-of-thought or claim to reproduce private model internals. Instead, it gives an agent a practical operating discipline:

- **Classify before acting**: identify the task type, risk, scope, and done condition.
- **Gather evidence with tools**: read files, run commands, inspect sources, render outputs.
- **Separate facts from assumptions**: label facts, inferences, assumptions, and unknowns.
- **Verify before claiming done**: match every completion claim to evidence.
- **Protect the user's workspace**: avoid unrelated edits and irreversible actions.
- **Deliver inspectable artifacts**: provide files, drafts, checklists, evidence, and risks.

## Why It Exists

Many AI agents can answer. Fewer can work reliably.

For real desktop tasks, the hard part is not sounding smart. The hard part is knowing when to inspect files, when to run tests, when to stop and ask, when to avoid touching user state, and when a claim like "done" is actually justified.

This skill turns those habits into a portable protocol.

## Cross-Agent Feedback

I tested the idea with several desktop-agent systems and used their feedback to refine the skill.

### Qoder

Qoder's evaluation framed the skill as a "work discipline suit" for general agents: useful for raising the floor, but not a substitute for expertise. It rated the strongest mechanisms as self-refutation, evidence layering, quality gates, failure handling, and trust-boundary labels. Its main critique was that task routing and the example library should become more executable and evaluable.

That feedback led to:

- stronger `quality-gates.md`
- clearer trust-boundary handling
- tighter completion-claim rules
- a more explicit path toward routing tables and eval cases

### Trae

Trae summarized the before/after behavior clearly:

- without the skill, an agent may jump straight into action, rely on memory, skip verification, get blocked by one missing fact, or say "done" without explaining what changed
- with the skill, an agent classifies the task, gathers enough context, separates facts from assumptions, does what can be done first, verifies with tools, protects user state, and reports what was verified

That feedback shaped the README positioning and reinforced the core loop:

```text
classify -> ground in context -> split work -> plan lightly -> gather evidence -> preserve state -> verify -> self-refute -> deliver
```

### WorkBuddy

WorkBuddy distilled the project into one sentence:

> Make AI work like a reliable desktop collaborator, not just a chat bot.

It highlighted six core capabilities:

- classify before acting
- gather evidence with tools
- separate facts from guesses
- verify before claiming completion
- protect the workspace
- deliver checkable outputs

That feedback became the current top-level product framing.

## Repository Structure

```text
codex-style-agentic-thinking/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── task-patterns.md
│   ├── verification.md
│   ├── quality-gates.md
│   └── examples.md
└── scripts/
    └── thinking_scaffold.py
```

## Files

### `SKILL.md`

The main skill entry point. It defines the core loop:

1. Classify the task.
2. Ground in context.
3. Split work into `do now` and `needs info`.
4. Plan at the right resolution.
5. Use tools for evidence.
6. Preserve user state.
7. Iterate and verify.
8. Self-refute important conclusions.
9. Deliver concise, checkable results.

### `references/task-patterns.md`

Task-specific workflows for research, code changes, debugging, reviews, decisions, document work, creative work, automation, releases, and external actions.

### `references/verification.md`

A completion discipline for claims like "fixed", "done", "passed", or "ready". It includes a claim-strength ladder so agents do not say "done" when they only drafted, guessed, or partially checked.

### `references/quality-gates.md`

Safety gates for complex or risky work:

- scope gate
- evidence gate
- mutation gate
- verification gate
- failure gate
- handoff gate
- budget and stop gate
- trust boundary gate

### `references/examples.md`

Concrete examples showing expected observable behavior across common desktop-agent tasks, including debugging, code review, refactoring, research, CSV analysis, document creation, release preparation, external messages, log diagnosis, and high-uncertainty decisions.

### `scripts/thinking_scaffold.py`

A small helper that emits a structured Markdown scaffold for complex tasks.

```bash
python scripts/thinking_scaffold.py "decide whether to accept a job offer in 48 hours"
```

The scaffold includes task classification, context, evidence, unknown handling, quality gates, action plan, verification, and deliverables.

## Installation

Copy the skill folder into your Codex skills directory:

```bash
~/.codex/skills/codex-style-agentic-thinking
```

On Windows, this may be:

```powershell
C:\Users\<you>\.codex\skills\codex-style-agentic-thinking
```

Then invoke it explicitly:

```text
Use $codex-style-agentic-thinking to handle this complex task with context, tools, verification, and clear deliverables.
```

## Example Prompt

```text
Use $codex-style-agentic-thinking to review this repo, identify why the login test is flaky, fix it, and verify the result without changing unrelated files.
```

Expected behavior:

- inspect the repo before editing
- reproduce or observe the failure
- form a narrow hypothesis
- patch the smallest cause
- run the relevant test
- report changed files and verification
- avoid claiming success if verification fails

## Design Principles

- **Evidence over assertion**: read, run, inspect, render, or cite.
- **Smallest useful action**: avoid unnecessary scope and unrelated edits.
- **State preservation**: treat the user's workspace as live and shared.
- **Explicit uncertainty**: unknowns become verification, negotiation, monitoring, or accepted risk.
- **Safe external actions**: draft before sending, publishing, merging, deleting, or paying.
- **Right-sized process**: simple tasks get direct answers; complex tasks get structure.

## Non-Goals

This skill does not:

- expose hidden chain-of-thought
- replace domain-specific skills
- make a weak model as capable as a stronger model
- guarantee correctness without verification
- authorize irreversible actions on behalf of the user

## License

MIT. See `LICENSE`.
