# Architecture Decisions

Record of significant decisions and trade-offs for this Home Assistant configuration.

## Format

Each decision follows this template:

```
### [Short Title]
**Date:** YYYY-MM-DD
**Status:** Accepted / Superseded / Deprecated
**Context:** What prompted this decision?
**Decision:** What did we decide?
**Alternatives Considered:** What else was evaluated?
**Consequences:** What are the trade-offs?
```

---

## Decisions

### YAML-Based Light Groups Over UI Groups

**Date:** 2026-01-13
**Status:** Accepted

**Context:** Needed reliable light groups for voice control across Alexa/Siri/Google. UI-created groups weren't version controlled and had sync issues.

**Decision:** Define all light groups in `light_groups.yaml` using `platform: group`.

**Alternatives Considered:**

- UI-created groups (rejected: not version controlled)
- Template lights (rejected: overkill for simple grouping)
- Scenes (rejected: not suitable for on/off/dim control)

**Consequences:**

- (+) Version controlled, reproducible
- (+) Consistent across HA restarts
- (-) Requires manual sync to server
- (-) Must restart HA to apply changes

---

### Notify Groups for Family Alerts

**Date:** 2026-01-14
**Status:** Accepted

**Context:** Litterbot and other automations needed to notify multiple family members. Individual service calls were repetitive.

**Decision:** Create `notify.adults` group in configuration.yaml targeting mobile app services.

**Alternatives Considered:**

- Individual notify calls per person (rejected: verbose, hard to maintain)
- Script that loops through people (rejected: unnecessary complexity)

**Consequences:**

- (+) Single service call notifies all adults
- (+) Easy to add/remove members
- (-) Service names use slugified device names, must update if device changes

---

### Stop/Start vs Restart for Registry Edits

**Date:** 2026-01-14
**Status:** Accepted

**Context:** Entity registry edits via `.storage/core.entity_registry` were being overwritten on restart.

**Decision:** Always use `ha core stop` then `ha core start` (not `ha core restart`) when editing storage files.

**Alternatives Considered:**

- Edit via UI only (rejected: some operations not possible in UI)
- Restart and hope (rejected: unreliable)

**Consequences:**

- (+) Registry changes persist reliably
- (-) Slightly longer downtime than restart
- (-) Must remember this non-obvious requirement

---

### Multi-Agent Task Distribution

**Date:** 2026-01-14
**Status:** Accepted

**Context:** Spending too much on a single AI service. Multiple services available with unused capacity.

**Decision:** Distribute work across agents by capability:

| Agent | Use For |
|-------|---------|
| Claude Code | Server ops, SSH, debugging, .storage edits |
| Codex (VS Code) | Documentation, linting, YAML drafting |
| ChatGPT | Quick questions, planning discussions |
| Perplexity Pro | Deep research, finding solutions, citations |
| Gemini/NotebookLM | Long document analysis, summarization |
| Haiku/cheap models | Simple syntax lookups |

**Alternatives Considered:**

- Single agent for everything (rejected: expensive, context bloat)
- Manual work (rejected: slower, error-prone)

**Consequences:**

- (+) Cost optimization across subscriptions
- (+) Each agent used for its strengths
- (-) Requires handoff coordination via TASKS.md
- (-) Context must be transferred via files, not chat

---

## Pending Decisions

### Music Assistant Strategy

**Status:** Needs Research

**Context:** 39 virtual media players from Music Assistant cluttering entity list.

**Options to Evaluate:**

1. Disable Music Assistant entirely
2. Keep but hide entities
3. Reduce to essential players only

**Assigned To:** Perplexity Pro (research) → ChatGPT (plan) → Claude Code (implement)

---

### Tuya Light Renaming

**Status:** Needs Planning

**Context:** 8 RGBCW lights have non-descriptive names.

**Blocked By:** Need to decide naming convention first.

**Assigned To:** Codex (document naming convention) → Claude Code (rename via registry)

---
