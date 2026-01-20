# Copilot Instructions for Home Assistant Configuration

## Project Overview

This is a **Home Assistant (HA) smart home configuration** supporting a 5-person household with multi-platform device control (iOS, Android), voice assistants (Alexa, Siri, Google), and extensive custom automation.

**Key Paths:**
- Local dev: `/Users/ankit/ha-config`
- Server: `/config` on minipc (192.168.4.141) running HA OS
- Entity registry: `.storage/core.entity_registry` (JSON, requires special sync procedure)

## Architecture Essentials

### Configuration Structure

HA uses a modular YAML-based configuration with version control:

| Component | Files | Purpose |
|-----------|-------|---------|
| **Core config** | `configuration.yaml` | Integrations, includes, notify groups, logger |
| **Automations** | `automations/` (YAML) + `automations.yaml` (UI) | Both manual YAML and UI-created automations |
| **Scripts & Scenes** | `scripts.yaml`, `scenes.yaml` | Reusable action sequences |
| **Helpers** | `inputs/` directory | Input selects, text, booleans, numbers, datetimes, buttons |
| **Light Groups** | `light_groups.yaml` | Custom light grouping (version controlled) |
| **Templates** | `template.yaml` | Computed sensors, binary sensors, switches |
| **Custom Components** | `custom_components/` | 23+ custom integrations (Tuya, Eufy, Tesla, etc.) |
| **Automations** | `automations/` | Manual YAML automations split by category (lighting, litterbot, etc.) |
| **Blueprints** | `blueprints/` | Reusable automation templates |

### Key Architectural Patterns

**Multi-agent cost optimization** (see `DECISIONS.md` and `TASKS.md`):
- Different AI agents handle different task types
- Handoff coordination via TASKS.md + git commits
- Each agent focuses on its strength (research, code, ops, docs)

**Light group design** (YAML-based, not UI):
- Defined in `light_groups.yaml` using `platform: group`
- Version controlled and reproducible across HA restarts
- Synced to server via `sync_to_ha.sh`
- Entity IDs must match actual devices in registry

**Entity registry management**:
- Changes via `.storage/core.entity_registry` require special sync
- Use `ha core stop` → edit → `ha core start` (NOT `ha core restart`)
- UI-based changes persist but may be duplicated

**Notification architecture**:
- `notify.adults` group targets multiple mobile devices
- Service names use slugified device names (e.g., `mobile_app_ankit_s_iphone`)
- Device name changes require manual notify group updates

### Custom Components (23+)

**Patched components:**
- `openplantbook` - Requires manual version patching (see CHANGELOG.md)
- `tuya_local` - May need patching for API compatibility

**Large entity generators:**
- Music Assistant - 39 virtual media players (clutters entity list, subject to cleanup decision)
- Tuya Local - Generates entities for all cloud-connected devices
- Mail and Packages - Creates persistent entities per mailbox/package

## Critical Workflows

### Deployment Flow

```
Code changes (YAML/Python)
  ↓
Commit to git
  ↓
`./sync_to_ha.sh` (copies files to 192.168.4.141)
  ↓
HA restart via UI or SSH
  ↓
Test in Alexa/Siri/UI
  ↓
If successful: git push to origin
```

### Syncing to Server

**For YAML changes:**
```bash
./sync_to_ha.sh  # Rsyncs all .yaml files to HA OS
# Then restart HA via UI or: ha core restart
```

**For entity registry edits:**
```bash
ha core stop
# Edit .storage/core.entity_registry on server
ha core start  # (not restart - crucial!)
```

**For custom component patches:**
- SSH to server: `ssh root@192.168.4.141`
- Edit in `config/custom_components/[component]/`
- Restart HA

### Common Debugging Commands

**Check entity registry:**
```bash
ssh root@192.168.4.141
cat /config/.storage/core.entity_registry | python3 -m json.tool
```

**Validate YAML without deploying:**
```bash
python3 -c "import yaml; yaml.safe_load(open('automations/some_file.yaml'))"
```

**Tail HA logs (remote):**
```bash
ha logs follow
```

## Conventions & Patterns

### Entity Naming

**Standard format:** `[domain].[location]_[description]`

Examples:
- `light.living_room_ceiling` - Overhead light
- `switch.bedroom_nightstand_left` - Bedside switch
- `sensor.kitchen_temperature` - Temperature sensor

**DO:**
- Use snake_case (spaces → underscores)
- Include location prefix for grouping
- Use descriptive, discoverable names

**DON'T:**
- Use generic names like `light_1`, `device_2`
- Mix naming conventions
- Use device names that change (syncs break)

