# Pattern: Non-Blocking Side Effects

## Maturity: 🔴 Alpha
## Used in: ai-consultant-cloud-ru
## Extracted: 2026-03-02
## Version: v1.0

---

## Intent

Decouple the critical user-facing operation from optional downstream effects (CRM sync, lead scoring, analytics events, notification dispatch, audit logging) so that failures in side effects never block, delay, or degrade the primary response. The core operation completes and returns to the user first; side effects execute afterward with independent error handling. Failures in side effects are logged and can be retried, but are invisible to the end user.

## When to Use

- Any operation where the primary response to the user is independent of downstream processing
- Systems with integrations that have variable reliability (CRM APIs, analytics services, notification providers)
- Operations where side effect latency would unacceptably increase response time
- Event-driven architectures where the response and the reaction are logically separate
- High-throughput systems where side effect failures should not create backpressure on the main flow

## When NOT to Use

- Side effects are critical to the user flow (e.g., payment processing must complete before showing confirmation)
- Regulatory requirements mandate synchronous processing (e.g., audit log must be written before response)
- Side effects modify data that the user immediately reads (eventual consistency is not acceptable)
- The system has no mechanism for detecting or retrying failed side effects
- Debugging requires strict ordering of operations (side effects must be traceable to the triggering request)

## Structure (pseudocode)

```
function handle_user_message(message, conversation):
    # === CRITICAL PATH (blocking) ===
    response = orchestrator.process(message, conversation)
    save_message(conversation.id, message, response)

    # Return response to user immediately
    send_response_to_user(response)

    # === SIDE EFFECTS (non-blocking) ===
    fire_and_forget([
        lambda: sync_to_crm(conversation, message, response),
        lambda: update_lead_score(conversation),
        lambda: track_analytics_event("message_processed", {
            "conversation_id": conversation.id,
            "agent": response.agent_name,
            "confidence": response.confidence,
            "response_time_ms": response.response_time_ms
        }),
        lambda: check_escalation_triggers(conversation, response),
        lambda: update_conversation_summary(conversation)
    ])

function fire_and_forget(tasks):
    for task in tasks:
        try:
            # Execute asynchronously (thread pool, async task, message queue)
            execute_async(task)
        except Exception as e:
            # Log failure but do NOT propagate
            log.error(f"Side effect failed: {task.__name__}: {e}")
            track_metric("side_effect_failure", {
                "task": task.__name__,
                "error": str(e)
            })
            # Optionally enqueue for retry
            retry_queue.add(task, max_retries=3)

# --- Alternative: Async/Await Implementation ---

async function handle_user_message_async(message, conversation):
    # Critical path
    response = await orchestrator.process(message, conversation)
    await save_message(conversation.id, message, response)

    # Side effects - create tasks but don't await them
    asyncio.create_task(safe_execute(sync_to_crm, conversation, message, response))
    asyncio.create_task(safe_execute(update_lead_score, conversation))
    asyncio.create_task(safe_execute(track_analytics_event, "message_processed", {...}))

    return response

async function safe_execute(func, *args):
    try:
        await func(*args)
    except Exception as e:
        log.error(f"Side effect {func.__name__} failed: {e}")
```

## Implementation Variants

| Variant | Mechanism | Trade-off |
|---------|-----------|-----------|
| A - Try-catch wrapper | Wrap each side effect in try-catch, execute sequentially after response | Simplest, but side effects still add to request processing time |
| B - Async tasks (asyncio/threads) | Fire tasks on thread pool or event loop, don't await | Low latency, but no delivery guarantee |
| C - Message queue (Redis/RabbitMQ) | Publish events to queue, separate workers process | Reliable, retryable, but adds infrastructure |
| D - Event bus (in-process) | Publish domain events, registered handlers execute | Clean architecture, but in-process failures may be lost |
| E - Outbox pattern | Write side effect intent to DB, separate process reads and executes | Strongest guarantee (at-least-once), but highest complexity |

## Trade-offs

| Dimension | Benefit | Cost |
|-----------|---------|------|
| Response latency | User sees response immediately without waiting for side effects | Side effects complete later (eventual consistency) |
| Reliability | Side effect failures don't crash the main flow | Side effect failures may go unnoticed without monitoring |
| Simplicity (Variant A) | No additional infrastructure | Still sequential, adds some latency |
| Reliability (Variant C/E) | Guaranteed delivery with retry | Queue infrastructure to manage |
| Debugging | Main flow and side effects are independently debuggable | Correlation between request and side effect requires trace IDs |
| Resource usage | Side effects can be batched and processed efficiently | Async tasks consume thread/memory resources |

## Gotchas

1. **Lost side effects on crash** -- If the process crashes after sending the response but before side effects complete (Variants A, B, D), those side effects are lost. For critical side effects, use the outbox pattern (Variant E) or a message queue (Variant C) to ensure at-least-once execution.

2. **Context propagation** -- Async tasks may lose request context (tenant ID, user ID, trace ID, auth context). Explicitly capture and pass all necessary context when creating the async task. Do not rely on thread-local or request-scoped variables.

3. **Resource exhaustion** -- Firing many async tasks per request (e.g., 5 side effects per message in a high-traffic system) can exhaust thread pools or event loop capacity. Use bounded task pools and monitor queue depth.

4. **Retry storms** -- If a side effect fails due to a downstream outage and retries are configured, all failed tasks retry simultaneously when the service recovers. Implement exponential backoff with jitter on retry, and cap the retry queue size.

5. **Ordering assumptions** -- Side effects may complete in any order and at any time. If side effect B depends on side effect A having completed (e.g., lead scoring depends on CRM sync), you need explicit ordering or saga patterns, not fire-and-forget.

6. **Silent failure accumulation** -- If side effect failures are only logged (not alerted), they can accumulate unnoticed. Set up alerts on side effect failure rates. A CRM sync that has been failing for 3 days means 3 days of missing customer data.

7. **Testing difficulty** -- Non-blocking side effects are hard to test because they complete asynchronously. In tests, either make side effects synchronous (inject a synchronous executor) or use explicit await/flush mechanisms to ensure all side effects complete before assertions.

8. **Database connection exhaustion** -- If side effects open new database connections (especially in separate threads), the connection pool can be exhausted. Share the connection pool or use a dedicated pool for side effects with a lower limit.

## Related Artifacts

- Pattern: Multi-Agent Orchestrator Pipeline (side effects execute after the orchestrator returns a response)
- Pattern: Confidence-Triggered Escalation (escalation notification is a side effect)
- Pattern: LLM Fallback & Retry Strategy (metrics tracking for LLM calls is a non-blocking side effect)
- Pattern: Multi-Tenant Data Isolation (tenant context must propagate to side effect tasks)

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
