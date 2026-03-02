# Insight 009: /go Scoring Audit — All 15 Features Retrospective

**Date:** 2026-03-02
**Severity:** Medium — audit-only, no broken functionality
**Affected commands:** /go (scoring matrix validation)

## Purpose

Retrospective audit of all 15 implemented features through the updated `/go` scoring matrix
(post-Insight 008 fixes). Validates that the new signals produce correct pipeline assignments.

## Scoring Matrix Used

Updated matrix from Insight 008:
- Removed: "agent is config, not code" (-3) — unfairly penalized agent features
- Added: "Has system prompt > 30 lines" (+1) — recognizes nontrivial prompt design
- Added: "Requires routing/orchestrator changes" (+1) — recognizes integration work
- Boundary examples added to prevent misclassification

## Results

| # | Feature | Score | Pipeline | Key Signals |
|---|---------|-------|----------|-------------|
| 1 | rag-pipeline | +5 | /feature | Qdrant API (+2), >2h (+3), DB entities (+2), ≤3 files (-2) |
| 2 | orchestrator | +2 | /feature | >2h (+3), Gherkin (+1), ≤3 files (-2) |
| 3 | architect-agent | +2 | /feature | Claude API (+2), prompt >30 lines (+1), routing (+1), ≤3 files (-2) |
| 4 | cost-calculator | +1 | /feature | prompt >30 lines (+1), routing (+1), Gherkin (+1), ≤3 files (-2) |
| 5 | compliance-agent | 0 | /feature | prompt >30 lines (+1), routing (+1), 1 file (-2) |
| 6 | human-escalation | +1 | /feature | prompt >30 lines (+1), routing (+1), Gherkin (+1), ≤3 files (-2) |
| 7 | telegram-bot | +1 | /feature | Telegram API (+2), Gherkin (+1), ≤3 files (-2) |
| 8 | api-endpoints | +7 | /feature | REST API (+2), DB entities (+2), >2h (+3), 4-10 files (0) |
| 9 | admin-dashboard | +8 | /feature | REST client (+2), >2h (+3), >10 files (+3) |
| 10 | lead-qualification | -3 | /plan | ≤3 files (-2), <30 min (-2), Gherkin (+1) |
| 11 | migration-agent | 0 | /feature | prompt 51 lines (+1), routing (+1), 1 file (-2) |
| 12 | ai-factory-agent | 0 | /feature | prompt 52 lines (+1), routing (+1), 1 file (-2) |
| 13 | web-chat-widget | +6 | /feature | REST API (+2), >2h (+3), Gherkin (+1), 4-10 files (0) |
| 14 | roi-analytics | +3 | /feature | Dashboard API (+2), Gherkin (+1), 4-10 files (0) |
| 15 | bitrix24-crm | +4 | /feature | Bitrix24 API (+2), >2h (+3), Gherkin (+1), ≤3 files (-2) |

## Distribution

- `/feature`: 14 features (score range: 0 to +8)
- `/plan`: 1 feature (lead-qualification, score -3)
- `/feature-ent`: 0 (no DDD docs in project — correct)

## Validation of Insight 008 Fixes

### Old matrix (with "agent is config" = -3):

| Feature | Old Score | Old Pipeline | New Score | New Pipeline | Changed? |
|---------|-----------|-------------|-----------|-------------|----------|
| compliance-agent | -3 | /plan | 0 | /feature | YES |
| migration-agent | -3 | /plan | 0 | /feature | YES |
| ai-factory-agent | -3 | /plan | 0 | /feature | YES |
| human-escalation | -2 | /plan | +1 | /feature | YES |
| architect-agent | -1 | /feature | +2 | /feature | no (same) |
| cost-calculator | -2 | /plan | +1 | /feature | YES |

**5 features changed pipeline** from /plan to /feature after removing the unfair signal.
This confirms that Insight 001 cause #5 ("agent prompts scored too low") was a real problem
affecting 5 out of 15 features.

## Key Takeaway

The scoring matrix now correctly routes all agent features through `/feature` lifecycle,
ensuring they get SPARC documentation, validation, and review. Only truly simple features
(single service file, <30 min) get /plan.

## Related
- [008: Pipeline discipline enforcement](008-pipeline-discipline-enforcement.md) — scoring matrix fixes
- [001: /run → /go → /feature pipeline gaps](001-run-go-feature-pipeline-gaps.md) — original root cause #5
