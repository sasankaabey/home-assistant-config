# Quick Cleanup Guide - Home Assistant Entity Audit

**Date:** 2026-01-13
**System:** Home Assistant 2026.1.1

## Summary

- **Total Entities:** 1,964 (1,225 enabled, 739 disabled)
- **High Priority Issues:** 4
- **Medium Priority Issues:** 3
- **Estimated Cleanup Time:** 1-2 hours for high priority items

---

## HIGH PRIORITY FIXES

### 1. Rename 8 Tuya RGBCW Lights

**Problem:** Lights have generic names like `light.rgbcw_lightbulb`, `light.rgbcw_lightbulb_2`, etc.

**Solution:**
1. Go to: Settings > Devices & Services > Entities
2. Search for: `rgbcw_lightbulb`
3. For each light:
   - Click the entity
   - Click "Edit"
   - Turn on the light to identify location
   - Rename to: `[room]_[location]` (e.g., `bedroom_ceiling`)
   - Click "Update"

**Entities to rename:**
- `light.rgbcw_lightbulb`
- `light.rgbcw_lightbulb_2`
- `light.rgbcw_lightbulb_3`
- `light.rgbcw_lightbulb_4`
- `light.rgbcw_lightbulb_5`
- `light.rgbcw_lightbulb_6`
- `light.rgbcw_lightbulb_7`
- `light.rgbcw_lightbulb_8`

---

### 2. Fix 2 Duplicate Automations

**Problem:** Duplicate automations are both enabled and may conflict

**Solution:**
1. Go to: Settings > Automations & Scenes
2. Find and disable these automations:
   - `automation.update_color_temp_helpers_by_time_of_day_2`
   - `automation.primary_bedroom_dial_toggle_2`
3. Test for 24 hours
4. If no issues, delete the disabled duplicates

**Keep the originals:**
- `automation.update_color_temp_helpers_by_time_of_day`
- `automation.primary_bedroom_dial_toggle`

---

### 3. Fix Living Room Floor Lamp Duplicate

**Problem:** Two entities for the same lamp

**Solution:**
1. Test both entities:
   - `light.living_room_floor_lamp`
   - `light.living_room_floor_lamp_2`
2. Turn each on/off to see which works
3. Disable the non-functional entity
4. If both work, you may need to unpair and re-pair the light in Hue app

---

### 4. Decide on Music Assistant Strategy

**Problem:** 39 Music Assistant virtual media players duplicate 21 physical players

**Option A - Keep Music Assistant:**
1. Continue using MA players for music playback
2. Hide native players (Sonos, Apple TV, etc.) from UI
3. Rename MA entities for clarity
4. Benefit: Unified music control across all devices

**Option B - Remove Music Assistant:**
1. Go to: Settings > Devices & Services > Music Assistant
2. Click "Delete"
3. Confirm deletion (removes 39 entities)
4. Use native integration players instead
5. Benefit: Simpler configuration, fewer entities

**Recommendation:** If you actively use Music Assistant for multi-room audio, keep it. If you rarely use it, remove it to simplify.

---

## MEDIUM PRIORITY FIXES

### 5. Fix Matter Integration Entities

**Problem:** Matter devices have numbered suffix entities (indicates re-addition)

**Affected entities:**
- Kitchen ceiling buttons: `_identify_2`, `_identify_3`, `_identify_4`
- Dining room updates: `_2`, `_3`
- Kitchen ceiling updates: `_2`, `_3`, `_4`

**Solution:**
1. Go to: Settings > Devices & Services > Matter
2. For each affected device:
   - Click the device
   - Click "Remove Device"
   - Factory reset the device (if needed)
   - Re-add to Matter integration
3. This should eliminate numbered suffixes

---

### 6. Review Device Tracker Duplicates

**Problem:** Old device trackers with `_2` suffix

**Entities to review:**
- `device_tracker.ankits_macbook_air_2`
- `device_tracker.luffy55_2`
- `device_tracker.zoe_s_phone_2`
- `device_tracker.l302qa0_49eb_2`

**Solution:**
1. Check if original entity exists (without `_2`)
2. If original exists and works, delete the `_2` version
3. Go to: Settings > Devices & Services > Entities
4. Search for entity, click, disable, then delete

---

### 7. Verify Friendly Names

**Problem:** 45 lights and other entities have "None" as original name

**Solution:**
1. These entities likely already have friendly names set in UI
2. Verify by checking Developer Tools > States
3. If missing friendly name, edit entity and add one
4. Focus on most-used entities first

---

## LOW PRIORITY (OPTIONAL)

### 8. Clean Up User-Disabled Entities

**Stats:**
- 78 user-disabled entities
- 26 sensors, 20 lights, 19 scenes, 7 switches, etc.

**Solution:**
1. Go to: Settings > Devices & Services > Entities
2. Filter by: Status = Disabled
3. Review each entity
4. If you'll never re-enable it, delete it
5. Otherwise leave disabled (no harm)

---

## VERIFICATION CHECKLIST

After completing high priority fixes:

```
[ ] All 8 Tuya lights have meaningful names
[ ] Only 1 version of each automation exists (no _2 suffix)
[ ] Living room floor lamp duplicate resolved
[ ] Music Assistant decision made and implemented
[ ] No numbered suffix entities in Matter integration
[ ] Device tracker duplicates removed
[ ] All frequently-used entities have friendly names
```

---

## WHAT'S GOOD

Your Home Assistant configuration is generally excellent:

✓ No cross-integration device duplicates found
✓ No Zigbee/Matter overlap issues
✓ Climate devices all working correctly
✓ Locks all working correctly
✓ Well-organized integration usage
✓ Good use of helpers and templates

The issues found are mostly naming/cosmetic, not functional problems.

---

## NEED MORE DETAIL?

See full audit report: `ENTITY_AUDIT_REPORT_2026-01-13.md`

This report includes:
- Complete entity breakdown by type
- Integration overlap analysis
- Detailed recommendations by priority
- Entity-by-entity listings
- Integration distribution statistics

---

## AUDIT FILES LOCATION

All analysis files saved to `/tmp/`:
- Entity/device/config registry JSON files
- Analysis scripts (Python)
- Full audit outputs (TXT)
- This report and detailed report (MD)

To re-run audit: `python3 /tmp/audit_ha_entities.py`
