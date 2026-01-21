# Laundry Load Management Automation

This automation system tracks laundry loads and nags household members to move clothes from the washer to the dryer.

## Features

- **Automatic Detection**: Detects when the washer starts based on power consumption
- **Load Ownership**: Asks whose load it is and tracks the owner
- **Smart Notifications**: Alerts the load owner when the washer finishes
- **Escalating Nags**: 
  - Starts with 5-minute reminders
  - Escalates to 1-minute reminders after 20 minutes of inaction
- **Automatic Completion**: Stops nagging when dryer vibration is detected

## Required Entities

### Already Configured
- `sensor.washer_running_current_consumption` - Power consumption sensor for the washer
- `input_number.washer_idle_threshold` - Threshold to determine when washer is idle (default: 2W)
- `input_select.washer_owner` - Tracks whose load is in the washer

### Needs to be Added
⚠️ **REQUIRED**: You need to add a dryer vibration sensor:
- `binary_sensor.dryer_vibration` - Detects when the dryer is running

**How to add a dryer vibration sensor:**
1. Use a Zigbee/Z-Wave vibration sensor (e.g., Aqara vibration sensor)
2. Attach it to the dryer
3. Ensure the entity ID is `binary_sensor.dryer_vibration` or update the automation

### New Input Helpers (Already Added)
- `input_boolean.laundry_nag_enabled` - Controls whether nagging is active
- `input_datetime.washer_stopped_time` - Tracks when the washer stopped

## Automations

### 1. automation_laundry_washer_started.yaml
Triggers when washer power consumption goes above the idle threshold. Asks whose load it is via notifications with actionable buttons.

### 2. automation_laundry_set_owner.yaml
Handles notification button presses to set the washer owner.

### 3. automation_laundry_washer_finished.yaml
Triggers when washer power consumption drops below the idle threshold. Alerts the load owner and starts nagging.

### 4. automation_laundry_nag.yaml
Sends periodic reminders to move clothes:
- Every 5 minutes for the first 20 minutes
- Every 1 minute after 20 minutes

### 5. automation_laundry_dryer_started.yaml
Stops nagging when dryer vibration is detected (dryer started). Detection requires the vibration sensor to be on for 10 seconds to confirm the dryer is running.

## Workflow

```
Washer starts (power > threshold)
    ↓
Ask: "Whose load is it?"
    ↓
[User selects owner via notification button]
    ↓
Washer finishes (power < threshold)
    ↓
Alert owner: "Move clothes to dryer"
    ↓
Start 5-minute nags
    ↓
After 20 min → Escalate to 1-minute nags
    ↓
Dryer vibration detected
    ↓
Stop nagging, reset owner to "Unknown"
```

## Notifications

Notifications are sent via:
- **Alexa announcements** using `script.alexa_announce_router`
- **Mobile push notifications** to the `notify.adults` group

## Customization

### Adjust Timing
Edit the automations to change:
- Washer detection delay (default: 2 minutes)
- Initial nag interval (default: 5 minutes)
- Escalation time (default: 20 minutes)
- Escalated nag interval (default: 1 minute)

### Change Messages
Edit the `message` fields in each automation to customize announcements.

### Add More Family Members
The notification buttons already include all members defined in `input_select.washer_owner`:
- Ankit, Danielle, Zoe, Max, Aiden, Mixed

## Testing

1. **Test washer detection**: Run the washer and verify you receive the "whose load" notification
2. **Test owner selection**: Tap a name on the notification
3. **Test finish detection**: Wait for washer to finish and verify the alert
4. **Test nagging**: Wait 5 minutes and verify you receive nag reminders
5. **Test escalation**: Wait 20+ minutes and verify nags increase to 1-minute intervals
6. **Test dryer detection**: Start the dryer and verify nagging stops

## Troubleshooting

### No notifications when washer starts
- Check that `sensor.washer_running_current_consumption` exists
- Verify `input_number.washer_idle_threshold` is set correctly (default: 2W)
- Check washer power consumption in Home Assistant UI

### Nags don't stop when dryer starts
- Verify `binary_sensor.dryer_vibration` exists and is working
- Check the entity ID matches in `automation_laundry_dryer_started.yaml`
- Ensure the vibration sensor is properly attached to the dryer

### Can't see notification buttons
- Ensure you're using the Home Assistant mobile app
- Check that notification actions are enabled in app settings

## Deployment

After making any changes:
```bash
# Sync to server
./sync_to_ha.sh

# Restart Home Assistant
ssh root@192.168.4.141 'ha core restart'

# Monitor logs
ssh root@192.168.4.141 'ha logs follow'
```
