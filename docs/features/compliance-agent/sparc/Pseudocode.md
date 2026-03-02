# Pseudocode: Compliance Agent

## detect_compliance_intent()

From `src/orchestrator/intent.py` -- scores message against 10 regex patterns (`152.?фз`, `фстэк`, `кии`, `персональн.*данн`, `compliance`, `сертификац`, `аттестац`, `безопасност`, `регулятор`). Returns `("compliance_check", score)` where score = number of matched patterns. Highest-scoring intent across all categories wins.

## classify_requirement()

Determines which regulatory framework applies based on query content:

```python
def classify_requirement(message: str, rag_docs: list[Document]) -> ComplianceCategory:
    """Classify the compliance domain from user query + RAG context.

    Returns:
        category: "152_fz" | "fstec" | "kii" | "mixed"
        security_level: "UZ-1".."UZ-4" (for 152-FZ) or None
        applicable_orders: list of FSTEC order numbers
    """
    # Step 1: Extract regulation references from message
    has_152fz = re.search(r"152.?фз|персональн.*данн", message)
    has_fstec = re.search(r"фстэк|фстек|сертификац|аттестац", message)
    has_kii = re.search(r"кии|критическ.*информац.*инфраструктур", message)

    # Step 2: If multiple frameworks detected, return "mixed"
    matches = sum(bool(x) for x in [has_152fz, has_fstec, has_kii])
    if matches > 1:
        return ComplianceCategory(category="mixed")

    # Step 3: For 152-FZ, determine security level from data description
    if has_152fz:
        level = infer_security_level(message, rag_docs)
        return ComplianceCategory(category="152_fz", security_level=level)

    # Step 4: For FSTEC, identify applicable orders
    if has_fstec:
        orders = extract_fstec_orders(message, rag_docs)
        return ComplianceCategory(category="fstec", applicable_orders=orders)

    if has_kii:
        return ComplianceCategory(category="kii")

    return ComplianceCategory(category="general")
```

## generate_advisory()

Executed by `AgentExecutor.execute()` with the compliance system prompt:

```python
async def generate_advisory(agent, user_message, history, rag_documents) -> AgentResponse:
    """Generate compliance advisory. System prompt (prompts/compliance.md) instructs LLM to:
    1. Identify applicable regulations  2. State Cloud.ru compliance status
    3. List certifications              4. Recommend security level (UZ-1..4)
    5. Perform gap analysis             6. Cite documents with article numbers
    Constraints: no legal claims, cite 2+ sources, acknowledge limitations.
    """
    messages = build_prompt(agent.system_prompt, history, rag_documents, user_message)
    response = await llm_client.chat(messages, model=settings.llm_model)
    confidence = extract_confidence(response)
    sources = extract_citations(response)
    return AgentResponse(
        content=response.text, agent_type="compliance",
        confidence=confidence, sources=sources,
        should_escalate=(confidence < agent.confidence_threshold),  # < 0.6
    )
```
