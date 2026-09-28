import hashlib
from app.models import Source,ResearchTask
DEMO=[{'title':'Quantum computing and the financial system','publisher':'BIS','source_type':'institutional_report','url':'https://www.bis.org/','publication_date':'2024','jurisdiction':'International'},{'title':'Post-Quantum Cryptography Standards','publisher':'NIST','source_type':'standard','url':'https://csrc.nist.gov/projects/post-quantum-cryptography','publication_date':'2024','jurisdiction':'United States'}]
def discover(task:ResearchTask): return [Source(source_id='SRC-'+hashlib.sha1(x['url'].encode()).hexdigest()[:10],**x) for x in DEMO]
