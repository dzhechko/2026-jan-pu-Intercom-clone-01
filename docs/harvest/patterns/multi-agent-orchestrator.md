# Pattern: Multi-Agent Orchestrator Pipeline

## Maturity: 🔴 Alpha
## Used in: ai-consultant-cloud-ru
## Extracted: 2026-03-02
## Version: v1.0

---

## Intent

Provide a unified entry point for systems with multiple specialized AI agents. A single orchestrator receives all incoming messages, detects the user's intent, selects the appropriate agent, enriches the context (e.g., via RAG), executes the LLM call through the selected agent, evaluates the response confidence, and decides whether to return the result or escalate to a human. This decouples agent specialization from routing logic.

## When to Use

- System has 3 or more specialized AI agents with distinct domains
- Users interact through a single channel (chat, API) and should not manually choose an agent
- Intent can shift mid-conversation (e.g., from technical question to pricing question)
- Response quality requires domain-specific context injection (RAG, tool calls)
- Confidence-based escalation to humans is needed

## When NOT to Use

- Single-purpose chatbot with one domain (no routing needed)
- User explicitly selects the agent/mode (manual dispatch suffices)
- All agents share the same prompt and tools (no specialization to route to)
- Latency budget cannot accommodate the orchestration overhead (intent detection + routing + context enrichment adds 200-500ms)

## Structure (pseudocode)

```
function orchestrate(user_message, conversation_history):
    # Step 1: Intent Detection
    intent = detect_intent(user_message, conversation_history)
    # Returns: {category: str, confidence: float, entities: dict}

    # Step 2: Agent Selection
    agent_config = select_agent(intent.category)
    # Returns: {name, system_prompt, tools, rag_collections}
    # Falls back to general agent if no match

    # Step 3: Context Enrichment
    rag_context = []
    for collection in agent_config.rag_collections:
        results = hybrid_search(collection, user_message)
        rag_context.extend(results)

    tool_results = []
    if agent_config.tools:
        tool_results = execute_relevant_tools(agent_config.tools, intent)

    # Step 4: LLM Execution
    prompt = build_prompt(
        system=agent_config.system_prompt,
        context=rag_context + tool_results,
        history=conversation_history,
        message=user_message
    )
    response = llm_call(prompt)

    # Step 5: Confidence Check
    if response.confidence < ESCALATION_THRESHOLD:
        return escalate_to_human(user_message, response, conversation_history)

    # Step 6: Return Response
    log_interaction(intent, agent_config.name, response)
    return response
```

## Implementation Variants

| Variant | Intent Detection | Trade-off |
|---------|-----------------|-----------|
| A - Regex/Rule-based | Pattern matching on keywords | Fast, predictable, but brittle with novel phrasing |
| B - LLM-based classification | LLM classifies intent from message | Flexible, handles novel queries, but adds latency and cost |
| C - Hybrid (rules + LLM) | Rules first for high-confidence matches, LLM fallback | Best of both: fast common path, smart edge cases |
| D - Embedding-based | Embed message, nearest-neighbor to intent exemplars | No LLM cost for routing, but requires curated exemplar set |

## Trade-offs

| Dimension | Benefit | Cost |
|-----------|---------|------|
| Modularity | Agents are independently deployable and configurable | Orchestrator becomes a coordination bottleneck |
| User experience | Single entry point, no manual agent selection | Misrouting causes confusing responses |
| Scalability | New agents added without changing routing code (if config-driven) | Intent detection must be updated for new categories |
| Observability | Central point for logging all interactions | Orchestrator logs become high-volume |
| Latency | Context enrichment improves response quality | Each pipeline step adds latency (typically 200-800ms total overhead) |

## Gotchas

1. **Intent detection accuracy is the ceiling** -- If the orchestrator misclassifies intent, the wrong agent responds. Monitor misrouting rates and invest in intent detection quality before optimizing anything else.

2. **Conversation context window management** -- Long conversations can exceed token limits. Implement a sliding window or summarization strategy for conversation history before injecting into the prompt.

3. **Agent overlap** -- When two agents cover adjacent domains (e.g., "infrastructure architecture" vs "migration planning"), ambiguous queries cause flickering between agents across turns. Define clear boundaries and add a "same agent preference" bias for follow-up messages.

4. **Cold start latency** -- First message in a conversation pays full pipeline cost (intent detection + RAG + LLM). Subsequent messages can cache intent and agent selection if the topic hasn't shifted.

5. **Fallback agent quality** -- The general/default agent that handles unmatched intents is often undertrained. Users hitting the fallback get the worst experience. Invest in making the fallback agent competent at basic tasks and clear about its limitations.

6. **Circular escalation** -- If the escalation handler itself triggers the orchestrator (e.g., human response re-enters the pipeline), you can get loops. Gate escalated conversations to bypass intent detection.

## Related Artifacts

- Pattern: Confidence-Triggered Human Escalation (Step 5 in the pipeline)
- Pattern: Hybrid RAG Search with RRF (Step 3 context enrichment)
- Pattern: Agent-as-Config (how agents are defined for Step 2)
- Pattern: LLM Fallback & Retry Strategy (Step 4 resilience)

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
