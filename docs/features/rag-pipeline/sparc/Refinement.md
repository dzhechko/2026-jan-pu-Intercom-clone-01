# Refinement: RAG Pipeline

## Edge Cases

### 1. Empty or Whitespace Query

**Trigger:** User sends `""`, `" "`, or `"\n\t"`.
**Current behavior:** Embedder hashes the empty/whitespace string, producing a valid but meaningless vector. Search returns arbitrary low-score results.
**Required fix:** Validate query at `RAGSearch.search()` entry. Return empty `RAGResult` immediately if `query.strip()` is empty. Log a warning.

### 2. Qdrant Service Unavailable

**Trigger:** Qdrant container is down, network partition, or connection timeout.
**Current behavior:** `_vector_search` catches the exception per-collection and logs it, returning partial results. If all collections fail, returns empty list.
**Validation:** This is correct -- the orchestrator should still function (with degraded quality) when RAG is unavailable. Ensure the agent's LLM prompt handles the "no RAG context available" case gracefully.

### 3. Very Long Document (>100K chars)

**Trigger:** Indexing a large PDF or documentation dump.
**Risk:** `_chunk_text` produces hundreds of chunks. `embed_batch` calls `embed()` sequentially, causing slow indexing. Memory pressure from storing all embeddings before upsert.
**Mitigation:** Add batch upsert with configurable batch size (e.g., 50 chunks per upsert call). Consider async embedding with concurrency limit. Log a warning if chunk count exceeds 100.

### 4. No Results Found (All Below Threshold)

**Trigger:** Query has no semantic match in the corpus, or `min_similarity=0.7` filters everything.
**Current behavior:** Returns empty `RAGResult(documents=[], scores=[], ...)`.
**Impact:** The orchestrator builds an LLM prompt with no RAG context. The agent may hallucinate.
**Mitigation:** When results are empty, the orchestrator should inject a system message: "No relevant documentation found. Acknowledge the gap rather than guessing." This is handled at the orchestrator level (error code RAG_002).

### 5. Duplicate Documents Across Collections

**Trigger:** Same document indexed in both `cloud_ru_docs` and `pricing` collections.
**Current behavior:** `_vector_search` iterates collections independently, so duplicates appear in results with separate Qdrant point IDs.
**Impact:** RRF merge treats them as distinct documents, wasting top_k slots.
**Mitigation:** Deduplicate by content hash or title before RRF merge. Not yet implemented.

### 6. Embedding Cache Unbounded Growth

**Trigger:** High query volume over time. `_cache` dict in `Embedder` grows without limit.
**Risk:** Memory exhaustion on long-running processes.
**Mitigation:** Replace dict cache with an LRU cache (bounded size) or use Redis for embedding cache with TTL. The `get_embedder()` singleton persists for process lifetime.

### 7. Chunk Boundary Splits a Key Term

**Trigger:** A critical keyword or phrase falls exactly on the `chunk_size` boundary and is split across two chunks.
**Current behavior:** The 200-char overlap partially mitigates this, but does not guarantee whole-word boundaries.
**Mitigation:** Enhance `_chunk_text` to prefer splitting at sentence or paragraph boundaries when possible. Overlap of 200 chars provides reasonable coverage for most cases.

## Test Coverage Gaps

| Scenario | Status | Priority |
|----------|--------|----------|
| `embed()` async with cache hit/miss | Not tested (requires async test) | High |
| `search()` end-to-end with mocked Qdrant | Not tested | High |
| `index_document()` with mocked Qdrant | Not tested | Medium |
| RRF merge with large input (100+ docs) | Not tested | Low |
| Concurrent `embed()` calls (race condition on cache) | Not tested | Medium |
