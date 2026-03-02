# Template: .env.example for Multi-Service Applications

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Comprehensive `.env.example` template organized by service domain. Covers LLM API keys, database, cache, vector database, authentication (JWT), object storage, external API integrations, and monitoring. All values are placeholders with descriptive comments. This file is committed to version control; the actual `.env` file with real secrets is not.

## Template

```bash
# ==============================================================================
# Environment Configuration Template
# ==============================================================================
# Copy this file to .env and fill in the values.
# NEVER commit the .env file to version control.
# ==============================================================================

# === LLM / AI API ===
# Primary LLM provider API key
LLM_API_KEY=your-api-key-here
# Model identifier for primary LLM
LLM_MODEL=claude-sonnet-4-20250514
# Fallback model (optional, used when primary is unavailable)
LLM_FALLBACK_MODEL=
# Maximum tokens per LLM request
LLM_MAX_TOKENS=4096

# === Database (PostgreSQL) ===
# Async connection string: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL=postgresql+asyncpg://app:change_me@postgres:5432/app_db
# Connection pool size (number of persistent connections)
DB_POOL_SIZE=20
# Max overflow connections beyond pool_size
DB_MAX_OVERFLOW=10

# === Cache (Redis) ===
# Redis connection URL
REDIS_URL=redis://redis:6379/0

# === Vector Database (Qdrant) ===
# Qdrant server hostname
QDRANT_HOST=qdrant
# Qdrant gRPC/HTTP port
QDRANT_PORT=6333
# Qdrant API key (leave empty if auth is disabled)
QDRANT_API_KEY=

# === Authentication (JWT) ===
# HMAC signing key for JWT tokens (minimum 32 characters)
JWT_SECRET_KEY=change-me-to-at-least-32-characters-long-secret
# JWT signing algorithm
JWT_ALGORITHM=HS256
# Access token expiry in minutes
JWT_EXPIRE_MINUTES=60
# Refresh token expiry in days (optional)
JWT_REFRESH_EXPIRE_DAYS=7

# === Object Storage (S3-compatible / MinIO) ===
# MinIO or S3-compatible endpoint
MINIO_ENDPOINT=minio:9000
# Root username for MinIO
MINIO_ROOT_USER=minioadmin
# Root password for MinIO
MINIO_ROOT_PASSWORD=change_me_in_production
# Default bucket name
MINIO_BUCKET=uploads

# === External APIs (optional) ===
# Messaging platform bot token
MESSAGING_BOT_TOKEN=
# Webhook signature verification secret
WEBHOOK_SECRET=
# Public URL for incoming webhooks
WEBHOOK_URL=https://your-domain.com/api/webhooks/incoming
# CRM integration webhook URL
CRM_WEBHOOK_URL=
# CRM API key
CRM_API_KEY=

# === Monitoring (optional) ===
# Error tracking DSN (e.g., Sentry)
SENTRY_DSN=
# Application log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# === Application Settings ===
# Enable debug mode (never true in production)
DEBUG=false
# Rate limit: max requests per minute per user
RATE_LIMIT_PER_MIN=30
# CORS allowed origins (JSON array)
CORS_ORIGINS=["http://localhost:3000"]
# Application environment: development, staging, production
APP_ENV=development
```

## Usage

1. Copy this template into your project root as `.env.example`.
2. Ensure `.env` is listed in your `.gitignore`.
3. Developers copy `.env.example` to `.env` and fill in their local values.
4. For CI/CD, inject environment variables from your secret manager rather than using `.env` files.

## Notes

- Group variables by service domain for readability. Each section is self-contained.
- Every variable includes a comment explaining its purpose. This serves as inline documentation for new team members.
- The `DATABASE_URL` uses the `asyncpg` dialect for async SQLAlchemy. Change to `psycopg2` if using synchronous SQLAlchemy.
- Secrets like `JWT_SECRET_KEY` and `MINIO_ROOT_PASSWORD` have obviously-fake placeholder values to remind developers to change them.
- The `CORS_ORIGINS` value is a JSON array string. Your application config should parse it accordingly.
- For production deployments, consider using Docker secrets, Vault, or cloud provider secret managers instead of `.env` files.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
