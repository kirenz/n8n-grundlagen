#!/bin/bash
# Migriert alle workflows/*.json vom lokalen Repo auf die Server-n8n-Instanz.
#
# Voraussetzungen:
# - API-Key vom Server-n8n (UI: Avatar → Settings → n8n API → Create)
# - Server-Domain auf https-Endpoint erreichbar
#
# Aufruf:
#   N8N_SERVER_URL="https://n8n.kirenz.de" \
#   N8N_SERVER_API_KEY="dein-api-key" \
#   ./infra/server/migrate-workflows.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
WORKFLOW_DIR="$REPO_DIR/workflows"

: "${N8N_SERVER_URL:?Setze N8N_SERVER_URL=https://n8n.kirenz.de}"
: "${N8N_SERVER_API_KEY:?Setze N8N_SERVER_API_KEY=...}"

# Trailing-Slash entfernen
N8N_SERVER_URL="${N8N_SERVER_URL%/}"

echo "Server: $N8N_SERVER_URL"
echo ""

# Existierende Workflows holen, um Duplikate zu erkennen
EXISTING=$(curl -s -H "X-N8N-API-KEY: $N8N_SERVER_API_KEY" \
    "$N8N_SERVER_URL/api/v1/workflows" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print('\n'.join(w['name'] for w in d.get('data',[])))" 2>/dev/null || echo "")

for f in "$WORKFLOW_DIR"/modul-*.json; do
    name=$(python3 -c "import json,sys; print(json.load(open('$f'))['name'])")

    if echo "$EXISTING" | grep -Fxq "$name"; then
        echo "SKIP: '$name' existiert bereits — überspringe"
        continue
    fi

    code=$(curl -s -o /tmp/n8n-mig.out -w "%{http_code}" \
        -X POST \
        -H "X-N8N-API-KEY: $N8N_SERVER_API_KEY" \
        -H "Content-Type: application/json" \
        --data @"$f" \
        "$N8N_SERVER_URL/api/v1/workflows")

    if [ "$code" = "200" ] || [ "$code" = "201" ]; then
        wid=$(python3 -c "import json; print(json.load(open('/tmp/n8n-mig.out')).get('id','?'))" 2>/dev/null || echo "?")
        echo "OK ($code): $name → id=$wid"
    else
        echo "FAIL ($code): $name"
        cat /tmp/n8n-mig.out
        echo ""
    fi
done

rm -f /tmp/n8n-mig.out
echo ""
echo "Fertig."
