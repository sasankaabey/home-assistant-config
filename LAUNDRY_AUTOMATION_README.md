# Laundry Load Management Automation

This automation system tracks laundry loads from washer to dryer with comprehensive ownership tracking, escalating reminders, and availability notifications.

## Features

### Washer Management
- **Automatic Detection**: Detects when the washer starts based on power consumption
- **Load Ownership**: Asks whose load it is and tracks the owner
- **Smart Notifications**: Alerts the load owner when the washer finishes
- **Escalating Nags**: 
  - Starts with 5-minute reminders
  - Escalates to 1-minute reminders after 20 minutes of inaction
- **Next Load Handling**: Asks if owner has another load when washer finishes

### Dryer Management
- **Ownership Transfer**: Washer owner becomes dryer owner when dryer starts
- **Finish Detection**: Alerts when dryer vibration stops
- **Smart Nagging**: 
  - 5-minute grace period
  - Only nags if washer is running AND door hasn't been opened
  - Escalates to 1-minute nags after 10 minutes total
- **Door Integration**: 
  - Tracks door opening (stops nagging)
  - Asks if clothes are dry when door closes
- **Not Dry Handling**: Guides user to restart dryer if clothes need more time

### Availability Notifications
- **Dryer Available**: Alerts household when dryer is free
- **Washer Available**: 
  - Gives owner 5 minutes for next load
  - Alerts all household if no response or no more loads

## Required Entities

### Already Configured
- `sensor.washer_running_current_consumption` - Power consumption sensor for the washer
- `input_number.washer_idle_threshold` - Threshold to determine when washer is idle (default: 2W)
- `input_select.washer_owner` - Tracks whose load is in the washer

### Needs to be Added
⚠️ **REQUIRED**: You need to add these sensors:
- `binary_sensor.dryer_vibration` - Detects when the dryer is running (e.g., Aqara vibration sensor)
- `binary_sensor.dryer_door` - Detects when dryer door opens/closes (e.g., contact sensor)

**How to add sensors:**
1. **Dryer vibration sensor**: Use a Zigbee/Z-Wave vibration sensor (e.g., Aqara vibration sensor) attached to the dryer
2. **Dryer door sensor**: Use a contact sensor on the dryer door
3. Ensure entity IDs match or update the automations

### New Input Helpers (Already Added)
- `input_boolean.laundry_nag_enabled` - Controls whether washer nagging is active
- `input_boolean.dryer_nag_enabled` - Controls whether dryer nagging is active
- `input_boolean.dryer_door_opened_since_stop` - Tracks if door was opened after dryer finished
- `input_boolean.awaiting_dry_confirmation` - Waiting for user to confirm if clothes are dry
- `input_boolean.awaiting_next_load_response` - Waiting for user to respond about next load
- `input_datetime.washer_stopped_time` - Tracks when the washer stopped
- `input_datetime.dryer_stopped_time` - Tracks when the dryer stopped
- `input_select.dryer_owner` - Tracks whose load is in the dryer

## Automations

### Washer Automations

#### 1. automation_laundry_washer_started.yaml
Triggers when washer power consumption goes above the idle threshold. Asks whose load it is via notifications with actionable buttons.

#### 2. automation_laundry_set_owner.yaml
Handles notification button presses to set the washer owner.

#### 3. automation_laundry_washer_finished.yaml
Triggers when washer power consumption drops below the idle threshold. Alerts the load owner, starts nagging, and asks if they have another load.

#### 4. automation_laundry_nag.yaml
Sends periodic reminders to move clothes:
- Every 5 minutes for the first 20 minutes
- Every 1 minute after 20 minutes

### Dryer Automations

#### 5. automation_laundry_dryer_started.yaml
Stops washer nagging when dryer vibration is detected. Transfers ownership from washer_owner to dryer_owner.

#### 6. automation_laundry_dryer_finished.yaml
Triggers when dryer vibration stops. Alerts dryer owner to check if clothes are dry.

#### 7. automation_laundry_dryer_nag.yaml
Nags dryer owner to check the dryer:
- 5-minute grace period initially (no nags)
- After 5 minutes, nags every 5 minutes
- After 10 minutes total elapsed, escalates to every 1 minute
- Only nags if washer is running AND door hasn't been opened

#### 8. automation_laundry_dryer_door_opened.yaml
Tracks when dryer door is opened after dryer finishes. Stops dryer nagging.

#### 9. automation_laundry_dryer_door_closed.yaml
Asks if clothes are dry when dryer door is closed after being opened.

#### 10. automation_laundry_handle_dry_confirmation.yaml
Handles responses to "are clothes dry" question:
- If dry: Resets dryer owner, announces dryer availability
- If not dry: Guides user to restart dryer

#### 11. automation_laundry_dryer_restarted.yaml
Resets state when dryer is restarted after clothes weren't dry.

### Availability Automations

