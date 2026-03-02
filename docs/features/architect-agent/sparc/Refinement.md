# Refinement: Architect Agent

## Edge Cases

### 1. LLM Timeout

**Trigger:** Claude API does not respond within timeout window.

**Current handling** (`executor.py` lines 79-103):
- Catch `anthropic.APITimeoutError`
- Retry once using `settings.llm_fallback_model` (e.g., GigaChat)
- If retry succeeds: return response with `confidence=0.5` (degraded)
- If retry fails: return Russian error message, `confidence=0.0`, `should_escalate=True`

**Test case:** Mock `APITimeoutError` on first call, verify fallback model is used, verify confidence is 0.5.

### 2. Low Confidence / No RAG Results

**Trigger:** RAG search returns no relevant documents, or average RAG score is low.

**Current handling:**
- No RAG docs: `_estimate_confidence()` returns 0.4 (below 0.6 threshold)
- Low RAG scores: confidence formula `avg_score * 0.8 + 0.2` may fall below 0.6
- Below threshold: `should_escalate=True`, conversation status set to `"escalated"`

**Test case:** Pass empty `rag_documents`, verify confidence=0.4, verify escalation triggered.

### 3. FPGA / Custom Workload (Out-of-domain)

**Trigger:** User describes specialized hardware (FPGA, custom ASICs, bare-metal GPU clusters) not covered in Cloud.ru documentation.

**Expected behavior:**
- RAG search returns low-relevance or no documents
- Confidence drops below 0.6
- Agent acknowledges limitation per prompt constraint: "If confidence is low (<0.6), acknowledge limitations honestly"
- Escalation to human Solution Architect with full conversation context

**Test case:** Send FPGA workload description, verify low confidence, verify escalation with context preserved in `conversation.context`.

### 4. Follow-up Context Maintenance

**Trigger:** User asks follow-up ("What about Kubernetes instead?") after receiving an architecture recommendation.

**Current handling:**
- `_build_messages()` includes last 20 messages from conversation history
- `detect_intent()` receives `conversation.context` with previous `detected_intent`
- Agent sees full prior exchange and can adjust recommendation

**Risk:** If conversation exceeds 20 messages, early context is lost (sliding window).

**Test case:** Build a 25-message history, verify only last 20 are sent to LLM, verify first 5 are dropped.

### 5. Message Truncation

**Trigger:** User sends message exceeding 4000 characters.

**Current handling** (`executor.py` lines 40-44):
- Truncate to 4000 chars
- Append notice: "[Message was shortened to 4000 characters]"

**Test case:** Send 5000-char message, verify truncation, verify notice appended.

### 6. RAG Search Failure

**Trigger:** Qdrant service is unreachable or returns an error.

**Current handling** (`router.py` lines 58-60):
- Catch all exceptions from `rag.search()`
- Log error, set `rag_result = None`
- Continue execution with empty RAG docs (agent runs without knowledge base context)
- Confidence will be 0.4, likely triggering escalation

**Test case:** Mock RAG search to raise `ConnectionError`, verify agent still responds, verify low confidence.
