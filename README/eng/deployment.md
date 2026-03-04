# Deployment Guide

## System Requirements

### Minimum (Development / Pilot)

| Resource | Specification |
|----------|---------------|
| OS | Ubuntu 24.04 LTS |
| CPU | 4 vCPU |
| RAM | 16 GB |
| Storage | 200 GB SSD |
| Docker | 25+ |
| Docker Compose | 2.24+ |
| Network | Static IP, ports 80 and 443 open |

### Recommended (Production)

| Resource | Specification |
|----------|---------------|
| OS | Ubuntu 24.04 LTS |
| CPU | 8 vCPU |
| RAM | 32 GB |
| Storage | 500 GB NVMe SSD |
| Docker | 25+ |
| Docker Compose | 2.24+ |
| Network | Static IP, domain with DNS A-record |

### 152-FZ Compliance Requirement

The server **must** be located in a Moscow data center (or another Russian DC) to comply with Federal Law 152-FZ on personal data. Recommended VPS providers: AdminVPS, HOSTKEY, Selectel.

---

## Quick Start (Development)

```bash
# 1. Clone the repository
git clone <repo-url> cloud-consultant
cd cloud-consultant

# 2. Copy and configure environment variables
cp .env.example .env
# Edit .env — set at least ANTHROPIC_API_KEY and JWT_SECRET_KEY

# 3. Start all services
docker compose up -d

# 4. Verify services are running
docker compose ps

# 5. Run database migrations
docker compose exec api alembic upgrade head

# 6. Verify API health
curl http://localhost:8001/health
```

After startup, the following services are available:

| Service | URL |
|---------|-----|
| API (Swagger docs) | http://localhost:8001/docs |
| Admin Dashboard | http://localhost:3000 |
| MinIO Console | http://localhost:9001 |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

## Database Initialization

### Using Alembic (Recommended)

```bash
# Apply all migrations
docker compose exec api alembic upgrade head

# Check current migration version
docker compose exec api alembic current

# Generate a new migration after model changes
docker compose exec api alembic revision --autogenerate -m "description"
```

### Using SQLAlchemy create_all (Development Only)

If Alembic migrations are not yet set up, you can create tables directly:

```bash
docker compose exec api python -c "
from src.models.base import Base
from src.core.database import engine
import asyncio

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())
"
```

### Seed Data

```bash
# Run seed script to populate demo data
docker compose exec api python scripts/seed.py
```

---

## Environment Variables Reference

Copy `.env.example` to `.env` and configure the following variables:

### LLM Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | - | Anthropic API key for Claude |
| `LLM_MODEL` | No | `claude-sonnet-4-20250514` | Primary LLM model |
| `LLM_FALLBACK_MODEL` | No | - | Fallback model (e.g., GigaChat) |

### Database

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `postgresql+asyncpg://app:app_secret@postgres:5432/cloud_consultant` | PostgreSQL connection string |
| `DB_POOL_SIZE` | No | `20` | Connection pool size |
| `DB_MAX_OVERFLOW` | No | `10` | Maximum overflow connections |

### Redis

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REDIS_URL` | No | `redis://redis:6379/0` | Redis connection URL |

### Qdrant

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `QDRANT_HOST` | No | `qdrant` | Qdrant hostname |
| `QDRANT_PORT` | No | `6333` | Qdrant HTTP port |
| `QDRANT_API_KEY` | No | - | Qdrant API key (if auth enabled) |

### Telegram

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes* | - | Bot token from @BotFather |
| `TELEGRAM_WEBHOOK_SECRET` | Yes* | - | Webhook validation secret |
| `TELEGRAM_WEBHOOK_URL` | Yes* | - | Public HTTPS URL for the webhook |

*Required only if the Telegram channel is enabled.

