# Rule: Log All Pipeline Routing Decisions Before Execution

## Maturity: 🔴 Alpha

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

## Rule

When a system routes work to different execution paths based on scoring, classification, or any decision logic, every routing decision must be logged BEFORE execution begins. The log entry must contain:

1. **Input identifier**: What is being routed (item name, ID, or description)
2. **Decision signals**: The raw inputs to the routing decision (scores, features, classifications)
3. **Computed result**: The final score or classification
4. **Selected path**: Which pipeline/branch/handler was chosen
5. **Timestamp**: When the decision was made
6. **Decision rule**: Which rule or threshold triggered the selection

Logging must occur before execution, not after, so that routing decisions are captured even when execution fails or hangs.

## Why

Without decision logging, misrouting is invisible. The work item enters the wrong pipeline, gets processed incorrectly, and the error is only discovered (if ever) when downstream results are wrong. By then, the routing decision is lost -- there is no record of why the item went where it did.

This creates several problems:
- **Silent misclassification**: Items processed by the wrong pipeline produce subtly wrong results that pass surface-level checks
- **Undebuggable failures**: When something goes wrong downstream, there is no way to trace back to the routing decision
- **No audit trail**: Cannot answer "why was this item handled this way?" after the fact
- **No calibration data**: Cannot improve routing logic without knowing what decisions were made and whether they were correct

## Example (what goes wrong)

A system routes feature requests to one of three pipelines based on a complexity score:

```
Feature "Add user profile page"
  → Complexity score computed internally
  → Routed to Pipeline A (simple)
  → Pipeline A produces a minimal implementation
  → QA finds the implementation missed 4 requirements
  → Investigation: "Why was this routed to the simple pipeline?"
  → No log exists. The complexity score, the signals that produced it,
    and the routing decision are all lost.
```

Root cause: the scoring function underweighted the number of API integrations, producing a score of 6 (simple) when the correct score was 9 (complex). But without the log, this can only be discovered by re-running the scoring, which may produce a different result if inputs have changed.

## Correct Approach

```
Feature "Add user profile page"
  → Log entry BEFORE routing:
    {
      "timestamp": "2026-03-02T14:30:00Z",
      "item": "Add user profile page",
      "signals": {
        "file_count": 5,
        "api_integrations": 3,
        "has_db_migration": true,
        "test_coverage_exists": false
      },
      "computed_score": 6,
      "selected_pipeline": "Pipeline A (simple)",
      "decision_rule": "score < 7 → Pipeline A"
    }
  → Routed to Pipeline A
  → QA finds issues
  → Investigation: read log → "score was 6 because api_integrations
    weight was 0.5, should have been 1.5"
  → Fix: adjust weight, re-test on historical data, deploy updated scoring
```

The log makes the routing decision transparent, debuggable, and auditable. It also provides calibration data: over time, you can compare routing decisions to outcomes and adjust thresholds.

Implementation requirements:
- [ ] Log entry written BEFORE execution begins (not after)
- [ ] Log includes all decision inputs, not just the final score
- [ ] Log is stored durably (not just stdout that gets truncated)
- [ ] Log format is structured (JSON, not free-form text) for automated analysis
- [ ] Log entries are queryable by item identifier and by time range

## Scope

Any system with multiple execution paths selected by automated decision logic:
- Work item triage and routing systems
- Feature pipeline selection
- Incident severity classification and escalation
- Content moderation pipelines
- A/B test assignment
- Load balancing with content-based routing
- Any scoring system that drives downstream behavior

Applies to both LLM-driven and traditional rule-based routing systems.

## Expiry

Review after 12 months. The principle of decision logging is durable and unlikely to expire. Log format and storage mechanisms may evolve.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction. Identified from incidents where silent misrouting went undetected due to absent decision logs, making root cause analysis impossible. |
