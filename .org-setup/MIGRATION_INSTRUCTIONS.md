# Migration Instructions: Single Repo → Org-Wide Multi-Agent System

This guide will help you transition from the ha-config single-repo setup to the organization-wide hybrid model.

## Overview

**What's changing:**
- Global docs (AGENTS.md, MULTI_AGENT_WORKFLOW.md, etc.) → Moving to org/.github
- Local docs (LOCAL_CONTEXT.md, TASKS.md) → Stay in ha-config, updated to reference org
- Benefits: Update workflow once → applies to all repos, zero ongoing maintenance per repo

**Time required:** ~30 minutes total

---

## Phase 1: Create Organization Repository (10 min)

### Step 1: Create the org/.github repo on GitHub

```bash
# On GitHub web UI:
1. Go to: https://github.com/organizations/sasankaabey/repositories/new
2. Repository name: .github
3. Description: "Organization-wide multi-agent coordination system"
4. Visibility: Public (or Private if you prefer)
5. Initialize with: README
6. Click "Create repository"
```

### Step 2: Clone and populate org/.github

```bash
# Clone the new org repo
cd ~
git clone git@github.com:sasankaabey/.github.git
cd .github

# Copy coordination files from ha-config
cp /Users/ankit/ha-config/.org-setup/org-files/AGENTS.md ./
cp /Users/ankit/ha-config/.org-setup/org-files/MULTI_AGENT_WORKFLOW.md ./
cp /Users/ankit/ha-config/.org-setup/org-files/MULTI_AGENT_ARCHITECTURE.md ./
cp /Users/ankit/ha-config/.org-setup/org-files/HANDOFF_TEMPLATE.md ./
cp /Users/ankit/ha-config/.org-setup/org-files/EVOLUTION_LOG.md ./
cp /Users/ankit/ha-config/.org-setup/org-files/README.md ./

# Copy PATTERNS directory
cp -r /Users/ankit/ha-config/.org-setup/org-files/PATTERNS ./

# Commit and push
git add .
git commit -m "Setup: Initialize org-wide multi-agent coordination

Added:
- AGENTS.md (agent roles and routing)
- MULTI_AGENT_WORKFLOW.md (process)
- MULTI_AGENT_ARCHITECTURE.md (design)
- EVOLUTION_LOG.md (improvement tracking)
- HANDOFF_TEMPLATE.md (handoff format)
- PATTERNS/ (reusable templates)

All sasankaabey repos can now reference these docs."

git push origin main
```

### Step 3: Verify org repo

Check these URLs work:
- https://github.com/sasankaabey/.github/blob/main/AGENTS.md
- https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md
- https://github.com/sasankaabey/.github/blob/main/PATTERNS/NEW_REPO_SETUP_GUIDE.md

✅ If you can see the docs, Phase 1 is complete!

---

## Phase 2: Migrate ha-config (10 min)

### Step 4: Run migration script

```bash
cd /Users/ankit/ha-config

# Run the migration script (backs up files, updates references)
./migrate_to_org_structure.sh

# Review changes
git status
git diff TASKS.md
cat .vscode/README.md

# Verify LOCAL_CONTEXT.md exists
cat LOCAL_CONTEXT.md
```

**What the script does:**
- ✅ Backs up old files to `.migration-backup/`
- ✅ Updates TASKS.md to reference org/.github
- ✅ Creates .vscode/README.md with org links
- ✅ Moves global docs to archive
- ✅ Creates MIGRATION_SUMMARY.md

### Step 5: Commit migration

```bash
git add .
git commit -m "Migrate: Switch to org-level coordination

Changes:
- Updated TASKS.md to reference org/.github docs
- Created .vscode/README.md linking to org workflows
- Moved global docs to .migration-backup/ (now in org/.github)
- LOCAL_CONTEXT.md contains ha-config specific context

All workflow docs now centralized at:
https://github.com/sasankaabey/.github

Benefits:
- Update workflow once → applies to all repos
- Zero ongoing maintenance for ha-config
- Process improvements captured globally"

git push origin main
```

### Step 6: Verify migration

**Check these files:**
- [x] LOCAL_CONTEXT.md exists (project-specific)
- [x] TASKS.md updated with org/.github links
- [x] .vscode/README.md exists
- [x] Old AGENTS.md, MULTI_AGENT_WORKFLOW.md moved to .migration-backup/
- [x] MIGRATION_SUMMARY.md created

**Test workflow:**
1. Open TASKS.md → Click link to org/.github/AGENTS.md
2. Should open GitHub to organization docs
3. If link works, migration successful!

✅ Phase 2 complete!

---

## Phase 3: Apply to Other Repos (5 min per repo)

For each additional repo in sasankaabey org:

### Quick setup (2 commands)

```bash
cd ~/[other-repo]

# Copy templates
cp ~/sasankaabey/.github/PATTERNS/NEW_REPO_TEMPLATE/LOCAL_CONTEXT_TEMPLATE.md ./LOCAL_CONTEXT.md
cp ~/sasankaabey/.github/PATTERNS/NEW_REPO_TEMPLATE/TASKS_TEMPLATE.md ./TASKS.md

# Customize LOCAL_CONTEXT.md (5 min)
code LOCAL_CONTEXT.md

# Add initial tasks
code TASKS.md

# Commit
git add .
git commit -m "Setup: Initialize multi-agent coordination"
git push origin main
```

