from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_chat import router as chat_router
from app.api.routes_documents import router as docs_router
from app.core.vector_store import vector_store

app = FastAPI(
    title="Enterprise RAG Document Assistant",
    description="Scalable knowledge-base RAG engine with citation provenance, BM25 semantic retrieval, and streaming LLM integration.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1")
app.include_router(docs_router, prefix="/api/v1")

# Preload sample enterprise knowledge
@app.on_event("startup")
def preload_enterprise_policies():
    policies = [
        ("Cloud Architecture Blueprint", "All enterprise retail services must follow microservices patterns with stateless Node.js/Python containers deployed on Azure Kubernetes Service (AKS)."),
        ("Data Encryption & Key Management", "Customer Personally Identifiable Information (PII) must be encrypted at rest using AES-256 with Azure Key Vault customer-managed keys (CMK) and in transit via TLS 1.3."),
        ("AI Agent Reliability Policy", "All Generative AI and RAG agents must incorporate grounding checks, citation references to verified internal documents, and strict input/output guardrails."),
        ("Banking SLA & Fault Tolerance", "Financial transactions require zero-data-loss architecture using synchronous multi-region MySQL database replication with an RPO of 0 and RTO < 60 seconds.")
    ]
    for i, (title, content) in enumerate(policies):
        vector_store.add_chunk(
            chunk_id=f"init-c{i+1}",
            doc_id="policy-core-v1",
            source=f"{title}.md",
            text=content,
            metadata={"category": "Enterprise Architecture"}
        )

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "enterprise-rag-api", "version": "1.0.0"}
