# Rule: Use Checklists, Not Prose, for LLM Workflow Enforcement

## Maturity: 🔴 Alpha

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

## Rule

When defining multi-step workflows that will be executed by an LLM agent, express each required action as a checklist item with a concrete, verifiable artifact -- never as a prose paragraph describing what "should" happen.

Each checklist item must specify:
- The exact artifact to produce (filename, format)
- The pass/fail criterion (threshold, existence check, structural requirement)
- The action on failure (retry, escalate, abort)

## Why

LLMs process instructions probabilistically. Prose instructions like "make sure to validate the output" are treated as suggestions and are routinely skipped when the LLM optimizes for completion speed. Checklists with concrete artifacts create discrete verification points that the LLM can confirm or deny, making skipped steps detectable.

The failure mode is silent: the LLM reports success, the workflow appears to complete, but critical steps were never performed. This is only discovered downstream when defects surface.

## Example (what goes wrong)

Prose-based instruction in a workflow definition:

```
Phase 2: Validation
Make sure to validate the generated artifacts against the specification.
Check for completeness, correctness, and consistency. If issues are found,
address them before proceeding.
```

Result: The LLM reads this, generates a brief "Validation complete, no issues found" message, and moves to Phase 3. No validation was actually performed. Five features ship without validation. Defects discovered in production.

## Correct Approach

Checklist-based instruction in the same workflow:

```
Phase 2: Validation
- [ ] Run structural check: all required sections present in output
- [ ] Generate `validation-report.md` with section-by-section scoring
- [ ] Overall validation score > 70 in `validation-report.md`
- [ ] Zero critical findings (severity: critical) in report
- [ ] If score <= 70: log failure reason, retry generation (max 3 attempts)
- [ ] If 3 retries exhausted: abort pipeline, escalate to human review
```

Each item is independently verifiable. The existence of `validation-report.md` can be checked. The score threshold is unambiguous. Failure handling is explicit.

## Scope

Universal. Applies to any workflow where an LLM agent executes multi-step processes:
- Code generation pipelines
- Document generation workflows
- Evaluation and review pipelines
- Deployment checklists
- Data processing workflows

Not limited to any specific domain, language, or tool.

## Expiry

Review after 12 months or when LLM instruction-following fidelity demonstrably improves to the point where prose and checklists produce equivalent compliance rates.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction. Discovered when 5 features were built without validation due to prose-only workflow instructions. |
