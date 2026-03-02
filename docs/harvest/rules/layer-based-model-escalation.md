# Rule: Use Cheapest Model First, Escalate Only When Insufficient

## Maturity: 🔴 Alpha

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

## Rule

Structure multi-model AI pipelines as a sequence of escalating layers. Always start with the cheapest, fastest model. Escalate to a more expensive model only when the current layer's task exceeds the cheaper model's capabilities. Never escalate if the current layer fails -- reject and retry at the same layer first.

Layer structure:
- **Layer 0** (structural checks): Cheapest model. Pattern-matching, format validation, completeness checks. No reasoning required.
- **Layer 1** (semantic baseline): Cheap model. Coherence scan, relevance check, basic factual consistency. Fast pass/fail.
- **Layer 2** (deep evaluation): Mid-tier model. Nuanced reasoning, domain-specific judgment, quality scoring with rubrics.
- **Layer 3** (creative synthesis): Most expensive model. Novel combinations, cross-domain reasoning, creative optimization. Applied only to top-N candidates that passed all lower layers.

## Why

Cost scales nonlinearly with model capability. Running every artifact through the most powerful model is wasteful when 60-80% of artifacts fail basic structural checks that a cheap model can detect in milliseconds.

The layered approach provides:
1. **Cost efficiency**: Most rejections happen at Layer 0/1 (cheapest). Only high-quality candidates reach expensive layers.
2. **Speed**: Cheap models respond faster, so failures are caught sooner.
3. **Resource allocation**: Expensive model capacity is reserved for tasks that genuinely require it.
4. **Clear failure attribution**: Each layer has a defined scope, making it easy to diagnose why an artifact was rejected.

## Example (what goes wrong)

A pipeline sends every generated artifact directly to the most expensive model for evaluation:

```
Input: 100 generated artifacts
Step 1: Expensive model evaluates all 100 → $50 cost, 20 minutes
Result: 70 rejected for basic structural issues (missing sections, empty placeholders)
```

70% of the cost was wasted on artifacts that a cheap model could have rejected in seconds for pennies. The expensive model spent its capacity on pattern-matching that required no reasoning.

Worse: when a Layer 0 check fails and the system escalates to a more expensive model hoping for a different result, it gets the same rejection at 10x the cost.

## Correct Approach

```
Input: 100 generated artifacts

Layer 0 (cheapest model):
  - Check: required sections present, no empty placeholders, length within bounds
  - Result: 30 rejected (structural failures)
  - Cost: $0.50, Time: 30 seconds

Layer 1 (cheap model):
  - Check: coherence, relevance, basic factual consistency
  - Result: 20 rejected (incoherent or off-topic)
  - Cost: $1.00, Time: 1 minute

Layer 2 (mid-tier model):
  - Check: domain accuracy, quality scoring, nuanced evaluation
  - Result: 35 scored below threshold
  - Cost: $5.00, Time: 5 minutes

Layer 3 (expensive model):
  - Check: creative synthesis, cross-pollination of top candidates
  - Input: only the top 15 candidates
  - Cost: $3.00, Time: 3 minutes

Total: $9.50 instead of $50.00. Same quality outcome.
```

Critical rules:
- Never promote an artifact to a higher layer if the current layer's gate fails
- Layer 0 may auto-retry generation up to 3 times before escalating to human review
- Escalation means "this task needs more capability," NOT "retry the same check with a bigger model"

## Scope

Any multi-model AI pipeline where tasks vary in complexity:
- Document evaluation pipelines
- Content generation with quality gates
- Code review automation
- Multi-stage data processing
- Prompt optimization loops

Applicable wherever multiple model tiers are available (e.g., small/medium/large models from any provider).

## Expiry

Review after 12 months or when model pricing structures change significantly enough to invalidate the cost ratios. The principle of "cheapest sufficient model first" is durable; the specific layer assignments may need updating as model capabilities shift.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction. Derived from cost optimization analysis of evaluation pipelines where uniform use of expensive models wasted 70%+ of budget on trivially rejectable artifacts. |
