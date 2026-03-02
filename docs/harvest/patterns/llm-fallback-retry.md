# Pattern: LLM Fallback & Retry Strategy

## Maturity: 🔴 Alpha
## Used in: ai-consultant-cloud-ru
## Extracted: 2026-03-02
## Version: v1.0

---

## Intent

Ensure reliable LLM-powered features in production by implementing a layered resilience strategy: primary model call with timeout, automatic retry with a fallback model on failure, and graceful degradation when all models fail. The system should never crash or hang due to an LLM provider outage. Every call is instrumented with response time tracking for observability and capacity planning.

## When to Use

- Any LLM-powered feature deployed in production with real users
- Systems where LLM provider outages should not cause user-visible failures
- Multi-model architectures where a cheaper/faster model can serve as backup
- Applications with response time SLAs (e.g., < 5 seconds for user-facing chat)
- Platforms where LLM costs vary and fallback models offer cost optimization during degraded mode

## When NOT to Use

- Batch processing pipelines where latency does not matter and retries are free
- Development/testing environments where you want failures to surface immediately
- Single-model systems with no alternative provider available
- Use cases where partial/degraded responses are worse than no response (e.g., medical diagnosis)

## Structure (pseudocode)

```
PRIMARY_MODEL = "claude-sonnet"
FALLBACK_MODEL = "alternative-model"
PRIMARY_TIMEOUT_MS = 30000
FALLBACK_TIMEOUT_MS = 45000
MAX_RETRIES = 2

function llm_call_with_fallback(messages, tools=None):
    start_time = now()

    # Attempt 1: Primary model
    for attempt in range(MAX_RETRIES):
        try:
            response = call_llm(
                model=PRIMARY_MODEL,
                messages=messages,
                tools=tools,
                timeout=PRIMARY_TIMEOUT_MS
            )
            track_metric("llm_call", {
                "model": PRIMARY_MODEL,
                "attempt": attempt + 1,
                "status": "success",
                "response_time_ms": elapsed(start_time)
            })
            return response

        except (TimeoutError, RateLimitError, ServerError) as e:
            track_metric("llm_call", {
                "model": PRIMARY_MODEL,
                "attempt": attempt + 1,
                "status": "error",
                "error_type": type(e).__name__,
                "response_time_ms": elapsed(start_time)
            })
            log.warning(f"Primary model attempt {attempt + 1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                wait(exponential_backoff(attempt))

    # Attempt 2: Fallback model
    try:
        log.info("Switching to fallback model")
        response = call_llm(
            model=FALLBACK_MODEL,
            messages=messages,
            tools=tools,
            timeout=FALLBACK_TIMEOUT_MS
        )
        track_metric("llm_call", {
            "model": FALLBACK_MODEL,
            "status": "success",
            "response_time_ms": elapsed(start_time),
            "is_fallback": True
        })
        response.metadata["used_fallback"] = True
        return response

    except Exception as e:
        log.error(f"Fallback model also failed: {e}")
        track_metric("llm_call", {
            "model": FALLBACK_MODEL,
            "status": "error",
            "error_type": type(e).__name__
        })

    # Attempt 3: Graceful degradation
    return GracefulDegradationResponse(
        text="I'm experiencing technical difficulties. Please try again "
             "in a moment, or I can connect you with a human specialist.",
        type="degraded",
        response_time_ms=elapsed(start_time)
    )
```

## Implementation Variants

| Variant | Strategy | Trade-off |
|---------|----------|-----------|
| A - Single fallback | Primary -> Fallback -> Degrade | Simple, covers most outage scenarios |
| B - Model chain | Primary -> Fallback 1 -> Fallback 2 -> Degrade | More resilient, but longer worst-case latency |
| C - Circuit breaker | Track failure rate; if > threshold, skip primary entirely for N minutes | Prevents hammering a failing provider, faster fallback activation |
| D - Active-active | Send to both models simultaneously, use first response | Lowest latency, but doubles cost |
| E - Hedged requests | Send to primary; if no response in P50 latency, also send to fallback | Balances latency and cost |

## Trade-offs

| Dimension | Benefit | Cost |
|-----------|---------|------|
| Availability | System stays responsive during provider outages | Fallback model may produce lower-quality responses |
| Latency | Timeouts prevent indefinite hangs | Retry + fallback adds latency in failure cases |
| Cost | Fallback model can be cheaper | Active-active/hedged variants double cost |
| Observability | Metrics reveal provider reliability and response time trends | Instrumentation adds code complexity |
| User experience | Users see a response instead of an error | Fallback response quality may differ noticeably |
| Complexity | Resilient to multiple failure modes | More code paths to test and maintain |

## Gotchas

1. **Fallback model capability mismatch** -- The fallback model may not support the same tools, function calling, or output formats as the primary. Test the full feature set against the fallback model, not just simple completions. Degrade features gracefully when the fallback lacks capabilities.

2. **Exponential backoff without jitter** -- Retrying with pure exponential backoff causes thundering herd problems when multiple instances retry simultaneously. Always add random jitter: `wait_time = base_delay * 2^attempt + random(0, base_delay)`.

3. **Timeout too generous** -- A 60-second timeout means a user waits 60 seconds before seeing a retry. Set primary timeouts aggressively (e.g., 2x the P95 latency) so failures are detected quickly. The fallback can have a more generous timeout.

4. **Silent quality degradation** -- When the system falls back to a cheaper model, response quality drops but no one notices if it is not monitored. Track `is_fallback` in metrics and alert when fallback usage exceeds a threshold (e.g., > 10% of requests).

5. **Circuit breaker state persistence** -- If the circuit breaker state is in-memory, each instance makes independent decisions. Use a shared store (Redis) for circuit breaker state so all instances switch to fallback simultaneously.

6. **Token limit differences** -- Primary and fallback models may have different context window sizes. A prompt that fits in the primary's 200K context may not fit in the fallback's 32K. Implement prompt truncation in the fallback path.

7. **Rate limit cascading** -- If the primary fails due to rate limiting, the fallback may also be rate-limited (especially if from the same provider). Diversify providers for primary and fallback models.

8. **Graceful degradation messaging** -- The degradation message should match the application's tone and offer a concrete next step (retry, contact support, escalate to human). "An error occurred" is not graceful degradation.

## Related Artifacts

- Pattern: Multi-Agent Orchestrator Pipeline (LLM calls happen within the orchestrator's execution step)
- Pattern: Confidence-Triggered Escalation (graceful degradation may trigger escalation to human)
- Pattern: Non-Blocking Side Effects (LLM call metrics tracking is a non-blocking side effect)

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
