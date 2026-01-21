# Fallback Integration Pattern

## Problem

Some integrations (especially tuya_local) occasionally show devices as `unavailable` while the cloud integration (tuya) remains available. We prefer local integrations for:
- Lower latency
- No cloud dependency
- Better privacy
- More reliable when internet is down

But we need fallback to cloud when local becomes unavailable.

## Solution: Template Sensors with Fallback Logic

Create template sensors that:
1. **Prefer local** integration entity
2. **Fallback to cloud** when local is unavailable/unknown
3. **Report availability** based on either source being available

## Implementation

### Pattern Template (binary_sensor)

```yaml
- binary_sensor:
    - name: "Device Name"
      unique_id: device_name_fallback
      device_class: door  # or motion, window, etc.
      state: >-
        {# Prefer local, fallback to cloud #}
        {% if states('binary_sensor.device_local') not in ['unavailable', 'unknown'] %}
          {{ states('binary_sensor.device_local') }}
        {% else %}
          {{ states('binary_sensor.device_cloud') }}
        {% endif %}
      availability: >-
        {{ states('binary_sensor.device_local') not in ['unavailable', 'unknown']
           or states('binary_sensor.device_cloud') not in ['unavailable', 'unknown'] }}
```

### Pattern Template (sensor)

```yaml
- sensor:
    - name: "Device Name"
      unique_id: device_name_fallback
      state: >-
        {% if states('sensor.device_local') not in ['unavailable', 'unknown'] %}
          {{ states('sensor.device_local') }}
        {% else %}
          {{ states('sensor.device_cloud') }}
        {% endif %}
      unit_of_measurement: "W"  # or °C, %, etc.
      device_class: power  # or temperature, humidity, etc.
      availability: >-
        {{ states('sensor.device_local') not in ['unavailable', 'unknown']
           or states('sensor.device_cloud') not in ['unavailable', 'unknown'] }}
```

## Current Implementation

### Washer Door Sensor

**Template**: `binary_sensor.washer_door` (in `template.yaml`)  
**Prefers**: `binary_sensor.washer_door_local` (tuya_local)  
**Fallback**: `binary_sensor.contact_sensor_door` (tuya cloud)  
**Used in**: `automation_laundry_washer_started.yaml`

### Dryer Door Sensor

**Template**: `binary_sensor.dryer_door` (in `template.yaml`)  
**Prefers**: `binary_sensor.dryer_door_local` (tuya_local)  
**Fallback**: `binary_sensor.contact_sensor_2_door` (tuya cloud)  
**Used in**: _(future dryer automation)_

## When to Use This Pattern

✅ **Use fallback for critical automation triggers:**
- Door sensors that trigger load assignments
- Motion sensors for lighting
- Contact sensors for security
- Power sensors for appliance state

❌ **Don't use fallback for:**
- Diagnostic/debugging sensors
- Sensors that are informational only
- Entities that are rarely unavailable

## Benefits

1. **Resilience**: Automation continues working even when local integration fails
2. **Preference**: Still uses local when available (lower latency, no cloud)
3. **Transparency**: Clear availability status (shows unavailable only when BOTH fail)
4. **Simplicity**: Automations use one sensor name, fallback is transparent

## Adding New Fallback Sensors

### Step 1: Identify Entity IDs

Find both local and cloud entity IDs:
```bash
# SSH to HA server
ssh root@192.168.4.141
ha core check
# Check entity registry for device
grep -A10 "device_name" /config/.storage/core.entity_registry
```

### Step 2: Add Template to template.yaml

Copy the pattern above and customize:
- Set unique `name` and `unique_id`
- Update local entity ID
- Update cloud entity ID
- Set correct `device_class`
- Add custom icon (optional)

### Step 3: Update Automations

Replace direct entity references with the fallback template:
```yaml
# OLD:
entity_id: binary_sensor.device_cloud

# NEW:
entity_id: binary_sensor.device_name  # Uses fallback template
```

### Step 4: Deploy and Test

```bash
./sync_to_ha.sh
ssh root@192.168.4.141 'ha core restart'
# Test: disable local integration, verify automation still works
# Test: re-enable local, verify it's preferred again
```

## Monitoring Fallback Usage

### Check Current State Source

In Developer Tools → Template:
```yaml
{# Check which source is being used #}
Washer door local: {{ states('binary_sensor.washer_door_local') }}
Washer door cloud: {{ states('binary_sensor.contact_sensor_door') }}
Washer door fallback: {{ states('binary_sensor.washer_door') }}

{# Determine active source #}
{% if states('binary_sensor.washer_door_local') not in ['unavailable', 'unknown'] %}
  Using: LOCAL (preferred)
{% else %}
  Using: CLOUD (fallback)
{% endif %}
```

### Create Alert for Fallback Usage (Optional)

```yaml
# In automations/
- alias: "Alert: Tuya Local Integration Unavailable"
  trigger:
    - platform: state
      entity_id: binary_sensor.washer_door_local
      to: "unavailable"
      for:
        minutes: 5
  action:
    - service: notify.adults
      data:
        title: "Integration Issue"
        message: "Washer door sensor fell back to cloud. Check tuya_local integration."
```

## Troubleshooting

### Fallback Not Working

1. **Check entity IDs are correct:**
   - Developer Tools → States
   - Search for both local and cloud entities
   - Verify exact entity_id matches template

2. **Check template syntax:**
   ```bash
   # Test in Developer Tools → Template
   {% if states('binary_sensor.device_local') not in ['unavailable', 'unknown'] %}
     LOCAL
   {% else %}
     CLOUD
   {% endif %}
   ```

3. **Check HA logs:**
   ```bash
   ssh root@192.168.4.141
   ha logs | grep -i template
   ```

### Both Sources Unavailable

If both local AND cloud show unavailable:
1. Check device power/connectivity
2. Check integration status: Configuration → Integrations
3. Reload integration: Configuration → Integrations → [Integration] → Reload
4. Check network connectivity to device

### Local Never Used (Always on Cloud)

If fallback always uses cloud even when local is available:
1. Verify local entity_id is correct
2. Check local entity state: Developer Tools → States
3. Ensure local integration is loaded: Configuration → Integrations
4. Check tuya_local logs for errors

## Future Enhancements

Consider expanding to other entities:
- Power monitoring sensors (washer/dryer current consumption)
- Temperature sensors
- Motion sensors for lighting automations
- Smart switch/plug states

Pattern is reusable - just update entity IDs and device_class.

