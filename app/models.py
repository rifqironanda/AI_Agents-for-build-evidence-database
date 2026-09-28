from typing import Optional, List
from pydantic import BaseModel, Field


class Document(BaseModel):
    document_id: str
    filename: str
    path: str
    page_count: int
    file_hash: str


class PageText(BaseModel):
    document_id: str
    page_number: int
    text: str


class Summary(BaseModel):
    document_id: str
    summary: str
    key_points: List[str] = Field(default_factory=list)
    limitations: str = ""
    model: str = ""


class Validation(BaseModel):
    document_id: str
    status: str = "pending"
    notes: Optional[str] = None
