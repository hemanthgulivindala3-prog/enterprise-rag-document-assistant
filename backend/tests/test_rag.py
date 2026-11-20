from app.core.vector_store import InvertedVectorIndex
from app.core.rag_engine import RAGEngine

def test_vector_indexing_and_search():
    index = InvertedVectorIndex()
    index.add_chunk("c1", "d1", "Policy.md", "Microservices deployed to Azure Kubernetes with strict security.")
    index.add_chunk("c2", "d2", "Billing.md", "Invoice payments processed monthly via automated wire transfers.")

    results = index.search("Azure Kubernetes security")
    assert len(results) > 0
    assert results[0][0]["chunk_id"] == "c1"

def test_rag_synthesis():
    engine = RAGEngine()
    res = engine.answer_query("Microservices")
    assert res.query == "Microservices"
    assert res.latency_ms >= 0
