import random, hashlib
from datetime import datetime, timezone
from .domain import *
from .seed import MODELS, DATASETS
MODEL_MAP={m.id:m for m in MODELS}; DATASET_MAP={d.id:d for d in DATASETS}
PROFILES={
 "atlas-large":dict(q=99.35,c=99.72,s=99.8,f=.10,a=91,abst=97.2,unsafe=0,sec=0),
 "atlas-mini":dict(q=97.9,c=98.84,s=99.1,f=.32,a=94,abst=88,unsafe=.18,sec=1),
 "nova-reasoner":dict(q=99.15,c=99.60,s=99.7,f=.08,a=89,abst=98.3,unsafe=0,sec=0),
 "local-czech-14b":dict(q=97.55,c=98.95,s=98.8,f=.25,a=86,abst=93.4,unsafe=0,sec=0),
 "vision-extractor":dict(q=99.45,c=99.81,s=99.9,f=.05,a=93,abst=98.8,unsafe=0,sec=0)}
ADJ={"invoice":{"vision-extractor":.25,"atlas-mini":-.15},"meeting":{"nova-reasoner":.20,"vision-extractor":-.40},"shift":{"nova-reasoner":.25,"atlas-mini":-.35},"agent_order":{"nova-reasoner":.30,"atlas-mini":-.45}}
def jitter(seed,key,scale):
 h=hashlib.sha256(f"{seed}:{key}".encode()).hexdigest(); return random.Random(int(h[:12],16)).uniform(-scale,scale)
def metrics_for(mid,use_case,seed):
 m=MODEL_MAP[mid]; p=PROFILES[mid].copy(); a=ADJ.get(use_case,{}).get(mid,0); p['q']+=a;p['c']+=a;qj=jitter(seed,mid+use_case,.07);lat=int(m.latency_ms*(1+jitter(seed,mid+'lat',.08)))
 return Metrics(task_quality=round(p['q']+qj,2),critical_accuracy=round(min(100,p['c']+qj),2),schema_compliance=round(min(100,p['s']+qj/2),2),fabricated_rate=round(max(0,p['f']+jitter(seed,mid+'fab',.025)),2),p50_latency_ms=lat,p95_latency_ms=int(lat*1.65),cost_per_task=m.cost_per_task,automation_rate=round(p['a']+jitter(seed,mid+'auto',1),1),abstention_quality=round(p['abst']+jitter(seed,mid+'abst',.5),1),unsafe_auto_action=p['unsafe'],security_failures=p['sec'])
def score(m): return round(.30*m.critical_accuracy+.20*m.task_quality+.15*m.schema_compliance+.15*m.abstention_quality+.10*m.automation_rate+.10*max(0,100-m.fabricated_rate*20),2)
def gate(m,b,p):
 rs=[]; hard=False; review=False; cd=((m.cost_per_task-b.cost_per_task)/b.cost_per_task)*100 if b.cost_per_task else 0
 def f(metric,exp,actual,severity='hard'):
  nonlocal hard,review;rs.append(GateReason(metric=metric,expected=exp,actual=actual,severity=severity));hard|=severity=='hard';review|=severity=='soft'
 if m.critical_accuracy<p.critical_accuracy_min:f('critical_accuracy',f'>= {p.critical_accuracy_min}%',m.critical_accuracy)
 if m.schema_compliance<p.schema_compliance_min:f('schema_compliance',f'>= {p.schema_compliance_min}%',m.schema_compliance)
 if m.fabricated_rate>p.fabricated_rate_max:f('fabricated_rate',f'<= {p.fabricated_rate_max}%',m.fabricated_rate)
 if m.security_failures>p.security_failures_max:f('security_failures',f'<= {p.security_failures_max}',m.security_failures)
 if m.unsafe_auto_action>p.unsafe_auto_action_max:f('unsafe_auto_action',f'<= {p.unsafe_auto_action_max}%',m.unsafe_auto_action)
 if m.p95_latency_ms>p.p95_latency_ms_max:f('p95_latency_ms',f'<= {p.p95_latency_ms_max}',m.p95_latency_ms,'soft')
 if cd>p.cost_regression_pct_max:f('cost_regression_pct',f'<= {p.cost_regression_pct_max}%',round(cd,2),'soft')
 return ('BLOCK' if hard else 'REVIEW' if review else 'PASS'),rs,round(cd,2)
def run_benchmark(req,policy):
 ds=DATASET_MAP[req.dataset_id]; bm=metrics_for(req.baseline_model_id,req.use_case,req.seed); base=CandidateResult(model_id=req.baseline_model_id,metrics=bm,business_score=score(bm),status='PASS',reasons=[],cost_delta_pct=0,evidence_count=ds.cases)
 cs=[]
 for cid in req.candidate_model_ids:
  cm=metrics_for(cid,req.use_case,req.seed);st,rs,cd=gate(cm,bm,policy);cs.append(CandidateResult(model_id=cid,metrics=cm,business_score=score(cm),status=st,reasons=rs,cost_delta_pct=cd,evidence_count=ds.cases))
 now=datetime.now(timezone.utc);rid='run-'+hashlib.sha1(f'{now.isoformat()}:{req.seed}:{req.use_case}'.encode()).hexdigest()[:12]
 return BenchmarkRun(id=rid,created_at=now.isoformat(),seed=req.seed,use_case=req.use_case,dataset_id=ds.id,dataset_version=ds.version,policy_id=policy.id,baseline_model_id=req.baseline_model_id,baseline=base,candidates=cs)
