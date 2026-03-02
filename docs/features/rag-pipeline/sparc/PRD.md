# PRD: RAG Pipeline

## Feature Overview

Hybrid Retrieval-Augmented Generation pipeline that provides contextual document retrieval for all 6 specialized agents. Combines vector similarity search (Qdrant) with BM25 keyword matching, merged via Reciprocal Rank Fusion (RRF), to surface the most relevant Cloud.ru documentation chunks in response to user queries.

## User Story

```
As an Enterprise CTO consulting via Telegram or web widget,
I want the AI agents to ground their answers in actual Cloud.ru documentation,
So that I receive accurate, cited recommendations instead of hallucinated information.
```

## Acceptance Criteria

```gherkin
Feature: RAG Pipeline Hybrid Search

  Scenario: Successful document retrieval
    Given the Qdrant collection contains indexed Cloud.ru documentation
    When a user asks "Does Cloud.ru support Kubernetes?"
    Then the RAG pipeline returns top-5 relevant document chunks
    And each chunk includes a title, content, and relevance score
    And retrieval completes within 2 seconds (p50)

  Scenario: Empty query handling
    Given a user sends an empty or whitespace-only message
    When the orchestrator invokes RAG search
    Then the pipeline returns an empty result set without errors

  Scenario: Qdrant unavailable
    Given the Qdrant service is unreachable
    When a search is attempted
    Then the error is logged and an empty result is returned gracefully

  Scenario: Document indexing with chunking
    Given a 5000-character Cloud.ru documentation page
    When the document is indexed
    Then it is split into overlapping 1000-char chunks (200-char overlap)
    And each chunk is embedded and stored with tenant_id metadata
```

## Files

| File | Purpose |
|------|---------|
| `src/rag/embedder.py` | Text embedding generation (1536-dim vectors) |
| `src/rag/search.py` | Hybrid search: vector + BM25 + RRF merge |
| `src/rag/indexer.py` | Document chunking, embedding, and Qdrant upsert |
| `tests/unit/test_rag.py` | Unit tests for embedder, RRF merge, chunking |

## Phase Tracking

- [x] Phase 1: PLAN -- SPARC docs created, 3 files (embedder, search, indexer)
- [x] Phase 2: VALIDATE — code matches SPARC docs
- [x] Phase 3: IMPLEMENT — 138 tests passing, lint clean
- [x] Phase 4: REVIEW — 22 ruff issues fixed, all clean
