# Pattern: Confidence-Triggered Human Escalation

## Maturity: 🔴 Alpha
## Used in: ai-consultant-cloud-ru
## Extracted: 2026-03-02
## Version: v1.0

---

## Intent

Automatically detect when an AI agent's response is insufficiently reliable and hand off the conversation to a human operator with full context preserved. The escalation decision is driven by a numeric confidence score (0.0-1.0) attached to every agent response, combined with explicit trigger phrases from the user. This ensures high-stakes or ambiguous interactions always reach a qualified human rather than producing a low-quality AI response.

## When to Use

- Regulated domains where incorrect AI responses carry legal, financial, or safety risk
- Customer-facing AI systems where brand reputation depends on response quality
- High-stakes decision support (enterprise sales, medical triage, compliance advice)
- Systems where user trust calibration requires transparent "I don't know" behavior
- Any AI system with contractual SLAs on response accuracy

## When NOT to Use

- Internal tools where incorrect responses have low impact and users can self-correct
- Low-risk automation (content suggestions, formatting help, search)
- Systems without human operators available to receive escalations
- Batch processing pipelines with no real-time user interaction
- Prototypes or MVPs where escalation infrastructure is premature

## Structure (pseudocode)

```
CONFIDENCE_THRESHOLD = 0.6
ESCALATION_KEYWORDS = ["speak to human", "agent please", "help me", "real person"]

function evaluate_and_maybe_escalate(user_message, agent_response, conversation):
    # Check 1: Explicit user request
    if any(keyword in user_message.lower() for keyword in ESCALATION_KEYWORDS):
        return escalate(
            reason="user_requested",
            conversation=conversation,
            agent_response=agent_response
        )

    # Check 2: Confidence score below threshold
    if agent_response.confidence < CONFIDENCE_THRESHOLD:
        return escalate(
            reason="low_confidence",
            confidence=agent_response.confidence,
            conversation=conversation,
            agent_response=agent_response
        )

    # Check 3: Sensitive topic detection (optional)
    if detect_sensitive_topic(user_message):
        return escalate(
            reason="sensitive_topic",
            conversation=conversation,
            agent_response=agent_response
        )

    return agent_response

function escalate(reason, conversation, agent_response, **metadata):
    # Preserve full context for human operator
    escalation_record = {
        "conversation_id": conversation.id,
        "reason": reason,
        "full_history": conversation.messages,
        "last_ai_response": agent_response,  # human sees what AI would have said
        "metadata": metadata,
        "timestamp": now(),
        "status": "pending"
    }
    save_escalation(escalation_record)
    notify_human_operators(escalation_record)

    # Return holding message to user
    return Response(
        text="I want to make sure you get the best answer. "
             "Let me connect you with a specialist.",
        type="escalation",
        escalation_id=escalation_record.id
    )
```

## Implementation Variants

| Variant | Confidence Source | Trade-off |
|---------|------------------|-----------|
| A - LLM self-assessment | Ask the LLM to rate its own confidence | Simple, but LLMs are poorly calibrated (often overconfident) |
| B - RAG retrieval score | Use top retrieval similarity score as proxy | Grounded in evidence quality, but ignores reasoning quality |
| C - Ensemble scoring | Combine retrieval score + LLM self-assessment + topic classifier | Most accurate, but adds latency and complexity |
| D - Human feedback calibration | Train confidence model on historical human corrections | Best long-term accuracy, requires feedback loop infrastructure |

## Trade-offs

| Dimension | Benefit | Cost |
|-----------|---------|------|
| User safety | Prevents harmful or incorrect AI responses in critical moments | Some valid AI responses get unnecessarily escalated |
| Trust | Users learn the system knows its limits | Over-escalation frustrates users who wanted instant answers |
| Human workload | Only truly difficult queries reach humans | Threshold tuning is critical -- too low floods humans, too high lets bad answers through |
| Observability | Escalation logs become a gold mine for AI improvement | Requires escalation management infrastructure |
| Response time | Users get a fast "connecting you" rather than waiting for a bad answer | Human response time is orders of magnitude slower than AI |

## Gotchas

1. **LLM confidence is not probability** -- When an LLM says it is "80% confident," that number is not a calibrated probability. It is a token generated to satisfy the prompt. Treat self-assessed confidence as a relative signal, not an absolute measure. Calibrate thresholds empirically against human judgment.

2. **Threshold tuning requires data** -- The 0.6 threshold is a starting point, not a universal constant. Track escalation rates and human resolution outcomes to tune. Too many escalations (> 30%) means the threshold is too high or the agents need improvement.

3. **Context window for humans** -- Dumping the entire conversation history on a human operator is not helpful if the conversation is 50 messages long. Provide a summary view with the option to expand full history.

4. **Escalation queue management** -- Without SLA tracking on the human side, escalated conversations can sit unresolved for hours. Implement queue prioritization (by wait time, customer tier, topic urgency) and alerting for stale items.

5. **Re-entry after human resolution** -- After a human resolves the escalation, the conversation may return to the AI. The AI must be aware that a human intervened and what was resolved, to avoid re-asking the same question or contradicting the human.

6. **Keyword escalation gaming** -- Users may discover that certain phrases trigger human escalation and use them for every query to bypass the AI. Rate-limit explicit escalation requests or require a brief AI interaction before allowing escalation.

7. **Confidence score for multi-turn** -- A single message may have high confidence, but the overall conversation trajectory may be going off-track. Consider rolling confidence across the last N turns, not just the latest response.

## Related Artifacts

- Pattern: Multi-Agent Orchestrator Pipeline (escalation is the final step in orchestration)
- Pattern: LLM Fallback & Retry Strategy (escalation is the last resort after technical retries)
- Pattern: Non-Blocking Side Effects (escalation notifications are side effects of the main flow)

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
