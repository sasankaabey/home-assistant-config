# Task Queue

Split tasks across agents to optimize cost and capability.

## Agent Allocation

| Agent | Best For | Cost Profile |
|-------|----------|--------------|
| **Claude Code** | Server ops, SSH, config validation, debugging, .storage edits | High (use sparingly) |
| **Codex (VS Code)** | Documentation, linting, YAML drafting, PR reviews | Included in ChatGPT plan |
| **ChatGPT** | Quick questions, planning discussions, brainstorming | Included in plan |
| **Perplexity Pro** | Deep research, finding solutions, current docs, citations needed | Pro subscription |
| **Gemini/NotebookLM** | Long document analysis, summarizing large codebases, audio summaries | Free/Pro |
| **Haiku/fast models** | Simple syntax lookups, quick checks | Low |

## Decision Tree

```
Is it a live server operation (SSH, restart, .storage)?
  → Claude Code

Is it documentation, markdown, or text formatting?
  → Codex

Is it YAML drafting (automation, script, blueprint)?
  → Codex drafts → Claude Code validates/deploys

Is it deep research needing citations or current info?
  → Perplexity Pro

Is it analyzing a large doc/codebase or creating summaries?
  → Gemini NotebookLM

Is it a quick question or brainstorming?
  → ChatGPT

Is it a simple syntax lookup?
  → Haiku or ChatGPT

Is it debugging/log analysis requiring server access?
  → Claude Code

Is it code review or PR feedback?
  → Codex (has PR review feature)
```

## Current Tasks

### For Codex (Documentation/Linting)

- [x] Fix 65 markdown linting warnings in HOME_ASSISTANT.md → DEPLOYED
- [ ] Document entity naming conventions (after Perplexity research)

### For Claude Code (Server/Config)

- [ ] (none pending)

### For Perplexity Pro (Deep Research)

- [ ] Research Music Assistant cleanup strategy (39 virtual media players)
  - What do others do? Best practices for large MA installs?
  - Can you disable entity creation without removing MA?
- [ ] Research HA entity naming conventions - what do large installs use?

### For Gemini/NotebookLM (Analysis)

- [ ] Summarize this repo's structure for onboarding new agents
- [ ] Create audio overview of HA config for reference

### For ChatGPT (Quick Questions/Planning)

- [ ] Plan room-by-room entity cleanup approach (after Perplexity research)

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
3. **Perplexity for research** - Get citations and current info before implementation
4. **NotebookLM for large docs** - Upload entire repos/docs for analysis instead of pasting into chat
5. **Haiku for quick checks** - Simple syntax questions don't need expensive models
6. **Avoid context rebuilding** - Keep sessions focused; switching tasks wastes tokens
7. **End sessions at deploy** - Don't let stale context accumulate

## Session Notes

_Use this space to leave notes between sessions/agents_

---
Last updated: 2026-01-14
