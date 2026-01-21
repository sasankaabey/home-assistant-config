# Washer Door Sensor Setup

## What You Need

The improved washer load assignment trigger now uses **door close + power spike** detection for faster, more reliable load assignment.

### Required Entity: `binary_sensor.washer_door`

This automation expects a door/window sensor on your washer that provides:
- **State: `off`** when door is CLOSED (load is starting)
- **State: `on`** when door is OPEN

## How to Find Your Door Sensor

### Option 1: Check Home Assistant UI
1. Go to **Developer Tools → States**
2. Search for entities containing `washer` or `door`
3. Look for binary_sensor entities on your washer device
4. Common names: `door_open`, `device_state`, `contact_sensor`

### Option 2: Check Your Device
If your washer is a smart device (Meross, Tuya, etc.), check what entities it exposes:
1. **Configuration → Integrations**
2. Find your washer device
3. Click to view all entities
4. Look for door/contact sensor entities

### Option 3: SSH to Production Server
```bash
ssh root@192.168.4.141
ha core check
grep -r "washer" /config/.storage/core.entity_registry | grep binary_sensor
```

## Setup Steps

### If Door Sensor Exists

1. **Find the entity ID** using one of the methods above
2. **Update the automation:**
   ```bash
   cd /Users/ankit/Developer/sasankaabey/home-assistant-config
   # Edit automations/automation_laundry_washer_started.yaml
   # Change line ~20 from:
   #   entity_id: binary_sensor.washer_door
   # To your actual entity ID, e.g.:
   #   entity_id: binary_sensor.washer_contact
   ```
3. **Deploy to production:**
   ```bash
   ./sync_to_ha.sh
   ssh root@192.168.4.141 'ha core restart'
   ```

### If Door Sensor Does NOT Exist

You have two options:

#### Option A: Add a Physical Door Sensor (Recommended)
1. Purchase a Zigbee/Z-Wave door sensor (e.g., Aqara Door Sensor)
2. Attach it to the washer door
3. Pair with Home Assistant
4. Update automation with the new entity ID

#### Option B: Use Fallback Automation (Power-Based)
1. **Disable the door-based automation:**
   ```bash
   # Comment out automation_laundry_washer_started.yaml
   # Uncomment automation_laundry_washer_started_fallback.yaml
   ```
2. **The fallback uses:**
   - 30-second power threshold (vs old 2-minute delay)
   - Sustained power confirmation to prevent false positives
   - Same notification logic

## Testing

Once deployed, test by:
1. Close washer door (if using door sensor)
2. Start a load
3. You should receive "Whose load is it?" notification within 3-5 seconds
4. If notification doesn't arrive, check Home Assistant logs:
   ```bash
   ssh root@192.168.4.141
   ha logs follow | grep laundry
   ```

## Benefits of Door Sensor Approach

- **Faster**: Notification in 3-5 seconds vs 2 minutes (or 30 sec with fallback)
- **More Reliable**: Physical door close = definite load being added
- **Prevents False Positives**: Power spike + door close = high confidence
- **Handles Edge Cases**: If power spikes and drops, no false notification

## Current Status

As of 2026-01-21, the automation is configured for `binary_sensor.washer_door` but **NOT YET TESTED** on production.

**Next Step**: Identify the actual door sensor entity ID and update the automation before deploying.

## Troubleshooting

### Notification Not Firing
1. Check door sensor state in UI: Developer Tools → States
2. Verify power sensor is working: `sensor.washer_running_current_consumption`
3. Check `input_number.washer_idle_threshold` value (should be above zombie draw, e.g., 5W)
4. Check logs: `ha logs follow | grep laundry`

### False Positives (Notifications When Washer Not Started)
1. Increase `input_number.washer_idle_threshold` value
2. Increase the 3-second stabilization delay in automation
3. Consider using fallback automation with 30-second threshold

### Notification Too Slow
1. Decrease the 3-second stabilization delay
2. Verify door sensor is responding quickly (check state changes in UI)

