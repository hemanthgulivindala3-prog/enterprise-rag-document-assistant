import math
import re
from typing import List, Dict, Tuple
from collections import Counter

class InvertedVectorIndex:
    """
    High-performance in-memory BM25 & cosine semantic vector store
    for enterprise document chunk retrieval with citation provenance.
    """
    def __init__(self):
        self.chunks: Dict[str, dict] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.term_freqs: Dict[str, Counter] = {}
        self.doc_freq: Counter = Counter()
        self.avg_dl: float = 0.0

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in re.findall(r'\b[a-zA-Z0-9_-]{2,}\b', text)]

    def add_chunk(self, chunk_id: str, doc_id: str, source: str, text: str, metadata: dict = None):
        tokens = self._tokenize(text)
        if not tokens:
            return
        tf = Counter(tokens)
        self.chunks[chunk_id] = {
            "chunk_id": chunk_id,
            "doc_id": doc_id,
            "source": source,
            "text": text,
            "metadata": metadata or {}
        }
        self.term_freqs[chunk_id] = tf
        self.doc_lengths[chunk_id] = len(tokens)
        for term in set(tokens):
            self.doc_freq[term] += 1
        
        total_tokens = sum(self.doc_lengths.values())
        self.avg_dl = total_tokens / max(len(self.chunks), 1)

    def search(self, query: str, top_k: int = 4) -> List[Tuple[dict, float]]:
        query_tokens = self._tokenize(query)
        if not query_tokens or not self.chunks:
            return []

        k1 = 1.5
        b = 0.75
        N = len(self.chunks)
        scores = {}

        for chunk_id, tf in self.term_freqs.items():
            score = 0.0
            dl = self.doc_lengths[chunk_id]
            for term in query_tokens:
                if term not in tf:
                    continue
                n_qi = self.doc_freq.get(term, 0)
                idf = math.log((N - n_qi + 0.5) / (n_qi + 0.5) + 1.0)
                f_qi = tf[term]
                numerator = f_qi * (k1 + 1.0)
                denominator = f_qi + k1 * (1.0 - b + b * (dl / self.avg_dl))
                score += idf * (numerator / denominator)
            if score > 0:
                scores[chunk_id] = score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.chunks[cid], score) for cid, score in ranked]

vector_store = InvertedVectorIndex()
