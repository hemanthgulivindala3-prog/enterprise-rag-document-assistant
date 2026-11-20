from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.core.rag_engine import rag_engine

router = APIRouter(prefix="/chat", tags=["RAG Chat"])

@router.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    return rag_engine.answer_query(request.query, top_k=request.top_k)
