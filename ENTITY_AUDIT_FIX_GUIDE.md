# Entity Audit - Immediate Fix Guide

Date: 2026-01-13
Status: 4 HIGH PRIORITY issues found

================================================================================

## ISSUE 1 AND 2: Missing Group Entities

Problem: Two groups are not loading as entities
- group.household
- group.kids

Where Used:
- /config/scripts.yaml (TTS announcement targeting)
- /config/template.yaml (kids_home sensor)

Current State:
- Groups ARE defined in /config/groups.yaml
- groups.yaml IS included in configuration.yaml (line 18)
- YAML syntax is VALID
- BUT groups are not in entity registry

Root Cause: Groups may not have been loaded since groups.yaml was created/modified

FIX: Restart Home Assistant
1. SSH: ssh root@192.168.4.141
2. Run: ha core restart
3. Wait 2-3 minutes
4. Check Developer Tools -> States for group.household and group.kids

================================================================================

## ISSUE 3 AND 4: Missing Mobile App Notify Services

Problem: Automations reference old notify service names
- notify.mobile_app_ankit_s_iphone
- notify.mobile_app_pixel_7a

Where Used:
- /config/automations.yaml
- All litterbot automation files (5 files)

Current State:
Mobile app devices ARE registered but notify services use device UUID not friendly names

Correct Service Names:

For Ankits iPhone:
- OLD: notify.mobile_app_ankit_s_iphone
- NEW: notify.mobile_app_7b4b3d84_ce9d_418e_ad95_576581ee855e

For Pixel 7a:
- OLD: notify.mobile_app_pixel_7a
- NEW: notify.mobile_app_6edede162518e0a8

FIX: Update all automation files with correct service names

Quick fix command:
cd /config
cp automations.yaml automations.yaml.backup
sed -i 's/notify.mobile_app_ankit_s_iphone/notify.mobile_app_7b4b3d84_ce9d_418e_ad95_576581ee855e/g' automations.yaml
sed -i 's/notify.mobile_app_pixel_7a/notify.mobile_app_6edede162518e0a8/g' automations.yaml

Update litterbot files:
for file in automations/automation_litterbot*.yaml; do
  sed -i 's/notify.mobile_app_ankit_s_iphone/notify.mobile_app_7b4b3d84_ce9d_418e_ad95_576581ee855e/g' "$file"
  sed -i 's/notify.mobile_app_pixel_7a/notify.mobile_app_6edede162518e0a8/g' "$file"
done

================================================================================

QUICK FIX CHECKLIST

1. Restart Home Assistant to load groups
2. Verify group.household and group.kids exist
3. Update notify service names in automations
4. Test notifications
5. Check HA logs for errors

================================================================================
