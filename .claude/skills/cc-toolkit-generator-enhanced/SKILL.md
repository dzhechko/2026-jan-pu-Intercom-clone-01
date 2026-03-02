---
name: cc-toolkit-generator-enhanced
description: >
  Generate complete Claude Code toolkit from idea2prd-manual or SPARC documentation.
  Supports: PRD, SPARC, DDD, ADR, C4, Pseudocode, Gherkin, Fitness Functions.
  Creates CLAUDE.md, agents, skills, commands, hooks, rules, MCP configs.
  Feature lifecycle: /feature + sparc-prd-mini + requirements-validator + brutal-honesty-review.
  Enterprise lifecycle: /feature-ent + idea2prd-manual (conditional P1).
  Feature suggestions: /next + feature-navigator skill + SessionStart hook.
  Insights: /myinsights + index/detail architecture. Plans: /plan with auto-commit.
  Automation: /go (smart pipeline), /run (autonomous build loop), /docs (bilingual RU/EN docs).
  Triggers: "cc-toolkit-enhanced", "generate toolkit from docs", "создай инструменты из документации".
  Three modes: AUTO, HYBRID (default), MANUAL.
---

# CC-Toolkit-Generator Enhanced

Generate production-ready Claude Code instruments from **SPARC or idea2prd-manual documentation**.

## Input Documents

### SPARC Pipeline

| Document | Maps To |
|----------|---------|
| **PRD.md** | CLAUDE.md overview, /plan command, feature context |
| **Solution_Strategy.md** | CLAUDE.md problem context, architect agent |
| **Specification.md** | coding-standards/ skill, security.md rule, /test command |
| **Pseudocode.md** | planner agent templates, /start Phase 2 references |
| **Architecture.md** | CLAUDE.md tech stack, /start structure, architect agent, MCP |
| **Refinement.md** | testing.md rule, code-reviewer agent, /test command |
| **Completion.md** | /deploy command, /start Phase 3, CI/CD hooks |
| **Research_Findings.md** | project-context/ skill, domain knowledge |
| **Final_Summary.md** | CLAUDE.md quick reference, DEVELOPMENT_GUIDE.md |
| **CLAUDE.md** (from docs) | Base for enhanced CLAUDE.md |

### idea2prd-manual Pipeline

