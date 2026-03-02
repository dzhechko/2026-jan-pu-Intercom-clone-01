# Insight 006: Command Audit Results — /go, /next, /run, /plan, /feature-ent

**Date:** 2026-03-02
**Severity:** Mixed (see per-command)
**Affected skills:** cc-toolkit-generator-enhanced (Phase 3 generation)

## Audit Methodology

Compared each generated command (`.claude/commands/*.md`) against its source template in `.claude/skills/cc-toolkit-generator-enhanced/references/templates/`. Used `diff` for exact comparison.

## Results

### /go — 95% match (automation-commands.md §1)
- **Cosmetic**: Emojis stripped from "Available pipelines" box and summary
- **Functional gap (FIXED)**: Missing "IF complex fallback was used" block in Step 4 summary report. This means when score ≥ +5 but /feature-ent is absent, user gets no guidance about re-generating toolkit with idea2prd-manual.
- **Fix applied**: Restored the complex fallback note

### /next — 100% match (feature-suggestions.md §5)
- Perfect copy from template. No issues.

### /run — 90% match (automation-commands.md §2)
- **Correct adaptation**: `npm test` → `pytest tests/ -v` (project-specific)
- **Cosmetic**: Emojis stripped from summary report
- **Missing**: `Duration: <time>` field in summary
- **No fix needed**: Adaptations are appropriate for this project

### /plan — NO TEMPLATE EXISTS
- **Critical (FIXED)**: Wrote to `docs/features/$NAME.md` (flat file), conflicting with `/feature`'s `docs/features/<name>/sparc/` directory structure
- **Fix applied**: Changed output to `docs/plans/$NAME.md`, created `docs/plans/` directory
- **Root cause**: No template for /plan in `references/templates/` — generated ad-hoc

### /feature-ent — Correctly absent
- Conditional on `{{IF_DDD}}` — project uses SPARC pipeline, no DDD docs
- /go handles absence gracefully (checks `ls .claude/commands/feature-ent.md`)

## Recommendations for cc-toolkit-generator-enhanced

### R1: Add /plan template
Create `references/templates/plan-command.md` with:
- Explicit `docs/plans/` output path
- Clear differentiation from /feature Phase 1 output
- Lightweight plan template (no SPARC, just files/steps/tests/edge-cases)

### R2: Add {{TEST_COMMAND}} placeholder to /run template
Current template hardcodes `npm test or equivalent`. Should use:
```
1. Run full test suite: `{{TEST_COMMAND}}`
```
Where `{{TEST_COMMAND}}` is resolved from project's package.json/pyproject.toml/Cargo.toml during toolkit generation.

### R3: Path conflict validation in Phase 6
Add to Master Validation Checklist:
```
- [ ] /plan output path (docs/plans/) does NOT overlap with /feature output path (docs/features/<name>/sparc/)
- [ ] /feature output path (docs/features/<name>/sparc/) does NOT overlap with /feature-ent output path (docs/features/<name>/)
```

### R4: Preserve emojis from templates
During generation, templates' emojis (✅ ⚠️ 🏁 📊 📋 🏷️) were stripped. These serve as visual anchors in long command outputs. Consider preserving them or making it configurable.

### R5: "complex fallback" block in /go is important
The /go command's fallback block is the only place that recommends re-generating toolkit with idea2prd-manual. Without it, users with complex features never learn about /feature-ent.
