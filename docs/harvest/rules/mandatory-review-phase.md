# Rule: Review Phase Must Be Mandatory, Not Optional

## Maturity: 🔴 Alpha

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

## Rule

In any multi-phase development or generation workflow, the review phase must be mandatory and enforced by a gate -- not suggested, recommended, or left as an optional step. Specifically:

1. The review phase must produce a review artifact (e.g., review report, findings log)
2. The workflow must not proceed to the next phase until the review artifact exists and meets acceptance criteria
3. Review must include both automated checks (linter, security scanner, format validator) AND a qualitative assessment (human or LLM-based)
4. "No findings" is a valid review outcome, but "review not performed" must block progression

## Why

When review is optional in an automated workflow, it is skipped 100% of the time. This is not an exaggeration -- it is an observed empirical fact. LLM agents optimize for forward progress and treat optional steps as unnecessary overhead. Humans under deadline pressure behave identically.

The cost of skipping review is deferred but real:
- Linting issues accumulate and become expensive to fix in bulk
- Security vulnerabilities ship to production
- Duplicate code proliferates when no one checks for existing implementations
- Architectural drift goes undetected until it causes systemic problems

Mandatory review with automated tooling catches 5-7 real issues per feature on average. These are not theoretical risks -- they are concrete defects (unused imports, SQL injection vectors, missing error handling, duplicated logic) that would otherwise reach production.

## Example (what goes wrong)

A workflow with an optional review step:

```
Phase 1: Plan       → implementation-plan.md ✓
Phase 2: Implement  → source code changes ✓
Phase 3: Review     → (optional, skipped under time pressure)
Phase 4: Test       → tests pass ✓
Phase 5: Deploy     → deployed ✓
```

Result: Code ships with 3 lint violations, 1 moderate security finding (unvalidated input passed to a shell command), and a function that duplicates existing utility code. Tests pass because they test the happy path and the security issue is in an error handler. Issues discovered 3 weeks later during an incident.

## Correct Approach

```
Phase 1: Plan       → implementation-plan.md ✓
Phase 2: Implement  → source code changes ✓
Phase 3: Review     → MANDATORY
  Step 3a: Automated checks (all must pass or be explicitly waived):
    - [ ] Linter: zero errors (warnings logged but not blocking)
    - [ ] Security scanner: zero high/critical findings
    - [ ] Format check: code matches project style
    - [ ] Dependency audit: no known vulnerabilities in new deps
  Step 3b: Qualitative review:
    - [ ] Code duplication check: no reimplementation of existing utilities
    - [ ] Architecture alignment: changes match documented patterns
    - [ ] Error handling: all new code paths have error handling
  Output: review-report.md (must exist, must list all findings and resolutions)
  Gate: Phase 4 blocked until review-report.md exists
Phase 4: Test       → tests pass ✓
Phase 5: Deploy     → deployed ✓
```

If automated checks find issues, the workflow loops back to Phase 2 for fixes before review can pass. This loop is bounded (max 3 retries before human escalation).

## Scope

Any multi-phase workflow that produces deliverable artifacts:
- Software development workflows (plan, implement, review, test, deploy)
- Document generation pipelines
- Configuration change workflows
- Infrastructure-as-code pipelines
- Content publication workflows

Applies to both human-driven and LLM-driven workflows. The enforcement mechanism differs (gate checks for LLMs, process controls for humans), but the principle is identical.

## Expiry

Review after 12 months. The principle of mandatory review is durable. Specific automated checks and tools may change as tooling evolves.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction. Based on observation that optional review phases were skipped in 100% of automated workflow executions, resulting in an average of 5-7 catchable issues per feature reaching production. |
