# Insight 001: /run → /go → /feature Pipeline Gaps

**Date:** 2026-03-02
**Severity:** Critical — affects all features built via /run
**Affected skills:** /run, /go, /feature, /plan

## Problem

When executing `/run all`, the pipeline collapsed to direct implementation without going through the proper `/go` → `/feature` lifecycle. All 5 v1.0 features were implemented as if they were trivial hotfixes rather than proper features.

## Root Causes

### 1. /run doesn't enforce /go invocation
**Location:** `.claude/commands/run.md` Step 2.3
**Issue:** `/run` says "Run `/go <feature-name>`" but this is just a text instruction. There's no enforcement mechanism — the LLM can (and did) skip straight to implementation.
**Fix needed:** /run should explicitly reference the /go decision matrix and require the LLM to output complexity scoring before proceeding.

### 2. /go scoring matrix boundary error
**Location:** `.claude/commands/go.md` Step 2
**Issue:** Score boundaries are ambiguous at exactly -2. The matrix says `≤ -2` → /plan and `-1 to +4` → /feature, but it's easy to misread -1 as "close to -2, so use /plan."
**Fix needed:** Add explicit examples: "Score -1 = /feature. Score -2 = /plan. Only truly trivial tasks (hotfixes, config-only) should reach ≤ -2."

### 3. /feature lifecycle phases are description-only
**Location:** `.claude/commands/feature.md`
**Issue:** The 4 phases (PLAN → IMPLEMENT → TEST → REVIEW) are described narratively but have no mandatory output artifacts. There's nothing that forces the LLM to actually produce SPARC docs, run validation, or invoke brutal-honesty-review.
**Fix needed:** Each phase should require a concrete output:
- Phase 1: MUST create `docs/features/{name}.md` with SPARC template
- Phase 2: MUST run validation and output score
- Phase 3: MUST produce code + tests
- Phase 4: MUST run review and output findings

### 4. docs/features/ vs docs/plans/ path confusion
**Location:** `.claude/commands/plan.md` says "Write plan to `docs/features/$FEATURE_NAME.md`"
**Issue:** There's no `docs/plans/` directory. Both /plan and /feature write to `docs/features/`. But /feature should produce richer output than /plan.
**Fix needed:** Either:
- (a) Keep single `docs/features/` but differentiate by content template (simple plan vs SPARC plan)
- (b) Use `docs/plans/` for /plan output and `docs/features/` for /feature output

### 5. Agent prompts scored too low
**Issue:** Migration Agent and AI Factory Agent scored -1 because "agent is config, not code" (-3). But creating an agent prompt + integrating it into the routing system IS meaningful work that benefits from /feature lifecycle (spec review, validation, testing).
**Fix needed:** Adjust scoring signals:
- "Agent is config, not code" should NOT be a -3 modifier. Remove this signal.
- Add: "Has system prompt > 30 lines" → +1 (nontrivial prompt design)
- Add: "Requires routing/orchestrator changes" → +1

### 6. /run's loop doesn't track which pipeline was used
**Issue:** /run's summary format includes `(via /plan)` or `(via /feature)` per feature, but there's no logging during execution. This made it easy to skip the pipeline without noticing.
**Fix needed:** /run should log the pipeline decision for each feature:
```
Feature: migration-agent
  Complexity score: -1
  Signals: ≤3 files (-2), agent config (-3, REMOVED), routing change (+2)
  Pipeline: /feature
  Starting Phase 1: PLAN...
```

## Impact

- 5 features implemented without validation phase
- 5 features have no requirements score (requirements-validator never ran)
- 5 features have no code review (brutal-honesty-review never ran)
- Feature plans are retroactive documentation, not pre-implementation planning
- No SPARC mini-docs generated per feature

## Recommendations for Skill Fixes

1. **`/run`**: Add explicit Step 2.3a: "BEFORE implementing, run /go scoring and log the result"
2. **`/go`**: Add mandatory complexity score output block with all signal values
3. **`/feature`**: Add checkpoint after each phase with required artifact check
4. **`/plan`**: Differentiate output from /feature Phase 1 output
5. **Scoring matrix**: Remove "agent is config" signal. Add "prompt complexity" signal.
6. **General**: Add a "pipeline audit" check that verifies docs/features/ has an entry for every done feature in roadmap
