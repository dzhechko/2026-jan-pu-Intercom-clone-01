# Insight 002: Phase 4 REVIEW Catches Real Issues

**Date:** 2026-03-02
**Severity:** Medium — validates the need for mandatory review phase
**Affected skills:** /feature

## Context

Re-ran all 5 v1.0 features through proper `/feature` lifecycle. Phase 4 (REVIEW) consistently found issues that would have been missed without it.

## Issues Found by Phase 4

| Feature | Issue | Type | Severity |
|---------|-------|------|----------|
| Migration Agent | Unused `import re` in `src/agents/base.py` | Lint (F401) | Low |
| ROI Analytics | Unused `from src.models.message import Message` in `dashboard.py` | Lint (F401) | Low |
| ROI Analytics | Duplicate `IRoiMetrics` interface in `RoiAnalyticsPage.tsx` instead of import from `types/index.ts` | Code duplication | Medium |
| Bitrix24 CRM | Unused `from src.models.message import Message` in `lead_qualification.py` | Lint (F401) | Low |
| Bitrix24 CRM | Import sorting issue in `test_crm.py` (I001) | Lint (I001) | Low |

## Issues Found by Phase 2 (VALIDATE)

| Feature | Issue | Type |
|---------|-------|------|
| ROI Analytics | `IRoiMetrics` defined in both `types/index.ts` and `RoiAnalyticsPage.tsx` | Type duplication |
| Bitrix24 CRM | `extract_architecture_summary` truncated to 500 chars, spec requires 1000 | Spec mismatch |

## Conclusion

- Phase 4 catches **5 lint/code quality issues** across 5 features
- Phase 2 catches **2 logic/spec issues** that would cause bugs or maintenance problems
- **Total: 7 issues** found by running proper lifecycle vs 0 issues found by skipping it
- The cost is ~2 minutes per feature for validation + review
- The value: spec compliance, no dead imports, no duplicated types

## Recommendation

Phase 4 REVIEW should be **mandatory** in `/feature`, not optional. It should:
1. Run `ruff check` on all modified files
2. Run `ruff format --check` on all modified files
3. Check for unused imports (F401)
4. Check for type/interface duplication across files
5. Verify spec compliance (test assertions match acceptance criteria numbers)

Phase 2 VALIDATE should:
1. Check each Gherkin scenario has corresponding implementation
2. Check numeric constants match spec (truncation limits, thresholds, rates)
3. Score ≥ 70/100 to proceed (current gate is correct)
