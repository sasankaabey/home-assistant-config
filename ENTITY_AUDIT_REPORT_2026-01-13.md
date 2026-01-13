# Home Assistant Comprehensive Entity Audit Report

**Date:** 2026-01-13
**System:** Home Assistant 2026.1.1
**Total Entities:** 1,964 (1,225 enabled, 739 disabled)
**Total Devices:** 287
**Total Integrations:** 122

---

## Executive Summary

This audit analyzed all entities, devices, and integrations to identify duplicates, orphaned entities, and problematic configurations. Key findings include:

- **39 Music Assistant duplicate media players** creating confusion
- **8 Tuya RGBCW lights** with generic names needing identification
- **2 duplicate automations** that should be consolidated
- **Multiple Matter devices** with numbered suffix entities indicating re-addition issues
- **78 user-disabled entities** that could be reviewed for deletion

---

## HIGH PRIORITY ISSUES

### 1. Music Assistant Duplicate Media Players

**Impact:** High - Creates 39 duplicate entities across all media players

**Issue:** Music Assistant creates virtual players that duplicate physical devices from Sonos, Apple TV, WebOS TV, etc.

**Current State:**
- 39 Music Assistant virtual players
- 21 Physical media players
- All MA players have "None" as original name

**Recommendations:**
```
OPTION A - Keep Music Assistant:
  1. Continue using MA players for playback
  2. Hide/disable original integration players in UI
  3. Rename MA entities for clarity

OPTION B - Remove Music Assistant:
  1. Disable Music Assistant integration
  2. Use native integration players (Sonos, Apple TV, etc.)
  3. This will remove 39 duplicate entities
```

**Priority:** HIGH - Decide on architecture


### 2. Tuya RGBCW Lightbulbs with Generic Names

**Impact:** High - 8 lights cannot be identified by location

**Issue:** Tuya Local integration created generic entity IDs:
- `light.rgbcw_lightbulb`
- `light.rgbcw_lightbulb_2` through `light.rgbcw_lightbulb_8`

**Recommendations:**
```
1. Identify physical location of each bulb:
   - Turn on one at a time via HA
   - Note which room/fixture it controls

2. Rename each entity in HA UI:
   Settings > Devices & Services > Entities > Click entity > Edit

3. Suggested naming pattern:
   - [room]_[location] (e.g., bedroom_ceiling, living_room_lamp)
```

**Priority:** HIGH - Affects daily usability


### 3. Duplicate Automations

**Impact:** High - May cause double-triggering or conflicts

**Found Issues:**
```
1. automation.update_color_temp_helpers_by_time_of_day_2
   - Duplicate of: automation.update_color_temp_helpers_by_time_of_day
   - Status: ENABLED
   - Risk: Running twice

2. automation.primary_bedroom_dial_toggle_2
   - Duplicate of: automation.primary_bedroom_dial_toggle
   - Status: ENABLED
   - Risk: Conflicting actions
```

**Recommendations:**
```
1. Review automations.yaml for duplicate definitions
2. Check HA UI: Settings > Automations & Scenes
3. Disable one version and test
4. Delete the duplicate after confirming correct operation
```

**Priority:** HIGH - May cause automation issues


### 4. Living Room Floor Lamp Duplicates

**Impact:** Medium - Two entities controlling same light

**Issue:** Both entities point to Hue integration:
- `light.living_room_floor_lamp` (hue)
- `light.living_room_floor_lamp_2` (hue)

**Recommendations:**
```
1. Test both entities to identify which one works
2. Disable the non-functional entity
3. If both work, this is a Hue bridge duplicate registration
4. Remove and re-pair the light in Hue app to fix
```

**Priority:** HIGH - Duplicate control entities

---

## MEDIUM PRIORITY ISSUES

### 5. Matter Integration Duplicate Entities

**Impact:** Medium - Indicates devices were re-added multiple times

**Issue:** Matter devices have numbered suffix entities:

**Button Entities:**
- `button.kitchen_ceiling_4_identify_2`
- `button.kitchen_ceiling_2_identify_3`
- `button.kitchen_ceiling_3_identify_4`

**Update Entities:**
- `update.dining_room_ceiling_2`
- `update.dining_room_table_3`
- `update.kitchen_ceiling_4_2`
- `update.kitchen_ceiling_2_3`
- `update.kitchen_ceiling_3_4`