### Authentication

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JWT_SECRET_KEY` | Yes | - | Signing key (minimum 32 characters) |
| `JWT_ALGORITHM` | No | `HS256` | JWT algorithm |
| `JWT_EXPIRE_MINUTES` | No | `60` | Token expiration in minutes |

### MinIO

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MINIO_ROOT_USER` | No | `minioadmin` | MinIO admin username |
| `MINIO_ROOT_PASSWORD` | No | `minioadmin` | MinIO admin password |
| `MINIO_ENDPOINT` | No | `minio:9000` | MinIO endpoint |

### CRM Integration (Optional)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BITRIX24_WEBHOOK_URL` | No | - | Bitrix24 incoming webhook URL |
| `AMOCRM_API_KEY` | No | - | amoCRM API key |

### Application

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DEBUG` | No | `false` | Enable debug mode |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `RATE_LIMIT_PER_MIN` | No | `30` | API rate limit per user per minute |
| `CORS_ORIGINS` | No | `["http://localhost:3000"]` | Allowed CORS origins (JSON array) |
| `SENTRY_DSN` | No | - | Sentry error tracking DSN |

---

## Production Deployment with TLS

### 1. Configure DNS

Point your domain (e.g., `consultant.example.com`) to the server's IP address via an A-record.

### 2. Install Certbot and obtain certificates

```bash
sudo apt update && sudo apt install -y certbot
sudo certbot certonly --standalone -d consultant.example.com
```

### 3. Configure Nginx

Edit `nginx/nginx.conf` to use the obtained certificates:

```nginx
server {
    listen 443 ssl http2;
    server_name consultant.example.com;

    ssl_certificate /etc/letsencrypt/live/consultant.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/consultant.example.com/privkey.pem;
    ssl_protocols TLSv1.3;

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    location /api/ {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://admin:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name consultant.example.com;
    return 301 https://$host$request_uri;
}
```

### 4. Mount certificates in docker-compose

Update the nginx volumes in `docker-compose.yml`:

```yaml
nginx:
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - /etc/letsencrypt:/etc/letsencrypt:ro
  ports:
    - "80:80"
    - "443:443"
```

### 5. Set up certificate auto-renewal

```bash
# Add cron job for automatic renewal
echo "0 3 * * * certbot renew --quiet && docker compose restart nginx" | sudo crontab -
```

---

## Update Procedure

```bash
# 1. Pull latest code
cd /path/to/cloud-consultant
git pull origin main

# 2. Rebuild and restart containers
docker compose up -d --build

# 3. Run database migrations
docker compose exec api alembic upgrade head

# 4. Verify health
curl https://consultant.example.com/health
curl https://consultant.example.com/health/ready
```

---

## Rollback Procedure

```bash
# 1. Stop current containers
docker compose down

# 2. Check out previous version
git checkout <previous-tag-or-commit>

# 3. Rebuild and start
docker compose up -d --build

# 4. Rollback database if needed
docker compose exec api alembic downgrade -1

# 5. Verify
curl https://consultant.example.com/health
```

---

## Backup and Restore

### PostgreSQL

```bash
# Backup
docker compose exec postgres pg_dump -U app cloud_consultant > backup_$(date +%Y%m%d).sql

# Restore
docker compose exec -T postgres psql -U app cloud_consultant < backup_20260301.sql
```

### Qdrant

```bash
# Create snapshot
curl -X POST http://localhost:6333/snapshots

# List snapshots
curl http://localhost:6333/snapshots
```

### Full backup script

```bash
#!/bin/bash
BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# PostgreSQL
docker compose exec -T postgres pg_dump -U app cloud_consultant > "$BACKUP_DIR/postgres.sql"

# Qdrant snapshot
curl -s -X POST http://localhost:6333/snapshots

# Redis
docker compose exec redis redis-cli BGSAVE

echo "Backup completed: $BACKUP_DIR"
```

---

## Health Checks

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Basic liveness check (API is responding) |
| `GET /health/ready` | Readiness check (all dependencies connected) |

```bash
# Quick health verification
curl -s http://localhost:8001/health | python3 -m json.tool

# Check all container statuses
docker compose ps

# View API logs
docker compose logs api --tail 50

# View all logs
docker compose logs --tail 100
```
