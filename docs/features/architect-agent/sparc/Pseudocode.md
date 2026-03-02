# Pseudocode: Architect Agent

## Orchestrator.process_message()

```
async process_message(conversation, user_message):     # router.py
    save Message(role="user", content=user_message)
    intent = detect_intent(user_message, conversation.context)
    agent_type = select_agent_type(intent)              # --> "architect"
    agent = get_agent_definition(agent_type)
    rag_docs = await rag.search(query=user_message, collections=["{tenant}_cloud_docs"], top_k=5)
    history = load last messages for conversation
    response = await executor.execute(agent, user_message, history, rag_docs)
    save Message(role="assistant", content=response.content, metadata={confidence, sources})
    if response.should_escalate: conversation.status = "escalated"
    await check_lead_qualification(conversation)
    return response
```

## AgentExecutor.execute()

Source: `src/agents/executor.py`

```
async execute(agent, user_message, conversation_history, rag_documents):
    if len(user_message) > 4000:
        user_message = truncate to 4000 chars + append notice

    system_prompt = build_system_prompt(agent, rag_documents)
    messages = build_messages(conversation_history, user_message)

    try:
        response = await claude_api.messages.create(model, max_tokens=4096, system_prompt, messages)
        confidence = estimate_confidence(rag_documents, response.text)
        should_escalate = confidence < agent.confidence_threshold  # 0.6
        return AgentResponse(content, confidence, agent_type, sources, should_escalate)
    except APITimeoutError:
        retry with fallback_model, confidence=0.5
        if retry fails: return error message, confidence=0.0, escalate=True
    except Exception:
        return error message, confidence=0.0, escalate=True
```

## build_system_prompt()

```
build_system_prompt(agent, rag_documents):
    prompt = agent.system_prompt           # contents of prompts/architect.md

    if rag_documents:
        for i, doc in enumerate(rag_documents):
            append "[Source i: doc.title]\n{doc.content}"
        prompt += "\n\n## Context from knowledge base\n\n" + joined_sources

    return prompt
```

## build_messages()

```
build_messages(conversation_history, user_message):
    recent = conversation_history[-20:]    # sliding window of last 20 messages
    messages = [{"role": m.role, "content": m.content} for m in recent]
    messages.append({"role": "user", "content": user_message})
    return messages
```

## estimate_confidence()

```
estimate_confidence(rag_documents, response_text):
    if no rag_documents: return 0.4
    avg_score = mean(doc.score for doc in rag_documents)
    reference_bonus = 0.1 if any doc.title found in response_text else 0.0
    return min(1.0, avg_score * 0.8 + reference_bonus + 0.2)
```
