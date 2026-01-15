# Home Assistant Configuration

Repository: https://github.com/anktaggrwl/home-assistant-config
Local Path: `/Users/ankit/ha-config`
HA OS Path: `/config` on minipc (192.168.4.141)

## Overview

This repository contains the Home Assistant configuration for a multi-platform smart home supporting:
- 5 family members (2 Android, 3 iOS devices)
- Voice control via Alexa, Siri (HomeKit), and Google Assistant
- Version-controlled configuration with git

## Configuration Structure

### Core Files
- `configuration.yaml` - Main configuration file
- `automations.yaml` - UI-created automations
- `scripts.yaml` - UI-created scripts
- `scenes.yaml` - UI-created scenes
- `groups.yaml` - Person groups (household, kids)
- `template.yaml` - Template sensors and helpers

### Modular Includes
- `automations/` - Manual YAML automations organized by category
  - `lighting/` - Lighting automations
  - `automation_litterbot_*.yaml` - Litter box automations
- `inputs/` - Input helpers (select, text, boolean, number, datetime, button)
- `blueprints/` - Automation blueprints
- `themes/` - Frontend themes

### Custom Components
- Alexa Media Player
- Eufy Security
- Hue Sync Box
- Mail and Packages
- Meross LAN
- OpenPlantbook
- Plant monitoring
- PyScript
- TCL TV Remote
- Tesla Custom
- Tuya Local

## Light Groups

Light groups are defined in `light_groups.yaml` and provide:
- Unified control of multiple lights as a single entity
- Voice assistant compatibility (automatically exposed via cloud integration)
- Simplified automation targeting
- Room-based organization

### Managing Light Groups

**To modify light groups:**
1. Edit `light_groups.yaml` in the repository
2. **IMPORTANT:** Ensure entity IDs match actual devices (check entity registry if needed)
   - If entity names are wrong, groups will fail to load or work incorrectly
   - Verify entity IDs exist: SSH to minipc and check entity registry
3. Commit and push changes
4. Sync to HA OS and restart

**Common mistake:** Using old/renamed entity IDs will cause groups to fail silently

**After making changes:**
1. Sync files to HA OS and restart Home Assistant
2. **Trigger device discovery:** "Alexa, discover devices" (or use Alexa app)
3. Wait 1-2 minutes for discovery to complete
4. Test voice commands

### Living Room Light Groups

#### `light.living_room_lamps`
Combines all soft/ambient lighting that flanks the living room:
- Hue Iris
- Floor Lamp 2
- Floor Lamp 1
- TV Light

#### `light.living_room_ceiling`
Main overhead lighting:
- Living Room Ceiling

#### `light.living_room_lights`
Master control for all living room lights:
- Living Room Ceiling
- TV Light
- Floor Lamp 2
- Floor Lamp 1
- Hue Iris

**Light Sync Behavior:**
- When controlled via HA/Alexa/Google/Siri: All lights in the group stay in sync (brightness, color, effects stopped)
- When controlled via Hue app directly: Individual lights can diverge (color loops, effects, etc.)
- Automation: `sync_living_room_light_groups.yaml` ensures group coherence

### Voice Control Examples

**Alexa:**
- "Alexa, turn on living room lamps"
- "Alexa, set living room lights to 50%"
- "Alexa, turn off living room ceiling"

**Siri:**
- "Hey Siri, turn on living room lamps"
- "Hey Siri, dim living room lights to 25%"

**Google:**
- "Hey Google, turn on living room lamps"
- "Hey Google, brighten living room lights"

## Voice Assistant Configuration

### Alexa & Google Assistant
Configured via Nabu Casa Cloud in `configuration.yaml:39-97`
- Auto-exposes: lights, switches, fans, covers, locks, climate, and more
- Sensor filters for temperature, humidity, air quality, motion, etc.
- No additional configuration needed for light groups

### HomeKit (Siri)
Configured in `configuration.yaml:99-127`
- Exposes: lights, switches, locks, covers, fans
- Excludes helper/virtual entities
- Light groups automatically available

## Workflow

### Making Configuration Changes

1. **Edit locally** in `/Users/ankit/ha-config`
2. **Test** changes if possible
3. **Commit** to git with descriptive message
4. **Push** to GitHub
5. **Sync** to minipc HA OS at `/config`
6. **Restart** Home Assistant to apply changes

### Syncing to HA OS

```bash
# SSH or file sync method to minipc
# Then restart HA via UI or service call
```

### Restarting Home Assistant

Via UI: Configuration → Settings → System → Restart
Via service: `homeassistant.restart`

## Family Members

- Ankit Aggarwal (Android)
- Danielle Goodwin (iOS)
- Zoe Aggarwal (iOS)
- Max Aggarwal (iOS)
- Aiden Kampe (Android)

Groups defined in `groups.yaml`:
- `group.household` - All family members
- `group.kids` - Zoe, Max, Aiden

## Cleanup History

### 2026-01-13: Comprehensive Entity Cleanup
✅ **Completed:**
- Removed 15 duplicate/orphaned entities
- Disabled 2 duplicate automations
- Fixed Living Room light groups (YAML-based)
- Created sync automation for light group coherence
- Fixed mobile app notification service names in litterbot automations
- Created comprehensive audit reports

**Backups:** `a4b62dfd` ("Before entity cleanup Jan 2026")

**Audit Reports:**
- `entity_audit_report.md` - Full findings and dashboard issues
- `ENTITY_AUDIT_FIX_GUIDE.md` - Step-by-step fix instructions
- `COMPREHENSIVE_CLEANUP_SUMMARY.md` - Cleanup summary
- `QUICK_CLEANUP_GUIDE.md` - Quick reference

