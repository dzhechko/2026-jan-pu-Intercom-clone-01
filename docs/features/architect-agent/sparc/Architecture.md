# Architecture: Architect Agent

## Request Flow

```
User Message (Telegram / Web Widget)
        |
        v
+------------------+
| Orchestrator     |  router.py: process_message()
|  1. Save message |
|  2. detect_intent() --> "architecture" / "migration" / ...
|  3. select_agent_type() --> "architect"
|  4. get_agent_definition("architect")
+------------------+
        |
        v
+------------------+
| RAG Search       |  rag/search.py: RAGSearch.search()
|  - Collection: {tenant_id}_cloud_docs
|  - Hybrid: vector + BM25 + RRF
|  - top_k=5 documents
+------------------+
        |
        v
+------------------+
| Agent Executor   |  agents/executor.py: AgentExecutor.execute()
|  1. _build_system_prompt(agent, rag_docs)
|     - Append RAG context to prompts/architect.md
|  2. _build_messages(history[-20:], user_msg)
|  3. Claude API call (anthropic.AsyncAnthropic)
|     - model: settings.llm_model
|     - max_tokens: 4096
|  4. _estimate_confidence(rag_docs, response)
+------------------+
        |
        v
+------------------+
| Post-processing  |  router.py (continued)
|  1. Save assistant message + metadata
|  2. If confidence < 0.6 --> set status="escalated"
|  3. check_lead_qualification() (non-blocking)
|  4. Return AgentResponse
+------------------+
```

## Key Components

| Component | File | Responsibility |
|-----------|------|----------------|
| Orchestrator | `src/orchestrator/router.py` | Pipeline coordinator: intent, agent, RAG, execute, persist |
| Intent Detector | `src/orchestrator/intent.py` | Classify user message into intent, map to agent type |
| Agent Definition | `src/agents/base.py` | Load prompt from `prompts/architect.md`, build `AgentDefinition` |
| Agent Executor | `src/agents/executor.py` | Build LLM payload, call Claude API, estimate confidence |
| RAG Search | `src/rag/search.py` | Hybrid retrieval from Qdrant collections |

## Confidence Estimation

```
confidence = min(1.0, avg_rag_score * 0.8 + reference_bonus + 0.2)
```

- `avg_rag_score`: mean of RAG document similarity scores
- `reference_bonus`: +0.1 if LLM response mentions RAG doc titles
- No RAG documents found: confidence defaults to 0.4

## Fault Tolerance

| Failure | Handling |
|---------|----------|
| Claude API timeout | Retry once with fallback model; confidence = 0.5 |
| Retry also fails | Return error message in Russian; confidence = 0.0; escalate |
| RAG search fails | Continue without RAG context (confidence will be lower) |
| Unknown exception | Log, return error message, escalate |

## Data Flow (Multi-tenant)

All queries scoped by `tenant_id`: RAG collection `{tenant_id}_cloud_docs`, DB queries filtered by conversation ownership, context persisted in `conversation.context` JSON column.
