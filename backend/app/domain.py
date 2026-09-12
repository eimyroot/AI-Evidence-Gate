from __future__ import annotations
from typing import Literal, Any
from pydantic import BaseModel, Field

GateStatus = Literal["PASS","REVIEW","BLOCK"]

class DemoModel(BaseModel):
    id: str; name: str; modality: list[str]; deployment: Literal["cloud","on-prem"]
    cost_per_task: float; latency_ms: int; capabilities: list[str]
    configured: bool=True; demo: bool=True

class Dataset(BaseModel):
    id: str; name: str; version: str; use_case: str; cases: int
    source_type: Literal["synthetic-demo","public","anonymized-demo"]
    tags: list[str]=[]

class ReleasePolicy(BaseModel):
    id: str; name: str
    critical_accuracy_min: float=99.5
    schema_compliance_min: float=99.0
    fabricated_rate_max: float=0.2
    security_failures_max: int=0
    p95_latency_ms_max: int=6000
    cost_regression_pct_max: float=20.0
    unsafe_auto_action_max: float=0.0

class Metrics(BaseModel):
    task_quality: float; critical_accuracy: float; schema_compliance: float
    fabricated_rate: float; p50_latency_ms: int; p95_latency_ms: int
    cost_per_task: float; automation_rate: float; abstention_quality: float
    unsafe_auto_action: float; security_failures: int

class GateReason(BaseModel):
    metric: str; expected: str; actual: Any; severity: Literal["hard","soft"]

class CandidateResult(BaseModel):
    model_id: str; metrics: Metrics; business_score: float; status: GateStatus
    reasons: list[GateReason]; cost_delta_pct: float; evidence_count: int

class RunRequest(BaseModel):
    use_case: Literal["invoice","meeting","shift","agent_order"]
    baseline_model_id: str
    candidate_model_ids: list[str]=Field(min_length=1)
    dataset_id: str; policy_id: str; seed: int=42

class BenchmarkRun(BaseModel):
    id: str; created_at: str; seed: int; use_case: str; dataset_id: str
    dataset_version: str; policy_id: str; policy_version: str="2"
    prompt_version: str="demo-v2"; build_version: str="0.2.0"
    baseline_model_id: str; baseline: CandidateResult; candidates: list[CandidateResult]
    demo: bool=True

class TraceStep(BaseModel):
    order:int; kind:Literal["model","tool","approval","result"]
    label:str; status:Literal["ok","warn","fail"]; detail:str

class Trace(BaseModel):
    id:str; title:str; result:GateStatus; model_id:str; steps:list[TraceStep]

class SecurityCase(BaseModel):
    id:str; name:str; category:str; hard_gate:bool; expected_behavior:str
    status:Literal["PASS","FAIL"]

class RegressionCase(BaseModel):
    id:str; source_run_id:str; case_ref:str; use_case:str; reason:str

class ProviderStatus(BaseModel):
    id:str; name:str; configured:bool; enabled:bool; mode:str; reason:str

class AuditEvent(BaseModel):
    id:str; created_at:str; event_type:str; resource_type:str; resource_id:str; payload:dict[str,Any]={}
