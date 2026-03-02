# Architecture: Cost Calculator Agent

## Request Flow

```
User message ("Compare costs for 50 VMs...")
        |
        v
  +--------------+
  | Orchestrator  |  Intent: cost_optimization --> routes to cost_calculator
  +--------------+
        |
        v
  +--------------------+
  | Cost Calculator     |  1. Parse workload from message
  | Agent (LLM call)    |  2. Call Pricing MCP tool
  +--------------------+  3. Build comparison table
        |
   +----+----+
   |         |
   v         v
+--------+ +----------------+
| RAG    | | Pricing MCP    |
| Search | | Server         |
+--------+ +----------------+
   |              |
   v              v
+--------+ +----------------+
| Qdrant | | Pricing DB /   |
| pricing| | Cloud.ru API   |
| corpus | +----------------+
+--------+
        |
        v
  +--------------------+
  | TCO Comparison     |  Formatted table + recommendation
  | Response           |
  +--------------------+
        |
        v
  Lead qualification (extract_tco_data)
```

## Components

| Component | Location | Role |
|-----------|----------|------|
| Agent prompt | `prompts/cost_calculator.md` | Defines behavior, response format, constraints |
| Orchestrator | `src/orchestrator/` | Routes `cost_optimization` intent to this agent |
| RAG search | `src/rag/` | Retrieves pricing docs from `pricing` collection |
| Pricing MCP | `src/mcp/pricing/` | Live pricing lookup, SKU matching |
| Lead extraction | `src/services/lead_qualification.py` | `extract_tco_data()` saves TCO to lead |
| Tests | `tests/unit/test_tco.py` | Validates calculation logic |

## Data Flow

1. **Orchestrator** detects `cost_optimization` intent, loads cost_calculator agent config.
2. **RAG pipeline** queries `pricing` and `cloud_ru_docs` collections for pricing data.
3. **LLM call** receives system prompt + RAG context + conversation history.
4. **MCP tool calls**: LLM invokes `pricing.get_sku`, `pricing.get_discount` tools.
5. **TCO calculation**: Agent assembles compute + storage + network + managed costs per provider.
6. **Discounts applied**: Annual (10-20%) or 3-year (20-40%) based on period.
7. **Response**: Comparison table with recommendation, caveats, and sources.
8. **Post-processing**: `extract_tco_data()` captures TCO data into the lead record.

## Confidence and Escalation

- If RAG returns no pricing documents (score < `min_similarity` 0.7): agent notes data gap.
- If confidence < 0.6: escalate to human SA with partial TCO context.
- If pricing data is older than 30 days: add staleness disclaimer.
