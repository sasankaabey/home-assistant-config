# Multi-Agent VS Code Workspace Setup

Complete VS Code configuration optimized for coordinating multiple AI agents to work efficiently on the Home Assistant configuration project.

---

## 📦 What's Included

### Configuration Files
- **`.vscode/settings.json`** — Editor formatting, YAML/Python/Markdown rules, extensions
- **`.vscode/extensions.json`** — Recommended extensions (YAML, Python, Git, SSH, etc.)
- **`.vscode/launch.json`** — SSH remote connection to HA server
- **`.vscode/tasks.json`** — Quick launch tasks (sync, validate, SSH, logs)
- **`.editorconfig`** — Consistent formatting across team

### Coordination Documents
- **[CONTEXT.md](CONTEXT.md)** — 2-minute quick reference for any agent starting a task
- **[AGENTS.md](AGENTS.md)** — Which agent handles which work + decision tree
- **[MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md)** — Complete workflow process + examples
- **[TASKS.md](TASKS.md)** — Current task queue and agent assignments

### PR & Deployment
- **[.github/pull_request_template.md](.github/pull_request_template.md)** — PR structure for handoffs
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** — SSH ops and deployment

---

## 🚀 Quick Start for Agents

### First Time Setup (One Agent, One Time)

1. **Clone repo:**
   ```bash
   git clone <repo-url> /Users/ankit/ha-config
   cd /Users/ankit/ha-config
   ```

2. **Open in VS Code:**
   ```bash
   code .
   ```

3. **Install recommended extensions:**
   - VS Code will prompt: "Do you want to install the recommended extensions?"
   - Click "Install All"

### Every Time an Agent Starts Work

1. **Read these in order (takes 5-10 minutes total):**
   - [CONTEXT.md](CONTEXT.md) — 2-minute quick ref
   - [AGENTS.md](AGENTS.md) — Your role
   - [TASKS.md](TASKS.md) — Your assignment
   - Relevant docs:
     - **Codex:** [HOME_ASSISTANT.md](HOME_ASSISTANT.md)
     - **Claude Code:** [.github/copilot-instructions.md](.github/copilot-instructions.md)
     - **Perplexity:** [DECISIONS.md](DECISIONS.md)

2. **Pull latest code:**
   ```bash
   git pull origin main
   ```

3. **Make starting commit:**
   ```bash
   git commit -m "Task: [Name] - Starting (Agent: [Your Name])"
   ```

4. **Do your work** (30-90 minutes typically)

5. **Make completion commit:**
   ```bash
   git add .
   git commit -m "Task: [Name] - Complete

   [Summary of what was done]
   
   Next: [Next Agent] to [next action]"
   ```

6. **Update [TASKS.md](TASKS.md)** with results

---

## 🛠️ VS Code Features

### Keyboard Shortcuts

| Command | Windows/Linux | Mac |
|---------|---------------|-----|
| Command palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Find in files | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Source control | `Ctrl+Shift+G` | `Cmd+Shift+G` |
| Terminal | `Ctrl+`` | `Ctrl+`` |
| Format document | `Shift+Alt+F` | `Shift+Option+F` |

### Quick Tasks (Cmd+Shift+P, type task name)

- **sync_to_ha** — Sync YAML files to 192.168.4.141
- **validate_yaml** — Check YAML syntax without deploying
- **ssh_to_server** — SSH directly to HA server
- **check_ha_status** — Quick status check
- **view_ha_logs** — Tail HA logs live

### File Format

| Type | Rule |
|------|------|
| YAML | 2-space indent, auto-format on save |
| Markdown | Word wrap on, 80-120 char rulers |
| Python | 4-space indent, black formatting |
| JSON | 2-space indent |

### Extensions Installed

| Extension | Purpose |
|-----------|---------|
| Red Hat YAML | YAML validation and HA schema support |
| Prettier | Code formatting (YAML, Markdown, JSON) |
| Python | Python development and linting |
| Ruff | Python linter |
| Remote SSH | SSH to HA server |
| Error Lens | Inline error display |
| GitLens | Git history and blame |
| GitHub Copilot | AI coding assistance |
| Git Graph | Visual git history |

---

## 📋 Task Workflow

### Creating a New Task

1. **Add entry to [TASKS.md](TASKS.md):**
   ```markdown
   ### Task Name
   **Status:** Not Started
   **Agent:** [Who should do this?]
   **Description:** [1-2 sentence summary]
   **Acceptance Criteria:** [How do we know it's done?]
   ```

