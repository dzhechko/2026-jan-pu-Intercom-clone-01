# Refinement -- Web Chat Widget

## Edge Cases and Mitigations

### 1. CORS (Cross-Origin Resource Sharing)

| Risk | The widget runs on `cloud.ru` but calls `api.cloud-ru-ai.ru` |
|------|--------------------------------------------------------------|
| Mitigation | Backend must return `Access-Control-Allow-Origin` for allowed domains. Nginx config should include `Access-Control-Allow-Headers: Content-Type, X-API-Key`. Preflight OPTIONS must be handled. |
| Test | Integration test: send request from different origin, verify 200 not 403. |

### 2. CSP (Content Security Policy) Headers

| Risk | Host page CSP may block inline scripts or fetch to API domain |
|------|--------------------------------------------------------------|
| Mitigation | Document required CSP directives for customers: `script-src` must allow the CDN domain, `connect-src` must allow the API domain. Widget uses no `eval()` or inline event handlers. Shadow DOM styles are injected via DOM API, not inline `style` attributes. |
| Customer guidance | `script-src https://cdn.cloud-ru-ai.ru; connect-src https://api.cloud-ru-ai.ru` |

### 3. Mobile Responsive

| Risk | 380x520px panel is unusable on small screens |
|------|----------------------------------------------|
| Mitigation | `@media (max-width: 480px)` makes panel full-viewport (`100vw x 100vh`, no border-radius). Textarea has `max-height: 100px` to prevent keyboard overlap. Touch targets are 36px+ (WCAG minimum 44px recommended -- flagged for v2.0). |
| Test | Verify panel dimensions at 375px viewport width. |

### 4. Offline State / Network Errors

| Risk | API unreachable, slow network, or timeout |
|------|------------------------------------------|
| Mitigation | `sendMessage()` catches all fetch errors and renders a fallback error message ("Sorry, an error occurred. Please try again.") instead of crashing. `isSending` flag prevents duplicate submissions. No retry logic yet -- queued for v2.0. |
| Gap | No offline detection (`navigator.onLine`). No request timeout (relies on browser default). Both are v2.0 items. |

### 5. Widget Collision with Host Page

| Risk | Host page CSS or JS interferes with widget rendering |
|------|-----------------------------------------------------|
| Mitigation | Closed Shadow DOM (`mode: "closed"`) prevents all CSS inheritance. `:host { all: initial }` resets every inherited property. Widget uses a unique element ID (`cloudru-chat-widget`). No global event listeners that could conflict with the host page. |
| Remaining risk | Host page `z-index` wars -- widget uses `z-index: 999999`. A host element with higher z-index will cover the widget. |

### 6. Multiple Widget Instances

| Risk | Customer accidentally embeds the script twice |
|------|-----------------------------------------------|
| Mitigation | Host element has a fixed ID. Second `init()` call would create a duplicate. Not currently guarded -- add an ID-existence check in v2.0. |

### 7. localStorage Unavailable

| Risk | Incognito mode or disabled storage |
|------|-----------------------------------|
| Mitigation | `getOrCreateSessionId()` should wrap `localStorage` in try/catch. Currently unhandled -- session ID would be regenerated on each page load. Non-critical: conversation still works, just loses session continuity. |

### 8. XSS via Message Content

| Risk | Malicious content in assistant response rendered as HTML |
|------|--------------------------------------------------------|
| Mitigation | `escapeHtml()` uses `textContent` assignment on a detached `<div>`, then reads `innerHTML`. All user and assistant text is escaped before injection. Source URLs are also escaped. |

### 9. Message Length Limits

| Risk | User sends extremely long messages |
|------|-----------------------------------|
| Mitigation | Client-side: `textarea.maxLength = 4000`. Server-side: Pydantic `max_length=10000`. Server is the authoritative boundary. |

## Open Items for v2.0

- WebSocket streaming for real-time token delivery
- Feedback buttons (thumbs up/down) on assistant messages
- Offline queue with automatic retry
- `navigator.onLine` detection with UI indicator
- Touch target WCAG compliance (44px minimum)
- Duplicate widget instance guard
- localStorage unavailability graceful fallback
