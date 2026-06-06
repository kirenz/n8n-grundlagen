#!/usr/bin/env bash
# Tägliches Backup für n8n.kirenz.de.
# Pattern aus /Users/jankirenz/code/hdm/lernplattform/infra/backup/pg_dump.sh
# übernommen: daily + weekly mit Hardlink-Promotion (Sonntag).
#
# Install als Host-Cron (NICHT im Container):
#   0 3 * * *  /opt/n8n/backup.sh >> /var/log/n8n-backup.log 2>&1
#
# Retention: 14 daily + 8 weekly. Storage-Box-Sync läuft, falls die
# STORAGE_BOX_*-Vars in .env gesetzt sind.

set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-/opt/n8n}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/n8n}"
DAILY_DIR="${BACKUP_DIR}/daily"
WEEKLY_DIR="${BACKUP_DIR}/weekly"
RETENTION_DAILY="${RETENTION_DAILY:-14}"
RETENTION_WEEKLY="${RETENTION_WEEKLY:-8}"

mkdir -p "${DAILY_DIR}" "${WEEKLY_DIR}"
cd "${PROJECT_DIR}"

# .env laden für Postgres-Credentials und (optional) Storage-Box-Konfig
set -a
# shellcheck disable=SC1091
. ./.env
set +a

STAMP="$(date -u +%Y-%m-%d_%H%M%S)"
DAILY_PG="${DAILY_DIR}/postgres_${STAMP}.sql.gz"
DAILY_VOL="${DAILY_DIR}/n8n-volume_${STAMP}.tar.gz"

# === 1. Postgres-Dump ===
docker compose exec -T postgres \
    pg_dump --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" \
            --format=plain --clean --if-exists \
    | gzip --best > "${DAILY_PG}"
echo "wrote ${DAILY_PG} ($(du -h "${DAILY_PG}" | cut -f1))"

# === 2. n8n-Volume-Dump (binär-sicher: workflows.json, encryption-key, custom-nodes) ===
docker run --rm \
    -v n8n-prod_n8n-data:/data:ro \
    -v "${BACKUP_DIR}:/backup" \
    alpine \
    tar czf "/backup/daily/n8n-volume_${STAMP}.tar.gz" -C /data .
echo "wrote ${DAILY_VOL} ($(du -h "${DAILY_VOL}" | cut -f1))"

# === 3. Sonntag → Weekly-Promotion (Hardlinks, fällt auf Copy zurück bei FS-Grenze) ===
if [ "$(date -u +%u)" = "7" ]; then
    for f in "${DAILY_PG}" "${DAILY_VOL}"; do
        weekly_file="${WEEKLY_DIR}/$(basename "${f}")"
        cp -al "${f}" "${weekly_file}" 2>/dev/null || cp "${f}" "${weekly_file}"
        echo "promoted to ${weekly_file}"
    done
fi

# === 4. Lokale Retention ===
find "${DAILY_DIR}" -type f \( -name 'postgres_*.sql.gz' -o -name 'n8n-volume_*.tar.gz' \) \
    -mtime +"${RETENTION_DAILY}" -print -delete || true
find "${WEEKLY_DIR}" -type f \( -name 'postgres_*.sql.gz' -o -name 'n8n-volume_*.tar.gz' \) \
    -mtime +"$((RETENTION_WEEKLY * 7))" -print -delete || true

# === 5. Off-Site-Replikation zur Hetzner Storage Box ===
if [ -n "${STORAGE_BOX_HOST:-}" ] && [ -n "${STORAGE_BOX_USER:-}" ] && [ -n "${STORAGE_BOX_KEY:-}" ]; then
    STORAGE_BOX_PORT="${STORAGE_BOX_PORT:-23}"
    STORAGE_BOX_REMOTE_DIR="${STORAGE_BOX_REMOTE_DIR:-n8n}"

    rsync -a --delete \
        -e "ssh -p ${STORAGE_BOX_PORT} -i ${STORAGE_BOX_KEY} -o StrictHostKeyChecking=accept-new" \
        "${BACKUP_DIR}/" \
        "${STORAGE_BOX_USER}@${STORAGE_BOX_HOST}:${STORAGE_BOX_REMOTE_DIR}/"
    echo "rsync to ${STORAGE_BOX_HOST}:${STORAGE_BOX_REMOTE_DIR}/ ok"
else
    echo "STORAGE_BOX_HOST/USER/KEY unset — skipping off-site replication"
fi
