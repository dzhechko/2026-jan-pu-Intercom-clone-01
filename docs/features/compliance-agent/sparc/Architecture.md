# Architecture: Compliance Agent

## Flow Diagram

```
User Query (Telegram/Web)
    |
    v
[Orchestrator.process_message()]
    |
    v
[detect_intent()] ── regex patterns: 152.?фз, фстэк, кии, персональн.*данн,
    |                  compliance, сертификац, аттестац, безопасност, регулятор
    |
    v
intent = "compliance_check"
    |
    v
[select_agent_type()] ── maps to agent_type = "compliance"
    |
    v
[get_agent_definition("compliance")]
    |── loads prompts/compliance.md as system prompt
    |── returns AgentDefinition(confidence_threshold=0.6)
    |
    v
[RAG Search] ── queries tenant-scoped collections
    |── hybrid search: vector (Qdrant) + BM25
    |── Reciprocal Rank Fusion merge
    |── top_k=5 regulatory documents
    |
    v
[AgentExecutor.execute()]
    |── system_prompt = compliance.md content
    |── user_message = original query
    |── conversation_history = prior messages
    |── rag_documents = retrieved regulatory docs
    |── LLM call (Claude primary, GigaChat fallback)
    |
    v
[AgentResponse]
    |── content: structured advisory (regulations, certifications, gaps)
    |── confidence: float (< 0.6 triggers escalation)
    |── sources: list of cited regulatory documents
    |── should_escalate: bool
    |
    v
[Post-processing]
    |── Save Message(agent_type="compliance", metadata_={confidence, sources})
    |── If should_escalate: conversation.status = "escalated"
    |── check_lead_qualification() (async, non-blocking)
```

## Component Responsibilities

| Component | File | Role |
|-----------|------|------|
| Intent Detector | `src/orchestrator/intent.py` | Pattern-match compliance keywords (10 regex patterns) |
| Router | `src/orchestrator/router.py` | Orchestrate full pipeline: save -> detect -> RAG -> execute -> save |
| Agent Config | `prompts/compliance.md` | System prompt defining behavior, format, constraints |
| Agent Loader | `src/agents/base.py` | Load prompt file, build `AgentDefinition` |
| Executor | `src/agents/executor.py` | LLM call with prompt + RAG context |
| RAG Search | `src/rag/search.py` | Hybrid search over regulatory document corpus |

## RAG Corpus Requirements

The compliance agent depends on indexed regulatory documents in Qdrant:
- 152-FZ full text and amendments
- FSTEC orders (17, 21, 239) and guidance documents
- 187-FZ (KII) and subordinate regulations
- Cloud.ru certification documents and compliance matrices
- Security control mappings (Cloud.ru services to regulatory requirements)
