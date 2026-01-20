# Quick Context (2-Minute Read)

**Project:** Home Assistant configuration for a 5-person household with Alexa/Siri/Google voice control, custom automations, and multi-platform mobile app support.

**Repository:** `/Users/ankit/ha-config` (local dev) synced to `/config` on HA server at `192.168.4.141` (HA OS on minipc)

---

## The 30-Second Version

- **Config format:** YAML + Python scripts
- **Version control:** Git (this repo)
- **Deployment:** `./sync_to_ha.sh` copies files to server, then restart HA
- **23+ custom components** (Tuya, Tesla, Eufy, Music Assistant, etc.)
- **Multi-agent workflow:** Different agents handle different tasks (see [AGENTS.md](AGENTS.md))

---

## File Map

| Critical File | Purpose |
|---------------|---------|
| **[TASKS.md](TASKS.md)** | Task queue + agent assignments (READ FIRST) |
| **[AGENTS.md](AGENTS.md)** | Which agent does what (task routing) |
| **[HOME_ASSISTANT.md](HOME_ASSISTANT.md)** | Setup guide + entity naming conventions |
| **[.github/copilot-instructions.md](.github/copilot-instructions.md)** | SSH ops, deployment, debugging procedures |
| **[DECISIONS.md](DECISIONS.md)** | Architecture decisions + rationale |
| **[CHANGELOG.md](CHANGELOG.md)** | Recent changes, patches, breaking changes |
| **[configuration.yaml](configuration.yaml)** | Core HA config (rarely edited directly) |
| **[light_groups.yaml](light_groups.yaml)** | All light group definitions (version controlled) |
| **[automations/](automations/)** | Manual YAML automations (split by category) |
| **[inputs/](inputs/)** | Helper definitions (input_select, input_text, etc.) |

---

## Critical Procedures

### Deploy YAML Changes
```bash
./sync_to_ha.sh  # Copies to server
# Then restart HA via UI or: ha core restart
```

### Edit Entity Registry
```bash
ssh root@192.168.4.141
ha core stop
# Edit .storage/core.entity_registry
ha core start  # NOT restart — crucial!
```

### Validate YAML Before Deploy
```bash
python3 -c "import yaml; yaml.safe_load(open('file.yaml'))"
```

---

## Key Gotchas

1. **Light groups fail silently** if entity IDs don't exist in registry
2. **Notify groups fail** if service names don't match mobile app services
3. **Stop/Start beats Restart** when editing `.storage` (restart overwrites changes)
4. **Entity name changes break automations** — Use entity_rename_map.json to track
5. **Custom component patches are lost on update** — Re-apply and document in CHANGELOG

---

## Entity Naming Convention

**Format:** `[domain].[location]_[description]`

**Examples:**
- `light.living_room_ceiling`
- `switch.bedroom_nightstand_left`
- `sensor.kitchen_temperature`

**Rules:** snake_case, location prefix, descriptive names (no `light_1`)

---

## Agent Handoff Checklist

### Outgoing Agent (You're Done)
- [ ] Make git commit: `git commit -m "Task: [X] - Ready for [Agent]"`
- [ ] Update [TASKS.md](TASKS.md): mark as "Ready for [Next Agent]"
- [ ] Update task with "Next Agent: [Name]"
- [ ] Include key context in commit message

### Incoming Agent (You're Starting)
- [ ] Read this file ([CONTEXT.md](CONTEXT.md))
- [ ] Check [TASKS.md](TASKS.md) for your assignment
- [ ] Read relevant docs based on your role:
  - Codex: [HOME_ASSISTANT.md](HOME_ASSISTANT.md) + [DECISIONS.md](DECISIONS.md)
  - Claude Code: [.github/copilot-instructions.md](.github/copilot-instructions.md)
  - Perplexity: [DECISIONS.md](DECISIONS.md) + look for linked sources
- [ ] Review latest git commits for context
- [ ] Make starting commit: `git commit -m "Task: [X] - Starting"`

---

## Server Access

**Host:** 192.168.4.141 (minipc)  
**OS:** Home Assistant OS  
**User:** root  
**HA Config:** /config  
**Storage:** /config/.storage/  

**Login:**
```bash
ssh root@192.168.4.141
```

**HA CLI Tools:**
```bash
ha core status
ha core stop
ha core start
ha core restart
ha logs follow
```

---

## Multi-Agent Task Distribution

**Quick routing table:**

- **Brainstorm/Planning** → ChatGPT
- **YAML Drafting** → Codex
- **Deployment/SSH** → Claude Code
- **Research + Citations** → Perplexity
- **Large Document Analysis** → Gemini
- **Syntax Checks** → Haiku

**Full details:** See [AGENTS.md](AGENTS.md)

---

## Recent Work

Check git log for context:
```bash
git log --oneline -20
```

Check CHANGELOG.md for recent features/fixes.

---

## Questions?

1. **"Should I do X?"** → Check [DECISIONS.md](DECISIONS.md) and [HOME_ASSISTANT.md](HOME_ASSISTANT.md)
2. **"How do I deploy?"** → See [.github/copilot-instructions.md](.github/copilot-instructions.md)
3. **"Who handles this task?"** → See [AGENTS.md](AGENTS.md)
4. **"What's the entity naming rule?"** → It's in this file (scroll up)

---

**Next:** Read [AGENTS.md](AGENTS.md) for full task routing guide, then check [TASKS.md](TASKS.md) for assignments.
