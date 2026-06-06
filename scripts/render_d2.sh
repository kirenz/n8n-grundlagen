#!/usr/bin/env bash
# Rendert alle d2/*.d2 zu d2/*.svg im klaren (non-sketch) Editorial-Look.
# Aufruf vom Repo-Root: scripts/render_d2.sh
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v d2 >/dev/null 2>&1; then
  echo "Fehler: d2 nicht gefunden. Installation: brew install d2" >&2
  exit 1
fi

shopt -s nullglob
files=(d2/*.d2)
if (( ${#files[@]} == 0 )); then
  echo "Keine .d2-Dateien unter d2/ gefunden."
  exit 0
fi

for src in "${files[@]}"; do
  out="${src%.d2}.svg"
  echo "render $src -> $out"
  d2 --pad 24 "$src" "$out"
done