2. **Use [AGENTS.md](AGENTS.md) decision tree** to select the right agent

3. **Commit the task:**
   ```bash
   git add TASKS.md
   git commit -m "Plan: Task Name - Added to task queue"
   ```

### Agent Works on Task

1. **Read context docs** (see "Every Time an Agent Starts Work" above)

2. **Check out branch (optional but recommended):**
   ```bash
   git checkout -b task/task-name
   ```

3. **Do focused work** (30-90 minutes per session)

4. **Commit frequently:**
   ```bash
   git commit -m "Task: [Name] - [Checkpoint description]"
   ```

5. **Update [TASKS.md](TASKS.md)** with progress

### Agent Completes Task

1. **Mark complete in [TASKS.md](TASKS.md):**
   ```markdown
   **Status:** Complete (Agent Name)
   **Deliverables:** [What did you make?]
   **Next:** [Who's next?]
   ```

2. **Make final commit:**
   ```bash
   git add .
   git commit -m "Task: [Name] - Complete

   Codex completed:
   - automations/lighting/example.yaml
   - Updated CHANGELOG.md
   
   Ready for: Claude Code deployment"
   ```

3. **Merge to main (if using branch):**
   ```bash
   git switch main
   git merge task/task-name
   ```

---

## 📡 Server Integration

### Before First SSH

1. **Add SSH key to server (if needed):**
   ```bash
   ssh-copy-id -i ~/.ssh/id_rsa root@192.168.4.141
   ```

2. **Test connection:**
   ```bash
   ssh root@192.168.4.141 'ha core status'
   ```

### Quick Server Commands

**Via VS Code terminal (Ctrl+`` or Cmd+``):**
```bash
# Deploy changes
./sync_to_ha.sh

# SSH to server
ssh root@192.168.4.141

# Restart HA
ssh root@192.168.4.141 'ha core restart'

# Check logs
ssh root@192.168.4.141 'ha logs follow'
```

**Common HA CLI commands:**
```bash
ha core status        # Check if HA is running
ha core start         # Start HA
ha core stop          # Stop HA
ha core restart       # Restart HA
ha logs follow        # Tail logs live
```

---

## 🔐 Git Workflow

### Branching Strategy

- **main** — Production (always deployable)
- **task/feature-name** — Feature branches (optional, good for complex work)

### Commit Message Format

```
Task: [Task Name] - [Action/Status]

[Detailed explanation of what was done, why, and what's next]

See TASKS.md for full context.
```

### Example Commits

```bash
# Starting a task
git commit -m "Task: Sunset dimming - Starting"

# Checkpoint during work
git commit -m "Task: Sunset dimming - Drafted automation"

# Completing and handing off
git commit -m "Task: Sunset dimming - Ready for deployment

Codex created automations/lighting/sunset_dimming.yaml
Updated light_groups.yaml with sunset_lights group

Next: Claude Code to validate and deploy to 192.168.4.141"
```

### Useful Git Commands

```bash
# See what changed
git status
git diff

# View history
git log --oneline -10
git show <commit-hash>

# Switch branches
git checkout -b task/new-feature
git switch main

# Merge completed work
git merge task/feature-name

# Undo last commit (keep changes)
git reset --soft HEAD~1

# See who changed each line
git blame <filename>
```

---

## 🎯 Multi-Agent Coordination Examples

### Example 1: Simple Feature

**Day 1 - Plan & Draft (Codex):**
1. Read [CONTEXT.md](CONTEXT.md)
2. Check [TASKS.md](TASKS.md)
3. Draft `automations/lighting/example.yaml`
4. Update [TASKS.md](TASKS.md): "Ready for Claude Code"
5. Commit: "Task: Example - Ready for deployment"

**Day 2 - Deploy (Claude Code):**
1. Read [CONTEXT.md](CONTEXT.md)
2. Pull latest: `git pull`
3. Validate YAML
4. Run `./sync_to_ha.sh`
5. Test on server
6. Commit: "Task: Example - Deployed and tested"

### Example 2: Research + Code

**Day 1 - Research (Perplexity):**
1. Find best practices for integrating new device
2. Document findings in new `.md` file
3. Commit: "Research: Integration approach"

**Day 2 - Draft (Codex):**
1. Read research findings
2. Draft automation/script based on findings
3. Commit: "Draft: Automation for new device"

**Day 3 - Deploy (Claude Code):**
1. Validate and deploy
2. Commit: "Deployed: New device integration live"

---

