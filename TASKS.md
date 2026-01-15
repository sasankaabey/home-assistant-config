# Task Queue

Split tasks across agents to optimize cost and capability.

## Agent Allocation

| Agent | Best For | Cost Profile |
|-------|----------|--------------|
| **Claude Code** | Server ops, SSH, config validation, debugging, .storage edits | High (use sparingly) |
| **Codex (VS Code)** | Documentation, linting, YAML drafting, PR reviews | Included in ChatGPT plan |
| **ChatGPT** | Research, explanations, drafting text, planning | Included in plan |
| **Haiku/fast models** | Simple lookups, quick questions, syntax help | Low |

## Decision Tree

```
Is it a live server operation (SSH, restart, .storage)?
  → Claude Code

Is it documentation, markdown, or text formatting?
  → Codex or ChatGPT

Is it YAML drafting (automation, script, blueprint)?
  → Codex drafts → Claude Code validates/deploys

Is it a quick lookup or simple question?
  → ChatGPT or Haiku

Is it debugging/log analysis requiring server access?
  → Claude Code

Is it code review or PR feedback?
  → Codex (has PR review feature)
```

## Current Tasks

### For Codex (Documentation/Linting)

- [x] Fix 65 markdown linting warnings in HOME_ASSISTANT.md
  - MD034: Wrap bare URLs in angle brackets
  - MD032: Add blank lines around lists
  - MD022: Add blank lines before headings
  - → READY FOR DEPLOY
- [ ] Document entity naming conventions
- [ ] Create changelog template for future updates

### For Claude Code (Server/Config)

- [ ] (none pending)

### For ChatGPT (Research/Planning)

- [ ] Research Music Assistant cleanup strategy (39 virtual media players)
- [ ] Plan room-by-room entity cleanup approach

### Completed

- [x] Add VS Code schema comments to suppress false positives
- [x] Document VS Code warnings in HOME_ASSISTANT.md
- [x] Fix litterbot automations YAML format
- [x] Fix notify.adults service names
- [x] Patch tuya_local and openplantbook custom components
- [x] Fix conversation.chatgpt pipeline error

## Handoff Protocol

### Codex → Claude Code

When Codex completes work that needs deployment:

1. Codex commits changes to repo
2. Tag task in this file: `→ READY FOR DEPLOY`
3. Ask Claude Code to: `sync and restart HA`

### Claude Code → Codex

When Claude Code identifies documentation needs:

1. Add task to "For Codex" section
2. Include specific file paths and context
3. Codex picks up on next session

## Cost Optimization Tips

1. **Batch Claude Code requests** - Gather multiple server tasks, handle in one session
2. **Use Codex for iteration** - Documentation often needs multiple passes; let Codex iterate
3. **ChatGPT for research** - Before asking Claude Code to implement, use ChatGPT to research approaches
4. **Haiku for quick checks** - Simple syntax questions, quick lookups don't need expensive models
5. **Avoid context rebuilding** - Keep sessions focused; switching tasks wastes tokens on re-explaining

## Session Notes

_Use this space to leave notes between sessions/agents_

---
Last updated: 2026-01-14
