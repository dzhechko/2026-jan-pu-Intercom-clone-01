# Refinement: Orchestrator

## Edge Cases

### 1. Empty Message

- **Input:** `""` or `None`
- **Behavior:** `detect_intent` returns `"general_inquiry"` after stripping and lowercasing.
- **Test:** `test_empty_message` in test_orchestrator.py

### 2. Whitespace-Only Message

- **Input:** `"   \n\t  "`
- **Behavior:** After `.lower().strip()` becomes empty string, returns `"general_inquiry"`.
- **Test:** `test_whitespace_only` in test_orchestrator.py

### 3. Mixed Intents (Multiple Keywords Match)

- **Input:** `"Migrate VMware servers -- how much does migration cost?"`
- **Behavior:** Both `migration` and `cost_optimization` score hits. The intent with the
  highest keyword match count wins. If tied, `max()` returns the first one found.
- **Test:** `test_mixed_intent_highest_score` -- asserts result is one of the two valid intents.
- **Risk:** Tie-breaking is non-deterministic (dict ordering). Consider adding priority
  weights if this becomes a user-facing issue.

### 4. Unknown Intent (No Keywords Match)

- **Input:** `"Hello, tell me about Cloud.ru"`
- **Behavior:** No patterns match, returns `"general_inquiry"`, routed to `architect` agent.
- **Test:** `test_general_inquiry` in test_orchestrator.py

### 5. Escalation Trigger (Explicit Human Request)

- **Input:** `"I want to talk to a human"` / `"Позовите оператора"`
- **Behavior:** Escalation patterns are checked BEFORE intent patterns. Returns
  `"human_escalation"` immediately, even if other intent keywords are present.
- **Test:** `test_escalation_explicit_human`, `test_escalation_operator`,
  `test_escalation_specialist`

### 6. RAG Service Failure

- **Trigger:** Qdrant is unreachable or returns an error.
- **Behavior:** Exception caught in `process_message`, logged, `rag_result` set to `None`.
  Agent executes with empty document list. Response quality degrades but user is not blocked.

### 7. Lead Qualification Failure

- **Trigger:** Lead scoring service throws an exception.
- **Behavior:** Exception caught and logged. User response is already saved and returned.
  No impact on the user-facing flow.

### 8. Very Long Message

- **Input:** Message exceeding 4000 characters.
- **Behavior:** Currently no truncation in the orchestrator. Pydantic validation at the
  API layer should enforce the 4000-char limit before the message reaches the orchestrator.

## Testing Coverage

| Edge Case | Unit Test | Integration Test |
|-----------|:---------:|:----------------:|
| Empty message | yes | -- |
| Whitespace only | yes | -- |
| Mixed intents | yes | -- |
| Unknown intent | yes | -- |
| Escalation patterns | yes (3 tests) | -- |
| RAG failure | -- | needed |
| Lead qualification failure | -- | needed |
| Long message truncation | -- | needed |
