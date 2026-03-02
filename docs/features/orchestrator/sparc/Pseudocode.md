# Pseudocode: Orchestrator

## Algorithm: detect_intent(message, context)

```
INPUT:  message (string), context (dict | None)
OUTPUT: intent (string)

1. message_lower = message.lower().strip()

2. FOR pattern IN ESCALATION_PATTERNS:
     IF regex_search(pattern, message_lower):
       RETURN "human_escalation"

3. IF message_lower is empty:
     RETURN "general_inquiry"

4. scores = {}
   FOR intent, patterns IN INTENT_PATTERNS:
     score = COUNT(p for p in patterns IF regex_search(p, message_lower))
     IF score > 0:
       scores[intent] = score

5. IF scores is empty:
     RETURN "general_inquiry"

6. RETURN intent with MAX score
```

**Complexity:** O(P) where P = total number of regex patterns across all intents.

## Algorithm: select_agent_type(intent)

```
INPUT:  intent (string)
OUTPUT: agent_type (string)

1. mapping = {
     "migration"        -> "migration",
     "new_deployment"   -> "architect",
     "cost_optimization"-> "cost_calculator",
     "compliance_check" -> "compliance",
     "gpu_ai"           -> "ai_factory",
     "human_escalation" -> "human_escalation",
     "general_inquiry"  -> "architect"
   }

2. RETURN mapping.get(intent, "architect")
```

**Complexity:** O(1) dictionary lookup.

## Algorithm: Orchestrator.process_message(conversation, user_message)

```
INPUT:  conversation (Conversation), user_message (string)
OUTPUT: AgentResponse

1.  start_time = now()
2.  SAVE Message(role="user", content=user_message) to DB
3.  intent = detect_intent(user_message, conversation.context)
4.  UPDATE conversation.context.detected_intent = intent
5.  agent_type = select_agent_type(intent)
6.  agent = load_agent_definition(agent_type)
7.  TRY: rag_result = rag_search(user_message, agent.rag_collections)
    CATCH: rag_result = None  (log error, continue)
8.  history = SELECT messages WHERE conversation_id ORDER BY created_at
9.  response = agent_executor.execute(agent, user_message, history, rag_docs)
10. elapsed_ms = (now() - start_time) * 1000
11. SAVE Message(role="assistant", content=response.content, metadata={confidence, sources, elapsed_ms})
12. IF response.should_escalate:
      conversation.status = "escalated"
13. TRY: check_lead_qualification(conversation)
    CATCH: log error, continue
14. RETURN response
```

**Complexity:** O(H + R) where H = conversation history length, R = RAG search time.
