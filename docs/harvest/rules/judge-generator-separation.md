# Rule: Generator and Evaluator Models Must Be Different

## Maturity: 🔴 Alpha

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

## Rule

Never use the same LLM model instance for both generating an artifact AND evaluating that artifact. The generator and evaluator must be different models, different model versions, or -- at minimum -- isolated instances with different system prompts and no shared context.

This is a hard constraint, not a recommendation. Violations must be blocked at the pipeline configuration level, not merely discouraged.

## Why

Self-evaluation by the same model that generated an artifact produces systematically inflated scores and circular validation. The model recognizes its own patterns, finds its own outputs coherent (because they match its internal priors), and lacks the adversarial distance needed for genuine critique.

This creates a false sense of quality: artifacts score highly, pass evaluation gates, and reach production with defects that an independent evaluator would have caught.

The effect is amplified in optimization loops, where the generator learns to produce outputs that score well on its own evaluation criteria rather than outputs that are genuinely high quality.

## Example (what goes wrong)

A pipeline uses the same model (e.g., `sonnet`) for both generation and evaluation:

```
Step 1: sonnet generates a technical document
Step 2: sonnet evaluates the document on a 1-10 rubric
Result: Score 8.7 / 10
```

The score is meaningless. The model finds its own writing style coherent, its own structure familiar, and its own vocabulary appropriate. It does not notice missing sections, logical gaps, or domain inaccuracies because it would not have produced them differently.

When all judges in a panel use the same model, scores converge to near-identical high values (conformity collapse), and the evaluation provides no signal.

## Correct Approach

Separate the generator and evaluator:

```
Step 1: Model A generates the artifact
Step 2: Model B evaluates the artifact (different model family or version)
```

For panel-based evaluation:
- Use multiple distinct models or distinct prompting strategies
- Ensure judges operate in isolation (no access to each other's scores)
- Use an odd number of judges (3 or 5) to enable majority voting
- Set a disagreement threshold: if max - min score > 3 points, escalate to a meta-judge

Example panel configuration:
```
Generator:     Model A (e.g., creative/generative model)
Judge 1:       Model B — Domain Expert (weight: 0.4)
Judge 2:       Model C — Adversarial Critic (weight: 0.3)
Judge 3:       Model B — Completeness Auditor (weight: 0.3, different prompt)
Meta-judge:    Model C — activated only on disagreement
```

The key constraint: the generator model must not appear as a judge with the same prompt configuration.

## Scope

Any AI pipeline where artifacts are both generated and evaluated:
- Content generation with quality scoring
- Code generation with automated review
- Prompt optimization loops
- Multi-agent evaluation workflows
- Automated grading systems

Not limited to any specific model provider, domain, or artifact type.

## Expiry

Review after 12 months or when empirical evidence demonstrates that self-evaluation bias has been eliminated in a specific model family (unlikely in the near term).

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction. Identified as a critical anti-pattern in evaluation pipelines where score inflation masked quality issues. |
