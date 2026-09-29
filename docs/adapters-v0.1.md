# Adapter boundary v0.1

Office Hours core remains provider-neutral.

An executor adapter produces the accepted protocol-v0.1 Consultation Packet.

An expert provider consumes that packet and returns a protocol-v0.1 Consultation Result.

```text
ExecutorAdapter
  -> ConsultationPacket

ExpertProvider
  <- ConsultationPacket
  -> ConsultationResult
```

## Responsibilities

### Executor adapter

- derive only decision-relevant context from the active work session;
- redact secrets and unrelated confidential material;
- enforce the core context budget;
- assign consultation id / revision / executor provenance;
- deliver a packet to an ExpertProvider;
- handle `need_more_context` incrementally;
- keep final judgment and execution authority.

### Expert provider

- map the provider-specific invocation into a bounded advisory call;
- never receive execution authority through this interface;
- return `advice` or `need_more_context`;
- attach provider / model / adapter provenance when reliably known;
- avoid embedding credentials in the Consultation Result.

## First real adapter: Claude Code

The Claude Code adapter is implemented as:

- `skills/office-hours/SKILL.md` for executor-side orchestration;
- `agents/office-hours-expert.md` for the expert boundary.

The executor sends a compact packet to a separate subagent. The expert is configured with the `opus` family selector and read-only tools.

Claude Code can substitute the requested model because of organization policy or runtime configuration. The adapter must not pretend a configured alias is stronger evidence than the actual runtime can provide. For dogfood logs, record the configured selector and, when available from Claude Code runtime UI, the resolved model separately.

## Deterministic fake provider

`scripts/fake_expert.py` is a second provider implementation used only for portability tests.

It consumes the same JSON packet fixtures as the real adapter boundary:

- without `remote_rate_limit_signal`: returns `need_more_context`;
- with that evidence: returns `advice`.

The fake proves that the core packet/result contract is not structurally tied to Claude-specific response objects.

## Credentials

Credentials belong to provider runtime configuration, never to the Consultation Packet or Consultation Result.

The core contract does not have fields for API keys, bearer tokens, cookies, or provider session credentials.
