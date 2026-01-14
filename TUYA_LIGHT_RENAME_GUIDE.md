# Tuya RGBCW Light Renaming Guide

**Date:** 2026-01-13
**Issue:** 8 Tuya lights have generic names (rgbcw_lightbulb, _2, _3, etc.)

## The 8 Lights to Rename

**Office Staircase Fixture (4 bulbs - now grouped):**
- ✅ `light.rgbcw_lightbulb` - Part of office staircase group
- ✅ `light.rgbcw_lightbulb_3` - Part of office staircase group
- ✅ `light.rgbcw_lightbulb_4` - Part of office staircase group
- ✅ `light.rgbcw_lightbulb_7` - Part of office staircase group

**Remaining to identify:**
```
light.rgbcw_lightbulb_2
light.rgbcw_lightbulb_5
light.rgbcw_lightbulb_6
light.rgbcw_lightbulb_8
```

Note: The office staircase bulbs now function as one group via `light.office_staircase` - you can control all 4 together or individually.

## How to Identify and Rename

### Step 1: Identify Each Light

For each light, turn it on individually in Home Assistant:

1. Go to Settings → Devices & Services → Entities
2. Search for `rgbcw_lightbulb`
3. Click the first one and turn it on
4. Walk around your home to see which light turned on
5. Note the room/location

### Step 2: Rename in Home Assistant UI

1. While viewing the entity, click the settings/gear icon
2. Update the "Name" field to the room location (e.g., "Primary Bedroom Ceiling")
3. Update the "Entity ID" to match (e.g., `light.primary_bedroom_ceiling`)
4. Assign to the correct Area
5. Save
6. Repeat for all 8 lights

### Step 3: Common Room Locations to Check

Based on your config, check these areas:
- Primary Bedroom
- Kids' Bedrooms (Zoe, Max, Aiden)
- Dining Room
- Kitchen
- Living Room
- Bathrooms
- Hallways
- Outdoor spaces

## Recommended Naming Convention

**Pattern:** `light.{room}_{location}`

**Examples:**
- `light.primary_bedroom_ceiling`
- `light.kids_bedroom_ceiling`
- `light.dining_room_chandelier`
- `light.kitchen_island_pendant`
- `light.bathroom_vanity`
- `light.hallway_ceiling`

## After Renaming

1. Check if any automations reference the old names
2. Update light groups if any of these lights should be grouped
3. Test voice commands with new names

## Quick Rename via SSH (Advanced)

If you know which light is which, you can rename them via script. Example:

```python
# This is just an example - modify with your actual mappings
MAPPINGS = {
    'light.rgbcw_lightbulb': 'light.primary_bedroom_ceiling',
    'light.rgbcw_lightbulb_2': 'light.dining_room_ceiling',
    # ... etc
}
```

But it's safer to do it via the UI since you can test each light first.
