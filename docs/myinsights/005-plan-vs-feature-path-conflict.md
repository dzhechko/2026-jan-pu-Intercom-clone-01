# Insight 005: /plan and /feature Write to Same Directory (Path Conflict)

**Date:** 2026-03-02
**Severity:** High — causes filename/directory collision
**Affected skills:** /plan, /feature, cc-toolkit-generator-enhanced

## Problem

`/plan` wrote to `docs/features/$FEATURE_NAME.md` (flat file).
`/feature` Phase 1 creates `docs/features/<feature-name>/sparc/` (directory).

If you run `/plan user-auth` → creates `docs/features/user-auth.md`.
Then `/feature user-auth` tries to create `docs/features/user-auth/sparc/` — filesystem conflict.

## Root Cause

SKILL.md line 202 defines TWO output directories: `docs/features/, docs/plans/`
But `/plan` command was generated to write to `docs/features/` instead of `docs/plans/`.
No template exists for `/plan` in `references/templates/` — it was written ad-hoc.

## Fix Applied

- Changed `/plan` to write to `docs/plans/$FEATURE_NAME.md`
- Added explicit comment about path separation
- Created `docs/plans/` directory

## Recommendation for cc-toolkit-generator-enhanced

1. Add a `/plan` template to `references/templates/` (currently missing)
2. Template should specify `docs/plans/` as output path
3. Consider adding validation: if `/plan` output path overlaps with `/feature` output path → ERROR
