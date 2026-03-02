# Rule: Every Workflow Phase Must Have Verifiable Output Artifacts

## Maturity: 🔴 Alpha

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

## Rule

Every phase in a multi-step workflow must produce at least one concrete, verifiable output artifact. The artifact must be defined in the workflow specification with:
- An explicit filename or output location
- A structural or content-based acceptance criterion
- A gate condition: the next phase MUST NOT begin until the artifact exists and passes its criterion

Phases without mandatory artifacts are effectively optional and will be skipped.

## Why

LLMs (and humans under time pressure) optimize for completion. When a phase has no required output, the path of least resistance is to skip it entirely and proceed to the next phase. The absence of an artifact is invisible -- there is nothing to check, so nothing triggers a failure.

This is especially dangerous for validation, review, and planning phases, which produce understanding rather than code. Without a tangible artifact, these phases evaporate.

## Example (what goes wrong)

A four-phase workflow:

```
Phase 1: Plan the implementation
Phase 2: Validate the plan against requirements
Phase 3: Implement the feature
Phase 4: Test the feature
```

Phase 2 has no required artifact. The LLM generates the plan in Phase 1, immediately writes code in Phase 3, and produces test results in Phase 4. Phase 2 is acknowledged with "Plan validated" but no actual validation occurs. Requirements gaps discovered after deployment.

## Correct Approach

Define explicit artifacts for every phase:

```
Phase 1: Plan
  → Output: implementation-plan.md (must contain: scope, affected files, risk assessment)
  → Gate: file exists, all three sections present

Phase 2: Validate
  → Output: validation-report.md (must contain: requirement coverage matrix, score > 70)
  → Gate: file exists, score threshold met

Phase 3: Implement
  → Output: source files listed in implementation-plan.md, all modified
  → Gate: diff is non-empty for each listed file

Phase 4: Test
  → Output: test-results.json (must contain: pass rate, coverage percentage)
  → Gate: all tests pass, coverage >= threshold
```

Each phase has a named artifact and a gate condition. Skipping a phase means its artifact is missing, which blocks the next phase.

## Scope

Universal. Applies to any multi-phase workflow executed by LLM agents or automated pipelines:
- Software development lifecycles
- Document generation pipelines
- Evaluation and optimization loops
- Data processing pipelines
- Deployment workflows

The principle extends to human workflows but is critical for LLM-driven workflows where skipping is silent.

## Expiry

Review after 12 months. This rule addresses a fundamental property of sequential workflow execution and is unlikely to expire, but the specific artifact formats may evolve.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction. Identified from repeated observation that phases without artifacts are silently skipped by LLM agents. |
