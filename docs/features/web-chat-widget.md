# Feature: Web Chat Widget

## User Story (US-008)
As a website visitor on cloud.ru, I want to start a consultation via an embedded chat widget, so that I can get answers without leaving the website.

## Acceptance Criteria
1. Widget initialization: chat bubble appears bottom-right, opens panel on click, greeting within 1s
2. Proactive engagement: after 60s on pricing page, shows suggestion message
3. Lead capture: after high-intent consultation, asks for contact details

## Complexity Score: +3 (via /feature)
- Touches >10 files: +3
- New frontend application (widget/): +2
- Uses existing API endpoints: -1
- No new database entities: 0
- Estimated 1-2 hours: +1
- **Pipeline: /feature**

## Files Created
1. `widget/package.json` — esbuild + TypeScript build config
2. `widget/tsconfig.json` — TypeScript strict mode, ES2020 target
3. `widget/src/index.ts` — Main widget class (ChatWidget), auto-init from global config
4. `widget/src/api.ts` — API client (createConversation, sendMessage)
5. `widget/src/styles.ts` — Embedded CSS for Shadow DOM (bubble, panel, messages, input, lead form)
6. `widget/demo.html` — Demo page with integration examples
7. `widget/Dockerfile` — Multi-stage build (Node → Nginx)
8. `tests/unit/test_widget.py` — 15 tests (schemas, routing, intent)

## Architecture Decisions
- **Shadow DOM** for style isolation (no CSS conflicts with host page)
- **Vanilla TypeScript** with zero runtime dependencies (17KB minified)
- **esbuild** for fast bundling to single IIFE file
- **Existing API reuse**: widget uses same `/api/v1/conversations` + `/api/v1/conversations/:id/messages` endpoints with X-API-Key auth
- **Session persistence**: localStorage-based session ID (cloudru_widget_session)

## Implementation Steps
1. Create widget project structure (package.json, tsconfig, esbuild)
2. Implement CSS styles for Shadow DOM (bubble, panel, messages, input, proactive, lead form)
3. Implement API client (fetch wrapper with X-API-Key auth)
4. Implement ChatWidget class:
   - Shadow DOM host creation
   - Bubble rendering (position configurable)
   - Panel rendering (header, messages, input, footer)
   - Proactive engagement timer
   - Lead capture form (name, company, email, phone)
   - Agent type labels (Russian)
   - Message send/receive flow
5. Auto-init from `window.CHATWIDGET_CONFIG`
6. Create demo.html with integration examples
7. Create Dockerfile for CDN deployment
8. Write unit tests for backend integration points

## Tests
1. `tests/unit/test_widget.py::TestWidgetConversationSchema` — 4 tests (channel validation)
2. `tests/unit/test_widget.py::TestWidgetMessageSchema` — 4 tests (content length, role)
3. `tests/unit/test_widget.py::TestWidgetIntentRouting` — 7 tests (all agent types from widget)

## Edge Cases
- Mobile viewport: panel goes full-screen on <480px
- Message truncation: 4000 char client-side limit
- Session recovery: localStorage-based session ID persists across page reloads
- API errors: graceful fallback message shown in chat
- Proactive dismissal: once dismissed, won't show again in session

## Dependencies
- Depends on: api-endpoints (conversations API must exist)
- Uses: X-API-Key authentication (same as Telegram bot)

## Status: DONE
Committed: `feat: embeddable web chat widget (Shadow DOM, 17KB, zero deps)`
