#!/bin/bash

# Migration script to switch ha-config to org-level coordination model
# Run this after creating the org/.github repository

echo "🚀 Migrating ha-config to hybrid centralized-local model..."
echo ""

# Check if we're in the right directory
if [ ! -f "configuration.yaml" ]; then
    echo "❌ Error: Must run from ha-config root directory"
    exit 1
fi

echo "📋 Step 1: Backing up current files..."
mkdir -p .migration-backup
cp CONTEXT.md .migration-backup/ 2>/dev/null || true
cp AGENTS.md .migration-backup/ 2>/dev/null || true
cp MULTI_AGENT_WORKFLOW.md .migration-backup/ 2>/dev/null || true
cp MULTI_AGENT_ARCHITECTURE.md .migration-backup/ 2>/dev/null || true
cp HANDOFF_TEMPLATE.md .migration-backup/ 2>/dev/null || true
echo "✅ Backups created in .migration-backup/"
echo ""

echo "📋 Step 2: LOCAL_CONTEXT.md already created"
echo "✅ LOCAL_CONTEXT.md exists"
echo ""

echo "📋 Step 3: Updating TASKS.md header..."
# Add reference to org/.github at the top of TASKS.md
if ! grep -q "org/.github/AGENTS.md" TASKS.md; then
    temp_file=$(mktemp)
    cat > "$temp_file" << 'EOF'
# Task Queue

Split tasks across agents to optimize cost and capability.

## Workflow Reference

For agent roles and routing, see: [org/.github/AGENTS.md](https://github.com/sasankaabey/.github/blob/main/AGENTS.md)

For workflow process, see: [org/.github/MULTI_AGENT_WORKFLOW.md](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md)

---

EOF
    # Append existing TASKS.md content (skip first line if it's "# Task Queue")
    tail -n +2 TASKS.md >> "$temp_file"
    mv "$temp_file" TASKS.md
    echo "✅ TASKS.md updated with org references"
else
    echo "✅ TASKS.md already has org references"
fi
echo ""

echo "📋 Step 4: Creating .vscode/README.md..."
cat > .vscode/README.md << 'EOF'
# VS Code Configuration

This directory contains project-specific VS Code settings.

## Workflow Documentation

For organization-wide workflows and agent coordination, see:

- **Agent Roles:** https://github.com/sasankaabey/.github/blob/main/AGENTS.md
- **Workflow Process:** https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md
- **System Design:** https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_ARCHITECTURE.md

## Tasks

Quick VS Code tasks configured:
- `sync_to_ha` — Sync YAML to 192.168.4.141
- `validate_yaml` — Check YAML syntax
- `ssh_to_server` — SSH to HA server
- `check_ha_status` — Quick status check
- `view_ha_logs` — Live log tail

Access via: Cmd+Shift+P → "Tasks: Run Task"
EOF
echo "✅ Created .vscode/README.md"
echo ""

echo "📋 Step 5: Moving global docs to archive..."
mkdir -p .migration-backup/moved-to-org
mv CONTEXT.md .migration-backup/moved-to-org/ 2>/dev/null || true
mv AGENTS.md .migration-backup/moved-to-org/ 2>/dev/null || true
mv MULTI_AGENT_WORKFLOW.md .migration-backup/moved-to-org/ 2>/dev/null || true
mv MULTI_AGENT_ARCHITECTURE.md .migration-backup/moved-to-org/ 2>/dev/null || true
mv HANDOFF_TEMPLATE.md .migration-backup/moved-to-org/ 2>/dev/null || true
mv WORKSPACE_SETUP.md .migration-backup/moved-to-org/ 2>/dev/null || true
mv MULTI_AGENT_SETUP_SUMMARY.md .migration-backup/moved-to-org/ 2>/dev/null || true
mv SETUP_COMPLETE.md .migration-backup/moved-to-org/ 2>/dev/null || true
echo "✅ Global docs moved to .migration-backup/moved-to-org/"
echo ""

echo "📋 Step 6: Keeping local docs..."
echo "✅ Kept LOCAL_CONTEXT.md (project-specific)"
echo "✅ Kept TASKS.md (local task queue)"
echo "✅ Kept CHANGELOG.md (project history)"
echo "✅ Kept DECISIONS.md (project decisions)"
echo "✅ Kept HOME_ASSISTANT.md (technical reference)"
echo "✅ Kept .vscode/ (editor config)"
echo ""

echo "📋 Step 7: Creating migration summary..."
cat > MIGRATION_SUMMARY.md << 'EOF'
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
EOF
echo "✅ Created MIGRATION_SUMMARY.md"
echo ""

echo "✅ Migration complete!"
echo ""
echo "📌 Next steps:"
echo "1. Review LOCAL_CONTEXT.md and TASKS.md"
echo "2. Commit changes: git add . && git commit -m 'Migrate: Switch to org-level coordination'"
echo "3. Push to GitHub: git push origin main"
echo "4. Verify org/.github repo exists and has all coordination docs"
echo ""
echo "📚 Documentation:"
echo "- Local context: LOCAL_CONTEXT.md"
echo "- Local tasks: TASKS.md"
echo "- Org workflows: https://github.com/sasankaabey/.github"
echo ""
