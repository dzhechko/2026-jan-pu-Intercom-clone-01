# Pseudocode: RAG Pipeline

## pseudo_embedding(text)

```
FUNCTION pseudo_embedding(text: str) -> list[float]:
    FOR i IN 0..1536:
        seed_bytes = MD5("{text}:{i}").digest()[:4]
        val = unpack_float(seed_bytes)
        result[i] = clamp(val / 1e10, -1.0, 1.0)
    RETURN result
// Deterministic, 1536-dim, normalized to [-1, 1]
```

## embed(text)

```
FUNCTION embed(text: str) -> list[float]:
    cache_key = MD5(text).hexdigest()
    IF cache_key IN self._cache: RETURN self._cache[cache_key]
    TRY:   embedding = call_embedding_api(text)
    CATCH: embedding = pseudo_embedding(text)
    self._cache[cache_key] = embedding
    RETURN embedding
```

## hybrid_search(query, collections, tenant_id, top_k, min_similarity)

```
FUNCTION hybrid_search(query, collections, tenant_id, top_k=5, min_similarity=0.7):
    query_embedding = embed(query)

    // Vector search (over-fetch 2x for merge headroom)
    vector_results = []
    FOR EACH collection IN collections:
        points = qdrant.search(collection, query_embedding,
            limit=top_k*2, score_threshold=min_similarity,
            filter={tenant_id: tenant_id})
        vector_results.extend(to_documents(points))
    SORT vector_results BY score DESC; TRIM to top_k*2

    // BM25 keyword search (stub in current impl)
    keyword_results = keyword_search(query, collections, tenant_id, top_k*2)

    merged = rrf_merge(vector_results, keyword_results, k=60)
    RETURN RAGResult(documents=merged[:top_k], scores, query_embedding)
```

## rrf_merge(vector_results, keyword_results, k)

```
FUNCTION rrf_merge(vector_results, keyword_results, k=60):
    scores = {}; docs = {}
    FOR rank, doc IN enumerate(vector_results):
        scores[doc.id] += 1.0 / (k + rank + 1)
        docs[doc.id] = doc
    FOR rank, doc IN enumerate(keyword_results):
        scores[doc.id] += 1.0 / (k + rank + 1)
        IF doc.id NOT IN docs: docs[doc.id] = doc
    RETURN docs sorted by scores DESC
// O(n+m). Docs in both lists get boosted RRF scores.
```

## chunk_document(text, chunk_size, overlap)

```
FUNCTION chunk_document(text, chunk_size=1000, overlap=200):
    IF len(text) <= chunk_size: RETURN [text]
    chunks = []; start = 0
    WHILE start < len(text):
        chunks.append(text[start : start+chunk_size])
        start += chunk_size - overlap
    RETURN chunks
// Example: 2500 chars -> chunks at [0:1000], [800:1800], [1600:2500]
```
