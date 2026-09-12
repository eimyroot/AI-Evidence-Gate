# AI Evidence Gate — Architecture

```text
Browser / operator
  │
  ▼
Nginx :5173
  │ /api, /health, /ready
  ▼
FastAPI :8000
  ├── Registry: fictional demo models + versioned synthetic datasets
  ├── Benchmark engine: deterministic replay by seed
  ├── Grading + business metrics
  ├── Benchmark gate: PASS / REVIEW / BLOCK
  ├── Enterprise release gate: PROMOTE / HOLD / BLOCK / UNKNOWN
  ├── Provider boundary: explicit configured/enabled state
  └── Repository
        │
        ▼
PostgreSQL
  ├── benchmark_runs
  ├── regression_cases
  ├── release_policies
  ├── release_decisions
  └── audit_events
```

Every persisted benchmark carries dataset version, policy version, prompt version, build version and seed. Release decisions reference immutable benchmark evidence and preserve incumbent, challenger, workspace, environment and decision reasons.
