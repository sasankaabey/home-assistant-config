# Ha-Config Project Context

**Quick Reference:** This is what you need to know to work on this project.

---

## 🎯 **What Is This?**

Home Assistant configuration for a 5-person household with extensive smart home automation, voice control (Alexa, Siri, Google), and multi-platform device support (iOS, Android).

**Server:** 192.168.4.141 (minipc running HA OS)  
**Local Dev:** `/Users/ankit/ha-config`  
**Server Path:** `/config`

---

## 🏗️ **Tech Stack**

- **Core:** Home Assistant OS + YAML configuration
- **Custom Components:** 23+ integrations (Tuya, Tesla, Eufy, Music Assistant, etc.)
- **Automations:** Split by category in `automations/` directory
- **Deployment:** Rsync via `./sync_to_ha.sh` → restart HA
- **Version Control:** Git (this repo)

---

## 📂 **Key Files & Folders**

| Path | Purpose |
|------|---------|
| `configuration.yaml` | Core HA config (rarely edited) |
| `light_groups.yaml` | YAML-based light groups (version controlled) |
| `automations/` | Manual YAML automations (split by category) |
| `automations.yaml` | UI-created automations |
| `scripts.yaml` | Reusable action sequences |
| `scenes.yaml` | Scene definitions |
| `template.yaml` | Computed sensors, binary sensors, switches |
| `inputs/` | Helper definitions (input_select, text, boolean, etc.) |
| `custom_components/` | 23+ custom integrations |
| `CHANGELOG.md` | What changed in this project |
| `DECISIONS.md` | Architecture decisions for this project |
| `TASKS.md` | Current task queue |

---

## 🎨 **Project-Specific Conventions**

### Entity Naming
**Format:** `[domain].[location]_[description]`

**Examples:**
- `light.living_room_ceiling`
- `switch.bedroom_nightstand_left`
- `sensor.kitchen_temperature`

**Rules:**
- Use `snake_case` (spaces → underscores)
- Include location prefix for grouping
- Use descriptive, discoverable names
- No generic names like `light_1`, `device_2`

### Light Groups
- Defined in `light_groups.yaml` using `platform: group`
- Entity IDs MUST match exactly what's in the entity registry
- Changes require HA restart to apply
- Groups fail silently if entity IDs are wrong

### Notify Groups
- Defined in `configuration.yaml` under `notify:`
- Service names are auto-generated slugs from device names
- Example: Device "Ankit's iPhone" → `mobile_app_ankit_s_iphone`

---

## 🚀 **Deployment Process**

### Standard Workflow

```bash
# 1. Validate YAML locally
python3 -c "import yaml; yaml.safe_load(open('automations/file.yaml'))"

# 2. Sync to server
./sync_to_ha.sh

# 3. Restart HA (via UI or SSH)
ssh root@192.168.4.141 'ha core restart'

# 4. Check logs for errors
ssh root@192.168.4.141 'ha logs follow'

# 5. Test functionality
# - Check HA UI for new entities
# - Test via voice command (Alexa, Siri, Google)
# - Verify in logs
```

### Entity Registry Edits (Special Case)

When editing `.storage/core.entity_registry`:

```bash
ssh root@192.168.4.141
ha core stop
# Edit .storage/core.entity_registry
ha core start  # NOT restart — crucial!
```

**Why?** `ha core restart` overwrites uncommitted `.storage` changes.

---

## ⚠️ **Critical Gotchas**

1. **Light groups fail silently** if entity IDs don't exist in registry
2. **Notify groups break** if service names don't match mobile app services
3. **Stop/Start beats Restart** when editing `.storage` files
4. **Entity name changes break automations** — Track in `entity_rename_map.json`
5. **Custom component patches are lost on update** — Re-apply and document in CHANGELOG
6. **Tuya devices** are auto-discovered from cloud config
7. **Music Assistant** creates 39 virtual media players (can clutter entity list)

---

## 📋 **Common Tasks**

### Add New Automation
1. Create `automations/[category]/automation_name.yaml`
2. Follow existing patterns in that category
3. Validate YAML: `python3 -c "import yaml; yaml.safe_load(open('file.yaml'))"`
4. Deploy via `./sync_to_ha.sh`
5. Restart HA and test
6. Update `CHANGELOG.md`

