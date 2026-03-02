"""Document indexing for RAG — process and store documents in Qdrant."""

import uuid

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from src.core.config import settings
from src.core.logging import get_logger
from src.rag.embedder import EMBEDDING_DIMENSION, get_embedder

logger = get_logger(__name__)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


class DocumentIndexer:
    """Process and index documents into Qdrant for RAG search."""

    def __init__(self):
        self.embedder = get_embedder()
        self.qdrant = AsyncQdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)

    async def ensure_collection(self, collection_name: str) -> None:
        collections = await self.qdrant.get_collections()
        existing = {c.name for c in collections.collections}

        if collection_name not in existing:
            await self.qdrant.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=EMBEDDING_DIMENSION, distance=Distance.COSINE),
            )
            logger.info("collection_created", collection=collection_name)

    async def index_document(
        self,
        collection_name: str,
        tenant_id: str,
        title: str,
        content: str,
        metadata: dict | None = None,
    ) -> list[str]:
        await self.ensure_collection(collection_name)

        chunks = self._chunk_text(content)
        embeddings = await self.embedder.embed_batch(chunks)

        points = []
        point_ids = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point_id = str(uuid.uuid4())
            point_ids.append(point_id)
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "tenant_id": tenant_id,
                        "title": title,
                        "content": chunk,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "metadata": metadata or {},
                    },
                )
            )

        await self.qdrant.upsert(collection_name=collection_name, points=points)
        logger.info("document_indexed", collection=collection_name, chunks=len(chunks), title=title)

        return point_ids

    @staticmethod
    def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks

    async def close(self):
        await self.qdrant.close()
