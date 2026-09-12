# Product truth — R2

## Verified by design
- deterministic demo benchmark engine
- explicit PASS / REVIEW / BLOCK gate evaluation
- persistent run, policy, regression and audit repositories
- PostgreSQL default in Docker Compose; SQLite fallback for direct local API execution
- explicit provider status with real providers disabled unless both configuration and an allow flag exist
- `/health` for process liveness and `/ready` for database readiness

## Intentionally not claimed
- bundled demo results are not measurements of OpenAI, Anthropic, Google, Meta or any real model
- synthetic datasets are not client production data
- security demo cases are product behavior examples, not a third-party certification
- R2 does not claim production SLA, multi-tenant isolation, SSO/RBAC or regulated-industry certification

## Release invariant
UNKNOWN is not PASS. A hard security gate cannot be averaged away by a high business score.
