from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import DocumentUploadResponse
from app.core.vector_store import vector_store
import uuid
from datetime import datetime

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Only UTF-8 encoded text or markdown files are supported.")

    doc_id = str(uuid.uuid4())[:8]
    # Simple chunking
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks_created = 0
    total_tokens = 0

    for i, p in enumerate(paragraphs):
        chunk_id = f"{doc_id}-c{i+1}"
        vector_store.add_chunk(
            chunk_id=chunk_id,
            doc_id=doc_id,
            source=file.filename,
            text=p,
            metadata={"chunk_index": i+1}
        )
        chunks_created += 1
        total_tokens += len(p.split())

    return DocumentUploadResponse(
        doc_id=doc_id,
        filename=file.filename,
        chunks_created=chunks_created,
        total_tokens=total_tokens,
        indexed_at=datetime.utcnow()
    )

@router.get("/stats")
async def get_index_stats():
    return {
        "indexed_chunks": len(vector_store.chunks),
        "unique_terms": len(vector_store.doc_freq),
        "avg_chunk_tokens": round(vector_store.avg_dl, 1)
    }
