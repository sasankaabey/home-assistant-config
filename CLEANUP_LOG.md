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

## 2026-01-13: Automation & Script Cleanup (60-day stale)

**Criteria:** `last_triggered` older than 60 days (cutoff 2025-11-15) or never; scripts also required no repo references.

### Automations Removed (3)
- `automation.bedroom_nightlight_left_exit` (source `automations/lighting/bedroom_nightlight_on_bed_exit.yaml`, last_triggered: never)
- `automation.bedroom_nightlight_right_exit` (source `automations/lighting/bedroom_nightlight_on_bed_exit.yaml`, last_triggered: never)
- `automation.sensor_light_primary_bedroom` (source `automations/lighting/sensor_light_primary_bedroom.yaml`, last_triggered: 2025-10-16)

### Scripts Removed (5)
- `script.alexa_announce_living_room` (last_triggered: never; no repo references)
- `script.litterbot_tts_announce` (last_triggered: never; no repo references)
- `script.litterbot_nag_snooze` (last_triggered: never; no repo references)
- `script.litterbot_nag_snooze_until_home` (last_triggered: never; no repo references)
- `script.litterbot_nag_snooze_clear` (last_triggered: never; no repo references)

### Scripts Kept (at time of cleanup)
- `script.litterbot_alexa_announce` (kept temporarily; removed in follow-up below)

### Files Modified
- `scripts.yaml` - removed 5 scripts
- `automations/lighting/bedroom_nightlight_on_bed_exit.yaml` - deleted
- `automations/lighting/sensor_light_primary_bedroom.yaml` - deleted

## 2026-01-13: Litterbot Announcement Follow-up

### Scripts Removed (1)
- `script.litterbot_alexa_announce` (replaced with direct `script.alexa_announce_router` calls in Litterbot automations)

### Input Helpers Removed (1)
- `input_number.litterbot_nag_snooze_minutes` (no remaining references after snooze script removal)

### Input Helpers Removed (additional)
- `input_boolean.litterbot_nag_snooze_until_home`
- `input_text.litterbot_nag_snooze_until_home_person`
- `input_datetime.litterbot_nag_snooze_until`

### Automations Updated/Removed
- `automations/automation_litterbot_nag.yaml` - removed snooze logic (now always notifies while enabled)
- `automations/automation_litterbot_snooze_until_home_clear.yaml` - deleted (snooze helpers removed)

### Files Modified
- `scripts.yaml` - removed Litterbot Alexa announce script
- `automations/automation_litterbot_cycles_alert.yaml` - direct router call
- `automations/automation_litterbot_non_standby.yaml` - direct router call
- `inputs/input_number.yaml` - removed snooze minutes helper
- `inputs/input_boolean.yaml` - removed snooze until home helper
- `inputs/input_text.yaml` - removed snooze person helper
- `inputs/input_datetime.yaml` - cleared snooze datetime helper
- `automations/automation_litterbot_nag.yaml` - removed snooze handling
- `automations/automation_litterbot_snooze_until_home_clear.yaml` - deleted

## 2026-01-14: UI Automation Mass Cleanup

**Criteria:** Never triggered OR last_triggered > 60 days (stale)

### Automations Removed (44 total)

**Bedroom/Sleep Automations (8):**
- `automation.bedroom_nightlight_left_exit` - never triggered
- `automation.bedroom_nightlight_right_exit` - never triggered
- `automation.bedroom_nightlight_on_bed_exit` - never triggered
- `automation.bedroom_sensor_and_lights_off` - never triggered
- `automation.bedtime_conditional_lights_off_or_ask_alexa` - never triggered
- `automation.bedtime_office_motion_nightlight` - never triggered
- `automation.bedtime_turn_off_bedroom_tv` - never triggered
- `automation.primary_bedroom_motion_lights` - never triggered

**Sensor Light Automations (4):**
- `automation.sensor_light_primary_bedroom` - stale (2025-10-16)
- `automation.sensor_light_bedroom_trial` - never triggered
- `automation.sensor_light_office_ct_lights` - never triggered
- `automation.sensor_light_office_desk_only` - never triggered

**TV Mount Automations (3):**
- `automation.tv_mount_control_by_tv_power` - never triggered
- `automation.tv_mount_tracks_tv_power` - never triggered
- `automation.tv_mount_verify_alignment_every_3_minutes` - never triggered

**Alexa/Voice Automations (5):**
- `automation.alexa_routine_trigger_goodnight_on_last_called_device` - never triggered
- `automation.handle_alexa_actionable_by_person_id` - never triggered
- `automation.set_alexa_alarm_based_on_spoken_time` - never triggered
- `automation.daily_greeting_approved` - never triggered
- `automation.daily_greeting_edit_response` - never triggered

**Goodnight Routine Automations (2):**
- `automation.run_goodnight_routine_by_person` - never triggered
- `automation.run_goodnight_routine_by_person_or_device` - never triggered

**Litterbot Automations (6):**
- `automation.litterbot_alert_waits_for_someone` - never triggered
- `automation.litterbot_problem_alert` - never triggered (YAML version exists)
- `automation.litterbot_problem_cleared` - never triggered (YAML version exists)
- `automation.litterbot_problem_trigger` - never triggered
- `automation.modular_nag_loop` - never triggered
- `automation.reset_litterbot_snark_counter` - never triggered

**Plant Automations (3):**
- `automation.bedroom_plants` - never triggered
- `automation.wake_up_plants` - never triggered
- `automation.notify_on_monstera_plant_issues` - never triggered

**Color/Lighting Helper Automations (3):**
- `automation.update_bedroom_time_of_day_color_temp` - never triggered
- `automation.update_color_temp_helpers_by_time_of_day_2` - never triggered (duplicate)
- `automation.update_open_floorplan_dynamic_helpers` - never triggered

**Misc Automations (10):**
- `automation.new_automation` - placeholder, never triggered
- `automation.nighttime_motion_red_lights` - never triggered
- `automation.office_desk_light_by_monitor_consumption` - never triggered
- `automation.playful_greeting_for_danielle` - never triggered
- `automation.primary_bedroom_dial_toggle_2` - never triggered (duplicate)
- `automation.main_floor_thermostat_current_state` - never triggered
- `automation.max_s_lights_on` - never triggered
- `automation.turn_on_all_lights_except_front_door` - never triggered
- `automation.turn_off_all_lights_except_front_door` - never triggered
- `automation.turn_off_the_tv_if_no_one_s_watching` - never triggered

### Automations Kept (7 total)

All actively used and version-controlled:
- `automation.monthly_smoke_detector_health_check` - triggered 2026-01-03
- `automation.restore_lights_on_ha_startup` - triggered on every restart
- `automation.sensor_light_kitchen` - actively triggering
- `automation.sensor_lights_dining_room` - actively triggering
- `automation.sensor_lights_living_room` - actively triggering
- `automation.sync_living_room_lamps_on_change` - triggered 2026-01-13
- `automation.sync_living_room_lights_on_change` - triggered 2026-01-13

### Files Modified
- `.storage/core.entity_registry` - Removed 44 automation entities

### Statistics
- **Before:** 51 automations
- **After:** 7 automations
- **Removed:** 44 automations (86% reduction)
