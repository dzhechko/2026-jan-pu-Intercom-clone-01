# Specification: RAG Pipeline

## Data Model

### Embedding Vector

- Dimension: 1536 floats (matching text-embedding-3-small), normalized to [-1.0, 1.0]
- Deterministic pseudo-embedding fallback for dev (SHA-512/MD5 hash-based)
- In-memory cache keyed by MD5 hash of input text

### RAGDocument

```
RAGDocument:
  id: str                  # Qdrant point UUID
  content: str             # Chunk text (up to 1000 chars)
  title: str               # Source document title
  score: float             # Relevance score (vector sim or RRF)
  metadata: dict           # source_url, category, provider, chunk_index
```

### RAGResult

```
RAGResult:
  documents: list[RAGDocument]   # Ranked results after RRF merge
  scores: list[float]            # Parallel score array
  query_embedding: list[float]   # 1536-dim query vector (for caching)
```

### Qdrant Point Payload

```
  tenant_id: str           # Multi-tenant isolation filter
  title: str               # Document title
  content: str             # Chunk text
  chunk_index: int         # Position within source document
  total_chunks: int        # Total chunks from source document
  metadata: dict           # Arbitrary metadata (source_url, category)
```

## API Contract: Search

### Internal Interface (called by Orchestrator)

```
RAGSearch.search(
  query: str,              # User message text
  collections: list[str],  # Qdrant collection names (per agent config)
  tenant_id: str,          # Multi-tenant filter (required)
  top_k: int = 5,          # Number of results to return
  min_similarity: float = 0.7  # Vector similarity threshold
) -> RAGResult
```

### Internal Interface (called by Indexing Scripts)

```
DocumentIndexer.index_document(
  collection_name: str,    # Target Qdrant collection
  tenant_id: str,          # Owner tenant
  title: str,              # Document title
  content: str,            # Full document text (will be chunked)
  metadata: dict | None    # Optional metadata
) -> list[str]             # List of created Qdrant point IDs
```

## Qdrant Collection Config

- Vector size: 1536, distance: Cosine, created on demand via `ensure_collection()`
- Naming: `{tenant_slug}_{domain}` (e.g., `cloudru_cloud_docs`)
- Filter index on `tenant_id` for multi-tenant queries

## Chunking Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| CHUNK_SIZE | 1000 chars | Fits within LLM context alongside prompt |
| CHUNK_OVERLAP | 200 chars | Preserves context across chunk boundaries |
| Single-chunk threshold | <= 1000 chars | Short docs kept intact |
