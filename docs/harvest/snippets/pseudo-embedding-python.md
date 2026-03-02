# Snippet: Deterministic Pseudo-Embedding Generator (Python)

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Generates deterministic pseudo-embeddings from text input using MD5 hashing and `struct.unpack`. Produces reproducible N-dimensional float vectors from any string, without requiring an external embedding API or model. Designed for testing, development, and prototyping RAG pipelines where real embeddings are not yet available or too expensive to call repeatedly.

## Dependencies

None (Python standard library only: `hashlib`, `struct`).

## Code

```python
"""Deterministic pseudo-embedding generator for testing and development."""

import hashlib
import struct


def pseudo_embedding(text: str, dimensions: int = 1536) -> list[float]:
    """Generate a deterministic pseudo-embedding from text.

    Uses MD5 hashing to produce reproducible float vectors. The same input
    text always produces the same output vector. Different texts produce
    different vectors (with high probability).

    Args:
        text: Input text to embed.
        dimensions: Number of dimensions in the output vector.

    Returns:
        List of floats normalized to the range [-1.0, 1.0].
    """
    result = []
    for i in range(dimensions):
        seed = f"{text}:{i}".encode()
        hash_bytes = hashlib.md5(seed).digest()[:4]
        raw_float = struct.unpack("f", hash_bytes)[0]
        # Normalize to [-1.0, 1.0]
        normalized = max(-1.0, min(1.0, raw_float / 1e10))
        result.append(normalized)
    return result


def pseudo_embedding_batch(texts: list[str], dimensions: int = 1536) -> list[list[float]]:
    """Generate pseudo-embeddings for a batch of texts.

    Args:
        texts: List of input texts.
        dimensions: Number of dimensions per vector.

    Returns:
        List of embedding vectors.
    """
    return [pseudo_embedding(text, dimensions) for text in texts]
```

## Usage Example

```python
# Same input always produces the same output
vec1 = pseudo_embedding("hello world")
vec2 = pseudo_embedding("hello world")
assert vec1 == vec2  # Deterministic

# Different inputs produce different vectors
vec3 = pseudo_embedding("goodbye world")
assert vec1 != vec3

# Check dimensions
assert len(vec1) == 1536

# All values are in [-1.0, 1.0]
assert all(-1.0 <= v <= 1.0 for v in vec1)

# Use in tests as a drop-in replacement for real embeddings
class MockEmbedder:
    async def embed(self, text: str) -> list[float]:
        return pseudo_embedding(text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return pseudo_embedding_batch(texts)
```

## Notes

- This is NOT suitable for production use. The generated vectors have no semantic meaning -- "cat" and "kitten" will be just as distant as "cat" and "motorcycle." Use a real embedding model (e.g., OpenAI `text-embedding-3-small`, Voyage AI, or sentence-transformers) for actual similarity search.
- The primary use case is testing: verifying that your RAG pipeline correctly stores, retrieves, and ranks embeddings without incurring API costs or network latency.
- MD5 is used for speed and determinism, not for security. Since this is a testing utility, cryptographic weakness is irrelevant.
- The `1e10` normalization divisor is a heuristic that maps the arbitrary IEEE 754 float range into [-1, 1]. Some values will cluster near zero. This is acceptable for testing but means the distribution is not uniform.
- The default 1536 dimensions matches OpenAI's `text-embedding-3-small` output size. Adjust to match your production embedding model's dimensionality.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
