# Architecture -- Web Chat Widget

## Data Flow

```
Host Page (cloud.ru)
  |
  |  <script src="widget.js">
  v
Shadow DOM (style isolation)
  |
  |  fetch() with X-API-Key header
  v
REST API (FastAPI)
  |  POST /api/v1/conversations
  |  POST /api/v1/conversations/:id/messages
  v
Orchestrator
  |  detect_intent() -> select_agent_type()
  v
Agent (Architect | Cost | Compliance | Migration | AI Factory | Escalation)
  |  RAG search -> LLM call -> response
  v
JSON Response -> Widget renders message bubble
```

## Embedding Architecture

1. Host page sets `window.CHATWIDGET_CONFIG` (apiKey, apiUrl, options)
2. `widget.js` loads (async defer), registers `window.CloudRuWidget.init`
3. On DOMContentLoaded, auto-initializes if config present
4. Widget creates a `<div id="cloudru-chat-widget">` with closed Shadow DOM
5. All CSS injected inside Shadow DOM -- zero leakage to/from host page

## Component Structure (inside Shadow DOM)

```
ShadowRoot (closed)
  +-- <style>          WIDGET_CSS from styles.ts
  +-- <button>         .widget-bubble (toggle open/close)
  +-- <div>            .proactive (timed popup, dismissible)
  +-- <div>            .widget-panel
       +-- .panel-header     title, subtitle, close button
       +-- .messages         scrollable message list
       |    +-- .msg.user         user bubbles (blue, right-aligned)
       |    +-- .msg.assistant    assistant bubbles (gray, left-aligned)
       |    +-- .typing           animated dots during send
       +-- .lead-form        conditional lead capture (name/company/email)
       +-- .input-area       textarea + send button
       +-- .panel-footer     branding + escalation link
```

## Session and Conversation Lifecycle

1. **Session ID**: stored in `localStorage` as `cloudru_widget_session`.
   Generated via `crypto.randomUUID()` with fallback to timestamp+random.
2. **Conversation**: created lazily on first `sendMessage()` call.
   One conversation per widget session (reused across messages).
3. **Lead capture**: triggered after 5+ user messages when `confidence > 0.7`
   and at least one architect or cost_calculator response exists.

## Authentication

- Widget sends `X-API-Key` header on every request
- Backend validates the key and resolves `tenant_id`
- No user authentication required (anonymous visitor)

## Technology Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Vanilla TypeScript | Zero dependencies, small bundle |
| Bundler | esbuild | Sub-second builds, IIFE output |
| Isolation | Shadow DOM (closed) | CSS cannot leak in or out |
| Styling | Embedded CSS string | No external stylesheet requests |
| State | Class instance fields | Simple, no framework overhead |
| Responsive | CSS `@media (max-width: 480px)` | Full-screen on mobile |