**Recommendations:**
```
1. Review Matter integration devices
2. Remove affected devices from Matter integration
3. Re-add devices cleanly (ensure not already paired)
4. This should eliminate numbered suffixes
```

**Priority:** MEDIUM - Cosmetic but indicates integration issues


### 6. Entities with 'None' as Original Name

**Impact:** Medium - Makes entity identification difficult

**Found Issues:**
- 45 lights with None as name
- 13 device trackers with None as name
- 8 switches with None as name
- Various other entity types

**By Integration:**
```
Lights:
  - Hue: 17 lights
  - Tuya Local: 9 lights
  - Matter: 8 lights
  - Govee Light Local: 5 lights
  - TP-Link: 3 lights
  - Others: 3 lights
```

**Recommendations:**
```
1. Check if entities have friendly names set in HA UI
2. If friendly names exist, no action needed
3. If no friendly names:
   - Review each entity
   - Set meaningful names based on location/function
```

**Priority:** MEDIUM - Verify friendly names exist


### 7. Numbered Suffix Entities (Non-Duplicates)

**Impact:** Low-Medium - Indicates possible integration issues

**Found Across Entity Types:**
```
Switches: 13 entities
  - switch.office_automation_motion_area_2
  - Multiple Sonos switches (_2 suffix)
  - Hue switches (_2 suffix)

Sensors: 21 entities
  - sensor.luffy55_sim_2
  - sensor.living_room_next_alarm_2
  - sensor.battery_2
  - Mobile app SIM 2 sensors (legitimate dual SIM)

Device Trackers: 4 entities
  - device_tracker.ankits_macbook_air_2
  - device_tracker.luffy55_2
  - device_tracker.zoe_s_phone_2

Binary Sensors: 1 entity
  - binary_sensor.motion_area_2
```

**Recommendations:**
```
Some numbered entities are legitimate (SIM 2 for dual-SIM phones)
Others indicate integration re-registration:

1. Legitimate numbered entities:
   - SIM 2 sensors (dual SIM phones) - Keep
   - Motion area 2 (if multiple motion zones exist) - Keep

2. Suspicious numbered entities:
   - Device tracker duplicates - Review and remove older version
   - Switch duplicates - Check if both functional, remove duplicate
```

**Priority:** MEDIUM - Review case-by-case

---

## LOW PRIORITY ISSUES

### 8. Disabled Entities Cleanup

**Impact:** Low - Storage/performance optimization

**Current State:**
- 739 total disabled entities
- 649 disabled by integration (diagnostic/advanced entities)
- 78 disabled by user
- 12 disabled by device

**User-Disabled Breakdown:**
```
Sensors: 26
Lights: 20
Scenes: 19
Switches: 7
Buttons: 2
Binary Sensors: 2
Device Trackers: 1
Numbers: 1
```

**Recommendations:**
```
Integration-disabled (649):
  - These are diagnostic entities (RSSI, internal states, etc.)
  - Safe to leave disabled
  - No action needed

User-disabled (78):
  - Review in HA UI: Settings > Devices & Services > Entities
  - Filter by "Disabled" status
  - Delete entities you'll never use
  - Keep entities you may re-enable later
```

**Priority:** LOW - Optional cleanup


### 9. Orphaned Entities (No Device Association)

**Impact:** Low - Most are legitimate helper entities

**Found Issues:**
```
By Platform:
  - person: 5 entities (expected - persons aren't devices)
  - cloud: 3 entities (expected - cloud services)
  - wyoming: 3 entities (expected - voice assistants)
  - homeassistant: 3 entities (expected - system entities)
  - tag: 2 entities (expected - NFC tags)
  - shopping_list: 1 entity (expected - list integration)
  - google_translate: 1 entity (expected - TTS service)
  - input_button: 1 entity (expected - helper)
  - tod: 1 entity (expected - time of day sensor)
  - derivative: 1 entity (expected - utility sensor)
  - local_todo: 1 entity (expected - todo list)
```

**Recommendations:**
```
All identified orphaned entities are legitimate:
  - Template sensors
  - Helper entities (input_boolean, input_number, etc.)
  - System entities (person, zone, etc.)
  - Service entities (TTS, cloud, etc.)

NO ACTION NEEDED - This is normal behavior
```

**Priority:** LOW - No issues found

---

