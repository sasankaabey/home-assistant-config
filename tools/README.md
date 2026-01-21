# Home Assistant Tools

This folder contains **local developer utilities** used to inspect, migrate, and refactor the Home Assistant configuration.

## Purpose

- Keep one-off experiments out of \$HOME and out of random folders
- Centralize HA-related scripts alongside the config they operate on
- Make scripts easy to discover, re-run, and evolve over time

## Structure

tools/
  scripts/     # "Graduated" tools — reusable, documented, safe-ish
  one_off/     # One-time utilities or prototypes (may be promoted later)

## scripts/ (Graduated tools)

A script belongs in scripts/ when it:
- has been used more than once (or clearly will be),
- has clear inputs/outputs,
- has basic safety (dry-run, confirmation, or non-destructive default),
- and is documented below.

## one_off/ (Prototypes / one-time)

Scripts belong in one_off/ when they:
- were created during exploration,
- are narrow or time-bound,
- may be messy or hard-coded,
- or are “maybe useful later.”

Rule: new scripts land in one_off/ first. Promote only after review.

## Script Index

Update this list when promoting a script.

### Entity + Registry Utilities
- ha_registry_cleanup.py — cleans up registry artifacts (review required before use)
- update_entity_references.py — rewrites entity IDs across YAML (dry-run recommended)
- ha_bulk_entity_rename.py — bulk rename helper (validate carefully)

### Inventory / Discovery
- ha_inventory_dump.py — dumps entity inventory for audits

### Tuya
- tuya_cloud_pull.py — pulls Tuya info from cloud (credentials required)
- tuya_iot_pull.py — IoT platform pull (credentials required)
- tuya_local_probe.py — local probing utility (network-dependent)

### API
- ha_api.py — Home Assistant API helper (token required)

## Conventions (Minimum Bar)

- Prefer non-destructive defaults (dry-run mode) for anything that changes files
- Never commit tokens or credentials
- Keep scripts runnable from repo root:

  python3 tools/scripts/<script>.py --help

## Promotion Checklist (one_off -> scripts)

Before moving a script into scripts/:

- Has --help or usage header
- Supports --dry-run for destructive changes (or is read-only)
- No secrets in code
- Adds or updates entry in Script Index
- Minimal smoke test notes added
