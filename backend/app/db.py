import os, json, uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine, String, Text, DateTime, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from .domain import BenchmarkRun, RegressionCase, ReleasePolicy, AuditEvent
from .enterprise import ReleaseDecision
from .seed import DEFAULT_POLICIES
DATABASE_URL=os.getenv('DATABASE_URL','sqlite:///./aiql.db')
connect_args={'check_same_thread':False} if DATABASE_URL.startswith('sqlite') else {}
engine=create_engine(DATABASE_URL,pool_pre_ping=True,connect_args=connect_args)
Session=sessionmaker(engine,expire_on_commit=False)
class Base(DeclarativeBase): pass
class RunRow(Base):
 __tablename__='benchmark_runs'; id:Mapped[str]=mapped_column(String(80),primary_key=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True)); payload:Mapped[str]=mapped_column(Text)
class RegressionRow(Base):
 __tablename__='regression_cases'; id:Mapped[str]=mapped_column(String(120),primary_key=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True)); payload:Mapped[str]=mapped_column(Text)
class PolicyRow(Base):
 __tablename__='release_policies'; id:Mapped[str]=mapped_column(String(120),primary_key=True); payload:Mapped[str]=mapped_column(Text)
class AuditRow(Base):
 __tablename__='audit_events'; id:Mapped[str]=mapped_column(String(120),primary_key=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True)); event_type:Mapped[str]=mapped_column(String(120)); resource_type:Mapped[str]=mapped_column(String(120)); resource_id:Mapped[str]=mapped_column(String(160)); payload:Mapped[str]=mapped_column(Text)
class ReleaseRow(Base):
 __tablename__='release_decisions'; id:Mapped[str]=mapped_column(String(160),primary_key=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True)); payload:Mapped[str]=mapped_column(Text)
def init_db():
 Base.metadata.create_all(engine)
 with Session() as s:
  for p in DEFAULT_POLICIES:
   if not s.get(PolicyRow,p.id): s.add(PolicyRow(id=p.id,payload=p.model_dump_json()))
  s.commit()
def db_ready():
 try:
  with engine.connect() as c: c.exec_driver_sql('SELECT 1'); return True
 except Exception: return False
def add_audit(event_type,resource_type,resource_id,payload=None):
 now=datetime.now(timezone.utc); e=AuditEvent(id='evt-'+uuid.uuid4().hex[:16],created_at=now.isoformat(),event_type=event_type,resource_type=resource_type,resource_id=resource_id,payload=payload or {})
 with Session() as s:s.add(AuditRow(id=e.id,created_at=now,event_type=event_type,resource_type=resource_type,resource_id=resource_id,payload=json.dumps(e.payload)));s.commit()
 return e
def list_audit(limit=200):
 with Session() as s: rows=s.scalars(select(AuditRow).order_by(AuditRow.created_at.desc()).limit(limit)).all()
 return [AuditEvent(id=r.id,created_at=r.created_at.isoformat(),event_type=r.event_type,resource_type=r.resource_type,resource_id=r.resource_id,payload=json.loads(r.payload)) for r in rows]
def add_run(run):
 with Session() as s:s.add(RunRow(id=run.id,created_at=datetime.fromisoformat(run.created_at),payload=run.model_dump_json()));s.commit()
 add_audit('benchmark.completed','benchmark_run',run.id,{'use_case':run.use_case,'candidate_count':len(run.candidates)});return run
def list_runs():
 with Session() as s: rows=s.scalars(select(RunRow).order_by(RunRow.created_at.desc())).all()
 return [BenchmarkRun.model_validate_json(r.payload) for r in rows]
def get_run(run_id):
 with Session() as s:r=s.get(RunRow,run_id)
 return BenchmarkRun.model_validate_json(r.payload) if r else None
def add_regression(x):
 now=datetime.now(timezone.utc)
 with Session() as s:s.merge(RegressionRow(id=x.id,created_at=now,payload=x.model_dump_json()));s.commit()
 add_audit('regression.promoted','regression_case',x.id,{'source_run_id':x.source_run_id,'use_case':x.use_case});return x
def list_regressions():
 with Session() as s: rows=s.scalars(select(RegressionRow).order_by(RegressionRow.created_at.desc())).all()
 return [RegressionCase.model_validate_json(r.payload) for r in rows]
def list_policies():
 with Session() as s: rows=s.scalars(select(PolicyRow)).all()
 return [ReleasePolicy.model_validate_json(r.payload) for r in rows]
def get_policy(pid):
 with Session() as s:r=s.get(PolicyRow,pid)
 return ReleasePolicy.model_validate_json(r.payload) if r else None
def save_policy(p):
 with Session() as s:s.merge(PolicyRow(id=p.id,payload=p.model_dump_json()));s.commit()
 add_audit('policy.updated','release_policy',p.id,p.model_dump());return p

def save_release(x):
 with Session() as s:s.add(ReleaseRow(id=x.id,created_at=datetime.fromisoformat(x.created_at),payload=x.model_dump_json()));s.commit()
 add_audit('release.decision','release_decision',x.id,{'decision':x.decision,'run_id':x.run_id,'candidate':x.candidate_model_id,'workspace_id':x.workspace_id});return x
def list_releases():
 with Session() as s: rows=s.scalars(select(ReleaseRow).order_by(ReleaseRow.created_at.desc())).all()
 return [ReleaseDecision.model_validate_json(r.payload) for r in rows]
