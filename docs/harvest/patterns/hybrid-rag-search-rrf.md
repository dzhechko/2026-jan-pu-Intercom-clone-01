# Pattern: Hybrid RAG Search with Reciprocal Rank Fusion

## Maturity: 🔴 Alpha
## Used in: ai-consultant-cloud-ru
## Extracted: 2026-03-02
## Version: v1.0

---

## Intent

Improve retrieval quality in Retrieval-Augmented Generation (RAG) pipelines by combining two complementary search strategies -- dense vector similarity and sparse keyword matching (BM25) -- and merging their ranked results using Reciprocal Rank Fusion (RRF). Vector search captures semantic meaning; keyword search captures exact term matches. RRF merges without needing score normalization across fundamentally different scoring systems.

## When to Use

- Semantic search where keyword match alone misses contextual meaning
- Document corpus exceeds ~1,000 documents (enough for embedding quality to matter)
- Queries mix natural language phrasing with domain-specific terms or acronyms
- Retrieval feeds into an LLM context window (RAG) where precision matters
- Domain has both conceptual queries ("how to migrate a database") and exact lookups ("error code E-4021")

## When NOT to Use

- Exact match only is needed (e.g., ID lookups, SKU searches)
- Dataset is very small (< 1,000 documents) -- simple keyword search suffices
- Latency budget is extremely tight and two parallel searches are too expensive
- Corpus is highly structured/tabular -- SQL queries outperform free-text search
- No embedding model is available or feasible for the language/domain

## Structure (pseudocode)

```
function hybrid_search(query, top_k=10, rrf_k=60):
    # Phase 1: Parallel retrieval from two sources
    vector_results = vector_db.search(
        embedding=embed(query),
        limit=top_k * 3  # over-fetch for fusion
    )
    keyword_results = bm25_index.search(
        query=tokenize(query),
        limit=top_k * 3
    )

    # Phase 2: Build rank maps
    vector_ranks = {doc.id: rank for rank, doc in enumerate(vector_results, 1)}
    keyword_ranks = {doc.id: rank for rank, doc in enumerate(keyword_results, 1)}

    # Phase 3: Reciprocal Rank Fusion
    all_doc_ids = set(vector_ranks.keys()) | set(keyword_ranks.keys())
    fused_scores = {}
    for doc_id in all_doc_ids:
        score = 0.0
        if doc_id in vector_ranks:
            score += 1.0 / (rrf_k + vector_ranks[doc_id])
        if doc_id in keyword_ranks:
            score += 1.0 / (rrf_k + keyword_ranks[doc_id])
        fused_scores[doc_id] = score

    # Phase 4: Sort by fused score, return top_k
    ranked = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
```

## Implementation Variants

| Variant | Vector DB | Keyword Engine | Notes |
|---------|-----------|---------------|-------|
| A | Qdrant | In-memory BM25 (rank_bm25) | Lightweight, good for < 500K docs |
| B | Pinecone | Elasticsearch | Managed services, scales horizontally |
| C | FAISS | Whoosh | Fully local, no network dependencies |
| D | pgvector | PostgreSQL tsvector | Single-database approach, simpler ops |
| E | Weaviate (built-in hybrid) | Weaviate | Native hybrid search, no separate BM25 |

## Trade-offs

| Dimension | Benefit | Cost |
|-----------|---------|------|
| Retrieval quality | Captures both semantic and lexical matches | Two indices to maintain and keep in sync |
| Latency | Parallel execution keeps latency near single-source | Two queries per request (CPU/memory) |
| Score fusion | RRF is parameter-light (just k constant) | Loses absolute score information |
| Simplicity | No score normalization needed across systems | Additional infrastructure component |
| Relevance tuning | Can weight sources differently (weighted RRF) | Weights need empirical tuning per domain |

## Gotchas

1. **Index sync drift** -- If the vector index and BM25 index are updated independently, documents can appear in one but not the other. Use a single indexing pipeline that writes to both atomically, or accept eventual consistency with a reconciliation job.

2. **RRF k constant sensitivity** -- The default k=60 works well empirically, but highly skewed result sets (e.g., vector returns 1000 results, BM25 returns 5) can produce unexpected rankings. Test with your actual query distribution.

3. **Embedding model mismatch** -- If the embedding model was trained on a different domain than your corpus, vector search quality degrades silently. BM25 becomes the de facto primary retriever, and you lose the hybrid benefit. Validate embedding quality independently.

4. **Over-fetching ratio** -- The `top_k * 3` over-fetch multiplier is a heuristic. Too low and you miss good candidates from one source; too high and you pay latency/memory costs. Profile with representative queries.

5. **Chunk size alignment** -- Vector search and BM25 should operate on the same document chunks. If vector embeddings use 512-token chunks but BM25 indexes full documents, the rank fusion compares incompatible units.

6. **Empty result handling** -- If one source returns zero results (e.g., BM25 finds no keyword matches), RRF degrades gracefully to single-source ranking. This is correct behavior but should be logged for monitoring.

## Related Artifacts

- Pattern: Multi-Agent Orchestrator Pipeline (RAG search is typically a step within orchestration)
- Pattern: LLM Fallback & Retry Strategy (search failures need graceful degradation)
- Any document chunking/indexing pipeline that feeds the dual indices

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
