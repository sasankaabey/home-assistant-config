# Pull Request Template

## Description
Brief description of what this PR does and why.

**Related Task:** Link to [TASKS.md](../TASKS.md) task (e.g., "See TASKS.md: Motion-Triggered Lights")

---

## Changes

- [ ] YAML automation/script/scene (specify location)
- [ ] Python script/helper
- [ ] Entity registry changes
- [ ] Custom component patch
- [ ] Documentation update
- [ ] Light group configuration
- [ ] Other: ___________

---

## Testing

**Tested on:** 192.168.4.141 (minipc) HA OS

- [ ] YAML validated: `python3 -c "import yaml; yaml.safe_load(open('file.yaml'))"`
- [ ] Synced via `./sync_to_ha.sh`
- [ ] HA restarted successfully
- [ ] Entities appear in HA UI
- [ ] Voice commands work (Alexa/Siri/Google)
- [ ] Automations trigger correctly
- [ ] Logs show no errors

**Test Evidence:**
```
Paste relevant log snippets or screenshots here
```

---

## Deployment Notes

**Agent:** [Who deployed this? Claude Code, Codex, etc.]

**Sync Method:**
```bash
./sync_to_ha.sh  # For YAML changes
# Or other method for different changes
```

**Restart Type:**
```bash
ha core restart  # Standard restart
# OR
ha core stop && ha core start  # If editing .storage/core.entity_registry
```

**Rollback Plan:** If this breaks something, revert with:
```bash
git revert [commit-hash]
./sync_to_ha.sh
ha core restart
```

---

## Files Changed

| File | Type | Notes |
|------|------|-------|
| `automations/lighting/example.yaml` | New | Motion-triggered lights |
| `light_groups.yaml` | Updated | Added motion_lights group |
| `CHANGELOG.md` | Updated | Documented feature |

---

## Entity References

If this adds/renames/removes entities, list them:

```
NEW:
- automation.motion_triggered_lights
- light.motion_lights (group)

MODIFIED:
- light_groups.yaml (added motion_lights group)

REMOVED:
- (none)
```

See `entity_rename_map.json` if tracking renames.

---

## Checklist

- [ ] Code follows Home Assistant conventions ([see HOME_ASSISTANT.md](../HOME_ASSISTANT.md))
- [ ] YAML is valid and tested
- [ ] Commit message is clear ([see MULTI_AGENT_WORKFLOW.md](../MULTI_AGENT_WORKFLOW.md#git-commit-message-format))
- [ ] CHANGELOG.md updated with feature/fix
- [ ] TASKS.md updated with completion status
- [ ] No breaking changes without documented migration path
- [ ] No sensitive data (passwords, IPs, tokens) in code
- [ ] Tested and verified on server before opening PR

---

## Questions/Notes for Reviewer

Anything you'd like the next agent to know before deploying?

---

**See Also:**
- [AGENTS.md](../AGENTS.md) — Agent roles and responsibilities
- [MULTI_AGENT_WORKFLOW.md](../MULTI_AGENT_WORKFLOW.md) — Workflow process
- [copilot-instructions.md](../.github/copilot-instructions.md) — Deployment procedures
