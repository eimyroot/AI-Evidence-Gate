from app.domain import RunRequest, ReleasePolicy
from app.engine import run_benchmark
from app.enterprise import decide_release, model_radar

def strict_policy():
    return ReleasePolicy(id="enterprise-strict", name="Enterprise Strict")

def test_passing_candidate_promotes():
    run=run_benchmark(RunRequest(use_case="invoice", baseline_model_id="atlas-large", candidate_model_ids=["vision-extractor"], dataset_id="invoice-cz-v4", policy_id="enterprise-strict", seed=4242), strict_policy())
    d=decide_release(run, "vision-extractor", run.policy_id, "invoice-ops", "pilot", "test")
    assert d.decision == "PROMOTE"
    assert d.quality_delta >= 0

def test_blocked_candidate_never_promotes():
    run=run_benchmark(RunRequest(use_case="agent_order", baseline_model_id="atlas-large", candidate_model_ids=["atlas-mini"], dataset_id="agent-order-v5", policy_id="enterprise-strict", seed=4242), strict_policy())
    d=decide_release(run, "atlas-mini", run.policy_id, "order-ops", "pilot", "test")
    assert d.decision == "BLOCK"
    assert any("hard gate" in r for r in d.reasons)
def test_model_radar_rejects_blocking_evidence():
    run=run_benchmark(RunRequest(use_case="agent_order", baseline_model_id="atlas-large", candidate_model_ids=["atlas-mini"], dataset_id="agent-order-v5", policy_id="enterprise-strict", seed=4242), strict_policy())
    radar=model_radar([run])
    row=next(x for x in radar if x["model_id"] == "atlas-mini")
    assert row["state"] == "REJECTED"
