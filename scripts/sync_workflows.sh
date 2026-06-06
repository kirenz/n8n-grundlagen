#!/usr/bin/env bash
# Sync the live state of all Pattern workflows from n8n.kirenz.de
# back into workflows/pattern-*.json as the local source of truth.
#
# Usage:
#   export N8N_API_KEY="your-n8n-api-key"
#   scripts/sync_workflows.sh
#
# Why: the user manually optimizes sticky-note positions in the n8n UI.
# Without this sync, any AI-driven workflow update would reset those
# positions to the SDK-code defaults. Run this BEFORE asking the AI
# to change workflow content, so the AI can read positions from the
# local JSON and preserve them.

set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -z "${N8N_API_KEY:-}" ]]; then
  echo "ERROR: N8N_API_KEY environment variable not set." >&2
  echo "Set it with: export N8N_API_KEY=\"your-key\"" >&2
  exit 1
fi

N8N_HOST="${N8N_HOST:-https://n8n.kirenz.de}"

# Map of local filename → n8n workflow ID
# Update if you create new pattern workflows.
declare -a WORKFLOWS=(
  "pattern-01-prompt-chaining:M3mPVbB1hsXrXl0L"
  "pattern-02-routing:PzCErqut4xu2mKtm"
  "pattern-03-parallelization:0KCyFe60OFazSe2w"
  "pattern-04-orchestrator-worker:LY3QmuZ4XP6MheiT"
  "pattern-05-evaluator-optimizer:M8GIqEGzwt705Nnk"
  "pattern-06-tools-agent:36GnHsDJNWUOENFC"
  "pattern-07-hierarchical:xA78nufzSaYUQgEr"
  "pattern-08-collaborative:IKyKajoeF7LockqK"
  "pattern-09-sequential-multiagent:VLYODd9a65kB04YZ"
  "pattern-10-parallel-multiagent:nP54ioGjCH97SzF6"
  "pattern-11-network-swarm:Isursz6xp2nrWbMi"
)

mkdir -p workflows

TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

for entry in "${WORKFLOWS[@]}"; do
  name="${entry%%:*}"
  wf_id="${entry##*:}"
  out_file="workflows/${name}.json"

  echo "  → ${name} (${wf_id})"

  # Fetch the workflow, then strip the n8n-internal noise (versionId, scopes,
  # meta, isArchived, active, triggerCount, createdAt, updatedAt, id) and
  # attach a _meta block with the sync timestamp and the n8n URL.
  curl -sS \
    -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
    "${N8N_HOST}/api/v1/workflows/${wf_id}" \
  | jq --arg ts "${TIMESTAMP}" \
       --arg url "${N8N_HOST}/workflow/${wf_id}" \
       --arg wf_id "${wf_id}" '
      {
        name: .name,
        description: (.description // ""),
        settings: .settings,
        nodes: .nodes,
        connections: .connections,
        _meta: {
          n8nWorkflowId: $wf_id,
          n8nUrl: $url,
          lastSyncedFromN8n: $ts,
          note: "Source of truth. Mirrors the live n8n workflow including user-optimized sticky-note positions. Read this file before regenerating workflow SDK code."
        }
      }
    ' > "${out_file}"

  echo "    saved → ${out_file}"
done

echo ""
echo "✓ Synced ${#WORKFLOWS[@]} workflows."
