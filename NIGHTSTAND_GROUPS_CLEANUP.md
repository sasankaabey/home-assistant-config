# Bedroom Nightstand Groups Cleanup

**Date:** 2026-01-13

## Issue Found

Two broken UI-created nightstand groups exist with outdated entity references:

1. **`light.nightstands`** (config entry: 01JS74R5N7DSBM1RNMYKKZT49K)
   - References: `light.ankits_nightstand`, `light.danielles_nightstand`, `light.bed_lightstrip`
   - **Problem:** These entity IDs don't exist (entities were renamed)

2. **`light.primary_bedroom_nightstands`** (config entry: 01JTH30TNYQW541RZ2GAV4JZW9)
   - References: `light.ankits_nightstand`, `light.danielles_nightstand`
   - **Problem:** These entity IDs don't exist (entities were renamed)

## Correct Entity Names

The actual nightstand lights are:
- `light.primary_bedroom_ankits_nightstand` (Hue)
- `light.primary_bedroom_danielles_nightstand` (Hue)

## Solution Implemented

Created new YAML-based group in `light_groups.yaml`:
```yaml
- platform: group
  name: Bedroom Nightstands
  unique_id: bedroom_nightstands_group
  entities:
    - light.primary_bedroom_ankits_nightstand
    - light.primary_bedroom_danielles_nightstand
```

This creates: `light.bedroom_nightstands`

## Cleanup Steps (After Verification)

1. **Test the new YAML group:**
   - "Alexa, turn on bedroom nightstands"
   - Verify both Ankit's and Danielle's nightstands turn on
   - Test brightness/color control

2. **Delete old broken UI groups:**
   ```bash
   ssh root@192.168.4.141

   # Delete from entity registry
   python3 <<'EOF'
   import json

   with open('/config/.storage/core.entity_registry', 'r') as f:
       registry = json.load(f)

   to_delete = ['light.nightstands', 'light.primary_bedroom_nightstands']
   registry['data']['entities'] = [
       e for e in registry['data']['entities']
       if e['entity_id'] not in to_delete
   ]

   with open('/config/.storage/core.entity_registry', 'w') as f:
       json.dump(registry, f, indent=2)

   print("Deleted old nightstand groups")
   EOF

   # Delete config entries
   python3 <<'EOF'
   import json

   with open('/config/.storage/core.config_entries', 'r') as f:
       config = json.load(f)

   old_entry_ids = [
       '01JS74R5N7DSBM1RNMYKKZT49K',  # light.nightstands
       '01JTH30TNYQW541RZ2GAV4JZW9'   # light.primary_bedroom_nightstands
   ]

   config['data']['entries'] = [
       e for e in config['data']['entries']
       if e['entry_id'] not in old_entry_ids
   ]

   with open('/config/.storage/core.config_entries', 'w') as f:
       json.dump(config, f, indent=2)

   print("Deleted old config entries")
   EOF

   # Restart HA
   ha core restart
   ```

3. **Run Alexa device discovery:**
   - "Alexa, discover devices"
   - Wait 1-2 minutes
   - Test: "Alexa, turn on bedroom nightstands"

## Voice Control

After cleanup, use:
- "Alexa, turn on bedroom nightstands"
- "Alexa, set bedroom nightstands to 50%"
- "Alexa, turn off bedroom nightstands"

## Notes

- The old `light.bed_lightstrip` entity referenced in one group also doesn't exist
- All three entities in the old groups have been renamed with `primary_bedroom_` prefix
- YAML-based groups are preferred for version control and easier maintenance
