# Broken UI Groups Cleanup

**Date:** 2026-01-13

## Summary

Deleted **11 broken UI-created groups** that referenced non-existent entities (old/renamed entity IDs).

## All Broken Groups Deleted

### Nightstand Groups (2)

- `light.nightstands` - referenced non-existent `light.ankits_nightstand`, `light.danielles_nightstand`
- `light.primary_bedroom_nightstands` - same broken references

### Other Broken Groups (9)

- `light.office_overhead_lights` (Office Lights) - referenced `light.g45_rgbcw_wifi_le5w` variants that don't exist
- `light.primary_bedroom_ceiling_lights` (Bedroom Ceiling Lights) - referenced `light.bedroom_ceiling_1-4` that don't exist
- `light.stairway_lights` (Stairway Lights) - partially broken, missing `light.stairway_1`
- `light.first_floor_open_floorplan_lights` (Open Floorplan Lights) - referenced old floor lamp names
- `light.bedroom_ambient_lights` (Bedroom Ambient Lights) - referenced non-existent `light.bedroom_nightstands`
- `light.primary_bedroom_lights` (Bedroom Lights) - referenced non-existent `light.bedroom_ceiling_lights`
- `light.upstairs_hallway_lights` (Office CT Lights) - referenced `light.hallway_lamp`, `light.light_strip`
- `light.front_door_lights` (Front Door Lights) - referenced `light.front_door_light` (wrong name)
- `light.zoes_room_lights` (Zoes Room Lights) - referenced `light.zoes_light` (wrong name)

## Root Cause

These groups were created in the UI but the underlying entities were later renamed or removed, breaking the group references. UI groups don't auto-update when entities are renamed.

## YAML Groups Remain Active

The following YAML-defined groups in `light_groups.yaml` are unaffected and working:

- `light.living_room_lamps`
- `light.living_room_lights`
- `light.office_hallway_light`
- `light.bedroom_nightstands`

## Remaining Valid UI Groups

- Kitchen Lights (4 entities)
- Office Ambient Lights (1 entity)
- Downstairs Lights (1 entity)

## Best Practice

Use YAML-based groups in `light_groups.yaml` instead of UI helpers:

- Version controlled
- Easier to audit and maintain
- Can be synced across environments
- Won't break silently when entities are renamed

## Voice Control

After cleanup:

- "Alexa, turn on bedroom nightstands"
- "Alexa, turn on living room lamps"
- "Alexa, turn on office hallway light"
