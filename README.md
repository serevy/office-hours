# office-hours

[![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/serevy/office-hours?utm_source=oss&utm_medium=github&utm_campaign=serevy%2Foffice-hours&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)](https://coderabbit.ai)

**Borrow a few minutes of senior intelligence.**

`office-hours` is an experimental provider-neutral consultation layer for coding agents.

The idea comes from a familiar engineering habit:

> Keep doing the work yourself. When you hit a hard decision, borrow five or ten minutes from a senior engineer.

The active executor keeps ownership of the task and the original session. It compacts only the context needed for the current decision, asks a stronger or different model for short advice, then continues the work itself.

## Core idea

```text
Existing executor session
        |
        v
Hard decision / uncertainty
        |
        v
Executor-curated consultation packet
  - goal
  - current state
  - constraints
  - attempts / evidence
  - decision needed
        |
        v
Expert provider
Claude / OpenAI / Gemini / local / ...
        |
        v
Short advice
        |
        v
Original executor evaluates the advice
        |
        v
Same session continues
```

This is consultation, not delegation.

## Design principles

- **Keep the original session.** The expert does not take over the task.
- **Bound the context.** Do not resend the entire conversation when a compact decision packet is enough.
- **Advice only.** The expert does not gain execution authority.
- **Executor retains judgment.** Advice can be accepted, rejected, or partially adopted.
- **Provider-neutral.** The executor and expert may come from different vendors or model families.
- **Escalate incrementally.** If the packet is insufficient, the expert should be able to request specific additional context.
- **Measure value.** Strong-model calls should be evaluated against quality, retries, latency, context cost, and downstream outcomes.

## Candidate consultation contract

```yaml
goal:
current_state:
decision_needed:
constraints:
attempted:
evidence:
options:
question:
response_budget:
```

Candidate expert result:

```yaml
status: advice | need_more_context
advice:
rationale:
requested_context:
risks:
```

Protocol v0.1 is now specified as a provider-neutral JSON contract:

- [Protocol](docs/protocol-v0.1.md)
- [Request schema](spec/consultation-packet.schema.json)
- [Result schema](spec/consultation-result.schema.json)
- [Incremental-context fixtures](fixtures/protocol-v0.1/)

## Why not simply route the whole task?

A strong model is often most valuable at a narrow decision point, not necessarily as the worker for the entire session.

`office-hours` explores whether selective, context-bounded consultation can preserve continuity while reducing:

- repeated context ingestion;
- unnecessary use of the strongest model;
- session handoff cost;
- duplicated exploration.

## Initial scope

- provider-neutral consultation packet;
- one executor adapter and one or more expert-provider adapters;
- explicit context budget;
- short-response budget;
- `NEED_MORE_CONTEXT` / incremental-context flow;
- traceable consultation records;
- evaluation fixtures for usefulness, context reduction, latency, and cost.

## Non-goals

- replacing the executor;
- automatically accepting expert advice;
- hiding provider cost or context use;
- forcing the expert to be a more expensive model;
- cloning one provider's native advisor feature.

## Claude Code dogfood

The first real adapter keeps the user-facing entrypoint intentionally small:

```text
/office-hours
```

Install the dogfood Skill and expert agent at user scope.

Windows PowerShell:

```powershell
.\scripts\install-claude-code.ps1
```

macOS / Linux:

```bash
sh ./scripts/install-claude-code.sh
```

Start a new Claude Code session after the first install, then run `/office-hours` with or without an explicit question.

The Skill is manual-only during dogfood (`disable-model-invocation: true`) so existing Advisor workflows do not mix with Office Hours results.

This repository also includes a Claude Code plugin manifest for development and future packaging. Plugin mode uses the host namespace (`/office-hours:office-hours`); the canonical user-facing command remains `/office-hours`.

See [Claude Code dogfood](docs/claude-code-dogfood.md) and [adapter boundary](docs/adapters-v0.1.md).

## Status

Early extraction from a personally dogfooded workflow. Interfaces are expected to change.

## License

MIT.

## Project decisions

This repository uses [PDDR Kit](https://github.com/serevy/pddr-kit) to preserve durable Project / Product / Process decisions and their evidence.

- Records: [`docs/records/`](docs/records/)
- Template: [`.pddr/template.md`](.pddr/template.md)
- Validate: `python .pddr/pddr.py validate --allow-empty`

PDDR is not a task log. Create or update a record only when a durable decision is made; installation alone does not require a decision record.

## Baseline

The original personally dogfooded consultation flow is preserved separately from the future portable core.

- [Baseline design](docs/baseline-v0.md)
- [Claude Code reference behavior](reference/claude-code/SKILL.md)
- [Synthetic consultation fixtures](fixtures/baseline-v0/)
