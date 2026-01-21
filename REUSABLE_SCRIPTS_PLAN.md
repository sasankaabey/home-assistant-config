# Reusable Scripts & Functions Plan

## Overview
Current laundry automation has several patterns that would be valuable for other household automations (litterbox, chores, maintenance, etc.). This document outlines what to extract into reusable scripts.

---

## 1. **Nag Function** (HIGH PRIORITY)
### Current Implementation
- `automation_laundry_nag.yaml` - Repeating escalating reminders
- Pattern: Every 5 min → Every 1 min after 20 min

### Proposed: `script.nag_with_escalation`
```yaml
nag_with_escalation:
  description: Send escalating nag reminders for delayed tasks
  fields:
    enabled_entity:          # input_boolean to check/loop
    trigger_message:         # What to say in nags
    owner:                   # Person doing the task
    initial_interval:        # Minutes between nags (default 5)
    escalation_threshold:    # Minutes before escalating (default 20)
    escalated_interval:      # Minutes after escalation (default 1)
    use_alexa:              # Send Alexa announcements? (default true)
    use_mobile:             # Send mobile notifications? (default true)
    actions:                # Optional notification buttons
```

### Why Extract
- **Litterbox automation** needs nagging (scoop frequency)
- **Chore automations** need escalating reminders
- **Maintenance tasks** need repeated alerts if incomplete

### Usage Examples
```yaml
- service: script.nag_with_escalation
  data:
    enabled_entity: input_boolean.litterbox_nag_enabled
    trigger_message: "Litter box needs scooping"
    owner: "Mixed"  # Everyone
    initial_interval: 3
    escalation_threshold: 15
    escalated_interval: 1
    use_alexa: true
    use_mobile: true

- service: script.nag_with_escalation
  data:
    enabled_entity: input_boolean.trash_nag_enabled
    trigger_message: "Time to take out the trash"
    owner: "Max"
    initial_interval: 10
    escalation_threshold: 60
    escalated_interval: 5
```

---

## 2. **Notification Router** (MEDIUM PRIORITY - Partially Done)
### Current Implementation
- `script.laundry_notification_router` - Routes to adults/kids based on presence
- Only handles laundry-specific logic

### Proposed Enhancements: `script.notify_by_role`
```yaml
notify_by_role:
  description: Send notifications based on household role and presence
  fields:
    message:                 # Notification message
    title:                   # Notification title
    targets:                 # "adults" | "kids" | "all" | ["Zoe", "Max"]
    use_mobile:             # Send mobile app? (default true)
    use_alexa:              # Send Alexa announcement? (default false)
    actions:                # Notification action buttons
    tag:                    # Notification tag for grouping
    priority:               # "low" | "normal" | "high"
```

### Current Coverage
✅ `script.laundry_notification_router` - Works for laundry owner + presence routing

### New Features Needed
- Generic "adults only", "kids only", "all" routing
- Support for specific person lists: `["Zoe", "Ankit"]`
- Priority levels (affects retry behavior)
- Fallback routing if target not available

### Usage Examples
```yaml
# Alert all adults
- service: script.notify_by_role
  data:
    message: "Guest arriving in 5 minutes"
    title: "Doorbell Alert"
    targets: "adults"
    use_mobile: true

# Kids at home only
- service: script.notify_by_role
  data:
    message: "Time for dinner"
    title: "Family Alert"
    targets: "kids"
    use_alexa: true

# Specific people
- service: script.notify_by_role
  data:
    message: "Your package arrived"
    title: "Delivery"
    targets: ["Ankit", "Danielle"]
    use_mobile: true
```

---

## 3. **Mobile Notification Function** (LOW PRIORITY - Simple)
### Current Implementation
- Hardcoded `notify.adults` group in laundry
- Individual notify services used in kids logic

### Proposed: `script.send_mobile_notification`
```yaml
send_mobile_notification:
  description: Send push notification to specific devices
  fields:
    message:       # Text to send
    title:         # Notification title
    target:        # "adults" | "person_name" | notify service ID
    actions:       # Notification buttons/actions
    tag:           # Group related notifications
    url:           # Deep link URL (optional)
    image:         # Image URL (optional)
    sound:         # Audio cue type
```

### Why Extract
- Consistent formatting/tagging
- Easy to add new notification properties later
- Reusable for all automations

---

