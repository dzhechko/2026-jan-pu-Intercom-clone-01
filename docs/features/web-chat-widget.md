# Feature: Web Chat Widget

**Pipeline:** /feature (score: +3, range -1 to +4)
**Sprint:** v1.0
**Depends on:** api-endpoints

## User Story (US-008 from Specification.md L183-214)

As a website visitor on cloud.ru, I want to start a consultation via an embedded chat widget, so that I can get answers without leaving the website.

### Acceptance Criteria (Gherkin)

```gherkin
Scenario: Widget initialization
  Given a visitor lands on cloud.ru
  When the page loads
  Then a chat bubble appears in the bottom-right corner
  And clicking it opens the chat panel
  And the greeting message appears within 1 second

Scenario: Proactive engagement
  Given a visitor has been on the pricing page for 60+ seconds
  When the proactive trigger fires
  Then the widget shows "Need help calculating costs for your workload?"
  And clicking it opens a pre-filled consultation

Scenario: Lead capture
  Given a visitor completes a consultation with architecture + TCO
  When the AI detects high purchase intent (5+ messages, confidence > 0.7)
  Then it shows a lead capture form (name, company, email, phone)
  And creates a lead in the CRM with full consultation transcript
```

## Architecture References

### API Endpoints (Pseudocode.md L512-577)
- `POST /api/v1/conversations` — create with channel "web_widget"
- `POST /api/v1/conversations/:id/messages` — send/receive messages
- Auth: X-API-Key header (same as other channels)

### Frontend Stack (Architecture.md L109-206)
- Embeddable via `<script>` tag or iframe
- CORS enabled for cross-origin requests

### Performance (Refinement.md L143-155)
- Widget load: < 1 second
- Greeting: < 1 second
- Response: < 5s (p50), < 30s (p99)

## Complexity Scoring

| Signal | Score | Notes |
|--------|-------|-------|
| Touches >10 files | +3 | widget/src/*, tests, package.json, Dockerfile |
| New frontend application | +2 | Standalone TypeScript widget |
| Uses existing API (no backend changes) | -1 | Reuses conversation endpoints |
| No new database entities | 0 | Uses existing Conversation/Message |
| Estimated 1-2 hours | +1 | Frontend + API client + tests |
| **Total** | **+3** | **/feature pipeline** |

## Implementation Plan

### Files to Create
1. `widget/package.json` — esbuild + TypeScript build config
2. `widget/tsconfig.json` — TypeScript strict mode, ES2020
3. `widget/src/index.ts` — ChatWidget class with Shadow DOM
4. `widget/src/api.ts` — API client (createConversation, sendMessage)
5. `widget/src/styles.ts` — Embedded CSS (bubble, panel, messages, input, form)
6. `widget/demo.html` — Demo page with integration examples
7. `widget/Dockerfile` — Multi-stage build (Node → Nginx)
8. `tests/unit/test_widget.py` — Backend integration tests

### Architecture Decisions
- **Shadow DOM**: Style isolation from host page (no CSS conflicts)
- **Vanilla TypeScript**: Zero runtime dependencies → 17KB minified bundle
- **esbuild**: Sub-second builds, single IIFE output file
- **localStorage session**: Persistent session ID across page reloads
- **Existing API reuse**: No new backend routes needed

### Tests Required
1. Schema validation (web_widget channel accepted, invalid rejected)
2. Message schema (length limits, role validation)
3. Intent routing through widget (all agent types work)

### Edge Cases
- Mobile viewport: panel goes full-screen on < 480px
- Message truncation: 4000 char client-side limit
- Session recovery: localStorage session persists
- API errors: fallback error message in chat
- Proactive dismissal: once dismissed, won't reappear
- Multiple widgets on same page: prevented by host element ID

## Phase Tracking

- [x] Phase 1: PLAN — this document
- [x] Phase 2: VALIDATE — requirements score 92/100 (WebSocket streaming is v2.0, no feedback buttons yet)
- [x] Phase 3: IMPLEMENT — 15 tests passing, TypeScript clean, 17KB bundle
- [x] Phase 4: REVIEW — lint clean, no security issues, Shadow DOM isolates styles
