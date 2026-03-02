# Validation Report — AI-Консультант Cloud.ru

**Date:** 2026-03-02
**Iterations:** 1/3
**Verdict:** 🟡 CAVEATS

---

## Summary

| Validator | Score | Status | BLOCKED | WARNING |
|-----------|:-----:|--------|:-------:|:-------:|
| User Stories (INVEST) | 69/100 | WARNING | 2 | 5 |
| Acceptance Criteria (SMART) | 76/100 | WARNING | 0 | 7 |
| Architecture | 80/100 | WARNING | 0 | 10 |
| Pseudocode | 61/100 | WARNING | 0 | 14 |
| Cross-Document Coherence | 74/100 | WARNING | 0 | 10 |
| **AVERAGE** | **72/100** | **🟡 CAVEATS** | **2** | **46** |

---

## Verdict Rationale

**🟡 CAVEATS** — Average score 72/100 (above 70 threshold). Two BLOCKED stories (US-009 White-label, US-012 Agent config) are both **Could/Should** priority and not in MVP scope, so they don't block development. All Must-have stories pass validation. Multiple warnings exist but are documented as known limitations with clear remediation paths.

**Can proceed to Phase 3 (Toolkit Generation) with the following noted caveats:**

---

## Critical Issues (must address before implementation)

### 1. Pseudocode: Compliance Agent algorithm missing
- **Impact:** Must-have story (US-003) has no algorithmic specification
- **Fix:** Add compliance advisory pseudocode with 152-ФЗ/ФСТЭК/CII checking logic
- **Severity:** HIGH — but implementation can proceed using RAG-based approach (agent = config + prompt)

### 2. Pseudocode: DETECT_INTENT and CALCULATE_CONFIDENCE undefined
- **Impact:** Core orchestrator functions have no specification
- **Fix:** Define intent classification (LLM-based with Haiku) and confidence aggregation formula
- **Severity:** HIGH — but well-understood patterns, implementable from context

### 3. Coherence: M4 Gross Margin inconsistency
- **Impact:** Header claims 85-90% but COGS calculation yields 72-80%
- **Fix:** Correct M4 header to match COGS calculation (72-80%)
- **Severity:** MEDIUM — financial document accuracy

### 4. Coherence: amoCRM / White-label phase disagreement
- **Impact:** PRD says v1.1 (M7-9), Specification says v2.0 (M10-15)
- **Fix:** Align to Specification timing (v2.0) as authoritative
- **Severity:** LOW — both are post-MVP features

---

## Warnings by Category

### User Stories (INVEST) — 2 BLOCKED, 5 WARNING

