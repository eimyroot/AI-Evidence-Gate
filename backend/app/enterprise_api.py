from fastapi import APIRouter, HTTPException
from .enterprise import WORKSPACES, ReleaseDecisionRequest, decide_release, model_radar, portfolio_summary
from .db import list_runs, get_run, list_regressions, list_audit, list_releases, save_release

router = APIRouter(prefix="/api/enterprise", tags=["enterprise"])

@router.get("/summary")
def summary():
    return portfolio_summary(list_runs(), list_releases(), list_regressions(), list_audit())

@router.get("/workspaces")
def workspaces():
    return WORKSPACES

@router.get("/releases")
def releases():
    return list_releases()

@router.get("/radar")
def radar():
    return model_radar(list_runs())

@router.get("/incidents")
def incidents():
    out=[]
    for run in list_runs():
        for c in run.candidates:
            if c.status == "BLOCK":
                out.append({"id": f"inc-{run.id}-{c.model_id}", "severity": "high", "use_case": run.use_case, "run_id": run.id, "model_id": c.model_id, "title": "Release blocked by hard gate", "reasons": [r.metric for r in c.reasons if r.severity == "hard"]})
    return out[:50]
@router.post("/releases")
def create_release(req: ReleaseDecisionRequest):
    run=get_run(req.run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    if not any(w.id == req.workspace_id for w in WORKSPACES):
        raise HTTPException(400, "Unknown workspace")
    try:
        decision=decide_release(run, req.candidate_model_id, run.policy_id, req.workspace_id, req.environment, req.requested_by)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return save_release(decision)

@router.get("/compliance")
def compliance():
    return {
        "mode": "reference-enterprise-mvp",
        "controls": [
            {"id":"fail-closed", "name":"Unknown is not PASS", "status":"ENFORCED"},
            {"id":"security-gate", "name":"Security hard gates block promotion", "status":"ENFORCED"},
            {"id":"audit", "name":"Mutating quality actions leave audit receipts", "status":"ENFORCED"},
            {"id":"data-residency", "name":"Cloud/on-prem/hybrid deployment metadata", "status":"SCAFFOLDED"},
            {"id":"rbac", "name":"SSO/RBAC enforcement", "status":"ROADMAP"},
            {"id":"secrets", "name":"External secrets manager integration", "status":"ROADMAP"},
        ],
        "disclaimer": "Reference implementation; not a certification or security attestation."
    }