## ENTITY TYPE SUMMARY

### Enabled Entities by Type

```
Sensors:          331 entities (most common)
Switches:         114 entities
Numbers:          111 entities
Binary Sensors:    97 entities
Update:            84 entities
Buttons:           74 entities
Lights:            72 entities
Media Players:     63 entities
Automations:       54 entities
Selects:           42 entities
Input Numbers:     29 entities
Scripts:           22 entities
Device Trackers:   21 entities
Input Booleans:    19 entities
Input Texts:       19 entities
Scenes:            14 entities
Times:              8 entities
Covers:             5 entities
Climate:            5 entities
Input Selects:      5 entities
Locks:              4 entities
Remotes:            4 entities
TTS:                4 entities
Events:             4 entities
STT:                3 entities
Input Datetimes:    2 entities
Tags:               2 entities
Todos:              2 entities
(+ 6 single entities)

TOTAL:          1,225 enabled entities
```

### Integration Distribution (Top 15)

```
Music Assistant:  39 devices, 78 entities
Supervisor:       37 devices, 41 entities
Hue:              35 devices, 43 entities
HACS:             33 devices, 32 entities
Tuya:             23 devices, 5 entities
Tuya Local:       14 devices, 90 entities
Alexa Media:      14 devices, 94 entities
iBeacon:          13 devices, 26 entities
TP-Link:          10 devices, 94 entities
Matter:            9 devices, 60 entities
Mobile App:        7 devices, 103 entities
ZHA:               6 devices, 21 entities
Govee Light:       5 devices, 5 entities
Apple TV:          3 devices, 6 entities
ESPHome:           3 devices, 123 entities
```

---

## SPECIFIC ENTITY TYPE FINDINGS

### Lights (72 entities)

