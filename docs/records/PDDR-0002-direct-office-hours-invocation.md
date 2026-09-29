---
id: PDDR-0002
title: Direct Office Hours invocation and Claude Code dogfood packaging
decision_date: 2026-09-29
recorded_date: 2026-09-29
decision_status: accepted
delivery_status: in-progress
scope:
  - product
  - process
owners:
  - serevy
evidence:
  - https://github.com/serevy/office-hours/issues/3
related:
  - PDDR-0001
supersedes: []
superseded_by: null
---

# PDDR-0002: Direct Office Hours invocation and Claude Code dogfood packaging

## Summary

Use `/office-hours` as the canonical human-facing invocation.

For the first Claude Code dogfood, install the Skill and expert subagent at user scope so that the direct command remains `/office-hours`.

Keep a Claude Code plugin manifest and plugin-compatible layout in the repository for development and future distribution, while treating the plugin-namespaced command as a packaging detail rather than the canonical UX.

## Context and observations

The personally dogfooded predecessor was valuable partly because asking for advice was lightweight.

A generic `/advisor` name risks colliding with a future host-provided feature and does not preserve the Office Hours product identity.

Claude Code plugin skills are host-namespaced. Loading this repository as plugin `office-hours` therefore exposes the development skill as `/office-hours:office-hours`, while a user-scope Skill named `office-hours` is directly invocable as `/office-hours`.

The first dogfood also needs attributable behavior, so automatic model invocation would make test results harder to distinguish from existing advisor workflows.

## Options considered

### Option A: Canonical `/advisor`

- Description: Preserve the predecessor command name.
- Benefits: Familiar to the original operator.
- Costs / constraints: Generic name and potential future collision with a host command.
- Status: rejected

### Option B: Plugin-namespaced command only

- Description: Use `/office-hours:office-hours` as the public command.
- Benefits: Matches plugin namespace behavior without an installer.
- Costs / constraints: More typing and leaks packaging details into the product UX.
- Status: rejected

### Option C: Canonical `/office-hours` with plugin-compatible packaging

- Description: Install the dogfood Skill / agent at user scope for the direct command, while retaining a plugin shell in the repository.
- Benefits: Short stable product command, low collision risk, and packaging remains aligned with other agent tools.
- Costs / constraints: Dogfood install and plugin-development mode expose different command strings.
- Status: accepted

## Decision

Adopt Option C.

The dogfood Skill is human-invoked only with `disable-model-invocation: true`.

Do not provide a built-in `/advisor` alias.

## Delivery and validation

Implementation is in progress in the Issue #3 Claude Code dogfood branch.

Validation includes:

- plugin manifest structure;
- Skill manual-invocation setting;
- read-only expert subagent boundary;
- Windows and macOS/Linux user-scope installers;
- deterministic fake provider portability test;
- existing protocol-v0.1 fixtures.

Runtime dogfood on real Claude Code remains required before this record becomes `validated`.

## Consequences

Team members can use the same user-facing `/office-hours` command on Windows and macOS.

The repository remains compatible with Claude Code plugin development, but plugin mode is not the canonical command surface during dogfood.

A later marketplace/package distribution may revisit how to preserve the direct command without a bootstrap installer.

## Revisit when

Revisit if:

- Claude Code changes plugin command namespacing;
- a marketplace distribution path can preserve `/office-hours` directly;
- the standalone user-scope installer becomes an operational burden;
- another host reserves or conflicts with `office-hours`.

## Evidence

- https://github.com/serevy/office-hours/issues/3
- `docs/claude-code-dogfood.md`
- `skills/office-hours/SKILL.md`
- `agents/office-hours-expert.md`

## Related records

- PDDR-0001
