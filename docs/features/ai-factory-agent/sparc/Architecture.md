# Architecture -- AI Factory Agent

## Request Flow

```
User Message
  --> [Orchestrator] detect_intent(message) --> "gpu_ai"
  --> [select_agent_type("gpu_ai")] --> "ai_factory"
  --> [get_agent_definition("ai_factory")] --> loads prompts/ai_factory.md
  --> [RAG Search] collections: [{tenant}_gpu_docs, {tenant}_ml_pricing]
       hybrid search: vector + BM25 + RRF, top_k=5
  --> [AgentExecutor.execute()]
       system_prompt + conversation_history + rag_documents
       MCP tools: pricing_api, config_api
  --> [Claude API / GigaChat fallback]
  --> [AgentResponse] content, confidence, sources, should_escalate
  --> [Save to DB] Message(role="assistant", agent_type="ai_factory")
  --> [Lead Qualification Check] async, non-blocking
```

## Component Responsibilities

| Component | File | Role |
|-----------|------|------|
| Intent Detector | `src/orchestrator/intent.py` | Pattern-match `gpu_ai` from keywords |
| Router | `src/orchestrator/router.py` | Orchestrate full message pipeline |
| Agent Definition | `src/agents/base.py` | Load agent config (prompt, tools, RAG collections) |
| Agent Executor | `src/agents/executor.py` | Build LLM prompt, call Claude/GigaChat |
| RAG Search | `src/rag/search.py` | Hybrid search over Qdrant collections |
| Pricing MCP | `src/mcp/pricing.py` | Real-time GPU pricing lookup |
| Config MCP | `src/mcp/config.py` | GPU availability and quota checks |

## Data Model

```
Conversation (id, tenant_id, channel, status, context)
  +-- Message[] (role, agent_type="ai_factory", content, metadata_)
       metadata_: {confidence, sources, response_time_ms}
```

## Escalation Path

```
confidence < 0.6 --> conversation.status = "escalated"
  --> SA notification (Telegram/email)
  --> SA receives: transcript, intent, recommended config, cost data
```

## Key Design Decisions

1. **Agent is config, not code** -- `prompts/ai_factory.md` defines all behavior.
2. **RAG-first** -- GPU specs and pricing from indexed docs, not hardcoded tables.
3. **MCP for live data** -- `pricing_api` and `config_api` for real-time pricing/availability.
4. **Fallback chain** -- Claude (primary) -> GigaChat (fallback) for availability.
5. **Multi-tenant isolation** -- RAG collections namespaced by `tenant_id`.
