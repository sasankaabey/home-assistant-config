# Organization .github Repository Setup

This guide walks you through creating the centralized coordination system for all your repos.

---

## Step 1: Create the Organization .github Repository

1. **Go to GitHub:** https://github.com/orgs/sasankaabey/repositories
2. **Click "New repository"**
3. **Name:** `.github` (exactly this name)
4. **Description:** "Organization-wide multi-agent coordination and workflow documentation"
5. **Public/Private:** Your choice (Private recommended)
6. **Initialize:** Check "Add a README"
7. **Click "Create repository"**

---

## Step 2: Clone and Add Files

```bash
# Clone the new repo
cd ~/
git clone git@github.com:sasankaabey/.github.git
cd .github

# Copy coordination files from ha-config
cp /Users/ankit/ha-config/.org-setup/org-files/* ./

# Add and commit
git add .
git commit -m "Setup: Organization-wide multi-agent coordination system

Created centralized coordination docs:
- AGENTS.md - Agent roles and decision tree
- MULTI_AGENT_WORKFLOW.md - Process documentation
- MULTI_AGENT_ARCHITECTURE.md - System design
- EVOLUTION_LOG.md - Learning and improvements
- HANDOFF_TEMPLATE.md - Agent-to-agent handoffs
- PATTERNS/ - Reusable templates for new repos

All repos will reference these docs for consistency."

git push origin main
```

---

## Step 3: Update ha-config to Reference Org Docs

```bash
cd /Users/ankit/ha-config

# Run the migration script
./migrate_to_org_structure.sh

# Commit changes
git add .
git commit -m "Migrate: Switch to org-level coordination system

Updated to hybrid centralized-local model:
- Created LOCAL_CONTEXT.md (project-specific info)
- Updated TASKS.md to reference org workflows
- Added links to org/.github docs
- Kept local: .vscode, CHANGELOG, DECISIONS
- Removed: Global coordination docs (moved to org)

See org/.github for global workflow documentation."

git push origin main
```

---

## Step 4: Verify Setup

**Check Organization Repo:**
- Visit: https://github.com/sasankaabey/.github
- Verify AGENTS.md, MULTI_AGENT_WORKFLOW.md are there
- README.md shows clear navigation

**Check ha-config Repo:**
- LOCAL_CONTEXT.md exists and describes the project
- TASKS.md references org/.github for process
- .vscode/README.md links to org workflows

**Test Workflow:**
1. Agent clones ha-config
2. Reads LOCAL_CONTEXT.md (understands project)
3. Reads TASKS.md (sees assignment)
4. Follows link to org/.github/AGENTS.md (learns process)
5. Gets to work

---

## Step 5: Template for New Repos

When creating a new repo:

1. Copy from org/.github/PATTERNS/NEW_REPO_TEMPLATE/
2. Customize LOCAL_CONTEXT.md for your project
3. Start adding tasks to TASKS.md
4. Agents automatically use org/.github workflows

**Time to set up new repo:** ~5 minutes

---

## What Goes Where?

### Organization .github (Centralized - Update Once)
- ✅ AGENTS.md - Which agent for what task
- ✅ MULTI_AGENT_WORKFLOW.md - How to execute tasks
- ✅ MULTI_AGENT_ARCHITECTURE.md - System design
- ✅ EVOLUTION_LOG.md - What improved over time
- ✅ HANDOFF_TEMPLATE.md - Agent-to-agent handoffs
- ✅ PATTERNS/ - Templates and reusable patterns

### Each Repo (Local - Project-Specific)
- ✅ LOCAL_CONTEXT.md - What this project is
- ✅ TASKS.md - What to work on
- ✅ CHANGELOG.md - What changed in this project
- ✅ DECISIONS.md - Decisions specific to this project
- ✅ .vscode/ - Editor config for this project
- ✅ Links/references to org/.github

---

## Benefits

**For You:**
- Update workflow once → applies to all repos
- Track improvements in EVOLUTION_LOG.md
- Zero ongoing maintenance per repo
- Focus on building, not documentation

**For Agents:**
- Find everything needed in each repo
- Reference fresh workflows from org
- Contribute improvements to EVOLUTION_LOG
- Never learn a new process per repo

**For Evolution:**
- Better patterns captured globally
- All repos benefit from improvements
- Transparent learning over time
- Scales to unlimited repos

---

## Next Steps

1. Create org/.github repo on GitHub
2. Run setup commands above
3. Test with one task on ha-config
4. Create next repo using template
5. Watch improvements accumulate in EVOLUTION_LOG.md

**Estimated Time:** 30 minutes total