**BLOCKED (not in MVP, don't block development):**
- **US-009** (White-label, 42/100): Severely underspecified. Split into sub-stories, defer to v1.1
- **US-012** (Agent config UI, 45/100): No acceptance criteria. Define config schema first

**WARNING:**
- **US-004** (Migration plan, 57/100): Missing Gherkin AC. Split into wave planning + risk assessment
- **US-005** (Follow-up dialogue, 50/100): Cross-cutting concern, absorb into US-001 AC
- **US-007** (Bitrix24 CRM, 65/100): No AC. Define trigger events and Bitrix24 object mapping
- **US-013** (Approve recommendations, 65/100): "High-stakes" undefined. Define trigger conditions
- **US-016** (SA ratings, 55/100): Feedback loop not in scope. Rewrite "so that" clause

### Acceptance Criteria (SMART) — 7 WARNING

**Common gap:** Time-bound (T) criterion missing in many scenarios. Fix: Add explicit response time assertions to all scenarios.

- Follow-up questions: No response time threshold
- ФСТЭК/CII scenarios: Vague verbs ("explains", "maps") without measurable outputs
- Session continuity: "Restores context" not measurable; no session age limit
- Lead capture: "High purchase intent" undefined
- Rich message formatting: "Readable chunks" not quantified

**12 Missing Scenarios identified:**
- RAG corpus staleness disclaimer
- Rate limiting user-facing behavior
- Empty/whitespace input handling
- Offensive content rejection
- Token limit / context window summarization
- Concurrent cross-channel sessions
- LLM timeout and retry
- Multi-tenant data isolation
- Large TCO request (500+ VMs)
- Conversation timeout and auto-close
- PDF export from Telegram
- RBAC enforcement

### Architecture — 10 issues

**HIGH:**
- mTLS contradiction: Spec mandates internal mTLS, Architecture uses Docker network only
- Backup architecture: Not specified (Spec requires daily full + hourly incremental)
- Keycloak vs custom auth: Unresolved decision

**MEDIUM:**
- amoCRM integration not architecturally specified
- PDF generation service absent
- Docker Compose healthcheck probes not defined

**LOW:**
- Audit log table missing
- Proactive widget trigger not modeled
- Encrypted volumes not specified
- Missing sequence/flow diagrams

### Pseudocode — 14 issues

**Critical gaps:**
- Compliance Agent algorithm absent (Must-have)
- Migration Agent algorithm absent (Should)
- DETECT_INTENT undefined
- CALCULATE_CONFIDENCE undefined
- No auth API contracts
- No RAG ingestion API

**Significant gaps:**
- savings_vs_current always null
- Telegram session continuity no algorithm
- Proactive engagement no pseudocode
- Webhook signature verification absent
- Lead deduplication undefined
- Multi-tenancy isolation enforcement missing
- ROI calculation algorithm missing
- Escalation branch clarification needed

### Cross-Document Coherence — 9 contradictions

1. **amoCRM phase:** PRD v1.1 vs Spec v2.0
2. **White-label phase:** PRD v1.1 vs Spec v2.0
3. **NPS target M6:** PRD >60 vs Spec >65
4. **M4 Gross Margin:** Header 85-90% vs calculated 72-80%
5. **LLM fallback:** Architecture says GigaChat, Completion env says Haiku
6. **Conversion M3:** PRD unclear vs Spec 20%
7. **RBAC roles:** PRD 3 roles vs Spec/Architecture 4 roles (missing superadmin)
8. **Monitoring thresholds:** Stay at MVP levels, don't adapt to Prod/Enterprise
9. **Monthly consultations scaling:** Timeline labeling ambiguity

### Feature Traceability Gaps

| Feature | Gap in Chain |
|---------|-------------|
| US-016 (SA feedback) | No Spec AC → No Pseudocode → No Architecture → No Tests |
| AI Factory Agent | No Refinement tests (E2E, IT, Gherkin) |
| Proactive widget trigger | No Pseudocode → No Architecture component |
| PDF generation | No Pseudocode → Architecture partial → No tests |
| White-label branding | Architecture partial → No Pseudocode |
| Session continuity | No E2E test |

---

## Recommendations

### Before Sprint 1 (quick fixes):
1. Fix M4 gross margin to 72-80% (match COGS calculation)
2. Align amoCRM/White-label phases to Spec v2.0 timing
3. Fix NPS target to >65 consistently
4. Add LLM_FALLBACK_MODEL=gigachat to env config; note Haiku for routing optimization
5. Add superadmin role to PRD

### During Sprint 1 (address in implementation):
6. Implement DETECT_INTENT as LLM classifier (Haiku for speed)
7. Implement CALCULATE_CONFIDENCE as weighted average (RAG top score × 0.6 + LLM self-score × 0.4)
8. Compliance Agent: use RAG-based approach with 152-ФЗ document corpus
9. Add Telegram webhook signature verification
10. Define backup strategy in docker-compose (cron + pg_dump + qdrant snapshot)

### Post-MVP (backlog):
11. Write missing Gherkin scenarios (12 identified)
12. Add sequence diagrams for key flows
13. Resolve mTLS vs Docker network (ADR-006)
14. Add PDF generation service
15. Implement lead deduplication logic