**Integrations:**
- Hue: Primary lighting system (17 lights with None name)
- Matter: 8 lights (integration seems stable)
- TP-Link: 3 lights
- Tuya Local: 10 lights (8 need renaming - see HIGH PRIORITY #2)
- Govee Light Local: 5 lights
- Others: Various specialty lights

**Issues:**
- 8 Tuya lights need identification (HIGH PRIORITY)
- 45 total lights with "None" as original name (verify friendly names)
- 2 living room floor lamp duplicates (HIGH PRIORITY)

**Recommendations:**
- Hue lights appear properly configured
- Focus on Tuya light naming
- Verify all lights have meaningful friendly names

### Switches (114 entities)

**Integrations:**
- Alexa Media: 38 switches (Alexa routines)
- TP-Link: 28 switches (smart plugs)
- Sonos: 11 switches (player controls)
- Tuya Local: 10 switches
- Others: 27 switches

**Issues:**
- 13 switches with numbered suffixes
- Most are Sonos and Hue integration entities

**Recommendations:**
- Review Sonos switches with _2 suffix
- Most switches appear intentional

### Sensors (331 entities - Largest category)

**Integrations:**
- Mobile App: 85 sensors (phone sensors)
- ESPHome: 50 sensors (local devices)
- Alexa Media: 42 sensors
- TP-Link: 27 sensors
- Tesla: 18 sensors
- Others: 109 sensors

**Issues:**
- 21 sensors with numbered suffixes
- Most SIM 2 sensors are legitimate (dual-SIM phones)

**Recommendations:**
- SIM 2 sensors are correct for dual-SIM devices
- Review battery_2 and other unclear numbered sensors

### Climate Devices (5 entities)

**All Working Correctly:**
```
1. climate.gumphrey_hvac_climate_system (Tesla)
2. climate.primary_bedroom_dock_pro_ankits_side (SleepMe)
3. climate.primary_bedroom_dock_pro_danielles_side (SleepMe)
4. climate.dining_room_main_floor_thermostat (Nest)
5. climate.primary_bedroom_upstairs_thermostat (Nest)
```

**No Issues Found**

### Locks (4 entities)

**All Working Correctly:**
```
1. lock.gumphrey_doors (Tesla)
2. lock.gumphrey_charge_port_latch (Tesla)
3. lock.kitchen_back_door (August)
4. lock.basement_pantry_shitbot_child_lock (Tuya Local)
```

**No Issues Found**

### Device Trackers (21 entities)

**Integrations:**
- iBeacon: 13 trackers
- Mobile App: 6 trackers
- Tesla: 2 trackers

**Issues:**
- 4 device trackers with numbered suffixes
- 13 trackers with None as name

**Recommendations:**
- Review numbered suffix trackers (may be old devices)
- Verify iBeacon trackers are functioning

### Media Players (63 entities)

**See HIGH PRIORITY #1 - Music Assistant Duplicates**

39 of 63 media players are Music Assistant duplicates.

---

## INTEGRATION OVERLAP ANALYSIS

### No Cross-Integration Device Duplicates Found

**Good News:** No devices were found with the same IEEE/MAC address across multiple integrations.

**What This Means:**
- No Zigbee devices duplicated across ZHA/Zigbee2MQTT
- No devices exposed via both Matter and native integration
- No WiFi devices duplicated across integrations

**Exception:** Music Assistant intentionally creates virtual players

### Integration Instances

```
Matter: 1 instance (9 devices)
Zigbee (ZHA): 1 instance (6 devices)
HomeKit Controller: 0 instances
Hue: 1 instance (35 devices)
MQTT: 0 instances
ESPHome: 1 instance (3 devices)
```

**No problematic overlaps detected**

---

## ACTION PLAN

### Phase 1: High Priority (Do This Week)

1. **Decide on Music Assistant Strategy**
   - Keep MA: Disable/hide native players, rename MA entities
   - Remove MA: Disable integration, use native players
   - **Impact:** Resolves 39 duplicate entities

2. **Rename Tuya RGBCW Lights**
   - Identify each bulb's location
   - Rename all 8 lights with meaningful names
   - **Impact:** Makes lights usable in voice commands and UI

3. **Fix Duplicate Automations**
   - Review and disable automation.update_color_temp_helpers_by_time_of_day_2
   - Review and disable automation.primary_bedroom_dial_toggle_2
   - Test for 24 hours, then delete
   - **Impact:** Prevents double-triggering issues

4. **Fix Living Room Floor Lamp**
   - Test both entities
   - Disable non-functional duplicate
   - **Impact:** Eliminates confusion

### Phase 2: Medium Priority (Do This Month)

5. **Fix Matter Integration Issues**
   - Remove affected devices from Matter
   - Re-add cleanly
   - **Impact:** Removes 8 entities with wrong suffixes

6. **Review Numbered Suffix Entities**
   - Device trackers: Remove old/inactive devices
   - Switches: Identify and fix Sonos duplicates
   - Sensors: Keep SIM 2, review others
   - **Impact:** Cleaner entity list

7. **Verify Friendly Names**
   - Check all "None" named entities have friendly names
   - Set friendly names where missing
   - **Impact:** Better UI/voice command experience

### Phase 3: Low Priority (Optional)

8. **Clean Up Disabled Entities**
   - Review 78 user-disabled entities
   - Delete entities never to be re-enabled
   - **Impact:** Minor storage/performance improvement

---

## CONCLUSION

Your Home Assistant instance is generally well-configured with **no major structural issues**. The primary concerns are:

1. **Music Assistant duplicates** - Architectural decision needed
2. **Tuya light naming** - Quick fix with high usability impact
3. **2 duplicate automations** - Potential functional issue
4. **Matter integration** - Needs cleanup and re-pairing

After addressing the High Priority items, your system will be significantly cleaner and easier to manage.

**Estimated Time to Fix High Priority Issues:** 1-2 hours

---

## DETAILED ENTITY LISTS

For detailed entity-by-entity information, see:
- `/tmp/audit_report.txt` - Full audit with all duplicates
- `/tmp/audit_summary.txt` - Executive summary
- `/tmp/deep_dive_report.txt` - Entity type deep dive

## FILES GENERATED

All analysis files are saved to `/tmp/`:
- `entity_registry.json` - Raw entity data
- `device_registry.json` - Raw device data
- `config_entries.json` - Integration configuration
- `audit_ha_entities.py` - Comprehensive audit script
- `audit_summary.py` - Summary generation script
- `detailed_recommendations.py` - Detailed recommendation script
- `entity_type_deep_dive.py` - Deep dive analysis script
- `audit_report.txt` - Full audit output
- `audit_summary.txt` - Summary output
- `deep_dive_report.txt` - Deep dive output

---

**Report Generated:** 2026-01-13
**Audit Tool:** Custom Python analysis scripts
**Data Source:** Home Assistant Core Storage Files
