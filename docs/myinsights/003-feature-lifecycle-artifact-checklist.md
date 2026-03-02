# Insight 003: /feature Needs Mandatory Artifact Checklist Per Phase

**Date:** 2026-03-02
**Severity:** High — structural gap in feature lifecycle
**Affected skills:** /feature, /feature-ent

## Problem

The `/feature` command describes 4 phases narratively but doesn't enforce concrete outputs. An LLM following the command can "complete" each phase without producing any artifacts.

## Proposed Mandatory Artifacts Per Phase

### Phase 1: PLAN
- [ ] `docs/features/{name}.md` created with SPARC template
- [ ] User story written
- [ ] Acceptance criteria in Gherkin format
- [ ] Architecture references listed
- [ ] Complexity score calculated with all signals shown
- [ ] Files to create/modify listed
- [ ] Edge cases documented
- [ ] Phase Tracking section added (all 4 phases listed)

### Phase 2: VALIDATE
- [ ] Each Gherkin scenario checked against implementation plan
- [ ] Score output: `N/100` with breakdown
- [ ] Any discrepancies listed and fixed
- [ ] Phase Tracking updated: `[x] Phase 2: VALIDATE — score N/100 (details)`

### Phase 3: IMPLEMENT
- [ ] All planned files created/modified
- [ ] Tests written and passing
- [ ] Test count reported: `N tests passing`
- [ ] Phase Tracking updated: `[x] Phase 3: IMPLEMENT — N tests passing, lint clean`

### Phase 4: REVIEW
- [ ] `ruff check` passed on all modified files
- [ ] Unused imports removed
- [ ] No type/interface duplication
- [ ] Security review (no hardcoded secrets, no SQL injection, proper input validation)
- [ ] Phase Tracking updated: `[x] Phase 4: REVIEW — N fixes (details)`

## Why This Matters

Without mandatory artifacts, the LLM takes the path of least resistance:
- Phase 1 becomes "I'll figure it out as I code"
- Phase 2 becomes "looks good to me"
- Phase 3 is the only phase that actually produces work
- Phase 4 becomes "done!"

With mandatory artifacts, each phase has a verifiable checkpoint that both the LLM and the user can audit.

## Evidence

In the original `/run all` execution, **zero** of these artifacts were produced for any of the 5 features. When re-run with proper lifecycle, each feature produced all artifacts and 7 real issues were found.