### Detailed setup

See [org/.github/PATTERNS/NEW_REPO_SETUP_GUIDE.md](org-files/PATTERNS/NEW_REPO_SETUP_GUIDE.md)

✅ Each repo now benefits from centralized workflow!

---

## Phase 4: Maintenance (Ongoing)

### Per Repo (Local Work)
- Update TASKS.md as work progresses
- Update LOCAL_CONTEXT.md if project changes
- Add CHANGELOG.md for user-facing changes
- Add DECISIONS.md for architecture decisions

**Time:** Ongoing as needed (natural part of development)

### Organization-Wide (Benefits Everyone)
- Update org/.github docs when process improves
- Document improvements in EVOLUTION_LOG.md
- All repos benefit automatically (they link to central docs)

**Time:** ~5 min per improvement, applies to ALL repos

---

## Rollback Procedure

If you need to revert ha-config to pre-migration state:

```bash
cd /Users/ankit/ha-config

# Restore old files
cp .migration-backup/moved-to-org/* ./

# Remove new files
rm LOCAL_CONTEXT.md
rm .vscode/README.md
rm MIGRATION_SUMMARY.md

# Restore TASKS.md backup
cp .migration-backup/TASKS.md ./

# Commit rollback
git add .
git commit -m "Rollback: Restore pre-migration structure"
git push origin main
```

---

## Verification Checklist

After migration, verify:

### Organization Repository
- [ ] sasankaabey/.github exists on GitHub
- [ ] AGENTS.md accessible at https://github.com/sasankaabey/.github/blob/main/AGENTS.md
- [ ] MULTI_AGENT_WORKFLOW.md accessible
- [ ] PATTERNS/ directory exists with templates
- [ ] README.md explains hybrid model

### ha-config Repository
- [ ] LOCAL_CONTEXT.md exists (project-specific)
- [ ] TASKS.md updated with org/.github links
- [ ] .vscode/README.md exists
- [ ] Old global docs in .migration-backup/
- [ ] MIGRATION_SUMMARY.md created
- [ ] Links to org/.github work (click and verify)

### Workflow Test
- [ ] Agent clones ha-config
- [ ] Reads LOCAL_CONTEXT.md → understands project
- [ ] Opens TASKS.md → sees assignment
- [ ] Clicks link to org/.github/AGENTS.md → learns role
- [ ] Follows org/.github/MULTI_AGENT_WORKFLOW.md → executes work
- [ ] No confusion or broken links

---

## Success Criteria

**You know migration succeeded when:**

1. ✅ org/.github repo exists and is accessible
2. ✅ ha-config TASKS.md links to org docs
3. ✅ Clicking those links opens GitHub to org docs
4. ✅ LOCAL_CONTEXT.md describes ha-config project
5. ✅ New repos can be set up in 15 minutes using templates
6. ✅ Agents understand workflow by reading org docs
7. ✅ You can improve process once → applies everywhere

**ROI:** 30 min setup → Infinite repos benefit from centralized workflow

---

## Troubleshooting

**Problem:** Links to org/.github return 404

**Solution:**
- Verify org repo is public (or you're logged in to GitHub)
- Check URL format: `https://github.com/sasankaabey/.github/blob/main/AGENTS.md`
- Ensure files pushed to main branch: `cd ~/sasankaabey/.github && git status`

**Problem:** Can't create .github repo in org

**Solution:**
- Ensure you have admin access to sasankaabey org
- Try creating from org settings: https://github.com/organizations/sasankaabey/repositories/new
- Contact org owner if needed

**Problem:** Migration script fails

**Solution:**
- Check you're in ha-config directory: `pwd` should show `/Users/ankit/ha-config`
- Verify script is executable: `chmod +x migrate_to_org_structure.sh`
- Read error message, most common: missing configuration.yaml means wrong directory

**Problem:** Agents confused about where to find docs

**Solution:**
- Update TASKS.md header to clearly link to org/.github
- Add note to README.md with links
- Use HANDOFF_TEMPLATE.md to explicitly reference org docs
- Create .vscode/README.md if missing

---

## Next Steps

After successful migration:

1. **Test with real work** — Assign a task to an agent, verify workflow
2. **Document improvements** — As you discover better ways, update org/.github and log in EVOLUTION_LOG.md
3. **Migrate other repos** — Use NEW_REPO_SETUP_GUIDE.md for each repo
4. **Enjoy zero maintenance** — Workflow updates apply to all repos automatically

## Questions?

- **Do I need to re-migrate if org docs change?** No! That's the whole point. Links point to live docs.
- **Can I customize workflow per repo?** Yes, add project-specific notes to LOCAL_CONTEXT.md
- **What if I want private process docs?** Make org/.github repo private
- **How do I suggest workflow improvements?** Update org/.github docs + log in EVOLUTION_LOG.md

---

**Ready? Start with Phase 1!**