**Remaining Tasks:**
- Rename 8 Tuya RGBCW lights (see `TUYA_LIGHT_RENAME_GUIDE.md`)
- Decide on Music Assistant strategy (39 virtual media players)
- Clean up 70 dashboard references to missing entities (low priority)

## Ongoing Cleanup Tasks

### Current Phase: Living Room Light Groups
✅ **Complete** - Living room light groups with voice control
- YAML-based groups version controlled
- Sync automation keeps lights synchronized
- Multi-platform voice integration working (Alexa/Siri/Google)

### Next Phases: Room-by-Room
1. Identify all devices per room
2. Remove duplicate/ghost entities
3. Establish Source of Truth (SoT) for each device
4. Create room-specific light groups
5. Update automations to use groups
6. Document naming conventions

### Rooms to Process
- Living Room (✅ complete)
- Primary Bedroom
- Dining Room
- Kitchen
- Kids' Bedrooms
- Bathrooms
- Outdoor spaces

## Best Practices

### Configuration Management

1. **One Source of Truth**: Each device should have one authoritative entity
2. **Consistent Naming**: `{room}_{device_type}_{descriptor}`
3. **Use Groups**: Simplify automations and voice control
4. **Document Changes**: Update this file when making structural changes
5. **Test Before Committing**: Verify configurations load without errors
6. **Version Control Everything**: Commit regularly with clear messages

### Entity Cleanup & Maintenance

7. **Regular Entity Audits**: Run comprehensive audits quarterly or when adding/removing devices
   - Check for orphaned references in automations/scripts/dashboards
   - Identify disabled entities still referenced in active configs
   - Clean up entities from removed devices

8. **Before Deleting Entities**: Always audit references first
   ```bash
   # Search for entity references in all configs
   grep -r "entity_id_here" /config/ --include="*.yaml"
   # Check dashboards
   grep -r "entity_id_here" /config/.storage/lovelace*
   ```

9. **Mobile App Notify Services**: Device-specific UUIDs, not friendly names
   - Correct: `notify.mobile_app_7b4b3d84_ce9d_418e_ad95_576581ee855e`
   - Wrong: `notify.mobile_app_ankit_s_iphone` (breaks when device reinstalls app)
   - Find correct service: Developer Tools → Services → Filter "notify"

10. **Group Entities Must Load**: Groups defined in `groups.yaml` need HA restart to register
    - If automations reference groups but they don't exist as entities, restart HA
    - Verify in Developer Tools → States after restart

11. **Backup Before Major Cleanups**: Always create backup before entity cleanup
    ```bash
    ssh root@192.168.4.141
    ha backups new --name "Before [description] cleanup"
    ```

12. **Post-Cleanup Validation**: After deleting entities, verify:
    - No errors in HA logs (Settings → System → Logs)
    - Automations still work (check automation traces)
    - Dashboards display correctly
    - Voice commands still function

## YAML Automation Format

**CRITICAL:** When using `!include_dir_merge_list` (as in `configuration.yaml`), each automation file must be a **list** (starting with `-`), not a single object.

### Correct Format (list item)
```yaml
- alias: "My Automation"
  id: "my_automation"
  trigger:
    - platform: state
      entity_id: sensor.example
  action:
    - service: notify.adults
      data:
        message: "Hello"
  mode: single
```

### Wrong Format (single object - WILL NOT LOAD)
```yaml
alias: "My Automation"
id: "my_automation"
trigger:
  - platform: state
    entity_id: sensor.example
action:
  - service: notify.adults
    data:
      message: "Hello"
mode: single
```

**Symptom:** Automations exist as files on disk but don't appear in HA UI.

## Entity Registry Editing

The entity registry (`.storage/core.entity_registry`) controls which entities are enabled/disabled.

### Safe Editing Procedure
1. **Stop HA first** (not restart): `ha core stop`
2. Make edits to registry file
3. **Start HA**: `ha core start`

**WARNING:** If you just restart (`ha core restart`), HA will overwrite your registry changes with its in-memory state before shutting down.

### Disabling New Entity Auto-Sync
To prevent integrations from automatically creating entities (keeps environment clean):
```bash
# SSH to HA, then run Python to set pref_disable_new_entities=true
python3 << 'EOF'
import json
with open('/config/.storage/core.config_entries', 'r') as f:
    data = json.load(f)
for entry in data['data']['entries']:
    entry['pref_disable_new_entities'] = True
with open('/config/.storage/core.config_entries', 'w') as f:
    json.dump(data, f, indent=2)
EOF
```

## Notify Groups

Notify groups consolidate multiple device notifications. Defined in `configuration.yaml`:

```yaml
notify:
  - name: adults
    platform: group
    services:
      - service: mobile_app_device_uuid_1  # Ankit's iPhone
      - service: mobile_app_device_uuid_2  # Danielle's Pixel
```

**Usage in automations:**
```yaml
- service: notify.adults
  data:
    title: "Alert Title"
    message: "Message body"
```

## Syncing to HA OS

Use `sync_to_ha.sh` script (excludes .storage, www, custom_components, etc.):
```bash
./sync_to_ha.sh
ssh root@192.168.4.141 "ha core restart"
```

**NEVER use rsync --delete** against HA config - it will wipe .storage directory and destroy entity registry, causing need to restore from backup.

## Resources

- [Home Assistant Documentation](https://www.home-assistant.io/docs/)
- [Light Groups Documentation](https://www.home-assistant.io/integrations/group/#light-groups)
- [Cloud Integration](https://www.home-assistant.io/integrations/cloud/)
- [HomeKit Integration](https://www.home-assistant.io/integrations/homekit/)
