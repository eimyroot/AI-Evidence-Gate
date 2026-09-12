#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
docker compose config >/dev/null
docker compose build api web
docker compose up -d
for i in {1..45}; do curl -fsS http://127.0.0.1:5173/ready >/tmp/aeg-ready.json 2>/dev/null && break; sleep 1; done
python3 - <<'PY'
import json
x=json.load(open('/tmp/aeg-ready.json'))
assert x['status']=='ready' and x['database']=='ok', x
print('READINESS=PASS')
PY
docker compose run --rm -e PYTHONPATH=/app -v "$ROOT/backend:/app" api pytest -q
cd frontend
npm install
npx playwright install chromium
AIQL_BASE_URL=http://127.0.0.1:5173 npm run e2e
echo AI_EVIDENCE_GATE_VERIFY=PASS
