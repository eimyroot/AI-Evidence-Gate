from __future__ import annotations
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field

ReleaseDecisionStatus = Literal["PROMOTE", "HOLD", "BLOCK", "UNKNOWN"]

class EnterpriseWorkspace(BaseModel):
    id: str
    name: str
    use_case: str
    environment: Literal["demo", "pilot", "production"]
    deployment: Literal["cloud", "on-prem", "hybrid"]
    data_residency: str
    criticality: Literal["standard", "high", "critical"]
    owner: str
    integration: str

class ReleaseDecisionRequest(BaseModel):
    run_id: str
    candidate_model_id: str
    workspace_id: str = "coalbrain-lab"
    environment: Literal["pilot", "production"] = "pilot"
    requested_by: str = "quality-operator"
class ReleaseDecision(BaseModel):
    id: str
    created_at: str
    run_id: str
    workspace_id: str
    environment: str
    incumbent_model_id: str
    candidate_model_id: str
    decision: ReleaseDecisionStatus
    reasons: list[str]
    quality_delta: float
    cost_delta_pct: float
    p95_latency_delta_ms: int
    policy_id: str
    requested_by: str

WORKSPACES = [
    EnterpriseWorkspace(id="coalbrain-lab", name="Coalbrain Reference Lab", use_case="portfolio", environment="demo", deployment="hybrid", data_residency="EU / client-selectable", criticality="high", owner="AI Quality", integration="Provider + ERP adapter boundary"),
    EnterpriseWorkspace(id="invoice-ops", name="Document Processing", use_case="invoice", environment="pilot", deployment="on-prem", data_residency="client network", criticality="critical", owner="Finance Automation", integration="Email → extraction → ERP"),
    EnterpriseWorkspace(id="meeting-ops", name="Meeting Intelligence", use_case="meeting", environment="pilot", deployment="hybrid", data_residency="EU / on-prem option", criticality="high", owner="Knowledge Automation", integration="Audio → decisions/tasks → Teams/email"),
]
WORKSPACES += [
    EnterpriseWorkspace(id="shift-ops", name="Shift Planning", use_case="shift", environment="pilot", deployment="cloud", data_residency="EU", criticality="critical", owner="Workforce Automation", integration="HR/ERP → constraints → approved schedule"),
    EnterpriseWorkspace(id="order-ops", name="Order Agent", use_case="agent_order", environment="pilot", deployment="hybrid", data_residency="client-selectable", criticality="critical", owner="Logistics Automation", integration="Email → validation → approval → ERP"),
]

def decide_release(run, candidate_model_id: str, policy_id: str, workspace_id: str, environment: str, requested_by: str) -> ReleaseDecision:
    candidate = next((c for c in run.candidates if c.model_id == candidate_model_id), None)
    if candidate is None:
        raise ValueError("Candidate not found in run")
    reasons: list[str] = []
    if candidate.status == "BLOCK":
        decision: ReleaseDecisionStatus = "BLOCK"
        reasons.extend([f"hard gate: {r.metric}" for r in candidate.reasons if r.severity == "hard"] or ["benchmark blocked"])
    elif candidate.status == "REVIEW":
        decision = "HOLD"
        reasons.extend([f"review: {r.metric}" for r in candidate.reasons] or ["manual review required"])
    elif candidate.status == "PASS":
        decision = "PROMOTE"
        reasons.append("all configured release gates passed")
    else:
        decision = "UNKNOWN"
        reasons.append("unrecognized benchmark state")
    quality_delta = round(candidate.metrics.critical_accuracy - run.baseline.metrics.critical_accuracy, 2)
    p95_delta = candidate.metrics.p95_latency_ms - run.baseline.metrics.p95_latency_ms
    now = datetime.now(timezone.utc)
    rid = f"rel-{int(now.timestamp())}-{candidate_model_id}"
    return ReleaseDecision(
        id=rid, created_at=now.isoformat(), run_id=run.id,
        workspace_id=workspace_id, environment=environment,
        incumbent_model_id=run.baseline_model_id,
        candidate_model_id=candidate_model_id, decision=decision,
        reasons=reasons, quality_delta=quality_delta,
        cost_delta_pct=candidate.cost_delta_pct,
        p95_latency_delta_ms=p95_delta, policy_id=policy_id,
        requested_by=requested_by,
    )

def model_radar(runs) -> list[dict]:
    models: dict[str, dict] = {}
    for run in runs:
        for c in run.candidates:
            row = models.setdefault(c.model_id, {"model_id": c.model_id, "pass": 0, "review": 0, "block": 0, "runs": 0, "best_cost_delta_pct": None})
            row["runs"] += 1
            row[c.status.lower()] += 1
            if row["best_cost_delta_pct"] is None or c.cost_delta_pct < row["best_cost_delta_pct"]:
                row["best_cost_delta_pct"] = c.cost_delta_pct
    out=[]
    for row in models.values():
        if row["block"]:
            state="REJECTED"
        elif row["pass"] and (row["best_cost_delta_pct"] is not None and row["best_cost_delta_pct"] < 0):
            state="CANDIDATE"
        elif row["pass"]:
            state="CURRENT"
        else:
            state="WATCH"
        out.append({**row, "state": state})
    return sorted(out, key=lambda x: (x["state"], x["model_id"]))

def portfolio_summary(runs, releases, regressions, audit_events) -> dict:
    candidates=[c for r in runs for c in r.candidates]
    blocked=sum(1 for c in candidates if c.status=="BLOCK")
    promoted=sum(1 for r in releases if r.decision=="PROMOTE")
    avg_quality=round(sum(c.metrics.critical_accuracy for c in candidates)/len(candidates),2) if candidates else 0
    return {
        "workspaces": len(WORKSPACES), "benchmark_runs": len(runs),
        "candidate_evidence": len(candidates), "blocked_candidates": blocked,
        "promoted_releases": promoted, "regression_cases": len(regressions),
        "audit_events": len(audit_events), "avg_critical_accuracy": avg_quality,
        "control_mode": "fail-closed", "product_version": "enterprise-mvp-1",
    }
