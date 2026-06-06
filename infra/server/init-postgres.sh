#!/bin/bash
# Wird beim ersten Postgres-Start ausgeführt — legt einen n8n-User mit
# eingeschränkten Rechten an (statt n8n als Postgres-Superuser laufen zu
# lassen). Best Practice gegen Privilege-Escalation.

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${POSTGRES_NON_ROOT_USER} WITH PASSWORD '${POSTGRES_NON_ROOT_PASSWORD}';
    GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_NON_ROOT_USER};
    GRANT CREATE ON SCHEMA public TO ${POSTGRES_NON_ROOT_USER};
EOSQL
