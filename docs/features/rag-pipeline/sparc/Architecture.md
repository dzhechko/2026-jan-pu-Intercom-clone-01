# Architecture: RAG Pipeline

## Component Diagram

```
  User Query -> Orchestrator -> RAGSearch (search.py)
                                    |
                       +------------+------------+
                       |                         |
                Vector Search            Keyword Search
                (Qdrant API)             (BM25 stub)
                       |                         |
                       +----+   +----------------+
                            |   |
                            v   v
                        RRF Merge (k=60)
                            |
                       top_k results -> RAGResult
```

## Indexing Flow

```
  Corpus Documents (corpus/)
       -> DocumentIndexer (indexer.py)
           -> _chunk_text() [1000 chars, 200 overlap]
               -> Embedder.embed_batch() [1536-dim vectors]
                   -> Qdrant Upsert (PointStruct)
```

## Integration with Orchestrator

1. Orchestrator receives a user message and selects an agent.
2. Agent config declares `rag_collections` (e.g., `["cloud_ru_docs", "pricing"]`).
3. Orchestrator calls `RAGSearch.search(query, collections, tenant_id)`.
4. `RAGResult.documents` are injected into the agent's LLM prompt as context.
5. Agent response includes `sources` extracted from RAG document metadata.

## Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Vector DB | Qdrant (self-hosted) | 152-FZ compliant, built-in BM25, multi-tenant |
| Embeddings | Pseudo (dev) / text-embedding-3-small (prod) | 1536-dim |
| Merge | Reciprocal Rank Fusion | No training, robust across retrieval methods |
| HTTP client | httpx (async) | Non-blocking embedding API calls |

## Multi-Tenancy

- Every Qdrant search includes `Filter(must=[FieldCondition(key="tenant_id", ...)])`.
- Collections can be shared (with tenant filter) or per-tenant (`{slug}_collection`).
- `DocumentIndexer` stamps `tenant_id` into every point payload at index time.
