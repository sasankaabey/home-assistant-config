# Changelog

All notable changes to this Home Assistant configuration.

Format: Keep entries brief. Link to DECISIONS.md for rationale.

---

## 2026-01-21

### Added

- **Fallback Integration Pattern** - Template sensors that prefer local (tuya_local) but fallback to cloud (tuya)
  - `binary_sensor.washer_door` - Prefers local, fallback: `contact_sensor_door` (cloud)
  - `binary_sensor.dryer_door` - Prefers local, fallback: `contact_sensor_2_door` (cloud)
  - **Benefits**: Resilience when local unavailable, prefers local for lower latency, transparent to automations
  - **Documentation**: `FALLBACK_INTEGRATION_PATTERN.md` - Reusable pattern for other devices

### Improved

- **Washer Load Assignment Trigger** - Changed from 2-minute power delay to door close + sustained power detection
  - Now uses `binary_sensor.washer_door` close event as primary trigger
  - Verifies sustained power draw above idle threshold to confirm load started
  - 3-second stabilization delay prevents false positives from power spikes
  - **Result**: Load assignment notification in 3-5 seconds vs 2 minutes
  - **Fallback**: Created `automation_laundry_washer_started_fallback.yaml` for systems without door sensor (uses 30-sec power threshold)
  - **Setup Guide**: See `WASHER_DOOR_SENSOR_SETUP.md` for entity configuration

- **Laundry Nagging Logic** - Enhanced to pause when washer restarts
  - Added `washer_is_running` check to prevent confusing nags
  - Pauses nagging if power spikes again (clothes went back in or new load started)
  - Notifies owner if nagging paused due to washer restarting

### Fixed

- **Washer Power Sensor** - Updated all automations to use correct entity: `sensor.lg_washer_current_consumption`
  - Was: `sensor.washer_running_current_consumption` (non-existent)
  - Fixed in: washer_started, washer_finished, handle_next_load, nag, dryer_nag automations

### Documents Added

- `TASKS.md` - Notification enhancement backlog (styled buttons, text input, deep links, Telegram)
- `REUSABLE_SCRIPTS_PLAN.md` - Strategic plan for extracting reusable automation patterns
- `WASHER_DOOR_SENSOR_SETUP.md` - Complete guide for door sensor setup and troubleshooting
- `FALLBACK_INTEGRATION_PATTERN.md` - Reusable pattern for local→cloud fallback sensors

---

## 2026-01-14

### Added

- `TASKS.md` - Multi-agent task queue for coordinating work across Claude Code, Codex, ChatGPT, Perplexity, Gemini
- `DECISIONS.md` - Architecture decision records
- `CHANGELOG.md` - This file
- VS Code schema override comments in `light_groups.yaml` and `scripts.yaml`

### Fixed

- Markdown linting (65 warnings) in `HOME_ASSISTANT.md`
- `notify.adults` service names (changed from UUIDs to slugified device names)
- Litterbot automation YAML format (converted to list format for `!include_dir_merge_list`)
- Living room light sync automation (fixed color_temp/rgb_color mutual exclusion)
- Assist pipeline `conversation.chatgpt` error (changed to `conversation.home_assistant`)

### Patched (on server, not in repo)

- `tuya_local/light.py` - try/except for unknown color names
- `openplantbook/uploader.py` - initialize `latest_data` variable
- `.storage/core.config_entries` - smoke_sensor → smoke_detector device type

---

## 2026-01-13

### Added

- `light_groups.yaml` - YAML-based light groups (living room)
- `automations/lighting/sync_living_room_light_groups.yaml` - Keep grouped lights in sync
- Entity audit reports (`entity_audit_report.md`, etc.)

### Fixed

- Removed 15 duplicate/orphaned entities
- Disabled 2 duplicate automations

### Backup

- `a4b62dfd` - "Before entity cleanup Jan 2026"

---

## Template for Future Entries

```markdown
## YYYY-MM-DD

### Added
- New feature or file

### Changed
- Modifications to existing functionality

### Fixed
- Bug fixes

### Removed
- Deleted files or features

### Patched (server only)
- Changes made directly on HA server, not in repo

### Backup
- Backup ID if created before major changes
```

---
