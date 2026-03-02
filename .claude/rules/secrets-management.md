# Secrets Management Rules

## Environment Variables

All secrets MUST be stored in environment variables, never in code.

### Required Variables

```bash
# LLM
ANTHROPIC_API_KEY=           # Claude API key
LLM_MODEL=claude-sonnet-4-20250514     # Default model
LLM_FALLBACK_MODEL=          # Fallback (optional)

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/cloud_consultant
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://redis:6379/0

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_API_KEY=              # If auth enabled

# Telegram
TELEGRAM_BOT_TOKEN=          # Bot token from @BotFather
TELEGRAM_WEBHOOK_SECRET=     # Webhook signature secret
TELEGRAM_WEBHOOK_URL=        # Public URL for webhook

# Auth
JWT_SECRET_KEY=              # HS256 signing key (min 32 chars)
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# MinIO
MINIO_ROOT_USER=
MINIO_ROOT_PASSWORD=
MINIO_ENDPOINT=minio:9000

# CRM Integration (optional)
BITRIX24_WEBHOOK_URL=
AMOCRM_API_KEY=

# Monitoring
SENTRY_DSN=                  # Error tracking (optional)
```

## File Rules

| File | Purpose | Git Status |
|------|---------|------------|
| `.env` | Actual secrets | **NEVER commit** (in .gitignore) |
| `.env.example` | Template with placeholders | Committed |
| `.env.staging` | Staging overrides | **NEVER commit** |
| `.env.production` | Production overrides | **NEVER commit** |

## Security Practices

1. **Rotation**: API keys must be rotatable without code deployment
2. **Minimum privilege**: Each service gets only the keys it needs
3. **No defaults**: Never ship default passwords or keys
4. **Audit**: Log when secrets are accessed (not the values)
5. **Docker**: Use Docker secrets for production, env vars for dev

## Validation

```python
# Use pydantic-settings for config validation
class Settings(BaseSettings):
    anthropic_api_key: str
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = Field(min_length=32)

    model_config = SettingsConfigDict(env_file=".env")
```

## What Gets Flagged

The code-reviewer agent will flag:
- Hardcoded API keys or tokens in source code
- `.env` files in git staging area
- Default/weak JWT secrets
- Secrets logged or included in error messages
- API keys passed as URL parameters
