from app.engine import run_benchmark
from app.domain import RunRequest, ReleasePolicy

def test_deterministic_metrics_same_seed():
 req=RunRequest(use_case='invoice',baseline_model_id='atlas-large',candidate_model_ids=['vision-extractor'],dataset_id='invoice-cz-v4',policy_id='enterprise-strict',seed=777);p=ReleasePolicy(id='enterprise-strict',name='Strict')
 assert run_benchmark(req,p).candidates[0].metrics==run_benchmark(req,p).candidates[0].metrics

def test_security_failure_blocks():
 req=RunRequest(use_case='agent_order',baseline_model_id='atlas-large',candidate_model_ids=['atlas-mini'],dataset_id='agent-order-v5',policy_id='enterprise-strict',seed=42);p=ReleasePolicy(id='enterprise-strict',name='Strict')
 r=run_benchmark(req,p); assert r.candidates[0].status=='BLOCK'; assert any(x.metric=='security_failures' for x in r.candidates[0].reasons)

def test_cheaper_safe_candidate_passes_invoice():
 req=RunRequest(use_case='invoice',baseline_model_id='atlas-large',candidate_model_ids=['vision-extractor'],dataset_id='invoice-cz-v4',policy_id='enterprise-strict',seed=4242);p=ReleasePolicy(id='enterprise-strict',name='Strict')
 c=run_benchmark(req,p).candidates[0]; assert c.status=='PASS'; assert c.cost_delta_pct<0
