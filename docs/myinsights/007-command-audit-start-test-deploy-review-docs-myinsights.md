# Insight 007: Command Audit — /start, /test, /deploy, /review, /docs, /myinsights

**Date:** 2026-03-02
**Severity:** Mixed — 2 Critical, 1 Medium, 3 OK
**Affected skills:** cc-toolkit-generator-enhanced (Phase 3 generation)

## Audit Methodology

Compared each command against its source template in `references/templates/`.
Commands without templates compared against SKILL.md specifications.

---

## /myinsights — CRITICAL MISMATCH (insights-system.md §1)

### Template specifies:
- Frontmatter with description
- Subcommands: capture (default), `archive INS-NNN`, `status INS-NNN [active|workaround|obsolete]`
- **Step 0: Duplicate Detection** (grep index for matching error signatures)
- **Step 1: Collect** (error signatures, symptoms, diagnostic steps, root cause, solution, prevention, tags, related)
- **Step 2: Create detail file** `myinsights/INS-NNN-slug.md` with structured format
- **Step 3: Update index** `myinsights/1nsights.md` with table: ID, Error Signatures, Summary, Status, Hits, File
- **Step 4: Auto-numbering** (find highest INS-NNN, increment)
- **Step 5: Notify**
- Archive flow with `myinsights/archive/` directory
- Status flow with lifecycle (Active → Workaround → Obsolete)
- Hit counter for tracking insight usage

### Current has:
- NO frontmatter
- Simplified subcommands: view, add [topic], search [query]
- NO duplicate detection
- NO structured capture flow (no error signatures, no diagnostic steps)
- Storage at `docs/insights/` (WRONG) instead of `myinsights/`
- Category-based storage (architecture.md, performance.md) instead of individual INS-NNN files
- NO archive, NO status lifecycle, NO hit counter

### What's correct (rule + hooks):
- `insights-capture.md` rule — CORRECT (matches template §2 perfectly)
- `settings.json` Stop hook for myinsights/ — CORRECT (matches template §3)
- SessionStart hook — CORRECT

### Impact:
The command directs to `docs/insights/` but the rule and hooks reference `myinsights/`. The system is internally inconsistent — the rule says "grep myinsights/1nsights.md" but the command creates files in `docs/insights/`.

---

## /start — SIGNIFICANT SIMPLIFICATION (start-command.md)

### Template specifies:
- Frontmatter with description + flags (--skip-tests, --skip-seed, --dry-run)
- 4 phases: Foundation, Packages (parallel Tasks ⚡), Integration, Finalize
- Phase 2 uses `Task` tool for parallel package generation
- Each Task has explicit doc references ("Read and use as source: docs/X.md")
- Anti-hallucination: "Read actual docs, don't hallucinate code"
- Error recovery section (re-run detects existing files)
- Swarm agents table
- Estimated time/files/commits
- Conditional database support ({{IF_DATABASE}})

### Current has:
- NO frontmatter
- 4 phases but simplified: Scaffold, Core Implementation, Infrastructure, Testing
- NO parallel Tasks in Phase 2 (sequential steps instead)
- References docs but not per-task
- NO anti-hallucination emphasis
- NO flags support
- NO error recovery
- NO estimated time

### Impact:
/start works but misses parallelism (slower bootstrap) and anti-hallucination guard (may generate code from LLM memory instead of from docs).

---

## /docs — MEDIUM SIMPLIFICATION (automation-commands.md §3)

### Template specifies:
- Full markdown templates for each of 7 files with bilingual headers (Russian/English)
- Each file template has 4-6 sections with ### headers
- Example: `deployment.md` has "Требования к окружению", "Быстрый старт", "Полное развертывание", "Обновление"

### Current has:
- Same 7 files listed
- Same directory structure (README/rus/, README/eng/)
- Bullet-point descriptions instead of full section templates
- Correct project adaptation (requirements.txt instead of package.json)
- Same update mode logic

### Impact:
/docs generates less structured output because it lacks the detailed section templates. The LLM has to figure out section structure itself instead of following a template.

---

## /test — OK (no template, P1 ad-hoc)

- No template exists in `references/templates/`
- SKILL.md lists it as P1: generated from Refinement.md testing strategy
- Current is well-structured: subcommands (unit/integration/e2e/generate/coverage), test structure, execution commands
- Project-specific with pytest commands
- **No issues found**

---

## /deploy — OK (no template, P1 ad-hoc)

- No template exists in `references/templates/`
- SKILL.md lists it as P1: generated from Completion.md
- Current is well-structured: pre-deploy checks, staging/production/rollback flows, environment matrix
- Project-specific with Docker Compose commands
- **No issues found**

---

## /review — OK (no template, P2 ad-hoc)

- No template exists in `references/templates/`
- SKILL.md lists it as P2
- Current is well-structured with frontmatter: scope detection, automated checks, multi-agent swarm, severity levels, verdict system
- References brutal-honesty-review skill correctly
- **No issues found — actually one of the best-generated commands**

---

## Summary Table

| Command | Template | Match | Severity | Action Needed |
|---------|----------|-------|----------|---------------|
| `/myinsights` | insights-system.md §1 | ~15% | CRITICAL | Full rewrite from template |
| `/start` | start-command.md | ~40% | HIGH | Add parallelism, flags, error recovery, anti-hallucination |
| `/docs` | automation-commands.md §3 | ~70% | MEDIUM | Add full section templates for 7 files |
| `/test` | none (P1 ad-hoc) | N/A | OK | — |
| `/deploy` | none (P1 ad-hoc) | N/A | OK | — |
| `/review` | none (P2 ad-hoc) | N/A | OK | — |

## Recommendations for cc-toolkit-generator-enhanced

### R1: /myinsights must use template verbatim
The insights system is P0 mandatory. The entire architecture (INS-NNN files, 1nsights.md index, duplicate detection, archive, hit counter) is designed to work with the insights-capture rule and Stop hook. The current ad-hoc version breaks this contract.

### R2: /start should use Task tool template
The parallel Phase 2 is the key performance feature. Without it, bootstrapping is ~3x slower on multi-service projects. Add per-task doc references to prevent hallucination.

### R3: /docs should include section templates
The bilingual section headers (Russian/English) ensure consistent output quality. Without them, LLM may generate inconsistent section structures across languages.

### R4: Templates exist for exactly 5 commands
```
start-command.md        → /start (P0)
insights-system.md §1   → /myinsights (P0)
feature-lifecycle.md §2 → /feature (P0)
automation-commands.md   → /go (P1), /run (P1), /docs (P1)
feature-suggestions.md  → /next (P1)
feature-lifecycle-ent.md → /feature-ent (P1, conditional)
```
Commands without templates: /test, /deploy, /review, /plan
Consider adding templates for /plan (see Insight 005) at minimum.

### R5: Pattern — rule matches template but command doesn't
Same issue as /feature (Insight 004): `insights-capture.md` rule is correct but `myinsights.md` command is wrong. /replicate Phase 3 generates rules correctly from templates but commands get simplified. This suggests the generation loop handles rules and commands differently — rules are copied more faithfully.
