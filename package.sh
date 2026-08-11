#!/usr/bin/env bash
# Package deliverables into devsu-exercise.zip (excludes venv, caches, git, node_modules).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

OUT="devsu-exercise.zip"
rm -f "$OUT"

zip -r "$OUT" . \
  -x ".git/*" \
  -x ".venv/*" \
  -x "venv/*" \
  -x "**/__pycache__/*" \
  -x "**/.pytest_cache/*" \
  -x "node_modules/*" \
  -x "postman/node_modules/*" \
  -x ".idea/*" \
  -x "reports/*" \
  -x "*.zip" \
  -x "**/.DS_Store"

echo "Created: $ROOT/$OUT"
ls -lh "$OUT"
