import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .domain import RunRequest, RegressionCase, ReleasePolicy
from .seed import MODELS, DATASETS, TRACES, SECURITY_CASES
from .engine import run_benchmark
from .providers import provider_statuses
from .db import init_db,db_ready,add_run,list_runs,get_run,add_regression,list_regressions,list_policies,get_policy,save_policy,list_audit
from .enterprise_api import router as enterprise_router

DEMO_RUNS=[('invoice','atlas-large',['vision-extractor'],'invoice-cz-v4','enterprise-strict',110),('meeting','atlas-large',['nova-reasoner'],'meeting-cz-v2','balanced',120),('shift','atlas-large',['nova-reasoner'],'shift-v3','balanced',130),('agent_order','atlas-large',['atlas-mini'],'agent-order-v5','enterprise-strict',140),('invoice','atlas-large',['atlas-mini'],'invoice-cz-v4','enterprise-strict',150),('meeting','nova-reasoner',['local-czech-14b'],'meeting-cz-v2','balanced',160),('shift','nova-reasoner',['local-czech-14b'],'shift-v3','balanced',170),('agent_order','nova-reasoner',['atlas-large'],'agent-order-v5','balanced',180)]

def seed_history():
 if list_runs() or os.getenv('AIQL_DEMO_SEED','true').lower()!='true': return
 for uc,b,c,d,p,seed in DEMO_RUNS:
  pol=get_policy(p); add_run(run_benchmark(RunRequest(use_case=uc,baseline_model_id=b,candidate_model_ids=c,dataset_id=d,policy_id=p,seed=seed),pol))

@asynccontextmanager
async def lifespan(app):
 init_db(); seed_history(); yield
app=FastAPI(title='AI Evidence Gate API',version='1.0.0-enterprise-mvp',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(enterprise_router)
@app.get('/')
def root(): return {'product':'AI Evidence Gate','version':'1.0.0-enterprise-mvp','mode':'independent-demo','docs':'/docs','ready':'/ready'}
@app.get('/health')
def health(): return {'status':'ok','mode':'independent-demo','version':'1.0.0-enterprise-mvp'}
@app.get('/ready')
def ready():
 ok=db_ready(); return {'status':'ready' if ok else 'not_ready','database':'ok' if ok else 'failed','providers':provider_statuses()}
@app.get('/api/models')
def models(): return MODELS
@app.get('/api/datasets')
def datasets(): return DATASETS
@app.get('/api/policies')
def policies(): return list_policies()
@app.put('/api/policies/{pid}')
def update_policy(pid:str,p:ReleasePolicy):
 if p.id!=pid: raise HTTPException(400,'Policy id mismatch')
 return save_policy(p)
@app.get('/api/providers')
def providers(): return provider_statuses()
@app.get('/api/traces')
def traces(): return TRACES
@app.get('/api/security')
def security(): return SECURITY_CASES
@app.get('/api/runs')
def runs(): return list_runs()
@app.get('/api/runs/{run_id}')
def run_detail(run_id:str):
 r=get_run(run_id)
 if not r: raise HTTPException(404,'Run not found')
 return r
@app.post('/api/runs')
def run(req:RunRequest):
 mids={m.id for m in MODELS}; dids={d.id for d in DATASETS}
 if req.baseline_model_id not in mids or any(x not in mids for x in req.candidate_model_ids): raise HTTPException(400,'Unknown model id')
 if req.dataset_id not in dids: raise HTTPException(400,'Unknown dataset id')
 pol=get_policy(req.policy_id)
 if not pol: raise HTTPException(400,'Unknown policy id')
 return add_run(run_benchmark(req,pol))
@app.get('/api/regressions')
def regressions(): return list_regressions()
@app.post('/api/regressions')
def regression(x:RegressionCase): return add_regression(x)
@app.get('/api/audit')
def audit(): return list_audit()
