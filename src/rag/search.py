"""Hybrid RAG search: vector similarity + BM25 + RRF merge."""

from dataclasses import dataclass, field

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, ScoredPoint

from src.core.config import settings
from src.core.logging import get_logger
from src.rag.embedder import get_embedder

logger = get_logger(__name__)


@dataclass
class RAGDocument:
    id: str
    content: str
    title: str
    score: float
    metadata: dict = field(default_factory=dict)


@dataclass
class RAGResult:
    documents: list[RAGDocument]
    scores: list[float]
    query_embedding: list[float]


class RAGSearch:
    """Hybrid search combining vector similarity and keyword matching with RRF merge."""

    def __init__(self):
        self.embedder = get_embedder()
        self.qdrant = AsyncQdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)

    async def search(
        self,
        query: str,
        collections: list[str],
        tenant_id: str,
        top_k: int = 5,
        min_similarity: float = 0.7,
    ) -> RAGResult:
        query_embedding = await self.embedder.embed(query)

        # Vector search across collections
        vector_results = await self._vector_search(
            query_embedding, collections, tenant_id, top_k=top_k * 2, min_similarity=min_similarity
        )

        # BM25 keyword search (via Qdrant payload filtering as approximation)
        keyword_results = await self._keyword_search(query, collections, tenant_id, top_k=top_k * 2)

        # RRF merge
        merged = self._rrf_merge(vector_results, keyword_results, k=60)

        # Take top_k results
        final = merged[:top_k]

        return RAGResult(
            documents=final,
            scores=[d.score for d in final],
            query_embedding=query_embedding,
        )

    async def _vector_search(
        self,
        embedding: list[float],
        collections: list[str],
        tenant_id: str,
        top_k: int = 10,
        min_similarity: float = 0.7,
    ) -> list[RAGDocument]:
        results = []

        for collection_name in collections:
            try:
                points: list[ScoredPoint] = await self.qdrant.search(
                    collection_name=collection_name,
                    query_vector=embedding,
                    limit=top_k,
                    score_threshold=min_similarity,
                    query_filter=Filter(
                        must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))]
                    ),
                )
                for point in points:
                    payload = point.payload or {}
                    results.append(
                        RAGDocument(
                            id=str(point.id),
                            content=payload.get("content", ""),
                            title=payload.get("title", ""),
                            score=point.score,
                            metadata=payload.get("metadata", {}),
                        )
                    )
            except Exception:
                logger.exception("vector_search_failed", collection=collection_name)

        results.sort(key=lambda d: d.score, reverse=True)
        return results[:top_k]

    async def _keyword_search(
        self,
        query: str,
        collections: list[str],
        tenant_id: str,
        top_k: int = 10,
    ) -> list[RAGDocument]:
        """Approximate keyword search using Qdrant scroll with payload filtering."""
        # In production, use PostgreSQL full-text search or Qdrant's built-in BM25
        # For now, return empty — vector search is primary
        return []

    @staticmethod
    def _rrf_merge(
        vector_results: list[RAGDocument],
        keyword_results: list[RAGDocument],
        k: int = 60,
    ) -> list[RAGDocument]:
        """Reciprocal Rank Fusion to merge two result lists."""
        scores: dict[str, float] = {}
        docs: dict[str, RAGDocument] = {}

        for rank, doc in enumerate(vector_results):
            scores[doc.id] = scores.get(doc.id, 0) + 1.0 / (k + rank + 1)
            docs[doc.id] = doc

        for rank, doc in enumerate(keyword_results):
            scores[doc.id] = scores.get(doc.id, 0) + 1.0 / (k + rank + 1)
            if doc.id not in docs:
                docs[doc.id] = doc

        # Sort by RRF score
        sorted_ids = sorted(scores, key=lambda x: scores[x], reverse=True)

        result = []
        for doc_id in sorted_ids:
            doc = docs[doc_id]
            doc.score = scores[doc_id]
            result.append(doc)

        return result

    async def close(self):
        await self.qdrant.close()
