#!/usr/bin/env bash
# Подготовка data/vercel/ для боевого деплоя (ветка master).
# Если артефакты уже в репо — не перезаписываем graph.pkl и vectors.npy.
set -euo pipefail

DEST="${DATA_PROCESSED:-data/vercel}"
mkdir -p "$DEST"

if [[ ! -f "$DEST/documents.jsonl" ]]; then
  cp data/sample/documents.jsonl "$DEST/documents.jsonl"
  echo "Copied sample documents -> $DEST/documents.jsonl"
fi

if [[ ! -f "$DEST/graph.pkl" ]]; then
  python3 - <<'PY'
import os
from core.graph_store import NetworkxGraphStore

dest = os.environ.get("DATA_PROCESSED", "data/vercel")
path = os.path.join(dest, "graph.pkl")
NetworkxGraphStore().save(path)
print(f"Created empty graph -> {path}")
PY
fi

echo "Vercel data ready in $DEST:"
ls -la "$DEST"
