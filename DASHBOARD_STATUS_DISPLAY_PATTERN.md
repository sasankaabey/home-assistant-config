# Dashboard Integration Status Display Pattern

## Overview

When using fallback integrations (preferring local, falling back to cloud), it's helpful to show in dashboards **which integration is currently providing the data**. This helps users understand when fallbacks are active.

## Pattern

Create template sensors that show both the state AND which integration is active:

```yaml
- sensor:
    - name: "Device Status"
      unique_id: device_status_display
      state: >-
        {% set state = states('binary_sensor.device') %}
        {% set local_available = states('binary_sensor.device_local') not in ['unavailable', 'unknown'] %}
        {% set state_text = "Closed" if state == 'off' else "Open" if state == 'on' else "Unknown" %}
        {% set source = "tuya_local" if local_available else "tuya" %}
        {{ state_text }} ({{ source }})
      icon: ...
```

This creates a sensor that shows: `Closed (tuya_local)` or `Open (tuya)`

## Current Implementation

### Washer Door Status
**Entity**: `sensor.washer_door_status`  
**Format**: `"Closed (tuya_local)"` or `"Open (tuya)"`  
**Shows**: Current state + which integration is providing data

### Dryer Door Status
**Entity**: `sensor.dryer_door_status`  
**Format**: `"Closed (tuya_local)"` or `"Open (tuya)"`  
**Shows**: Current state + which integration is providing data

## Dashboard Examples

### Simple Entity Card (Recommended)

```yaml
type: entity
entity: sensor.washer_door_status
```

Shows: `Closed (tuya_local)`

With icon that changes based on state:
- Door open: 🔴 washing-machine-alert
- Door closed: ✅ washing-machine

### Custom Card with Details

For more control, use a template card:

```yaml
type: custom:template-entity-row
entity: binary_sensor.washer_door
name: Washer Door
state_template: >-
  {% set state = states('binary_sensor.washer_door') %}
  {% set local = states('binary_sensor.washer_door_local') not in ['unavailable', 'unknown'] %}
  {{ "Closed" if state == 'off' else "Open" }}
  ({{ "local" if local else "cloud" }})
```

### Alert Card (When Fallback Active)

Show a warning card when using cloud fallback:

```yaml
type: custom:button-card
template: warning
state_template: >-
  {% if states('binary_sensor.washer_door_local') in ['unavailable', 'unknown'] %}
    Washer door using cloud integration
  {% else %}
    Washer door using local integration
  {% endif %}
  
condition:
  - entity_id: binary_sensor.washer_door_local
    state: unavailable
```

### Laundry Dashboard Example

For your main laundry dashboard, replace the old entity references with the new status sensors:

```yaml
type: vertical-stack
cards:
  - type: heading
    heading: Laundry Status
  
  - type: grid
    columns: 2
    cards:
      - type: entity
        entity: sensor.washer_door_status
        name: Washer Door
      
      - type: entity
        entity: sensor.dryer_door_status
        name: Dryer Door
      
      - type: entity
        entity: input_select.washer_owner
        name: Washer Load
      
      - type: entity
        entity: input_select.dryer_owner
        name: Dryer Load
      
      - type: entity
        entity: sensor.lg_washer_current_consumption
        name: Washer Power
```

## Adding Status Display to Other Devices

### Step 1: Identify Your Entities

For any device with fallback, you have:
- `binary_sensor.device_local` (tuya_local)
- `binary_sensor.device_cloud` (tuya cloud)
- `binary_sensor.device` (fallback template)

### Step 2: Add Template to template.yaml

```yaml
- sensor:
    - name: "Device Status"
      unique_id: device_status_display
      state: >-
        {% set state = states('binary_sensor.device') %}
        {% set local_available = states('binary_sensor.device_local') not in ['unavailable', 'unknown'] %}
        {% set state_text = "Closed" if state == 'off' else "Open" if state == 'on' else "Unknown" %}
        {% set source = "tuya_local" if local_available else "tuya" %}
        {{ state_text }} ({{ source }})
```

### Step 3: Update Dashboard Cards

Replace old entity cards with new status sensor:

```yaml
# OLD
- type: entity
  entity: binary_sensor.washer_door_local

# NEW
- type: entity
  entity: sensor.washer_door_status
```

## Benefits

✅ **Transparency**: Users see which integration is active  
✅ **Debugging**: Easy to spot when fallback is in use  
✅ **Trust**: Shows automation isn't broken, just using fallback  
✅ **Maintenance**: Help homeowners understand integration health  

## Variations

### Compact Format

```yaml
state: >-
  {% set state = states('binary_sensor.device') %}
  {% set local = states('binary_sensor.device_local') not in ['unavailable', 'unknown'] %}
  {{ "🟢" if state == 'off' else "🔴" }} {{ "L" if local else "C" }}
```

Shows: `🟢 L` (closed, local) or `🔴 C` (open, cloud)

### Verbose Format

```yaml
state: >-
  {% set state = states('binary_sensor.device') %}
  {% set local = states('binary_sensor.device_local') not in ['unavailable', 'unknown'] %}
  {% set state_text = "Closed" if state == 'off' else "Open" %}
  {% set source = "local (tuya_local)" if local else "cloud (tuya)" %}
  {{ state_text }} via {{ source }}
```

Shows: `Closed via local (tuya_local)` or `Open via cloud (tuya)`

## Monitoring Integration Health

Create a helper card showing all fallback statuses:

```yaml
type: custom:template-entity-row
name: Integration Health
state_template: >-
  {% if states('binary_sensor.washer_door_local') not in ['unavailable', 'unknown'] %}
    ✅ All local
  {% elif states('binary_sensor.dryer_door_local') not in ['unavailable', 'unknown'] %}
    ⚠️ Dryer on fallback
  {% else %}
    ⚠️ Multiple fallbacks
  {% endif %}
```

## Next Steps

1. Update your laundry dashboard to use `sensor.washer_door_status` and `sensor.dryer_door_status`
2. Add status display templates for other fallback devices
3. Consider adding an "Integration Health" summary card
4. Create alerts when multiple fallbacks are active (see FALLBACK_INTEGRATION_PATTERN.md)

