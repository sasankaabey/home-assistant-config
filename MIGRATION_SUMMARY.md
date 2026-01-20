# Migration to Org-Level Coordination

**Date:** $(date +%Y-%m-%d)

This repo has been migrated to the hybrid centralized-local model.

## What Changed

### Moved to org/.github (Centralized)
- AGENTS.md → org/.github/AGENTS.md
- MULTI_AGENT_WORKFLOW.md → org/.github/MULTI_AGENT_WORKFLOW.md
- MULTI_AGENT_ARCHITECTURE.md → org/.github/MULTI_AGENT_ARCHITECTURE.md
- EVOLUTION_LOG.md → org/.github/EVOLUTION_LOG.md
- HANDOFF_TEMPLATE.md → org/.github/HANDOFF_TEMPLATE.md

### Kept Local (Project-Specific)
- LOCAL_CONTEXT.md — What this project is
- TASKS.md — What to work on (updated to reference org docs)
- CHANGELOG.md — Project history
- DECISIONS.md — Project decisions
- HOME_ASSISTANT.md — Technical reference
- .vscode/ — Editor config

### Backups
Old files backed up in `.migration-backup/moved-to-org/`

## For Agents

**Start here:**
1. Read [LOCAL_CONTEXT.md](LOCAL_CONTEXT.md) — Understand this project
2. Check [TASKS.md](TASKS.md) — See your assignment
3. Reference [org/.github/AGENTS.md](https://github.com/sasankaabey/.github/blob/main/AGENTS.md) — Learn your role
4. Follow [org/.github/MULTI_AGENT_WORKFLOW.md](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md) — Execute

## Benefits

- ✅ Update workflow once → applies to all repos
- ✅ Zero ongoing maintenance for this repo
- ✅ Process improvements captured globally
- ✅ All repos benefit from improvements
- ✅ Local context stays focused on this project

## Rollback

If you need to rollback:
```bash
cp .migration-backup/moved-to-org/* ./
git add .
git commit -m "Rollback: Restore pre-migration structure"
```
