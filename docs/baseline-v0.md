# Baseline v0 — expert consultation workflow

This document freezes the behavior that existed before `office-hours` was extracted as OSS.

The original workflow was created because the strongest model could not be used continuously under the available plan and environment.

The design goal was not “route every hard task to a bigger model.”

It was:

> **Borrow five or ten minutes from a senior engineer, then keep doing the work yourself.**

## Existing flow

```text
executor works in the current session
        |
        v
a hard decision / uncertainty appears
        |
        v
executor summarizes only the relevant background
        |
        v
stronger / different model gives short advice
        |
        v
executor evaluates the advice
        |
        v
the original session continues
```

## Behavioral invariants

### The task is not handed off

The expert is a consultant, not the new owner of the task.

### The original session remains authoritative

The executor keeps the full working context and continues after the consultation.

### Context is curated

The expert receives a self-contained packet containing only what it needs for the current question.

The packet should normally include:
- task goal;
- current state;
- decision point;
- known constraints;
- attempts / evidence;
- candidate options when useful;
- the exact question.

### Advice is bounded

The expert should give a short opinion, recommendation, trade-off analysis, or warning.
It should not start a new implementation project or deep research pass unless explicitly requested.

### Advice is not authority

The executor may accept, reject, or partially adopt the answer.

### Consultation can be cross-provider

The underlying concept does not depend on Claude, OpenAI, Gemini, or any one model family.

## Why preserve this separately from native advisor features?

Native features may:
- be unavailable in some plans or deployment environments;
- restrict model/provider combinations;
- forward a larger conversation context than desired;
- choose consultation timing differently.

`office-hours` is specifically about **executor-curated, context-bounded consultation**.

## Known limitations in the original personal implementation

- one harness-specific Agent invocation;
- one configured default expert model;
- no typed request/response contract;
- no explicit `NEED_MORE_CONTEXT` protocol;
- no portable provider interface;
- no automatic value/cost evaluation.

Those limitations become later Issues rather than being hidden in the baseline.
