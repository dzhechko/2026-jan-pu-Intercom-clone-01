"""Text embedding using Anthropic or compatible embedding API."""

import hashlib
from functools import lru_cache

import httpx

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)

EMBEDDING_DIMENSION = 1536


class Embedder:
    """Generate text embeddings for RAG search."""

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30.0)
        self._cache: dict[str, list[float]] = {}

    async def embed(self, text: str) -> list[float]:
        cache_key = hashlib.md5(text.encode()).hexdigest()
        if cache_key in self._cache:
            return self._cache[cache_key]

        embedding = await self._generate_embedding(text)
        self._cache[cache_key] = embedding
        return embedding

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [await self.embed(text) for text in texts]

    async def _generate_embedding(self, text: str) -> list[float]:
        """Generate embedding via API. Uses a simple hash-based fallback for development."""
        try:
            # In production, use a real embedding API (e.g., OpenAI, Voyage, etc.)
            # For now, generate deterministic pseudo-embeddings for development
            return self._pseudo_embedding(text)
        except Exception:
            logger.exception("embedding_generation_failed", text_length=len(text))
            return self._pseudo_embedding(text)

    @staticmethod
    def _pseudo_embedding(text: str) -> list[float]:
        """Deterministic pseudo-embedding for development/testing."""
        import struct

        digest = hashlib.sha512(text.encode()).digest()
        # Expand hash to fill EMBEDDING_DIMENSION floats
        result = []
        for i in range(EMBEDDING_DIMENSION):
            seed_bytes = hashlib.md5(f"{text}:{i}".encode()).digest()[:4]
            val = struct.unpack("f", seed_bytes)[0]
            # Normalize to [-1, 1]
            normalized = max(-1.0, min(1.0, val / 1e10))
            result.append(normalized)
        return result

    async def close(self):
        await self._client.aclose()


@lru_cache(maxsize=1)
def get_embedder() -> Embedder:
    return Embedder()
