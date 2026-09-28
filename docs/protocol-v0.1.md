# Consultation protocol v0.1

This document defines the first provider-neutral core contract for Office Hours.

The protocol is intentionally small. It describes a bounded consultation between an existing executor and an advisory expert without transferring task ownership.

## Contract surfaces

- Request schema: [`spec/consultation-packet.schema.json`](../spec/consultation-packet.schema.json)
- Result schema: [`spec/consultation-result.schema.json`](../spec/consultation-result.schema.json)
- Deterministic flow fixture: [`fixtures/protocol-v0.1/`](../fixtures/protocol-v0.1/)

## Request lifecycle

A consultation has one stable `consultation_id`.

Each packet revision increments `revision`.

```text
request revision 1
      |
      v
need_more_context
      |
      v
executor supplies only requested evidence
      |
      v
request revision 2
      |
      v
advice
```

A `need_more_context` response is not approval and is not an implementation instruction.

The executor remains responsible for deciding what evidence to reveal, whether to continue the consultation, and whether to use the final advice.

## Context budget

The portable core uses a UTF-8 byte budget rather than a token budget.

`context_budget.max_bytes` applies to the serialized consultation packet itself.

Why bytes:

- tokenizers vary by provider and model;
- some adapters may not expose tokenizer details;
- byte size is deterministic and provider-neutral;
- provider adapters can impose stricter provider-specific token limits separately.

Adapters may add prompt-wrapper overhead, but that overhead is outside the core packet budget and should be observable at the adapter layer.

## Response budget

`response_budget.max_bytes` is the executor's upper bound for the serialized expert result.

The expert adapter should ask the underlying model for a response that fits this budget and reject or safely truncate malformed over-budget output according to adapter policy.

Silence, timeout, malformed output, and `need_more_context` must never be converted into implicit approval.

## Incremental context

When the expert lacks evidence, it returns:

```json
{
  "status": "need_more_context",
  "requested_context": [
    {
      "key": "specific_evidence_key",
      "reason": "Why this evidence changes the decision",
      "max_bytes": 2048
    }
  ]
}
```

The executor should answer the requested keys, not append the full conversation by default.

The next request keeps the same `consultation_id` and increments `revision`.

## Provenance

Both request and result record adapter provenance.

Provider and model names are optional because a local or test adapter may not have meaningful vendor metadata. The adapter identity is required.

`trace_id` may connect the consultation to an external trace system, but raw credentials, API keys, cookies, authorization headers, and other secrets must never be stored in the packet or result.

## Authority boundary

The expert is advisory only.

It does not:

- gain write access to executor state;
- approve a change on behalf of the executor;
- mutate files, repositories, or external systems through this protocol;
- receive the full source session by default.

The executor may accept, reject, or partially adopt advice.

## Out of scope for v0.1

- provider SDK interfaces;
- retry policy for provider failures;
- model routing policy;
- token accounting normalization;
- pricing normalization;
- automatic quality scoring;
- global model ranking.

Those belong to later adapter and evaluation work.
