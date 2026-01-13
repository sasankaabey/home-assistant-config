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

### Configuration Format (IMPORTANT)

When using `light: !include light_groups.yaml` in configuration.yaml, the light_groups.yaml file MUST use list format:

```yaml
- platform: group
  name: Display Name
  unique_id: unique_identifier
  entities:
    - light.entity_1
    - light.entity_2
```

**Common mistakes to avoid:**
- ❌ Don't use dict/key format (`group_name:`) when using `light: !include`
- ❌ Don't nest light groups within other light groups (causes issues)
- ✅ Do use list format with `- platform: group` for each group
- ✅ Do add `unique_id` to each group for proper entity registry
- ✅ Do list all individual lights directly in "all lights" groups

**After making changes:**
1. Sync files to HA OS
2. Restart Home Assistant
3. **Trigger device discovery:** "Alexa, discover devices" (or use Alexa app)
4. Wait 1-2 minutes for discovery to complete
5. Test voice commands

### Living Room Light Groups

#### `light.living_room_lamps`
Combines all lamp lighting (floor lamps + accent lights + TV backlight):
- Floor Lamp 1
- Floor Lamp 2
- Hue Iris
- TV Light

#### `light.living_room_ceiling`
Main overhead lighting:
- Living Room Ceiling

#### `light.living_room_lights`
Master control for all living room lights (lists all individual lights directly):
- Floor Lamp 1
- Floor Lamp 2
- Hue Iris
- TV Light
- Living Room Ceiling

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

## Ongoing Cleanup Tasks

### Current Phase: Living Room Light Groups
✅ Create living room light groups with voice control
- Establishes pattern for other rooms
- Tests multi-platform voice integration

### Next Phases: Room-by-Room
1. Identify all devices per room
2. Remove duplicate/ghost entities
3. Establish Source of Truth (SoT) for each device
4. Create room-specific light groups
5. Update automations to use groups
6. Document naming conventions

### Rooms to Process
- Living Room (✅ in progress)
- Primary Bedroom
- Dining Room
- Kitchen
- Kids' Bedrooms
- Bathrooms
- Outdoor spaces

## Best Practices

1. **One Source of Truth**: Each device should have one authoritative entity
2. **Consistent Naming**: `{room}_{device_type}_{descriptor}`
3. **Use Groups**: Simplify automations and voice control
4. **Document Changes**: Update this file when making structural changes
5. **Test Before Committing**: Verify configurations load without errors
6. **Version Control Everything**: Commit regularly with clear messages

## Resources

- [Home Assistant Documentation](https://www.home-assistant.io/docs/)
- [Light Groups Documentation](https://www.home-assistant.io/integrations/group/#light-groups)
- [Cloud Integration](https://www.home-assistant.io/integrations/cloud/)
- [HomeKit Integration](https://www.home-assistant.io/integrations/homekit/)
