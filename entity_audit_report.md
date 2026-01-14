# HOME ASSISTANT ENTITY AUDIT REPORT

**Date:** 2026-01-13
**Focus:** Post-cleanup validation and broken reference detection

================================================================================

## EXECUTIVE SUMMARY

This audit examined all entity references across:
- YAML configuration files (automations, scripts, scenes, etc.)
- Dashboard configurations (Lovelace)
- Template sensors and groups

**Key Findings:**
- HIGH PRIORITY: 4 missing entities in active configurations
- MEDIUM PRIORITY: 0 disabled entities in active configurations
- INFO: 70 missing entities in dashboards (mostly old/renamed)
- INFO: 6 disabled entities still in dashboards

================================================================================

## HIGH PRIORITY: Missing Entities in Active Configurations

These entities are referenced in active automations/scripts but do not exist.
**Impact:** May cause errors or warnings in Home Assistant logs.

### 1. group.household

**Status:** Group defined in YAML but not loading properly
**Root Cause:** Groups defined in groups.yaml should create entities automatically.
**Recommendation:**
  1. Check if "group: !include groups.yaml" is in configuration.yaml
  2. Verify YAML syntax in groups.yaml
  3. Restart Home Assistant to register groups
  4. Check logs for YAML parsing errors

**Referenced in:**
  - /config/scripts.yaml (TTS scripts for household presence)

### 2. group.kids

**Status:** Group defined in YAML but not loading properly
**Root Cause:** Groups defined in groups.yaml should create entities automatically.
**Recommendation:**
  1. Check if "group: !include groups.yaml" is in configuration.yaml
  2. Verify YAML syntax in groups.yaml
  3. Restart Home Assistant to register groups
  4. Check logs for YAML parsing errors

**Referenced in:**
  - /config/scripts.yaml (TTS scripts for kids presence)
  - /config/template.yaml (kids_home sensor)

### 3. notify.mobile_app_ankit_s_iphone

**Status:** Mobile app notification service not registered
**Root Cause:** Mobile app may be disconnected or uninstalled.
**Recommendation:**
  1. Check if mobile app is installed and logged in on iPhone
  2. Reinstall mobile app if needed
  3. Update automations to use current mobile app notify services
  4. Check Settings -> Devices -> Mobile App for registered devices

**Referenced in:**
  - /config/automations.yaml
  - /config/automations/automation_litterbot_cycles_alert.yaml
  - /config/automations/automation_litterbot_main.yaml
  - /config/automations/automation_litterbot_nag.yaml
  - /config/automations/automation_litterbot_non_standby.yaml

### 4. notify.mobile_app_pixel_7a

**Status:** Mobile app notification service not registered
**Root Cause:** Mobile app may be disconnected or uninstalled.
**Recommendation:**
  1. Check if mobile app is installed and logged in on Pixel 7a
  2. Reinstall mobile app if needed
  3. Update automations to use current mobile app notify services
  4. Check Settings -> Devices -> Mobile App for registered devices

**Referenced in:**
  - /config/automations.yaml
  - /config/automations/automation_litterbot_cycles_alert.yaml
  - /config/automations/automation_litterbot_main.yaml
  - /config/automations/automation_litterbot_nag.yaml
  - /config/automations/automation_litterbot_non_standby.yaml

================================================================================

## MEDIUM PRIORITY: Disabled Entities in Active Configurations

**Status:** NONE FOUND

All entities referenced in active configurations are enabled and available.

================================================================================

## INFO: Dashboard Entity Issues

Entities referenced in dashboards that are missing or disabled.
**Impact:** Dashboard cards may show as unavailable or throw errors.

### Missing Entities in Dashboards (70 total)

These entities are referenced in Lovelace dashboards but do not exist.
Likely causes: devices removed, entities renamed, integrations disabled.

#### Binary Sensor (5 entities)
  - binary_sensor.esphome_web_470cfa_presence
  - binary_sensor.living_room_tv
  - binary_sensor.screek_office_motion_sensor_moving_target
  - binary_sensor.screek_office_motion_sensor_presence
  - binary_sensor.screek_office_motion_sensor_still_target

#### Climate (2 entities)
  - climate.main_floor
  - climate.upstairs

#### Light (9 entities)
  - light.aiden_s_lamp
  - light.back_deck_string_lights
  - light.bed_lightstrip
  - light.dining_room_table_2
  - light.front_door_light
  - light.living_room_lamps_and_tv_lights
  - light.wled
  - light.wled_main
  - light.wled_segment_1

#### Plant (1 entity)
  - plant.monstera

#### Scene (1 entity)
  - scene.turn_off_bedroom_lights_and_motion

#### Select (2 entities)
  - select.wled_playlist
  - select.wled_preset