#### 12. automation_laundry_handle_next_load.yaml
Handles responses about having another load:
- If yes: Reserves washer for 5 minutes
- If no: Announces washer availability to all
- If 5 minutes expire: Announces washer availability to all

#### 13. automation_laundry_next_load_timeout.yaml
Alerts household if no response about next load after 5 minutes.

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
Ask: "Do you have another load?"
    ↓
Start 5-minute nags
    ↓
After 20 min → Escalate to 1-minute nags
    ↓
Dryer vibration detected
    ↓
Stop washer nagging, transfer to dryer owner
Announce: "Thank you for moving clothes"
    ↓
Dryer vibration stops (dryer finishes)
    ↓
Alert dryer owner: "Check if clothes are dry"
Enable dryer nagging (5 min grace)
    ↓
If washer running & door not opened:
    → Nag every 5 min (up to 10 min total)
    → Then nag every 1 min
    ↓
Dryer door opens
    ↓
Stop dryer nagging
    ↓
Dryer door closes
    ↓
Ask: "Are clothes dry?"
    ↓
If YES:
    → Announce: "Dryer available"
    → Reset dryer owner
If NO:
    → Guide to restart dryer
    → Monitor for dryer restart
    ↓
Meanwhile, handle "next load" response:
    ↓
If YES (another load):
    → Reserve washer for 5 minutes
    → If not started: Announce washer available to all
If NO (no more loads):
    → Announce washer available to all
If NO RESPONSE (5 min timeout):
    → Announce washer available to all
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

### Phase 1: Washer Detection
1. **Test washer start detection**: Run the washer and verify you receive the "whose load" notification
2. **Test owner selection**: Tap a name on the notification
3. **Test washer finish detection**: Wait for washer to finish and verify the alert
4. **Test washer nagging**: Wait 5 minutes and verify you receive nag reminders
5. **Test nag escalation**: Wait 20+ minutes and verify nags increase to 1-minute intervals

### Phase 2: Dryer Transfer
6. **Test dryer start detection**: Start the dryer and verify:
   - Washer nagging stops
   - Ownership transfers to dryer
   - Thank you message is received

### Phase 3: Dryer Management
7. **Test dryer finish detection**: Wait for dryer to finish and verify the alert
8. **Test dryer nagging grace period**: Don't open door for 5 minutes, verify no nags if washer not running
9. **Test dryer nagging with washer running**: Start washer, verify dryer nags begin after 5 min grace
10. **Test dryer nag escalation**: Wait 10+ minutes total and verify nags increase to 1-minute intervals
11. **Test door opening**: Open dryer door and verify nagging stops

### Phase 4: Dry Confirmation
12. **Test door closing question**: Close dryer door and verify "are clothes dry" question
13. **Test "clothes are dry" response**: Select "Yes, Dry" and verify:
    - Dryer available announcement
    - Dryer owner reset
14. **Test "clothes not dry" response**: Select "No, Not Dry" and verify restart guidance

### Phase 5: Next Load Handling
15. **Test next load question**: When washer finishes, verify you're asked about another load
16. **Test "yes another load" response**: Select "Yes" and verify 5-minute reservation
17. **Test reservation timeout**: Don't start washer within 5 min, verify availability announcement
18. **Test "no more loads" response**: Select "No" and verify immediate availability announcement
19. **Test no response timeout**: Don't respond for 5 min, verify availability announcement

## Troubleshooting

### No notifications when washer starts
- Check that `sensor.washer_running_current_consumption` exists
- Verify `input_number.washer_idle_threshold` is set correctly (default: 2W)
- Check washer power consumption in Home Assistant UI

### Washer nags don't stop when dryer starts
- Verify `binary_sensor.dryer_vibration` exists and is working
- Check the entity ID matches in `automation_laundry_dryer_started.yaml`
- Ensure the vibration sensor is properly attached to the dryer
- Verify sensor updates when dryer is running

### Dryer nags not working
- Verify `binary_sensor.dryer_vibration` exists and detects when dryer stops
- Check that washer is running (nagging only happens if washer is running)
- Verify door hasn't been opened (check `input_boolean.dryer_door_opened_since_stop`)

### Door sensor not detected
- Verify `binary_sensor.dryer_door` exists and is working
- Check the entity ID matches in the door automations
- Test the sensor by opening/closing the door and checking state in HA UI

### "Are clothes dry" question not appearing
- Verify door was opened first (check `input_boolean.dryer_door_opened_since_stop`)
- Check that dryer owner is set (not "Unknown")
- Verify door close detection is working

### Next load question not appearing
- Check that washer owner was set (not "Unknown") when washer finished
- Verify the automation triggered by checking logs

### Can't see notification buttons
- Ensure you're using the Home Assistant mobile app
- Check that notification actions are enabled in app settings
- Verify you're receiving other actionable notifications

### Availability announcements not heard
- Check Alexa device connectivity
- Verify `script.alexa_announce_router` is working
- Test with manual Alexa announcement

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