| Category | Documents | Maps To |
|----------|-----------|---------|
| **Analyst** | Task_Brief, Research_Findings, Product_Idea | CLAUDE.md context, project-context skill |
| **PRD** | PRD.md | CLAUDE.md overview, commands |
| **DDD Strategic** | bounded-contexts/, context-map | domain-model skill, architect agent |
| **DDD Tactical** | aggregates/, entities/, events/ | coding-standards skill, validation hooks |
| **ADR** | adr/*.md | CLAUDE.md decisions, rules |
| **C4** | c4/*.mermaid | architect agent, CLAUDE.md diagrams |
| **Pseudocode** | pseudocode/*.pseudo | planner agent, tdd-guide agent |
| **Tests** | tests/*.feature (Gherkin) | /test command, testing rules |
| **Fitness** | fitness/*.md | hooks (quality gates), rules |
| **Completion** | COMPLETION_CHECKLIST.md | /deploy command, CI/CD hooks |
| **.ai-context/** | 8 context files | Direct CLAUDE.md integration |

## Mode Selection

| Mode | Triggers | Checkpoints | Time |
|------|----------|-------------|------|
| **AUTO** | "auto", "быстро" | 0 | ~5 min |
| **HYBRID** | default, "smart" | 2 | ~10 min |
| **MANUAL** | "manual", "пошагово" | 6 | ~20 min |

## Workflow

### Phase 1: Detect & Parse

1. Scan `/mnt/user-data/uploads/` for documents
   - If no documents found: ask user to upload SPARC or idea2prd documentation set
   - Minimum required: at least PRD.md + Architecture.md (SPARC) or docs/ddd/ (idea2prd)
2. Detect source pipeline:
   - Has `docs/ddd/` → idea2prd-manual
   - Has `Architecture.md` + `Solution_Strategy.md` → SPARC
   - Has `Architecture.md` only → SPARC minimal
   - Mixed → Use unified mapping
3. Detect project characteristics:
   - **has_external_apis** — scan for API integrations
   - **has_database** — scan for DB services
   - **monorepo_packages** — extract from project structure
   - **docker_services** — extract from docker-compose
4. Build Internal Project Model (IPM)

**MANUAL Checkpoint 1:** Document Detection Review

### Phase 2: Analyze & Map

**SPARC Pipeline:** See [SPARC Mapping](#sparc-document-mapping) below.
**idea2prd Pipeline:** See `references/extended-mapping.md` for complete DDD/ADR/Gherkin/Fitness mappings.

**MANUAL Checkpoint 2:** Mapping Approval

### Phase 3: Generate P0 (Mandatory)

Always generate these items:

| # | Instrument | Template Source |
|---|-----------|----------------|
| 1 | **CLAUDE.md** | `references/claude-md-strategy.md` — pipeline-specific strategy |
| 2 | **security.md** rule | From Specification NFRs or ADRs + Fitness Functions |
| 3 | **coding-style.md** rule | From Architecture tech stack or DDD Tactical + ADRs |
| 4 | **commands/start.md** | `references/templates/start-command.md` |
| 5 | **commands/myinsights.md** | `references/templates/insights-system.md` |
| 6 | **commands/feature.md** | `references/templates/feature-lifecycle.md` |
| 7 | **rules/git-workflow.md** | Semantic commit conventions |
| 8 | **rules/insights-capture.md** | `references/templates/insights-system.md` |
| 9 | **rules/feature-lifecycle.md** | `references/templates/feature-lifecycle.md` |
| 10 | **settings.json** hooks | insights + plans auto-commit, SessionStart |
| 11-16 | **6 lifecycle skills** | `references/templates/feature-lifecycle.md` — copy protocol + path rewrite |

**Conditional P0:**
- **rules/secrets-management.md** + **skills/security-patterns/** — IF has_external_apis
- **rules/domain-model.md** — IF has DDD Strategic docs

**MANUAL Checkpoint 3:** P0 Review

### Phase 4: Generate P1 (Recommended)

| Instrument | Source (SPARC) | Source (idea2prd) |
|------------|----------------|-------------------|
| planner.md agent | Pseudocode, PRD | Pseudocode, PRD |
| code-reviewer.md agent | Refinement, Specification | Fitness, ADR |
| architect.md agent | Architecture, Solution_Strategy | C4, ADR, DDD Strategic |
| project-context/ skill | Research_Findings, Final_Summary | Research, .ai-context |
| coding-standards/ skill | Architecture (tech stack) | DDD Tactical, ADR |
| testing-patterns/ skill | Refinement (test strategy) | Gherkin, Fitness |
| /plan command | PRD, Pseudocode | PRD, Pseudocode |
| /test command | Refinement, Specification | Gherkin |
| /deploy command | Completion | Completion Checklist |
| testing.md rule | Refinement | Fitness Functions |

**Enterprise Lifecycle (IF DDD detected) — see `references/templates/feature-lifecycle-ent.md`:**
- /feature-ent command, feature-lifecycle-ent.md rule
- Copy skills: idea2prd-manual/, goap-research-ed25519/

**Feature Suggestions System — see `references/templates/feature-suggestions.md`:**
- /next command, feature-navigator/ skill, feature-roadmap.json, SessionStart hook

**Automation Commands — see `references/templates/automation-commands.md`:**
- /go (smart pipeline), /run (autonomous build loop), /docs (bilingual RU/EN)

**MANUAL Checkpoint 4:** P1 Selection

### Phase 5: Generate P2-P3 (Optional)

**P2:** tdd-guide.md agent, settings.json hooks, /review command
**P2 DDD-only:** ddd-validator.md agent, aggregate-patterns/ skill, event-handlers/ skill, /validate-ddd
**P3:** .mcp.json (see `references/templates/mcp.md`), Coolify MCP, Docker MCP

**MANUAL Checkpoint 5:** P2-P3 Selection

### Phase 6: Package & Deliver

Create output archive per [Output Structure](#output-structure).
Run the [Master Validation Checklist](#master-validation-checklist) before delivery.

**MANUAL Checkpoint 6:** Final Review

## Output Structure

```
[project-name]-cc-toolkit/
├── CLAUDE.md
├── DEVELOPMENT_GUIDE.md
├── .claude/
│   ├── settings.json                   # Hooks: insights + roadmap + plans, SessionStart
│   ├── feature-roadmap.json            # Feature status (from PRD)
│   ├── hooks/feature-context.py        # SessionStart: inject feature context
│   ├── agents/
│   │   ├── planner.md, code-reviewer.md, architect.md
│   │   ├── tdd-guide.md               # P2
│   │   ├── domain-expert.md           # {{IF_DDD}}
│   │   └── ddd-validator.md           # {{IF_DDD}} P2
│   ├── skills/
│   │   ├── sparc-prd-mini/            # ⭐ P0 — feature planning orchestrator
│   │   ├── explore/                   # ⭐ P0 — Socratic questioning
│   │   ├── goap-research/             # ⭐ P0 — GOAP research
│   │   ├── problem-solver-enhanced/   # ⭐ P0 — 9 modules + TRIZ
│   │   ├── requirements-validator/    # ⭐ P0 — doc validation
│   │   ├── brutal-honesty-review/     # ⭐ P0 — post-impl review
│   │   ├── idea2prd-manual/          # {{IF_DDD}} P1
│   │   ├── goap-research-ed25519/    # {{IF_DDD}} P1
│   │   ├── feature-navigator/        # P1 — roadmap navigation
│   │   ├── project-context/, coding-standards/, testing-patterns/
│   │   ├── security-patterns/        # {{IF_EXTERNAL_APIS}}
│   │   ├── aggregate-patterns/       # {{IF_DDD}} P2
│   │   └── event-handlers/           # {{IF_DDD}} P2
│   ├── commands/
│   │   ├── start.md                   # ⭐ P0 — full project bootstrap
│   │   ├── myinsights.md             # ⭐ P0 — insight capture
│   │   ├── feature.md                # ⭐ P0 — feature lifecycle
│   │   ├── feature-ent.md           # {{IF_DDD}} P1
│   │   ├── next.md, plan.md         # P1
│   │   ├── go.md, run.md, docs.md   # P1 — automation
│   │   ├── test.md, deploy.md, review.md
│   │   └── validate-ddd.md          # {{IF_DDD}} P2
│   └── rules/
│       ├── security.md, coding-style.md, testing.md
│       ├── git-workflow.md           # ⭐ P0
│       ├── insights-capture.md      # ⭐ P0
│       ├── feature-lifecycle.md     # ⭐ P0
│       ├── feature-lifecycle-ent.md # {{IF_DDD}} P1
│       ├── secrets-management.md    # {{IF_EXTERNAL_APIS}}
│       ├── domain-model.md          # {{IF_DDD}}
│       └── fitness-functions.md     # {{IF_DDD}}
├── docs/features/, docs/plans/
├── README/                          # Bilingual (RU/EN), created by /docs
├── .mcp.json                        # {{IF_EXTERNAL_INTEGRATIONS}}
└── INSTALL.md
```

**Markers:** `{{IF_DDD}}` = DDD docs detected; `{{IF_EXTERNAL_APIS}}` = external APIs; `{{IF_EXTERNAL_INTEGRATIONS}}` = external MCP.

## SPARC Document Mapping

> Primary pipeline. Apply when `docs/ddd/` is NOT present.

| SPARC Document | Section | Primary Output | Secondary Output |
|----------------|---------|----------------|------------------|
| **PRD.md** | Executive Summary | CLAUDE.md Overview | — |
| PRD.md | Problem Statement | CLAUDE.md Problem Context | architect.md |
| PRD.md | Functional Requirements | /plan features | /start Phase 2 scope |
| PRD.md | NFRs | security.md, testing.md | rules |
| PRD.md | User Stories | /test templates | testing-patterns/ |
| **Solution_Strategy.md** | Root Cause / Framework | project-context/, architect.md | CLAUDE.md |
| **Specification.md** | Data Model / API / Security | /start Phase 2, security.md | coding-standards/ |
| **Pseudocode.md** | Algorithms / Error Handling | planner.md, code-reviewer.md | /start refs |
| **Architecture.md** | Structure / Stack / Docker / APIs | CLAUDE.md, /start, .mcp.json | coding-style.md |
| **Refinement.md** | Edge Cases / Testing / Security | code-reviewer.md, testing.md, /test | tdd-guide.md |
| **Completion.md** | CI/CD / Docker / Monitoring | /deploy, /start Phase 3 | hooks |
| **Research_Findings.md** | Tech Decisions / Best Practices | architect.md, coding-standards/ | CLAUDE.md |
| **Final_Summary.md** | Quick Reference | CLAUDE.md | DEVELOPMENT_GUIDE.md |

### Extraction Patterns

```
EXTRACT PRD.md:       name → title, problem → context, requirements → features, NFRs → rules
EXTRACT Architecture: structure → /start P1, packages → /start P2, docker → /start P3,
                      stack → CLAUDE.md, APIs → security-patterns, DB → migration
EXTRACT Pseudocode:   functions → planner templates, algorithms → /start P2 refs,
                      errors → code-reviewer
```

## Smart Recommendations

```
# SPARC Core
Architecture.md → architect.md (+10), /start (+10)
Pseudocode.md   → planner.md (+10), BOOST /start P2
Refinement.md   → testing.md (+8), code-reviewer.md (+8), /test (+8)
Solution_Strategy → project-context/ (+8), BOOST architect (+3)
Completion.md   → /deploy (+8), BOOST /start P3

# Detection-based
"API"|"integration"|"external" → security-patterns/ (+10), secrets-management.md (+10)
"PostgreSQL"|"MongoDB"|"database" → BOOST /start P3 with migration
"Coolify" → coolify MCP (+8);  "Docker" → docker MCP (+5)

# DDD-Specific
docs/ddd/strategic/         → domain-expert.md (+10)
docs/ddd/tactical/aggregates → ddd-validator.md (+10), /validate-ddd (+8)
docs/ddd/tactical/events/    → event-handlers/ (+8)
docs/adr/ (>10 files)       → architect.md (+10)
docs/tests/*.feature         → testing-patterns/ (+10), tdd-guide.md (+8)
docs/fitness/                → fitness-functions.md (+10)
.ai-context/                 → INTEGRATE into CLAUDE.md, project-context/ (+10)
```

See `references/enhanced-recommendations.md` for detailed scoring.

## CLAUDE.md Generation

**Read `references/claude-md-strategy.md`** for complete generation strategy.

Two pipeline-specific strategies with shared base sections:
- **SPARC** → emphasis on Problem & Solution, Key Algorithms
- **idea2prd** → emphasis on Domain Model, Key Decisions, Quality Gates

Both include: Parallel Execution Strategy, Swarm Agents, Git Workflow, Available Agents/Skills/Commands, Development Insights, Feature Lifecycle, Feature Roadmap, Plans, Automation Commands.

## Key Systems (read templates before generating)

| System | Template File | Key Components |
|--------|--------------|----------------|
| **/start** | `templates/start-command.md` | 4-phase bootstrap, parallel Tasks, anti-hallucination |
| **Insights** | `templates/insights-system.md` | /myinsights, insights-capture rule, Stop hook, index+detail |
| **Feature Lifecycle** | `templates/feature-lifecycle.md` | /feature (4 phases), 6 skills copy, path rewrite |
| **Enterprise Lifecycle** | `templates/feature-lifecycle-ent.md` | /feature-ent, idea2prd-manual, goap-research-ed25519 |
| **Feature Suggestions** | `templates/feature-suggestions.md` | /next, feature-navigator, roadmap.json, SessionStart |
| **Automation** | `templates/automation-commands.md` | /go, /run, /docs, command hierarchy |
| **DDD Agents** | `templates/ddd-agents.md` | domain-expert, ddd-validator |
| **DDD Skills** | `templates/ddd-skills.md` | aggregate-patterns, event-handlers |
| **DDD Hooks/Commands** | `templates/ddd-hooks-commands.md` | hooks, /validate-ddd |
| **MCP** | `templates/mcp.md` | .mcp.json generation |
| **Enhanced CLAUDE.md** | `templates/enhanced-claude-md.md` | Additional CLAUDE.md sections |

