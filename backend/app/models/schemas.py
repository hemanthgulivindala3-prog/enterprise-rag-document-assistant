from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DocumentChunk(BaseModel):
    chunk_id: str
    doc_id: str
    source_name: str
    text: str
    score: float
    metadata: dict = {}

class QueryRequest(BaseModel):
    query: str = Field(..., example="What is our security compliance policy for multi-tenant data?")
    top_k: Optional[int] = 4
    include_citations: bool = True

class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[DocumentChunk]
    latency_ms: float
    tokens_evaluated: int

class DocumentUploadResponse(BaseModel):
    doc_id: str
    filename: str
    chunks_created: int
    total_tokens: int
    indexed_at: datetime
