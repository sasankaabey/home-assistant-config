#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
REMOTE_HOST="${REMOTE_HOST:-homeassistant.local}"
REMOTE_USER="${REMOTE_USER:-root}"
DEST_DIR="${DEST_DIR:-/config}"

RSYNC_OPTS=(
  -a
  --delete
  --stats
  --filter=':- .gitignore'
  --exclude '.git/'
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
)

if [[ "${DRY_RUN:-}" == "1" ]]; then
  RSYNC_OPTS+=(--dry-run)
fi

rsync -e ssh "${RSYNC_OPTS[@]}" "$SRC_DIR/" "${REMOTE_USER}@${REMOTE_HOST}:${DEST_DIR}/"
