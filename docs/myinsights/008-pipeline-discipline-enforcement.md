# Insight 008: Pipeline Discipline Enforcement — /go, /run, /feature hardened

**Date:** 2026-03-02
**Severity:** Critical — closes all 6 root causes from Insight 001 + Insight 003
**Affected commands:** /go, /run, /feature

## Problem

Insights 001 and 003 identified that the `/run → /go → /feature` pipeline had no enforcement mechanisms:
- `/run` could skip `/go` scoring entirely (Insight 001, cause 1)
- `/go` scoring matrix had ambiguous boundaries and unfair signals (Insight 001, causes 2+5)
- `/feature` phases had no mandatory artifact checklists — LLM skipped validation and review (Insight 003)
- `/run` didn't log which pipeline was selected per feature (Insight 001, cause 6)

Combined effect: 5 v1.0 features were implemented without validation, review, or SPARC documentation.

## Fixes Applied

### /go — Scoring matrix overhaul

1. **Removed "agent is config, not code" signal** (-3 penalty)
   - Root cause: agent features like Migration Agent scored -1 and fell into /plan instead of /feature
   - Creating agent prompts + integrating into routing IS meaningful work
2. **Added new signals:**
   - "Has system prompt > 30 lines" → +1 (nontrivial prompt design)
   - "Requires routing/orchestrator changes" → +1 (touches core logic)
3. **Added boundary examples** to prevent misclassification:
   - Score -3: hotfix → /plan
   - Score -2: single-file config → /plan
   - Score -1: agent + routing → /feature (NOT /plan)
   - Score 0: standard feature → /feature
   - Score +5: multi-service → /feature-ent
4. **MANDATORY scoring output block** — must be printed before Step 3:
   ```
   COMPLEXITY SCORING: <feature-name>
     Signal: <signal> = <score>
     ...
     Total score: <N>
     Pipeline selected: /plan | /feature | /feature-ent
   ```

### /run — Enforce /go invocation

1. **CRITICAL guard** at Step 2: "Every feature MUST go through /go — never skip to direct implementation"
2. **Scoring block validation**: "IF /go's scoring block is missing → STOP and re-run /go"
3. **pipeline_log** array tracks `{feature, score, pipeline, status}` for every feature
4. **Summary report** now includes per-feature pipeline decisions:
   ```
   Pipeline decisions (from /go scoring):
     feature-1  score: 3 → /feature
     feature-2  score: -3 → /plan
   ```

### /feature — Mandatory artifact checklists

Added `[ ]` checklists that MUST be satisfied before proceeding to next phase:

| Phase | Checklist items | Key artifacts |
|-------|----------------|---------------|
| Phase 1: PLAN | 9 items | SPARC directory, PRD with Gherkin, Phase Tracking section |
| Phase 2: VALIDATE | 5 items | Validation score N/100, discrepancies fixed, validation-report.md |
| Phase 3: IMPLEMENT | 5 items | Tests passing, lint clean, test count reported |
| Phase 4: REVIEW | 6 items | Security review, unused imports, review-report.md |

Added **Phase Tracking template** for PRD.md:
```markdown
## Phase Tracking
- [ ] Phase 1: PLAN — SPARC docs created, N files planned
- [ ] Phase 2: VALIDATE — score N/100, N gaps fixed
- [ ] Phase 3: IMPLEMENT — N tests passing, lint clean
- [ ] Phase 4: REVIEW — N issues found, N fixed
```

Added explicit guard: "do NOT proceed if artifacts missing" with reference to Insight 003.

## Root Causes Closed

| Insight 001 Cause | Description | Fix |
|-------------------|-------------|-----|
| 1 | /run doesn't enforce /go | CRITICAL guard + scoring block validation |
| 2 | /go boundary ambiguity | Boundary examples + explicit score ranges |
| 3 | /feature phases description-only | Mandatory artifact checklists (25 items) |
| 4 | /plan path conflict | Fixed in earlier commit (docs/plans/) |
| 5 | Agent prompts scored too low | Removed -3 signal, added +1 signals |
| 6 | /run doesn't log pipeline | pipeline_log + summary report |

| Insight 003 | Description | Fix |
|-------------|-------------|-----|
| All | No mandatory outputs per phase | 9+5+5+6 checklist items + Phase Tracking |

## Prevention

- **For cc-toolkit-generator-enhanced**: When generating /go, /run, /feature — copy enforcement blocks verbatim from templates. Do not simplify.
- **For future audits**: Check that every MUST/MANDATORY keyword in a command has a corresponding verification step.
- **Pattern**: "Narrative instructions" ≠ "enforcement". LLMs follow checklists more reliably than prose descriptions.

## Related
- [001: /run → /go → /feature pipeline gaps](001-run-go-feature-pipeline-gaps.md) — original 6 root causes
- [003: /feature needs mandatory artifact checklist](003-feature-lifecycle-artifact-checklist.md) — original proposal
- [002: Phase 4 REVIEW catches real issues](002-feature-review-phase-value.md) — evidence that enforcement works
