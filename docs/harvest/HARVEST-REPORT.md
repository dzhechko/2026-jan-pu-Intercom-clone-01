# Harvest Report: AI-Consultant Cloud.ru

**Date:** 2026-03-02
**Mode:** QUICK
**Source Project:** ai-consultant-cloud-ru (Intercom-clone-01)

## Summary

| Metric | Value |
|--------|-------|
| Files scanned | ~55 source + ~17 test + ~17 commands + ~10 rules + ~10 insights |
| TOOLKIT_HARVEST.md markers | 0 (no pre-existing markers) |
| Candidates found (Phase 1) | 130+ (5 agents × ~25 each) |
| Classified for extraction (Phase 2) | 34 |
| Successfully decontextualized (Phase 3) | 34 |
| Integrated into toolkit (Phase 4) | 34 |
| Skipped (with reasons) | 10 |

## Extracted Artifacts

| # | Name | Category | Maturity | Version | Location |
|---|------|----------|----------|---------|----------|
| 1 | Hybrid RAG Search with RRF | Pattern | 🔴 Alpha | v1.0 | patterns/hybrid-rag-search-rrf.md |
| 2 | Multi-Agent Orchestrator | Pattern | 🔴 Alpha | v1.0 | patterns/multi-agent-orchestrator.md |
| 3 | Confidence-Triggered Escalation | Pattern | 🔴 Alpha | v1.0 | patterns/confidence-triggered-escalation.md |
| 4 | Multi-Tenant Data Isolation | Pattern | 🔴 Alpha | v1.0 | patterns/multi-tenant-data-isolation.md |
| 5 | Agent-as-Config | Pattern | 🔴 Alpha | v1.0 | patterns/agent-as-config.md |
| 6 | LLM Fallback & Retry | Pattern | 🔴 Alpha | v1.0 | patterns/llm-fallback-retry.md |
| 7 | Non-Blocking Side Effects | Pattern | 🔴 Alpha | v1.0 | patterns/non-blocking-side-effects.md |
| 8 | /myinsights — Insight Capture | Command | 🔴 Alpha | v1.0 | commands/myinsights.md |
| 9 | /review — Multi-Agent Review | Command | 🔴 Alpha | v1.0 | commands/review.md |
| 10 | /deploy — Deployment + Rollback | Command | 🔴 Alpha | v1.0 | commands/deploy.md |
| 11 | /go — Pipeline Router | Command | 🔴 Alpha | v1.0 | commands/go-pipeline-router.md |
| 12 | /run — Autonomous Build Loop | Command | 🔴 Alpha | v1.0 | commands/run-autonomous-loop.md |
| 13 | Checklists > Prose for LLM | Rule | 🔴 Alpha | v1.0 | rules/checklists-over-prose.md |
| 14 | Mandatory Phase Artifacts | Rule | 🔴 Alpha | v1.0 | rules/mandatory-phase-artifacts.md |
| 15 | Judge-Generator Separation | Rule | 🔴 Alpha | v1.0 | rules/judge-generator-separation.md |
| 16 | Layer-Based Model Escalation | Rule | 🔴 Alpha | v1.0 | rules/layer-based-model-escalation.md |
| 17 | Optimization Convergence Gate | Rule | 🔴 Alpha | v1.0 | rules/optimization-convergence-gate.md |
| 18 | Scoring Boundary Examples | Rule | 🔴 Alpha | v1.0 | rules/scoring-boundary-examples.md |
| 19 | Mandatory Review Phase | Rule | 🔴 Alpha | v1.0 | rules/mandatory-review-phase.md |
| 20 | Pipeline Decisions Logging | Rule | 🔴 Alpha | v1.0 | rules/pipeline-decisions-must-be-logged.md |
| 21 | Retroactive Docs via Agents | Rule | 🔴 Alpha | v1.0 | rules/retroactive-docs-via-parallel-agents.md |
| 22 | Docker Compose Multi-Service | Template | 🔴 Alpha | v1.0 | templates/docker-compose-multi-service.md |
| 23 | Python Dockerfile Multi-Stage | Template | 🔴 Alpha | v1.0 | templates/python-dockerfile-multistage.md |
| 24 | Nginx Reverse Proxy | Template | 🔴 Alpha | v1.0 | templates/nginx-reverse-proxy.md |
| 25 | .env.example Multi-Service | Template | 🔴 Alpha | v1.0 | templates/env-example-multi-service.md |
| 26 | pyproject.toml Python | Template | 🔴 Alpha | v1.0 | templates/pyproject-toml-python.md |
| 27 | CLAUDE.md Project Context | Template | 🔴 Alpha | v1.0 | templates/claude-md-project-context.md |
| 28 | RRF Merge Algorithm | Snippet | 🔴 Alpha | v1.0 | snippets/rrf-merge-python.md |
| 29 | Text Chunking with Overlap | Snippet | 🔴 Alpha | v1.0 | snippets/text-chunking-overlap-python.md |
| 30 | Structlog JSON Setup | Snippet | 🔴 Alpha | v1.0 | snippets/structlog-json-setup-python.md |
| 31 | Async SQLAlchemy Session | Snippet | 🔴 Alpha | v1.0 | snippets/async-sqlalchemy-session-python.md |
| 32 | JWT Token Create/Decode | Snippet | 🔴 Alpha | v1.0 | snippets/jwt-token-python.md |
| 33 | Confidence Estimation (RAG) | Snippet | 🔴 Alpha | v1.0 | snippets/confidence-estimation-rag-python.md |
| 34 | Pseudo-Embedding Generator | Snippet | 🔴 Alpha | v1.0 | snippets/pseudo-embedding-python.md |

