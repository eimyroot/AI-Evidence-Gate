# AI Evidence Gate

**Evidence-first evaluation and release control plane for AI systems.**

AI Evidence Gate is an independent reference implementation for deciding whether a model or agent workflow is safe and useful enough for a specific business process. Instead of asking “which model is best?”, it records evidence and produces explicit **PASS / REVIEW / BLOCK** benchmark outcomes and **PROMOTE / HOLD / BLOCK / UNKNOWN** release decisions.

> Independent portfolio project. No affiliation with Coalbrain or any model provider. Bundled models, datasets and default benchmark results are synthetic/demo evidence.

## Product surface

- deterministic, reproducible benchmark runs
- versioned dataset and model registries
- PostgreSQL-backed benchmark, regression, policy and audit persistence
- security hard gates and agent trace evidence
- editable release policies
- failed-case → regression workflow
- enterprise workspaces with cloud / on-prem / hybrid posture
- incumbent-vs-challenger release decisions
- model radar and executive evidence views
- explicit provider readiness boundary
- React control plane + FastAPI API + Docker Compose
- Playwright browser E2E and GitHub Actions CI

## Trust model

`UNKNOWN ≠ PASS.` Security hard-gate failures cannot be averaged away by a high business score. A cheaper or faster challenger is promotion-eligible only when the recorded policy still passes.

The current public MVP keeps live external-provider execution disabled by default. Provider credentials are never bundled in the repository.

## Architecture

```text
Model / agent candidate
        ↓
Versioned dataset + replay
        ↓
Deterministic / semantic / security graders
        ↓
Quality + latency + cost + safety evidence
        ↓
Release policy
        ↓
PASS / REVIEW / BLOCK
        ↓
Enterprise release gate
        ↓
PROMOTE / HOLD / BLOCK / UNKNOWN
        ↓
Persistent audit + regression feedback
```

## Quick start

```bash
docker compose up --build -d
curl -fsS http://localhost:5173/ready
open http://localhost:5173
```

Backend API: `http://localhost:8000/docs`

## Verification

```bash
# backend
docker compose run --rm -e PYTHONPATH=/app -v "$PWD/backend:/app" api pytest -q

# production frontend build
docker compose build web

# browser E2E
cd frontend
npm install
npx playwright install chromium
npm run e2e
```

## Coalbrain reference fit

The repository includes an independent use-case mapping for document processing, meeting intelligence, workforce scheduling and ERP/order-agent workflows. See `docs/COALBRAIN_FIT.md`. It is a portfolio fit assessment, not a claim that Coalbrain currently uses this product.

## Enterprise boundary

This is an Enterprise MVP/reference implementation, not a claim of production certification. Before a regulated or multi-tenant deployment, the hardening backlog includes enforceable OIDC/RBAC, tenant isolation, secrets/KMS integration, client-data ingestion/redaction/retention controls, telemetry/alerting, backup drills, signed attestations, HA/SLOs and real ERP/provider adapters.

See `docs/ENTERPRISE_MVP.md` for the explicit product boundary.
