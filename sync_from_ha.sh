#!/usr/bin/env bash
set -euo pipefail

LOCAL_DIR="$(cd "$(dirname "$0")" && pwd)"
REMOTE_HOST="${REMOTE_HOST:-homeassistant.local}"
REMOTE_USER="${REMOTE_USER:-root}"
SRC_DIR="${SRC_DIR:-/config}"

RSYNC_OPTS=(
  -a
  --delete
  --stats
  --filter=':- .gitignore'
  --exclude '.git/'
  --exclude '.gitignore'
  --exclude '.storage/'
  --exclude '.cloud/'
  --exclude '.ha_run.lock'
  --exclude '.HA_VERSION'
  --exclude '*.db'
  --exclude '*.db-shm'
  --exclude '*.db-wal'
  --exclude '*.log'
  --exclude '*.log.*'
  --exclude '*.zip'
  --exclude 'deps/'
  --exclude 'appdaemon/'
  --exclude 'image/'
  --exclude 'tts/'
  --exclude '.vscode/'
  --exclude 'www/alexa_tts/'
  --exclude 'home-assistant.log.fault'
  --exclude 'split_log.txt'
  --exclude 'watch_log.txt'
  --exclude 'watchman_report.txt'
  --exclude 'sync_to_ha.sh'
  --exclude 'sync_from_ha.sh'
)

if [[ "${DRY_RUN:-}" == "1" ]]; then
  RSYNC_OPTS+=(--dry-run)
fi

rsync -e ssh "${RSYNC_OPTS[@]}" "${REMOTE_USER}@${REMOTE_HOST}:${SRC_DIR}/" "$LOCAL_DIR/"
