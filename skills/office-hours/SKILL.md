---
name: office-hours
description: Ask a bounded expert for a short second opinion while keeping the current Claude Code session in control.
argument-hint: [question]
disable-model-invocation: true
allowed-tools: Agent
disallowed-tools: Write Edit NotebookEdit Bash PowerShell
---

# Office Hours

Get a bounded second opinion from the configured Office Hours expert without handing over the task.

The user invoked:

`/office-hours $ARGUMENTS`

## Rules

- This is consultation, not delegation.
- The current Claude Code session remains the executor and keeps final judgment.
- Do not modify files, run state-changing commands, or implement the expert's advice during the consultation itself.
- Do not send the full conversation by default.
- Never forward API keys, tokens, credentials, cookies, authorization headers, private environment values, or unrelated confidential material.
- Do not persist the consultation packet or result unless the user explicitly asks for a log.
- Keep the expert response short and decision-focused.

## Procedure

1. Identify the decision.
   - If `$ARGUMENTS` contains a question, use it as the consultation question.
   - Otherwise infer the current hard decision or uncertainty from the active conversation.
   - If there is no meaningful decision to consult on, ask one concise clarifying question and stop.

2. Build a compact in-memory Consultation Packet compatible with protocol v0.1:
   - `protocol_version: "0.1"`
   - a fresh `consultation_id`
   - `revision: 1`
   - `goal`
   - `current_state`
   - `decision_needed`
   - `constraints`
   - `attempted`
   - `evidence`
   - `options` when useful
   - `question`
   - `context_budget.max_bytes: 8192`
   - `response_budget.max_bytes: 4096`
   - executor provenance

   Keep it materially smaller than the source conversation. Summarize rather than paste.

3. Invoke the Office Hours expert subagent in the foreground and wait for it.
   - Prefer the user-scope agent named `office-hours-expert`.
   - When running this repository through Claude Code plugin mode, the scoped agent may be `office-hours:office-hours-expert`.
   - Send only the Consultation Packet plus the instruction to return a protocol-v0.1 Consultation Result.
   - Do not ask the expert to implement or edit anything.

4. Handle the result.
   - For `status: advice`, evaluate the advice yourself.
   - For `status: need_more_context`, provide only the specifically requested context that is relevant and safe to share.
   - Increment `revision` and consult once more.
   - If the second result still needs more context, stop and explain what remains missing instead of expanding to the full transcript.

5. Return control to the current session.
   Briefly show:
   - the expert's advice;
   - important rationale / risks;
   - your executor judgment: accept, partially accept, or reject;
   - the next step for the existing task.

If the user invoked Office Hours during an already-authorized implementation task, you may continue that existing task only after the consultation turn is complete. The expert itself never gains execution authority.
