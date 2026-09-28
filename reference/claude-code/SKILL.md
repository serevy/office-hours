---
name: office-hours-reference
description: |
  Reference-only Claude Code implementation of the original Office Hours idea.
  The current executor summarizes the relevant task context, asks a configured
  expert model for a short second opinion, and then continues the original session.
---

# Office Hours — Claude Code reference

This file exists to preserve the behavior of the original implementation while the portable core is designed.

It is **not** the provider-neutral core API.

## Concept

Use an expert for a short consultation when the current session reaches a meaningful decision point.

Do not transfer the whole task.

## Procedure

1. Identify the question.
   - If the user supplied a question, use it.
   - Otherwise derive the current decision point from the active session.
   - If the question is genuinely ambiguous, ask the user instead of inventing one.

2. Build a self-contained consultation prompt containing:
   - task background and goal;
   - current state;
   - the decision or uncertainty;
   - constraints;
   - relevant attempts / evidence;
   - candidate options when useful.

3. Invoke the configured expert model through the host harness.
   - Ask for a short second opinion.
   - Do not ask the expert to take over implementation.
   - Prefer a concise recommendation, trade-offs, and important risks.

4. Return the advice to the active executor.

5. The active executor decides whether to accept, reject, or partially adopt the advice and continues the original session.

## Boundaries

- Expert output is advisory.
- The expert does not gain write or execution authority.
- Do not forward secrets merely because they exist in the active session.
- Do not forward the entire transcript by default.
- Provider/model selection belongs to the adapter layer, not this behavioral reference.

## Future portable behavior

The provider-neutral core should eventually support a structured result equivalent to:

- `advice`
- `need_more_context`

When more context is needed, the expert should request the specific missing evidence rather than asking for the entire conversation.