## Context Budget

| Component | Target | Max |
|-----------|--------|-----|
| CLAUDE.md | 4k | 6k |
| /start command | 2k | 4k |
| /myinsights, /feature, /plan | 3k combined | 5.5k |
| Domain rules | 1.5k | 2.5k |
| Generated skills + agents | 3.5k | 5k |
| Copied lifecycle skills | 0 | 0 (on-demand) |
| Commands + hooks | 1k | 2k |
| DEVELOPMENT_GUIDE | 1k | 2k |
| **Total** | ~18k | 30k (<15% of 200k) |

## Checkpoint Commands (MANUAL Mode)

| Checkpoint | Commands |
|------------|----------|
| CP1: Detection | `ок`, `добавь [doc]`, `убери [doc]` |
| CP2: Mapping | `повысь [tool]`, `понизь [tool]`, `покажи mapping` |
| CP3: P0 | `измени [file]`, `покажи [file]` |
| CP4: P1 | `+N`, `-N`, `всё`, `минимум` |
| CP5: P2-P3 | `+agents`, `+skills`, `+hooks`, `+mcp` |
| CP6: Final | `превью [file]`, `скачать`, `добавить [tool]` |

## Master Validation Checklist

Run in Phase 6 before delivery.

### P0 Mandatory

- [ ] CLAUDE.md generated per `references/claude-md-strategy.md`
- [ ] CLAUDE.md includes: Parallel Execution, Swarm Agents, Insights, Feature Lifecycle, Roadmap, Plans, Automation
- [ ] DEVELOPMENT_GUIDE.md with full lifecycle instructions
- [ ] `/start` — complete project gen, all packages, Task parallelism, Docker health check, references actual docs
- [ ] `/myinsights` — duplicate detection, subcommands, index+detail architecture
- [ ] `insights-capture.md` rule with auto-grep pattern
- [ ] `/feature` — 4-phase lifecycle (plan → validate → implement → review)
- [ ] `feature-lifecycle.md` rule
- [ ] 6 lifecycle skills copied with path rewrite (`/mnt/skills/user/` → `.claude/skills/`)
- [ ] `git-workflow.md` rule (semantic commits)
- [ ] `settings.json` — Stop hooks (insights + roadmap + plans) + SessionStart hook
- [ ] `docs/features/` directory created

