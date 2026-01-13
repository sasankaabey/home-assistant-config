# Home Assistant Entity Cleanup Log

**Date:** 2026-01-13
**Backup Created:** a4b62dfd ("Before entity cleanup Jan 2026")

## Summary

Performed comprehensive entity cleanup to remove orphaned and duplicate entities, particularly focusing on Living Room light groups that were conflicting with the new YAML-based configuration.

## Entities Deleted

### Duplicate Light Groups (5 entities)
These were old UI-created helper groups that conflicted with the new YAML-based groups:

1. `light.living_room_lamps_2` - Old UI helper (duplicate of YAML group)
2. `light.living_room_lights_2` - Old UI helper (duplicate of YAML group)
3. `light.living_room_ceiling_3` - Old unused group
4. `light.living_room_all_lights` - Old unused group from initial setup
5. `light.living_room_ambient` - Old group (renamed to "lamps")

### Disabled Entities (7 entities)
User-disabled entities that were no longer needed:

**Hue Light Groups (3):**
- `light.hue_living_room` - Disabled by user
- `light.hue_living_room_lamps` - Disabled by user
- `light.hue_living_room_lamps_2` - Disabled by user

**Switches (4):**
- `switch.living_room_switch_3` - Disabled by user
- `switch.living_room_switch_4` - Disabled by user
- `switch.living_room_lower_tv_switch` - Disabled by user
- `switch.living_room_raise_tv_switch` - Disabled by user

## Config Entries Removed

Deleted 2 UI-created light group config entries:
1. "Living Room Lights" (entry_id: 01JS76SM9QNC3R082FECC8VMVH)
2. "Living Room Lamps Group" (entry_id: 01KD57J7J9DFNSCRJJWTDT72V4)

## Active Light Groups (After Cleanup)

**YAML-based groups in `light_groups.yaml`:**

### `light.living_room_lamps`
- light.living_room_hue_iris
- light.living_room_floor_lamp_2
- light.living_room_floor_lamp
- light.living_room_tv_light

### `light.living_room_lights`
- light.living_room_ceiling
- light.living_room_tv_light
- light.living_room_floor_lamp_2
- light.living_room_floor_lamp
- light.living_room_hue_iris

## Verification Steps

After restart, verify:
1. ✅ YAML light groups load correctly
2. ✅ No duplicate groups appear in UI
3. ✅ Voice commands work: "Alexa, turn on living room lamps"
4. ✅ Sync automation works (lights stay in sync)

## Files Modified

- `.storage/core.entity_registry` - Removed 12 entity entries
- `.storage/core.config_entries` - Removed 2 group config entries

## Rollback Instructions

If issues occur, restore from backup:
```bash
ssh root@192.168.4.141
ha backups restore a4b62dfd
```

## Next Steps

1. Test voice commands with Alexa/Siri/Google
2. Run "Alexa, discover devices" to sync changes
3. Verify sync automation keeps lights in sync
4. Consider room-by-room cleanup for other areas (bedrooms, kitchen, etc.)

## Notes

- Physical light entities with "_2" suffixes were preserved (these are real devices)
- Media player duplicates were preserved (legitimate multi-protocol endpoints)
- 739 disabled mobile app sensors remain disabled (auto-disabled by integration)
- Total entities reduced from 1,964 to 1,952 (12 deleted)
