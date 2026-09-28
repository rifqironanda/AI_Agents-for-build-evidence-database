import json
from openai import OpenAI
from .config import OPENAI_API_KEY,OPENAI_MODEL
class LLM:
 def __init__(self): self.enabled=bool(OPENAI_API_KEY); self.client=OpenAI(api_key=OPENAI_API_KEY) if self.enabled else None
 def json(self,system,user):
  r=self.client.chat.completions.create(model=OPENAI_MODEL,response_format={'type':'json_object'},messages=[{'role':'system','content':system},{'role':'user','content':user}]); return json.loads(r.choices[0].message.content)
llm=LLM()
