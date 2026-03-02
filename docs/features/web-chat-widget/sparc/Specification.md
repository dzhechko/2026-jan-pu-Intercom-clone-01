# Specification -- Web Chat Widget

## Embed Snippet

```html
<script>
  window.CHATWIDGET_CONFIG = {
    apiKey: 'YOUR_API_KEY',
    apiUrl: 'https://api.cloud-ru-ai.ru',
  };
</script>
<script src="https://cdn.cloud-ru-ai.ru/widget.js" async defer></script>
```

## Configuration Options (ChatWidgetConfig)

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `apiKey` | string | yes | -- | API key for X-API-Key header |
| `apiUrl` | string | yes | -- | Backend base URL (trailing slashes stripped) |
| `tenantId` | string | no | -- | Multi-tenant identifier |
| `position` | `"bottom-right"` / `"bottom-left"` | no | `"bottom-right"` | Bubble placement |
| `greeting` | string | no | Russian default greeting | First assistant message on open |
| `proactive.enabled` | boolean | no | false | Show proactive engagement popup |
| `proactive.delayMs` | number | no | 60000 | Milliseconds before proactive fires |
| `proactive.message` | string | no | Cost help prompt (Russian) | Proactive popup text |
| `theme.primaryColor` | string | no | `#2563eb` | Brand color |
| `theme.headerTitle` | string | no | `"Cloud.ru Assistant"` | Panel header title |

## Programmatic API

```typescript
// Auto-init: set window.CHATWIDGET_CONFIG before script loads
// Manual init:
const widget = window.CloudRuWidget.init({ apiKey, apiUrl });
widget.destroy(); // remove widget from DOM, clear timers
```

## REST Endpoints Used

| Method | Path | Body | Response |
|--------|------|------|----------|
| POST | `/api/v1/conversations` | `{ channel: "web_widget", channel_user_id, initial_message? }` | `ConversationData` |
| POST | `/api/v1/conversations/:id/messages` | `{ content, role: "user" }` | `SendMessageResult` |

## Message Schema (TypeScript)

```typescript
interface SendMessageResult {
  user_message: { id: string; content: string; role: string; created_at: string };
  assistant_response: {
    id: string;
    content: string;
    agent_type: string | null;  // architect, cost_calculator, compliance, etc.
    confidence: number;
    sources: { title: string; url: string }[];
    created_at: string;
  };
  response_time_ms: number;
}
```

## Backend Schema Constraints (Pydantic)

- `channel`: regex `^(telegram|web_widget|crm)$`
- `content`: max_length 10000 (server), 4000 (client textarea)
- `role`: regex `^user$` (only user role accepted from clients)

## Build Output

- Bundle: `dist/widget.js` (IIFE, ES2020, ~17KB minified)
- Build tool: esbuild (`npm run build`)
- Zero runtime dependencies (vanilla TypeScript)