## 4. **Alexa Announcement Router** (ALREADY EXISTS ✅)
### Current: `script.alexa_announce_router`
- ✅ Already handles quiet hours
- ✅ Audience routing (all, adults, auto)
- ✅ Device grouping

**No changes needed** - it's already generic enough!

---

## 5. **Timeout Handler** (MEDIUM PRIORITY)
### Current Implementation
- `automation_laundry_next_load_timeout.yaml` - Checks for expired datetime helper
- Pattern: "Did user respond? No → default action"

### Proposed: `script.handle_delayed_response`
```yaml
handle_delayed_response:
  description: Execute fallback action if user hasn't responded by deadline
  fields:
    response_entity:        # input_boolean tracking response
    deadline_entity:        # input_datetime of deadline
    timeout_action:         # Automations or scripts to run
    timeout_message:        # Message to announce/notify
    escalate_to:           # Who to notify if timeout (default: adults)
```

### Usage Examples
```yaml
# If washer owner doesn't respond in 5 min
- service: script.handle_delayed_response
  data:
    response_entity: input_boolean.awaiting_next_load_response
    deadline_entity: input_datetime.next_load_response_deadline
    timeout_action:
      - service: input_select.set_options
        target:
          entity_id: input_select.washer_owner
        data:
          option: "Unknown"
    timeout_message: "Washer available to everyone"
    escalate_to: "all"
```

---

## 6. **Ownership Transfer** (LOW PRIORITY - Task-Specific)
### Current Implementation
- `automation_laundry_confirm_load_transfer.yaml` - Move laundry from washer to dryer

This is too specific to laundry. Skip for now.

---

## 7. **Presence Check with Fallback** (MEDIUM PRIORITY)
### Current Pattern
```yaml
owner_is_home: >
  {% if owner == 'Zoe' %}
    {{ is_state('person.zoe', 'home') }}
  {% elif owner == 'Max' %}
    {{ is_state('person.max', 'home') }}
  ...
```

### Proposed: `script.is_person_home`
```yaml
is_person_home:
  description: Check if a specific person entity is home
  fields:
    person_name:    # "Zoe" | "Max" | "Aiden" | "Ankit" | "Danielle"
  response:
    state: true/false
```

Usage:
```yaml
- service: script.is_person_home
  data:
    person_name: "{{ owner }}"
  response:
    response_variable: person_home

- if: "{{ person_home.state == true }}"
  then: [...]
```

---

## Priority Roadmap

### Phase 1 (Now)
1. ✅ `script.laundry_notification_router` - Already exists, slightly enhanced
2. ✅ `script.alexa_announce_router` - Already exists, generic

### Phase 2 (Next automations)
3. `script.nag_with_escalation` - High reuse potential
4. `script.notify_by_role` - Generalize laundry notification router

### Phase 3 (Future)
5. `script.send_mobile_notification` - Wrapper for consistency
6. `script.handle_delayed_response` - Timeout pattern
7. `script.is_person_home` - Presence helper

---

## Implementation Notes

### For `script.nag_with_escalation`:
- Use `while` loop like current laundry nag
- Check `enabled_entity` to stop nagging
- Calculate `minutes_elapsed` from a `last_started` timestamp
- Support both Alexa + mobile notifications

### For `script.notify_by_role`:
- Use chooser logic like laundry router
- Map role names to entity lists
- Call `script.send_mobile_notification` + `script.alexa_announce_router`
- Support "adults" group, "kids" group, person-specific

### Shared Variables
Create a reference file for common person mappings:
```yaml
# inputs/household_members.yaml
adults:
  - "Ankit"
  - "Danielle"
kids:
  - "Zoe"
  - "Max"
  - "Aiden"
all:
  - "Ankit"
  - "Danielle"
  - "Zoe"
  - "Max"
  - "Aiden"
```

---

## Testing Plan

Each script should have:
1. **Unit test**: Call script manually with test data
2. **Integration test**: Use in an automation
3. **Failure test**: What happens if entity doesn't exist?

---

## Deprecation Plan

When new scripts are ready:
1. Keep old scripts for 2-3 weeks (safety fallback)
2. Update laundry automation to use new scripts
3. Document migration path in CHANGELOG
4. Delete old scripts + update README

Example migration:
```yaml
# Before
- service: script.laundry_notification_router
  data: {...}

# After
- service: script.notify_by_role
  data:
    targets: "adults"  # Instead of mode/owner logic
    ...
```
