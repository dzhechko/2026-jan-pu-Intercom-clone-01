# Architecture — Migration Agent

## Request Flow

```
User Message
  |
  v
Orchestrator.process_message()
  +--> detect_intent()  -- matches "migration" patterns (миграц, перенос, vmware...)
  +--> select_agent_type("migration") --> "migration"
  +--> get_agent_definition("migration") --> loads prompts/migration.md + config
  +--> RAGSearch.search()
  |      collections: ["{tenant_id}_migration_docs", "{tenant_id}_cloud_docs"]
  |      top_k: 5, hybrid search (vector + BM25 + RRF)
  +--> AgentExecutor.execute()
  |      system_prompt: prompts/migration.md
  |      rag_documents: migration guides, compatibility matrices
  |      conversation_history: previous messages
  |      tools: [rag_search, pricing_api, config_api]
  +--> Confidence check: >= 0.6 return plan, < 0.6 escalate
  v
Response (phased plan + timeline + rollback)
```

## Component Responsibilities

| Component | Role |
|-----------|------|
| `intent.py` | Detects migration intent via keyword patterns (RU + EN) |
| `router.py` | Orchestrates full pipeline (save, detect, RAG, execute, save) |
| `prompts/migration.md` | System prompt defining agent behavior and response format |
| `RAGSearch` | Retrieves Cloud.ru migration docs via hybrid search |
| `AgentExecutor` | Sends prompt + RAG context + history to Claude API |
| `pricing_api` (MCP) | Estimates target infrastructure costs |
| `config_api` (MCP) | Checks Cloud.ru service compatibility and limits |

## RAG Corpus Structure

```
corpus/migration/
  |- vmware-migration-guide.md       # VMware to Cloud.ru steps
  |- database-migration.md           # PostgreSQL, MySQL, Oracle migration
  |- kubernetes-migration.md         # K8s cluster migration
  |- storage-migration.md            # S3, block, file storage
  |- network-requirements.md         # VPN, peering, DNS setup
  |- compatibility-matrix.md         # OS/DB/middleware support
  |- migration-tools.md              # Cloud.ru migration toolkit
  |- rollback-procedures.md          # Standard rollback playbooks
```

## Conversation State

Migration agent persists state in `conversation.context` across turns:

```json
{
  "detected_intent": "migration",
  "migration_phase": "assess",
  "assessment": { "workloads": [], "compliance_flags": [] },
  "current_wave": 1
}
```

This enables multi-turn conversations where the agent tracks which
infrastructure has been discussed and which phase the user is in.

## Escalation Path

```
Migration Agent (confidence < 0.6)
  --> conversation.status = "escalated"
  --> Ticket with: transcript, assessment data, workload complexity
  --> Notification sent to SA pool
```
