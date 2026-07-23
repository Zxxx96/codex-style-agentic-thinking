# Codex-Style Agentic Thinking

English · [中文介绍](#中文介绍)

A portable execution protocol for AI agents working on complex desktop and workspace tasks.

It helps an agent choose the lightest safe workflow, inspect relevant context, act within authorization, preserve user state, handle uncertainty, and verify results before claiming success.

This is an independent community project. It is not affiliated with, endorsed by, or maintained by OpenAI.

## 中文介绍

`codex-style-agentic-thinking` 是一套面向 AI Agent 的执行纪律协议。它不展示或复现模型的隐藏思维过程，而是规范可观察、可检查的工作方式：先确认目标和权限，再根据任务风险选择合适的执行强度，使用工具获取证据，保护用户的工作区，并在验证完成后才声明任务已经修复、发布或交付。

它主要解决这几类问题：

- Agent 面对复杂任务时过早行动，没有先检查上下文和影响范围；
- 把事实、推断、假设和未知信息混在一起，导致结论看似确定却缺少证据；
- 遇到失败后重复相同操作，而不是调整假设或验证方法；
- 修改了无关文件、覆盖用户状态，或在未获授权时执行外部操作；
- 只完成了草稿或局部检查，却声称任务已经完成。

协议提供三种执行模式：`Direct` 用于简单、低风险的任务，`Standard` 用于需要多步处理的可逆工作，`Guarded` 用于发布、删除、凭据处理等高风险或外部操作。它适合代码修改与调试、资料研究、文档和媒体制作、桌面自动化，以及需要明确授权和验收证据的任务；简单问答、翻译或单条安全命令通常不需要启用。

安装时，克隆本仓库并将其中的 `codex-style-agentic-thinking` 文件夹复制到 Agent 主机的 Skill 目录。Codex on Windows 通常使用：

```powershell
C:\Users\<你的用户名>\.codex\skills\codex-style-agentic-thinking
```

具体结构、使用示例和评测方法见下方英文说明。

## What This Project Is

`codex-style-agentic-thinking` transfers observable work habits, not private model reasoning. It gives an agent a reusable execution discipline for tasks where a good answer is not enough and the work must be grounded, performed, checked, and handed off clearly.

The protocol is designed for:

- multi-step or ambiguous tasks
- code changes and debugging
- current research and uncertain decisions
- document and media creation
- desktop automation and external actions
- work that must preserve an existing workspace
- claims that require evidence before the agent can say `done`

It deliberately stays out of simple factual answers, translation, formatting-only requests, and single safe commands unless risk or uncertainty makes the protocol useful.

## Three Execution Modes

| Mode | Use when | Agent behavior |
|---|---|---|
| **Direct** | Simple, stable, read-only, low-risk | Answer or execute directly without ceremony |
| **Standard** | Multi-step or reversible local work | Inspect context, act narrowly, run a targeted check |
| **Guarded** | External, destructive, sensitive, expensive, or hard-to-reverse work | Resolve scope and authorization, protect data/state, define fallback, verify the risky path |

The mode controls diligence, not answer length. A careful agent should still be concise.

## Core Behaviors

- **Ground before acting**: inspect the smallest useful set of files, sources, logs, screenshots, or app state.
- **Separate intent from capability**: analysis does not silently become editing; preparation does not silently become publication.
- **Distinguish evidence layers**: keep facts, inferences, assumptions, and unknowns separate.
- **Treat unknowns deliberately**: verify, negotiate, monitor, or accept them as named risks.
- **Protect user state**: preserve unrelated changes and avoid destructive cleanup.
- **Change approach after failure**: capture the concrete result and revise the hypothesis before retrying.
- **Degrade honestly**: when tools or permissions are unavailable, leave a draft or handoff and weaken the completion claim.
- **Verify claims**: tie `fixed`, `passed`, `sent`, and `published` to observed evidence.
- **Avoid process theater**: do not print a full workflow when a direct result is enough.

## V2 Improvements

The current version adds:

- narrower triggering and explicit non-trigger cases
- Direct, Standard, and Guarded routing
- read-only, local-mutation, and external-action authorization levels
- task-specific references loaded only when needed
- privacy, credential, prompt-injection, interruption, and resume rules
- an adaptive Markdown/JSON worklog generator
- a JSON worklog validator
- a repository-level behavioral evaluation suite
- critical-failure rules for fabricated success, secret exposure, unauthorized actions, and user-state loss

## Repository Structure

```text
codex-style-agentic-thinking-repo/
|-- README.md
|-- CHANGELOG.md
|-- LICENSE
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- codex-style-agentic-thinking/
|   |-- SKILL.md
|   |-- agents/
|   |   `-- openai.yaml
|   |-- references/
|   |   |-- task-patterns.md
|   |   |-- code-and-debug.md
|   |   |-- research-and-decisions.md
|   |   |-- artifacts-and-external-actions.md
|   |   |-- verification.md
|   |   |-- quality-gates.md
|   |   `-- examples.md
|   `-- scripts/
|       `-- thinking_scaffold.py
|-- evals/
|   |-- README.md
|   |-- cases.json
|   |-- rubric.md
|   |-- run_eval.py
|   |-- validate_cases.py
|   `-- fixtures/
|       `-- <case-id>/ (workspace files and evaluator setup notes)
`-- tests/
    `-- test_skill_v2.py
```

The installable Skill remains lean. Evaluation files stay at repository level so normal Skill use does not load benchmark material into the agent context.

## Installation

Clone the repository:

```bash
git clone https://github.com/Zxxx96/codex-style-agentic-thinking.git
```

Copy the inner `codex-style-agentic-thinking` folder into the Skill directory used by your agent host.

For Codex on Windows, the destination is commonly:

```powershell
C:\Users\<you>\.codex\skills\codex-style-agentic-thinking
```

Other desktop agents can use the protocol when they support a compatible Skill or instruction-folder mechanism. Their tool access, permission model, and instruction precedence still determine what the protocol can actually enforce.

## Usage

Invoke it explicitly for a complex task:

```text
Use $codex-style-agentic-thinking to inspect this repository, fix the failing login test without touching unrelated changes, and verify the result.
```

The Skill can also be combined with a domain-specific Skill. The domain Skill supplies specialized procedures; this protocol supplies scope control, evidence handling, authorization, state protection, failure recovery, and verification.

## Adaptive Worklog

Generate a debugging worklog:

```bash
python codex-style-agentic-thinking/scripts/thinking_scaffold.py \
  --type debug --risk standard "fix the failing login test"
```

Generate JSON for a guarded decision:

```bash
python codex-style-agentic-thinking/scripts/thinking_scaffold.py \
  --type decision --risk guarded --format json \
  --output worklog.json "choose between three vendors"
```

After filling the worklog, validate required evidence and completion fields:

```bash
python codex-style-agentic-thinking/scripts/thinking_scaffold.py \
  --check worklog.json
```

## Evaluation

The `evals/` directory turns the protocol into a testable project rather than a collection of good intentions.

It currently covers:

- simple tasks that should remain Direct
- diagnosis without edit authority
- code changes in a dirty worktree
- current product research
- high-uncertainty decisions
- authorized publication
- unavailable execution tools
- prompt injection inside repository content
- changed hypotheses after command failure
- interrupted work and newest-request handling
- visual verification of generated artifacts

Run an evaluation case end to end:

```bash
# List cases and fixture availability
python evals/run_eval.py list

# Materialize a fixture and a run-record template
python evals/run_eval.py prepare --case dirty-worktree-code-fix \
  --workdir /tmp/run1 --condition skill

# After the run, fill the record and score it
python evals/run_eval.py score --record /tmp/run1.record.json

# Aggregate baseline vs skill records
python evals/run_eval.py summarize --records ./results
```

Validate the case library with:

```bash
python evals/validate_cases.py
```

Run the repository tests with:

```bash
python -B -m unittest discover -s tests -v
```

Both checks also run in CI (`.github/workflows/ci.yml`) on every push and pull request.

For a fair comparison, run the same model and agent host with and without the Skill, keep tools and permissions constant, use fresh fixtures, save raw traces, and score at least three runs per condition. See `evals/README.md` and `evals/rubric.md`.

## Cross-Agent Feedback

Early feedback from Qoder, Trae, and WorkBuddy helped shape the protocol.

### Qoder

Qoder described the Skill as a useful work-discipline layer that can raise an agent's reliability floor without replacing model capability or domain expertise. Its main critique was that task routing and examples needed to become more executable and evaluable. V2 responds with explicit routing modes, a structured case library, and a scoring rubric.

### Trae

Trae highlighted the behavioral contrast between agents that jump straight into action and agents that first classify risk, gather context, separate facts from assumptions, protect state, and verify outcomes. That feedback reinforced the core execution loop and the rule against unsupported `done` claims.

### WorkBuddy

WorkBuddy summarized the value as turning a chatbot into a disciplined desktop collaborator. It emphasized evidence gathering, state protection, verification, and checkable delivery, which remain the project's central product framing.

These are qualitative assessments, not controlled benchmark results. The reproducible evaluation protocol in `evals/` should be used for quantitative claims.

## Non-Goals

This Skill does not:

- expose hidden chain-of-thought
- make a weaker model equal to a stronger model
- replace domain-specific expertise or tools
- guarantee correctness without relevant evidence
- create permissions the host agent does not have
- authorize irreversible actions on the user's behalf
- prove improvement from a single screenshot or one-off score

## License

MIT. See `LICENSE`.
