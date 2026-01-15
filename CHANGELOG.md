# Changelog

All notable changes to this Home Assistant configuration.

Format: Keep entries brief. Link to DECISIONS.md for rationale.

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
