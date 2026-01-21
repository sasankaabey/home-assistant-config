# Policy: Dev Workspace Hygiene

## Goal

Keep development work organized and repeatable by ensuring:
- all project work lives under ~/Developer/
- the Home Assistant repo stays clean and purposeful
- experiments have a safe place that does not pollute $HOME

## Rules

### 1) No code in $HOME
Do not create Python scripts, repos, or ad-hoc tooling directly under:
- ~/
- Desktop, Documents, Downloads

### 2) Experiments go to scratch
If you are "just testing something", put it here:
- ~/Developer/_scratch/

### 3) HA utilities live in this repo under tools/
- New utilities start in: tools/one_off/
- Promote to: tools/scripts/ only after review

### 4) Secrets never enter git
Never commit:
- .env
- HA tokens
- shell history
- system dotfiles (.DS_Store, etc.)

If a tool needs environment variables:
- create .env.example
- document required vars in the script header

## Quick Sanity Check

Before running a command:
- Does pwd start with ~/Developer/? If not, stop and cd.
- Is this HA-related? Use home-assistant-config/tools/.
- Is this experimental? Use ~/Developer/_scratch/.

## Cleanup Rule

If you accidentally create scripts in $HOME:
1. Move HA-related scripts into tools/one_off/
2. Move non-HA experiments into ~/Developer/_scratch/
3. Delete or ignore system dotfiles
