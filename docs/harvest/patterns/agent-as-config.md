# Pattern: Agent-as-Config (Prompt-Driven Agents)

## Maturity: 🔴 Alpha
## Used in: ai-consultant-cloud-ru
## Extracted: 2026-03-02
## Version: v1.0

---

## Intent

Define AI agents as declarative configuration files rather than imperative code. Each agent is specified by a system prompt (markdown or YAML), a list of available tools, and a set of RAG document collections. Adding, modifying, or removing an agent requires editing a config file, not writing or modifying application code. The runtime engine reads the config at request time and constructs the appropriate LLM call. This separates agent behavior (what the agent knows and can do) from agent infrastructure (how the agent executes).

## When to Use

- Multi-agent systems where most agent differentiation is in the prompt and context, not in procedural logic
- Teams where domain experts (non-developers) need to author or tune agent behavior
- Systems that need rapid agent iteration without code deployments
- Platforms where agents are added frequently (new domains, new use cases)
- Any system where agent behavior is primarily "respond to a query using context and tools"

## When NOT to Use

- Agents with complex procedural logic (multi-step workflows, state machines, conditional branching that cannot be expressed in a prompt)
- Agents that require custom code for each action (e.g., programmatic API integrations with complex error handling)
- Systems with a single agent that never changes
- Environments where config file access is as restricted as code access (no ops benefit)

## Structure (pseudocode)

```
# --- Agent Config File (e.g., agents/architect.yaml) ---

name: architect
display_name: "Solution Architect"
description: "Designs infrastructure solutions based on requirements"
system_prompt_file: "prompts/architect.md"  # or inline
tools:
  - pricing_calculator
  - resource_estimator
  - compliance_checker
rag_collections:
  - infrastructure_docs
  - best_practices
  - case_studies
parameters:
  temperature: 0.3
  max_tokens: 2000
fallback_agent: general

# --- Runtime Agent Loader ---

function load_agent(agent_name):
    config = read_yaml(f"agents/{agent_name}.yaml")
    system_prompt = read_file(config.system_prompt_file)
    tools = [load_tool(t) for t in config.tools]
    rag_collections = config.rag_collections
    return AgentInstance(
        name=config.name,
        system_prompt=system_prompt,
        tools=tools,
        rag_collections=rag_collections,
        parameters=config.parameters
    )

function execute_agent(agent, user_message, context):
    # Retrieve relevant documents from agent's RAG collections
    rag_context = []
    for collection in agent.rag_collections:
        rag_context.extend(search(collection, user_message))

    # Build the prompt
    messages = [
        {"role": "system", "content": agent.system_prompt},
        {"role": "system", "content": format_rag_context(rag_context)},
        *context.conversation_history,
        {"role": "user", "content": user_message}
    ]

    # Execute LLM call with agent's parameters
    response = llm_call(
        messages=messages,
        tools=agent.tools,
        temperature=agent.parameters.temperature,
        max_tokens=agent.parameters.max_tokens
    )
    return response

# --- Adding a New Agent ---
# 1. Create agents/new_domain.yaml
# 2. Write prompts/new_domain.md
# 3. (Optional) Register new tools if needed
# 4. No code changes. Restart or hot-reload picks up the new agent.
```

## Implementation Variants

| Variant | Config Format | Trade-off |
|---------|--------------|-----------|
| A - YAML files | YAML config + markdown prompts | Human-readable, easy to diff in version control |
| B - Database records | Agent configs stored in DB | Supports runtime editing via admin UI, harder to version |
| C - JSON with schema validation | JSON files validated against JSON Schema | Strict typing, IDE support, less human-friendly |
| D - Python dataclasses | Config-as-code with dataclasses | Type-safe, IDE autocomplete, but requires dev to edit |
| E - Hybrid (DB + file override) | DB for runtime config, files for defaults | Flexible, but two sources of truth to reconcile |

## Trade-offs

| Dimension | Benefit | Cost |
|-----------|---------|------|
| Speed of iteration | New agent in minutes, not hours | Complex agent behaviors may fight the config-only constraint |
| Accessibility | Non-developers can author/tune agents | Config errors may be harder to debug than code errors |
| Testability | Agent configs can be unit-tested (load + validate) | Prompt behavior testing requires LLM-in-the-loop tests |
| Versioning | Config files diff cleanly in git | Prompt changes may have non-obvious behavioral impacts |
| Deployment | Agent changes without code deployment (if hot-reload) | Hot-reload introduces consistency risks during transitions |
| Standardization | All agents follow the same execution pattern | Agents that need custom execution paths require escape hatches |

## Gotchas

1. **Prompt drift** -- When prompts are easy to edit, they get edited frequently. Without version control discipline, you lose track of which prompt version produced which behavior. Always version prompts in git and tag releases.

2. **Tool registration gap** -- Adding a tool name to an agent config does nothing if the tool is not registered in the runtime. Validate at startup that all referenced tools exist, and fail fast with a clear error.

3. **Config validation** -- A missing field or typo in a YAML file can cause silent failures. Implement strict schema validation on config load. Fail loudly at startup, not at request time.

4. **Prompt injection via config** -- If agent configs are editable via an admin UI, the system prompt field becomes an injection vector. Validate and sanitize config inputs, especially if non-admin users can edit agent definitions.

5. **RAG collection lifecycle** -- An agent config may reference a RAG collection that has not been indexed yet (or has been deleted). The loader should verify collection existence at startup or gracefully handle missing collections at query time.

6. **Testing prompt changes** -- Unlike code changes that can be unit-tested, prompt changes require behavioral testing (send sample queries, evaluate responses). Build a prompt regression test suite: a set of (input, expected_behavior) pairs that run against each prompt version.

7. **The escape hatch problem** -- Eventually, one agent will need custom logic that does not fit the config pattern (e.g., a multi-step workflow with conditional branching). Design the escape hatch from day one: allow a config field like `custom_executor: "path.to.module"` that overrides the default execution path for specific agents.

## Related Artifacts

- Pattern: Multi-Agent Orchestrator Pipeline (orchestrator loads and routes to config-defined agents)
- Pattern: Confidence-Triggered Escalation (confidence thresholds can be per-agent config)
- Pattern: Hybrid RAG Search with RRF (RAG collections referenced in agent configs)

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
