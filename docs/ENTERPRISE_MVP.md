# AI Evidence Gate — Enterprise MVP

## Product thesis
AI Evidence Gate is a quality and release control plane for AI-powered business workflows. It does not ask which model is best in general. It asks which model, prompt, provider or agent workflow is safe and economically sensible for a specific process under an explicit policy.

## Enterprise MVP scope
- persistent benchmark evidence in PostgreSQL
- versioned datasets and regression corpus
- raw quality, safety, latency and cost metrics
- hard/soft release gates
- enterprise workspace metadata for cloud, on-prem and hybrid deployments
- model radar derived from evidence, not marketing labels
- PROMOTE / HOLD / BLOCK / UNKNOWN release receipts
- audit ledger for quality-control mutations
- provider configuration boundary with safe disabled default
- health/readiness endpoints, Docker Compose and browser E2E scaffold

## Release invariant
UNKNOWN is never PASS. A hard security gate cannot be averaged away by a high business score.
## Production-hardening backlog
The MVP deliberately labels unfinished enterprise controls instead of faking them:

- OIDC/SSO and enforceable RBAC
- row-level tenant isolation
- secrets manager / KMS integration
- client dataset ingestion with PII redaction and retention rules
- OpenTelemetry, alerting and SLOs
- backup/restore drills and disaster recovery
- signed release attestations
- HA deployment topology
- product-specific ERP/HR/solver contract tests

## Deployment posture
The reference stack supports PostgreSQL + FastAPI + Nginx/React via Docker Compose. Workspace metadata can represent cloud, on-prem or hybrid delivery. This is a scaffold for enterprise delivery, not a claim of certified production readiness.