#### Sensor (48 entities)
  - sensor.ankit_s_iphone_battery
  - sensor.ankit_s_sonos_arc_next_alarm
  - sensor.ankit_s_sonos_arc_next_reminder
  - sensor.ankit_s_sonos_arc_next_timer
  - sensor.ankits_apple_watch_battery
  - sensor.ankits_macbook_air_battery
  - sensor.ankurs_apple_watch_battery
  - sensor.connections_current_streak
  - sensor.connections_highest_streak
  - sensor.connections_last_played
  - sensor.connections_played
  - sensor.connections_won
  - sensor.living_room_soundbar_next_alarm
  - sensor.living_room_soundbar_next_reminder
  - sensor.living_room_soundbar_next_timer
  - sensor.luffy55_battery
  - sensor.max_s_bedroom_echo_next_alarm
  - sensor.max_s_bedroom_echo_next_reminder
  - sensor.max_s_bedroom_echo_next_timer
  - sensor.maxs_apple_watch_battery
  - sensor.monstera_air_humidity
  - sensor.monstera_conductivity
  - sensor.monstera_dli
  - sensor.monstera_illuminance
  - sensor.monstera_soil_moisture_2
  - sensor.monstera_temperature_2
  - sensor.screek_office_motion_sensor_bh1750_illuminance
  - sensor.screek_office_motion_sensor_move_energy
  - sensor.screek_office_motion_sensor_moving_distance
  - sensor.screek_office_motion_sensor_still_distance
  - sensor.screek_office_motion_sensor_still_energy
  - sensor.spelling_bee_played
  - sensor.stairway_motion_sensor_temperature
  - sensor.this_device_next_alarm
  - sensor.this_device_next_reminder
  - sensor.this_device_next_timer
  - sensor.tv_mount_position
  - sensor.washer_running_current
  - sensor.washer_running_current_consumption
  - sensor.washer_running_voltage
  - sensor.wordle_current_streak
  - sensor.wordle_highest_streak
  - sensor.wordle_played
  - sensor.wordle_won
  - sensor.zoe_s_phone_battery
  - sensor.zoe_s_room_next_alarm
  - sensor.zoe_s_room_next_reminder
  - sensor.zoe_s_room_next_timer
  - sensor.zoes_apple_watch_battery

#### Update (1 entity)
  - update.update_firmware

**Recommendation:**
  1. Review each dashboard and remove cards for missing entities
  2. Replace with current entity IDs if devices were renamed
  3. Remove cards for devices that no longer exist

### Disabled Entities Still in Dashboards (6 total)

- light.hue_downstairs (Disabled by: user, Platform: hue)
- light.hue_hallway (Disabled by: user, Platform: hue)
- light.hue_living_room (Disabled by: user, Platform: hue)
- light.hue_zoes_room (Disabled by: user, Platform: hue)
- sensor.primary_bedroom_monstera_soil_moisture (Disabled by: device, Platform: zha)
- sensor.primary_bedroom_monstera_temperature (Disabled by: device, Platform: zha)

**Recommendation:**
  - Re-enable entities if still needed in dashboards
  - OR remove dashboard cards for permanently disabled entities

================================================================================

## POST-CLEANUP VALIDATION

Validation of entities affected by 2026-01-13 cleanup:

### Entities Deleted in Recent Cleanup

**Validated:** None of the deleted entities are referenced in active configs

### Light Groups - YAML Configuration

**Status:** All light group entities from light_groups.yaml exist and are active

================================================================================

## RECOMMENDATIONS

### Immediate Actions Required

1. **Fix Missing Groups** (HIGH PRIORITY)
   - Verify configuration.yaml contains: "group: !include groups.yaml"
   - Check groups.yaml syntax
   - Restart Home Assistant
   - Verify group.household and group.kids appear in developer tools

2. **Fix Mobile App Notifications** (HIGH PRIORITY)
   - Check mobile app status for both devices (iPhone and Pixel 7a)
   - Reinstall apps if needed
   - Update automation notify services to use currently registered devices
   - Check Settings -> Devices & Services -> Mobile App

### Optional Cleanup Tasks

1. **Dashboard Cleanup** (MEDIUM PRIORITY)
   - Review and update/remove 70 cards with missing entities
   - Time estimate: 1-2 hours

2. **Re-enable or Remove Disabled Dashboard Entities** (LOW PRIORITY)
   - 6 disabled entities still showing in dashboards
   - Decide: re-enable or remove from dashboards

================================================================================

## SYSTEM HEALTH

- **Total Active Entities:** 1,212
- **Total Disabled Entities:** 748
- **Entity Registry Status:** Healthy
- **Configuration Errors:** 4 missing entity references
- **Automation Errors:** Potential issues in 5 litterbot automations

================================================================================

## TECHNICAL DETAILS

### Files Analyzed

/config/automations.yaml
/config/scripts.yaml
/config/scenes.yaml
/config/configuration.yaml
/config/template.yaml
/config/groups.yaml
/config/light_groups.yaml
/config/automations/*.yaml (13 files)
/config/.storage/lovelace
/config/.storage/lovelace.dashboard_main

### Analysis Methodology

1. Extracted all entities from entity registry (1,960 total)
2. Categorized into active (1,212) and disabled (748)
3. Parsed all YAML configuration files
4. Extracted all entity_id patterns using regex
5. Cross-referenced with entity registry
6. Filtered false positives (service calls, template vars, comments)
7. Analyzed dashboard JSON configurations
8. Generated severity-based report

================================================================================

## END OF REPORT