### By Category

| Category | Count | New | Updated |
|----------|-------|-----|---------|
| Patterns | 7 | 7 | 0 |
| Commands | 5 | 5 | 0 |
| Rules | 9 | 9 | 0 |
| Templates | 6 | 6 | 0 |
| Snippets | 7 | 7 | 0 |
| Hooks | 0 | 0 | 0 |
| Skills | 0 | 0 | 0 |
| **Total** | **34** | **34** | **0** |

## Skipped Items

| # | Name | Reason |
|---|------|--------|
| 1 | Lead scoring algorithm | Domain-specific (CRM/sales), not generalizable |
| 2 | Russian regex patterns | Language-specific, not universal |
| 3 | Bitrix24 CRM client | Vendor-specific integration |
| 4 | Telegram webhook handler | Vendor-specific integration |
| 5 | Agent prompt files | Domain-specific content |
| 6 | Seed data script | Project-specific data |
| 7 | BTO pipeline (/bto, /bto-build, /bto-test, /bto-optimize) | Already standalone toolkit — no extraction needed |
| 8 | /start, /feature, /plan commands | Too coupled to SPARC/project-specific lifecycle |
| 9 | Multi-tenant SQLAlchemy models | Pattern already captured in #4 (Multi-Tenant Isolation) |
| 10 | Standard coding rules (type hints, async I/O) | Common knowledge, not novel |

## Toolkit Status (after harvest)

| Maturity | Count |
|----------|-------|
| 🔴 Alpha | 34 |
| 🟡 Beta | 0 |
| 🟢 Stable | 0 |
| ⭐ Proven | 0 |
| **Total** | **34** |

## Recommendations

1. **Promote to Beta after next project** — Hybrid RAG Search, Multi-Agent Orchestrator, and LLM Fallback patterns are most likely to be reused first
2. **Add TypeScript variants** — All snippets are Python-only; add TS/Node.js variants for frontend-heavy projects
3. **Merge related artifacts** — "Checklists > Prose" and "Mandatory Phase Artifacts" rules overlap; consider consolidating
4. **Test templates independently** — Docker Compose and Dockerfile templates should be tested in a fresh project to validate parameterization
5. **Extract BTO as separate toolkit** — BTO pipeline (already 4 commands) deserves its own harvest report as a standalone evaluation framework
6. **Add Hook artifacts** — Claude Code hooks (PostCommit insights, SessionStart context injection) were found but not extracted — candidate for next harvest

## Next Harvest

Suggested after: next project using these artifacts (to validate and promote to Beta)
