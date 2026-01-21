# Copilot Instructions — Home Assistant Config

> **Note:** This file contains project-specific instructions only. For workflow and agent routing, see the [organization-level instructions](https://github.com/sasankaabey/.github).

---

## Quick Links
- **Org-level workflow**: See `sasankaabey/.github/MULTI_AGENT_WORKFLOW.md`
- **Agent routing**: See `sasankaabey/.github/AGENTS.md`
- **Project context**: See `LOCAL_CONTEXT.md` in this repo
- **Current tasks**: See `TASKS.md` in this repo

---

## Project-Specific Context

**Tech stack:**
- Python 3.11+
- Home Assistant Core
- YAML configuration files
- Custom components (Tuya Local, Music Assistant, etc.)

**Deployment:**
- Raspberry Pi 4 at 192.168.4.141
- Home Assistant OS
- SSH access for advanced operations

**Key constraints:**
- No breaking changes to existing automations
- Test changes on staging/dev environment first when possible
- Validate YAML syntax before deployment
- Keep entity IDs consistent and well-documented

**Architecture:**
- `automations/` — Automation YAML files
- `scripts/` — Helper scripts
- `custom_components/` — Custom integrations
- `light_groups.yaml`, `scenes.yaml` — Entity groupings
- `.storage/` — Entity registry and core storage (edit with caution)

---

## Project-Specific Instructions

### Entity Management
- Use snake_case for entity IDs (e.g., `light.living_room_ceiling`)
- Always check entity registry before creating new entities
- Use friendly names in automations for readability
- Document entity purposes in comments

### Automation Best Practices
- Add descriptive comments to complex automations
- Test light groups before referencing in automations
- Use conditions to prevent race conditions
- Keep automations in separate files by room or function

### Deployment
- Validate YAML with Home Assistant's `ha core check` before deploy
- Use `ha core restart` after config changes
- Monitor logs after deployment for errors
- Keep backups before major changes

### Custom Components
- Document custom component versions in README
- Test updates in isolation before deploying
- Keep custom component configs separate from core configs

---

## Learning Escalation

When you discover a **pattern, pitfall, or improvement** that would help other projects:

1. **Document it locally** in `TASKS.md` or commit message
2. **Escalate to org-level** by updating `sasankaabey/.github/EVOLUTION_LOG.md`:
   - What you learned (e.g., "Better YAML validation before deploy")
   - Why it matters (e.g., "Prevents breaking automations in production")
   - How other projects can apply it (e.g., "Add pre-commit hook for validation")

Example escalations:
- "Found a better way to validate YAML before deploy → add to org workflow"
- "Discovered common entity naming conflicts → document in org best practices"
- "New handoff pattern for SSH operations works well → update HANDOFF_TEMPLATE.md"

---

## See Also
- [Organization README](https://github.com/sasankaabey/.github/blob/main/README.md)
- [Multi-Agent Architecture](https://github.com/sasankaabey/.github/blob/main/MULTI_AGENT_ARCHITECTURE.md)
- [Home Assistant Documentation](https://www.home-assistant.io/docs/)
