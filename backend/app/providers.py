import os
from .domain import ProviderStatus
def provider_statuses():
 allow=os.getenv('AIQL_ALLOW_REAL_PROVIDERS','false').lower()=='true'
 specs=[('openai','OpenAI','OPENAI_API_KEY'),('anthropic','Anthropic','ANTHROPIC_API_KEY'),('google','Google Gemini','GOOGLE_API_KEY'),('openai-compatible','OpenAI-compatible / local','AIQL_OPENAI_COMPATIBLE_BASE_URL')]
 out=[]
 for pid,name,key in specs:
  configured=bool(os.getenv(key)); enabled=allow and configured
  reason='ready for explicit real-provider execution' if enabled else ('configured but disabled by AIQL_ALLOW_REAL_PROVIDERS' if configured else f'{key} not configured')
  out.append(ProviderStatus(id=pid,name=name,configured=configured,enabled=enabled,mode='real' if enabled else 'disabled',reason=reason))
 out.insert(0,ProviderStatus(id='deterministic-demo',name='Deterministic Demo Provider',configured=True,enabled=True,mode='demo',reason='offline reproducible reference adapter'))
 return out