### Add New Light Group
1. Edit `light_groups.yaml`
2. Verify entity IDs exist in registry: `ssh root@192.168.4.141 'cat /config/.storage/core.entity_registry | grep entity_id'`
3. Deploy via `./sync_to_ha.sh`
4. Restart HA (required for light groups)
5. Test: "Alexa, turn on [group name]"

### Fix Broken Entity
1. SSH to server: `ssh root@192.168.4.141`
2. Check entity registry: `cat /config/.storage/core.entity_registry | grep [entity_id]`
3. If missing, restore via `ha core stop`, edit registry, `ha core start`
4. Test functionality

---

## 🔗 **External References**

### Organization-Level Documentation
For workflow, agent roles, and process:
- **Agent Roles:** [org/.github/AGENTS.md](https://github.com/sasankaabey/.github/blob/main/AGENTS.md)
- **Workflow Process:** [org/.github/MULTI_AGENT_WORKFLOW.md](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md)
- **System Design:** [org/.github/MULTI_AGENT_ARCHITECTURE.md](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_ARCHITECTURE.md)
- **Improvements:** [org/.github/EVOLUTION_LOG.md](https://github.com/sasankaabey/.github/blob/main/EVOLUTION_LOG.md)

### Project-Specific Documentation
- **What to work on:** [TASKS.md](TASKS.md)
- **What changed:** [CHANGELOG.md](CHANGELOG.md)
- **Why decisions were made:** [DECISIONS.md](DECISIONS.md)
- **Detailed HA setup:** [HOME_ASSISTANT.md](HOME_ASSISTANT.md)
- **Server operations:** [.github/copilot-instructions.md](.github/copilot-instructions.md)

---

## 🤖 **For Agents**

### Starting Work
1. Read this file (you're doing it now!)
2. Check [TASKS.md](TASKS.md) for your assignment
3. Reference [org/.github/AGENTS.md](https://github.com/sasankaabey/.github/blob/main/AGENTS.md) for your role
4. Follow [org/.github/MULTI_AGENT_WORKFLOW.md](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md)

### Role-Specific Docs
- **Codex:** [HOME_ASSISTANT.md](HOME_ASSISTANT.md) + [DECISIONS.md](DECISIONS.md)
- **Claude Code:** [.github/copilot-instructions.md](.github/copilot-instructions.md)
- **Perplexity:** [DECISIONS.md](DECISIONS.md) for context

### Completing Work
1. Update [TASKS.md](TASKS.md) with results
2. Update [CHANGELOG.md](CHANGELOG.md) if user-facing change
3. Make clear git commit
4. If you improved the process, document in [org/.github/EVOLUTION_LOG.md](https://github.com/sasankaabey/.github/blob/main/EVOLUTION_LOG.md)

---

## 📊 **Project Stats**

- **Custom Components:** 23+
- **Automations:** ~20 (split across categories)
- **Light Groups:** ~15 (version controlled in YAML)
- **Entities:** 300+ (includes virtual entities from Music Assistant)
- **Active Users:** 5 people in household
- **Voice Platforms:** Alexa, Siri, Google Assistant
- **Mobile Platforms:** iOS (3 devices), Android (2 devices)

---

## 🎓 **Quick Start Summary**

1. **Understand the project:** Read this file (done!)
2. **Check your assignment:** [TASKS.md](TASKS.md)
3. **Learn the process:** [org/.github/MULTI_AGENT_WORKFLOW.md](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_WORKFLOW.md)
4. **Do your work:** Follow conventions above
5. **Deploy safely:** Validate → Sync → Restart → Test
6. **Document results:** Update TASKS.md, CHANGELOG.md
7. **Share improvements:** Update [org/.github/EVOLUTION_LOG.md](https://github.com/sasankaabey/.github/blob/main/EVOLUTION_LOG.md)

**Time to be productive:** ~10 minutes of reading this file + checking TASKS.md

---

**You now have everything needed to work on this project. Start with [TASKS.md](TASKS.md) to see what needs to be done!**
