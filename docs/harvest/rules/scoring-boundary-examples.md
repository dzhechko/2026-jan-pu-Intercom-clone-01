# Rule: Scoring Matrices Must Include Boundary Examples

## Maturity: 🔴 Alpha

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

## Rule

Every scoring matrix or classification system must include concrete examples at each decision boundary -- the points where an input could plausibly be classified into either of two adjacent categories. Abstract threshold definitions are insufficient. Boundary examples must:

1. Show a real or realistic input that falls just above the threshold
2. Show a real or realistic input that falls just below the threshold
3. Explain WHY the boundary example belongs in its assigned category (not the adjacent one)
4. Be tested retrospectively against known, previously-classified samples before deployment

## Why

Scoring thresholds without boundary examples are ambiguous. When a human or LLM evaluator encounters an input near a threshold, they must make a judgment call with no guidance. Different evaluators will classify the same input differently, producing inconsistent results.

This is especially problematic in automated pipelines where routing decisions depend on scores. A misclassification at a boundary sends work down the wrong pipeline, and the error is invisible until downstream failures surface.

LLMs are particularly susceptible: they interpret vague thresholds optimistically, default to the "nicer" classification, and lack the domain intuition that a human might use to resolve ambiguity.

## Example (what goes wrong)

A scoring matrix for routing work items:

```
Score >= 7:  Pipeline A (fast track, automated)
Score 4-6:   Pipeline B (standard, with review)
Score < 4:   Pipeline C (manual handling)
```

An item scores 6.8. Is it Pipeline A or Pipeline B? The matrix says B (score < 7), but the evaluator rounds up to 7 and routes to A. Another item scores 4.1 with characteristics that clearly need manual handling, but the score puts it in Pipeline B.

Without boundary examples, the evaluator has no reference for what a "6 vs 7" or a "3 vs 4" looks like in practice. Misrouting occurs silently.

## Correct Approach

```
Score >= 7:  Pipeline A (fast track, automated)
  Boundary example (7, Pipeline A):
    Input: "Feature request with complete spec, existing test coverage, single file change"
    Why A: Fully specified, low risk, automated tests cover the change

  Boundary example (6, NOT Pipeline A):
    Input: "Feature request with complete spec but touches 3 modules with no existing tests"
    Why NOT A: Cross-module impact and no test coverage require human review → Pipeline B

Score 4-6:   Pipeline B (standard, with review)
  Boundary example (4, Pipeline B):
    Input: "Bug report with reproduction steps, affects non-critical path"
    Why B: Reproducible but needs investigation, standard review sufficient

  Boundary example (3, NOT Pipeline B):
    Input: "Bug report with no reproduction steps, affects authentication flow"
    Why NOT B: Critical path + no repro = needs manual triage → Pipeline C

Score < 4:   Pipeline C (manual handling)
```

Before deployment, test the matrix retrospectively:
- Take 20-50 previously classified items with known correct classifications
- Run them through the scoring matrix
- Check: does the matrix produce the same classification as the known-correct one?
- If misclassification rate > 10%, revise the thresholds or boundary examples

## Scope

Any system that classifies, routes, or scores inputs:
- Work item triage systems
- Lead qualification scoring
- Content quality evaluation
- Risk assessment matrices
- Priority classification systems
- Automated routing pipelines

Applies to both human-evaluated and LLM-evaluated scoring systems. Especially critical when scoring drives automated routing decisions.

## Expiry

Review after 12 months. The principle of boundary examples is durable, but specific threshold values and examples need updating as the domain evolves and new edge cases are discovered.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction. Identified from misclassification events where ambiguous thresholds caused silent misrouting in automated pipelines. |
