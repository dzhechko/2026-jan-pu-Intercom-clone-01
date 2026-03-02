# Specification: Architect Agent

## Agent Config Model

Defined in `src/agents/base.py` as `AgentDefinition`:

```python
@dataclass
class AgentDefinition:
    agent_type: str              # "architect"
    name: str                    # "Architect"
    description: str             # First paragraph from prompt file
    system_prompt: str           # Full contents of prompts/architect.md
    rag_collections: list[str]   # Default: ["{tenant_id}_cloud_docs"]
    tools: list[str]             # ["rag_search", "pricing_api", "config_api"]
    confidence_threshold: float  # 0.6 -- below triggers escalation
    max_turns: int               # 20
```

Loading: `get_agent_definition("architect")` reads `prompts/architect.md` and parses it via `parse_agent_config()`.

## System Prompt Structure (`prompts/architect.md`)

| Section | Purpose |
|---------|---------|
| Header | Role definition: "expert cloud architect specializing in Cloud.ru" |
| Behavior | Rules: ask 2-3 clarifying questions, reference Cloud.ru services, include sizing, cite sources |
| Response Format | 5-step structure: acknowledge, clarify, recommend, size, cite |
| Available Tools | `rag_search`, `pricing_api`, `config_api` |
| Constraints | No hallucination, low confidence acknowledgment, respond in user's language |

## Tool Definitions

| Tool | Description | Usage |
|------|-------------|-------|
| `rag_search` | Search Cloud.ru documentation corpus via hybrid search (vector + BM25 + RRF) | Retrieve service specs, architecture patterns, best practices |
| `pricing_api` | MCP server for current Cloud.ru pricing | Get compute/storage/network costs for sizing |
| `config_api` | MCP server for service configuration details | Fetch VM flavors, storage tiers, network options |

## RAG Collections

Default collection pattern: `{tenant_id}_cloud_docs`. Search parameters:
- `top_k=5` documents returned
- Hybrid search: Qdrant vector similarity + BM25 keyword matching
- Reciprocal Rank Fusion (RRF) for result merging

## Response Schema

```python
@dataclass
class AgentResponse:
    content: str           # LLM-generated architecture recommendation
    confidence: float      # 0.0-1.0, computed from RAG scores + source references
    agent_type: str        # "architect"
    sources: list[dict]    # [{"title": ..., "url": ...}] from RAG documents
    should_escalate: bool  # True when confidence < 0.6
```