## 🐛 Troubleshooting

### YAML Format Issues

**Problem:** "I see red squiggly lines in my YAML"

**Solution:**
1. Install "Red Hat YAML" extension (check Extensions panel)
2. File → Preferences → Settings
3. Search "yaml.schemas"
4. Add Home Assistant schema: `https://github.com/home-assistant/home-assistant.io/blob/master/source/_integrations/homeassistant/manifest.json`

### SSH Connection Fails

**Problem:** "Permission denied" when trying to SSH

**Solution:**
1. Test locally: `ssh root@192.168.4.141 'echo test'`
2. Add SSH key: `ssh-copy-id -i ~/.ssh/id_rsa root@192.168.4.141`
3. Try again

### Sync Fails

**Problem:** "`./sync_to_ha.sh` fails or files don't appear on server"

**Solution:**
1. Check connection: `ping 192.168.4.141`
2. Check script permissions: `chmod +x sync_to_ha.sh`
3. Run manually: `rsync -avz ./ root@192.168.4.141:/config/`

### Git Conflicts

**Problem:** "Conflict when merging branches"

**Solution:**
1. VS Code will highlight conflicts
2. Choose "Accept Incoming" (server version) or "Accept Current" (your version)
3. Manually review if needed
4. Save and commit: `git add . && git commit -m "Merge: Resolved conflict"`

---

## 📚 Documentation Structure

| Document | Read When | Notes |
|----------|-----------|-------|
| [CONTEXT.md](CONTEXT.md) | Starting any task | 2-minute quick ref for all agents |
| [AGENTS.md](AGENTS.md) | Routing a task | Decide which agent handles work |
| [MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md) | Full workflow details | Step-by-step instructions + examples |
| [HOME_ASSISTANT.md](HOME_ASSISTANT.md) | YAML work (Codex) | Entity conventions, automation patterns |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Server ops (Claude Code) | SSH, deployment, debugging |
| [DECISIONS.md](DECISIONS.md) | Context on why decisions were made | References, rationale |
| [CHANGELOG.md](CHANGELOG.md) | Recent changes, users reading updates | What's new, what broke |
| [TASKS.md](TASKS.md) | Your current assignment | Always check before starting |

---

## 💡 Pro Tips

### 1. Use VS Code's Built-In Git
- **Cmd+Shift+G** (Mac) or **Ctrl+Shift+G** (Windows/Linux)
- Stage files, write commit messages, push all from sidebar
- No terminal needed for basic git work

### 2. Format on Save
- Enable in settings: `"editor.formatOnSave": true`
- YAML and Markdown auto-format when you save
- No manual cleanup needed

### 3. Open VS Code from Terminal
```bash
cd /Users/ankit/ha-config
code .
```

### 4. Quick File Search
- **Cmd+P** (Mac) or **Ctrl+P** (Windows/Linux)
- Type filename: "light_groups.yaml"
- Jump to any file instantly

### 5. Search in Files
- **Cmd+Shift+F** (Mac) or **Ctrl+Shift+F** (Windows/Linux)
- Search all .yaml files for "motion"
- Find all references to entity names

### 6. Integrated Terminal
- **Ctrl+`` ** (backtick)
- Run git, sync, SSH commands without leaving VS Code
- Output stays in side panel

---

## 📞 Support

### Issues with Setup?
1. Check [CONTEXT.md](CONTEXT.md) quick ref section
2. Review [copilot-instructions.md](.github/copilot-instructions.md) for server issues
3. Check VS Code Extensions panel (should see recommended extensions)
4. Try rebuilding: Close VS Code, delete `.vscode` folder, reopen

### Questions About Process?
1. Check [AGENTS.md](AGENTS.md) decision tree
2. Review [MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md) examples
3. Look at recent git commits for patterns

---

## Next Steps

1. **Review these docs in order:**
   - [CONTEXT.md](CONTEXT.md) — 2 minutes
   - [AGENTS.md](AGENTS.md) — 5 minutes
   - [MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md) — 10 minutes

2. **Install recommended extensions:**
   - Cmd+Shift+P → "Extensions: Install Recommended Extensions"

3. **Test connection to server:**
   - Open terminal (Ctrl+``)
   - Run: `ssh root@192.168.4.141 'ha core status'`

4. **Review [TASKS.md](TASKS.md)** to see current queue

5. **Start first task!** Follow workflow in [MULTI_AGENT_WORKFLOW.md](MULTI_AGENT_WORKFLOW.md)

---

**Happy building! 🚀**
