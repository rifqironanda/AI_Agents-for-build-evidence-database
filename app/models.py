from typing import Optional,List
from pydantic import BaseModel,Field
class ResearchTask(BaseModel):
 topic:str; query:str; source_types:List[str]=Field(default_factory=list); jurisdiction:Optional[str]=None
class Source(BaseModel):
 source_id:str; title:str; publisher:str; publication_date:Optional[str]=None; source_type:str; url:str; jurisdiction:Optional[str]=None
class Claim(BaseModel):
 claim_id:str; source_id:str; claim_text:str; claim_type:str; topic:str; threat_type:Optional[str]=None; evidence_quote:str; page_or_section:Optional[str]=None; time_expression:Optional[str]=None; extraction_confidence:float=0.0
class Validation(BaseModel):
 claim_id:str; status:str; claim_supported:bool; citation_present:bool; interpretation_risk:str; rationale:str
