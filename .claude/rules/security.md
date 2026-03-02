# Security Rules — AI-Консультант Cloud.ru

## Authentication & Authorization

- JWT tokens for admin dashboard (HS256, 1h expiry, refresh tokens 7d)
- API keys for external integrations (SHA-256 hashed in DB)
- Telegram webhook: validate X-Telegram-Bot-Api-Secret-Token header
- RBAC roles: admin, editor, viewer — enforce on every protected endpoint

## Input Validation

- All user input validated via Pydantic schemas before processing
- Message length limit: 4000 characters (truncate with notice)
- Content filtering before agent processing (offensive content)
- Webhook signature verification on all incoming webhooks
- No raw SQL — use SQLAlchemy ORM exclusively

## Data Protection

- TLS 1.3 for all external communications
- AES-256-GCM encryption for sensitive data at rest
- Multi-tenant isolation: ALL database queries MUST filter by `tenant_id`
- PII handling compliant with 152-ФЗ (Russian data protection law)
- Database in Russian DC (Moscow) — data sovereignty requirement

## Secrets Management

- All secrets in environment variables (never in code)
- `.env` files in `.gitignore` — never committed
- `.env.example` with placeholder values for documentation
- API keys rotatable without code changes
- Docker secrets for production deployment

## Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/conversations/*/messages` | 30 req | 60s per user |
| `/api/webhooks/telegram` | 100 req | 60s global |
| `/api/dashboard/*` | 60 req | 60s per user |
| `/api/auth/login` | 5 req | 60s per IP |
| Global | 1000 req | 60s |

## Security Headers (Nginx)

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

## Logging & Audit

- Log all authentication events (login, logout, failed attempts)
- Log all escalation events with full context
- Log rate limit violations with IP address
- Never log passwords, tokens, or API keys
- Structured JSON format for all logs
