# Insight 004: /feature Command Doesn't Match Its Own Template

**Date:** 2026-03-02
**Severity:** Critical — renders feature lifecycle ineffective
**Affected skills:** cc-toolkit-generator-enhanced (Phase 3 generation), /feature command

## Problem

The `/feature` command (`.claude/commands/feature.md`) was generated as a simplified 5-step text instead of using the template from `references/templates/feature-lifecycle.md`.

Meanwhile, the rule `feature-lifecycle.md` was generated **correctly** from the same template.

## Evidence

### Template specifies (Section 2: Command Template):
- Phase 0: Pre-flight check (6 skills verification)
- Phase 1: PLAN → `docs/features/<name>/sparc/` → 9 SPARC files via sparc-prd-mini
- Phase 2: VALIDATE → requirements-validator swarm (5 validators) → score ≥70
- Phase 3: IMPLEMENT → swarm agents from SPARC docs
- Phase 4: REVIEW → brutal-honesty-review swarm → review-report.md
- Completion block with directory tree output

### Generated command has:
- "Read user story from docs/Specification.md"
- "Create/modify files"
- "Write tests"
- "Run ruff check"
- "Commit"

### Consequence:
- No per-feature directory created
- No SPARC documentation per feature
- No validation phase with scoring
- No brutal-honesty-review
- Feature plans stored as flat .md files instead of `docs/features/<name>/sparc/` structure
- The rule says "ALL features get SPARC documentation, no exceptions" but the command doesn't enforce it

## Root Cause

During `/replicate` Phase 3, the toolkit generator:
1. Read the template file correctly
2. Generated `rules/feature-lifecycle.md` correctly from Section 3 of the template
3. Generated `commands/feature.md` as an **ad-hoc simplified version** instead of from Section 2 of the template
4. Likely ran out of context/tokens and fell back to a simpler generation

## Fix Required

Replace `.claude/commands/feature.md` with the full command template from `references/templates/feature-lifecycle.md` Section 2.

## Broader Pattern

This is the same pattern as Insight 001: when commands have no mandatory artifact enforcement, the LLM takes shortcuts. The template was designed to prevent this, but the template itself wasn't applied.
