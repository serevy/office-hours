# Claude Code dogfood

This is the first real Office Hours adapter.

The user-facing goal is intentionally small:

```text
/office-hours
```

The current Claude Code session remains the executor. It compacts the current decision into a Consultation Packet, invokes a separate read-only expert subagent, evaluates the result, and then returns control to the original session.

## Architecture

```text
Claude Code executor
      |
      | /office-hours
      v
skills/office-hours/SKILL.md
      |
      | compact protocol-v0.1 packet
      v
office-hours-expert
      |
      | advice or need_more_context
      v
original Claude Code executor
```

The expert is configured to request the `opus` model family. Claude Code may substitute a model according to organization allowlists or runtime configuration. The portable protocol therefore treats model metadata as provenance rather than authority.

## Recommended dogfood install

The direct `/office-hours` command is installed as a user Skill, together with its expert subagent.

### Windows PowerShell

From the cloned repository:

```powershell
.\scripts\install-claude-code.ps1
```

To replace an existing dogfood install:

```powershell
.\scripts\install-claude-code.ps1 -Force
```

### macOS / Linux

From the cloned repository:

```bash
sh ./scripts/install-claude-code.sh
```

To replace an existing dogfood install:

```bash
sh ./scripts/install-claude-code.sh --force
```

Start a new Claude Code session after the first install, then run:

```text
/office-hours
```

or:

```text
/office-hours Should we keep this adapter boundary or move provider-specific retry logic into core?
```

## Why not make plugin mode the default dogfood UX?

The repository also has the same plugin shell used by `agent-kpt`:

```text
.claude-plugin/plugin.json
skills/office-hours/SKILL.md
agents/office-hours-expert.md
```

During plugin development you can validate and load the cloned directory using Claude Code's plugin-development flow.

Plugin skills are namespaced by the host, so the skill is exposed as:

```text
/office-hours:office-hours
```

The canonical public UX is `/office-hours`, not the namespaced development command. The user-scope installer preserves that direct command while the plugin shell remains available for packaging and future distribution work.

## Invocation policy

The Skill sets:

```yaml
disable-model-invocation: true
```

Claude does not proactively call Office Hours during this dogfood phase. A human explicitly invokes `/office-hours`.

This avoids mixing Office Hours results with an existing Advisor Skill and makes test logs attributable to one consultation path.

## Privacy / authority boundary

By default:

- no raw transcript is persisted;
- no API keys, credentials, cookies, authorization headers, or private environment values are forwarded;
- the expert gets a compact packet rather than the full session;
- the expert cannot edit files or run state-changing tools;
- the executor retains final judgment;
- `need_more_context` requests specific evidence instead of the whole transcript.

If a team member shares a dogfood log, sanitize employer, customer, repository, credential, and other non-public details before posting it outside the authorized work environment.

## What to record from a dogfood run

A useful sanitized report contains:

- what kind of decision triggered `/office-hours`;
- whether revision 1 was sufficient;
- whether `need_more_context` happened;
- whether advice was accepted, partially accepted, or rejected;
- what felt slow, awkward, redundant, or surprisingly useful;
- the configured expert adapter/model selector;
- no private source material.

Raw consultation persistence and richer trace metrics belong to the later evaluation work.