### Automation File Naming

Pattern: `automation_[trigger]_[action].yaml`

Examples:
- `automation_litterbot_bin_emptied.yaml`
- `automation_auto_disable_stale_scenes.yaml`
- `automations/lighting/automation_motion_lights.yaml`

### Light Group Management

**Location in code:** `light_groups.yaml`

**Structure:**
```yaml
light:
  - platform: group
    name: "Living Room Lamps"
    entities:
      - light.hue_iris
      - light.floor_lamp_2
      - light.floor_lamp_1
```

**Gotchas:**
- Entity IDs must exist in registry (verify via SSH)
- Changes require HA restart
- Groups fail silently if entity IDs are wrong

### Notify Groups

**Location in code:** `configuration.yaml` under `notify:`

**Pattern:**
```yaml
notify:
  - name: adults
    platform: group
    services:
      - service: mobile_app_ankit_s_iphone
      - service: mobile_app_pixel_7a
```

**Key:** Service names are auto-generated slugs from device names

## Project-Specific Decisions

### Why YAML Light Groups?

UI groups weren't version controlled and had sync issues. YAML groups:
- Are reproducible
- Version controlled
- Consistent across restarts
- But require manual HA restart to apply changes

### Stop/Start vs Restart

When editing `.storage/core.entity_registry`:
- Use `ha core stop` + `ha core start` (NOT `ha core restart`)
- Restart overwrites uncommitted .storage changes
- Stop/start preserves edits

### Multi-Agent Workflow

Tasks distributed by capability:
- **Claude Code** - Server ops, SSH, .storage edits, debugging
- **Codex** - Documentation, linting, YAML drafting
- **ChatGPT** - Quick questions, planning
- **Perplexity** - Deep research, citations
- **Gemini/NotebookLM** - Large document analysis

Handoff via `TASKS.md` + git commits, not chat continuity.

## Development Best Practices

1. **Always test YAML before deploying:**
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('file.yaml'))"
   ```

2. **Use git commits as deployment gates:**
   - Never deploy breaking changes without commit message explaining the risk

3. **Keep entity_rename_map.json updated** when renaming entities:
   - Helps track migration history
   - Prevents duplicate references

4. **Document decisions in DECISIONS.md:**
   - Record context, alternatives, consequences
   - Helps future agents understand "why"

5. **Use CHANGELOG.md for user-facing changes:**
   - Breaking changes
   - New automations or features
   - Component patches applied

6. **Batch server operations:**
   - Multiple changes → single SSH session → single restart
   - Reduces downtime, prevents missed changes

7. **Test voice commands after automation changes:**
   - Alexa may cache entity discovery
   - "Alexa, discover devices" triggers fresh discovery (wait 1-2 min)

## Debugging Reference

**Problem:** Light group shows as unavailable

**Solution:**
1. Check entity IDs in `.storage/core.entity_registry`
2. Verify entity IDs in `light_groups.yaml` match exactly
3. Restart HA
4. Check Home Assistant UI → Entities for errors

**Problem:** Notify group fails to send

**Solution:**
1. Verify mobile app integrations are loaded (`Configuration → Integrations`)
2. Check service names in `notify.adults` match loaded services
3. Test manual service call from Developer Tools

**Problem:** Custom component patches lost after update

**Solution:**
1. Re-apply patch after component updates
2. Document patch in CHANGELOG.md
3. Consider using CUSTOM_UPDATER to pin versions

**Problem:** YAML syntax errors not caught until restart

**Solution:**
- Always validate locally: `python3 -c "import yaml; yaml.safe_load(open('file.yaml'))"`
- Use VS Code YAML extension with HA schema

## File Reference

| File | Purpose | When to Edit |
|------|---------|--------------|
| `configuration.yaml` | Core config, integrations, includes | Rarely; use includes instead |
| `DECISIONS.md` | Architecture decisions and rationale | When making new decisions |
| `TASKS.md` | Current task queue, agent assignments | Handoff between agents |
| `CHANGELOG.md` | User-facing changes, patches, breaking changes | Each deployment |
| `HOME_ASSISTANT.md` | Setup guide, overview, light group docs | Documentation updates |
| `light_groups.yaml` | All light group definitions | Adding/removing groups |
| `automations/**` | Manual YAML automations | Add features |
| `inputs/**` | Helper definitions | Add new helpers |

## Resources

- HA Docs: https://www.home-assistant.io/docs/
- Custom Components: https://github.com/hacs/integration
- YAML Validator: https://yamllint.readthedocs.io/
- Remote Access: 192.168.4.141 (minipc, HA OS)