### P0 Conditional

- [ ] `secrets-management.md` + `security-patterns/` — IF has_external_apis
- [ ] `domain-model.md` rule — IF DDD Strategic docs
- [ ] `/start` includes DB migration + seed — IF has_database

### P1 Enterprise (IF DDD)

- [ ] `/feature-ent` + `feature-lifecycle-ent.md` rule
- [ ] `idea2prd-manual/` + `goap-research-ed25519/` skills copied with path rewrites
- [ ] CLAUDE.md Enterprise Feature Lifecycle section

### P1 Feature Suggestions

- [ ] `feature-roadmap.json` populated (min 5 features from PRD)
- [ ] `feature-context.py` SessionStart hook
- [ ] `/next` command + `feature-navigator/` skill

### P1 Automation

- [ ] `/go` — complexity scoring → pipeline selection
- [ ] `/run` — /start → /next → /go loop (MVP/all scope)
- [ ] `/docs` — bilingual RU/EN generation

### Pipeline-Specific (IF applicable)

- [ ] Bounded Contexts → agent scopes (DDD)
- [ ] Aggregates → validation patterns (DDD)
- [ ] ADR decisions → rules (ADR)
- [ ] Fitness Functions → hooks (Fitness)
- [ ] Gherkin features → test commands (Gherkin)
- [ ] .ai-context/ → CLAUDE.md integration

## Dependencies

- SPARC documentation set (11 files) — primary pipeline
- Alternatively: idea2prd-manual/auto output
- Optional: .ai-context/ directory
