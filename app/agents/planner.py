from app.llm import llm
from app.models import ResearchTask
SYSTEM='Convert the research question into focused evidence-search tasks. Do not make factual claims. Return JSON: {"tasks":[{topic,query,source_types,jurisdiction}]}.'
def plan(q):
 if not llm.enabled:return [ResearchTask(topic='cryptographic threat',query='quantum computing RSA ECC banking cryptography',source_types=['regulator','academic']),ResearchTask(topic='HNDL',query='harvest now decrypt later financial sector',source_types=['regulator','government']),ResearchTask(topic='PQC',query='post quantum cryptography banking migration',source_types=['standards','regulator']),ResearchTask(topic='Indonesia',query='Indonesia banking cybersecurity quantum cryptography PQC',source_types=['government','regulator'],jurisdiction='Indonesia')]
 return [ResearchTask(**x) for x in llm.json(SYSTEM,q)['tasks']]
