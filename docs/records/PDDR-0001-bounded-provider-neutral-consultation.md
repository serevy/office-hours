---
id: PDDR-0001
title: Bounded provider-neutral consultation contract
decision_date: 2026-09-28
recorded_date: 2026-09-28
decision_status: accepted
delivery_status: validated
scope:
  - project
  - product
owners:
  - serevy
evidence:
  - https://github.com/serevy/office-hours/issues/2
related: []
supersedes: []
superseded_by: null
---

# PDDR-0001: Bounded provider-neutral consultation contract

## Summary

Propose a provider-neutral core contract built around a bounded Consultation Packet, a bounded Consultation Result, and an explicit `need_more_context` path.

The portable budget unit is UTF-8 bytes. Provider-specific token limits remain adapter concerns.

## Context and observations

The preserved baseline keeps the original executor session authoritative and sends only decision-relevant context to an advisory expert.

Issue #2 requires that behavior to become a concrete portable contract without coupling the core to one provider or one tokenizer.

Token counts are not stable across provider and model families. A deterministic core limit therefore needs a provider-neutral unit.

## Options considered

### Option A: Provider token budget in the core

- Description: Make input and output token counts the canonical portable budget.
- Benefits: Close to common provider billing and generation controls.
- Costs / constraints: Tokenizers differ and may not be available to every adapter.
- Status: considered

### Option B: UTF-8 byte budget in the core

- Description: Bound serialized request and result payloads by bytes, with adapters free to impose stricter token limits.
- Benefits: Deterministic, portable, dependency-free, and testable across providers.
- Costs / constraints: Byte limits are only an approximation of provider token cost.
- Status: accepted

### Option C: No core budget unit

- Description: Leave all size control to provider adapters.
- Benefits: Maximum adapter freedom.
- Costs / constraints: Weakens the core guarantee that consultations stay context-bounded.
- Status: considered

## Decision

Adopt Option B for protocol v0.1.

The accepted contract also defines:

- stable `consultation_id` across incremental turns;
- monotonically increasing request `revision`;
- result `request_revision` linkage;
- `advice` and `need_more_context` as distinct result states;
- specific requested-context keys instead of whole-transcript escalation;
- advisory authority only;
- required adapter provenance with optional provider/model metadata.

The protocol was reviewed and accepted on 2026-09-28 before merging PR #7.

## Delivery and validation

The protocol is implemented in PR #7 and its PDDR and protocol-fixture CI checks pass.

Validation target:

- JSON schemas parse successfully;
- synthetic request/result fixtures remain inside byte budgets;
- the insufficient-context fixture requests evidence not present in revision 1;
- revision 2 supplies exactly that requested evidence;
- advice is returned only after the enriched request;
- PDDR validation and protocol fixture CI both pass.

## Consequences

The protocol can be implemented by different SDKs without forcing a common tokenizer.

Provider adapters must separately account for prompt-wrapper overhead, token limits, credentials, retries, and provider-specific usage details.

Byte budgets must not be interpreted as normalized cost metrics.

## Revisit when

Revisit if:

- cross-provider adapters cannot map the byte-bounded packet cleanly;
- token-only provider constraints make the split impractical;
- real consultation traces show that byte budgets do not control context growth well enough;
- protocol v0.2 needs streaming or multi-part evidence.

## Evidence

- https://github.com/serevy/office-hours/issues/2
- https://github.com/serevy/office-hours/pull/7
- `docs/baseline-v0.md`
- `docs/protocol-v0.1.md`
- `fixtures/protocol-v0.1/`

## Related records

None yet.
