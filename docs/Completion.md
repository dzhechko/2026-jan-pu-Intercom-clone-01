# Completion — AI-Консультант Cloud.ru

## Deployment Plan

### Pre-Deployment Checklist

- [ ] All unit tests passing (pytest, coverage ≥ 80%)
- [ ] Integration tests passing (Docker Compose test environment)
- [ ] E2E smoke tests passing (Telegram bot responds, web widget loads)
- [ ] Security scan clean (no critical/high vulnerabilities — bandit, safety)
- [ ] Database migrations tested (Alembic up + down)
- [ ] Rollback procedure documented and tested
- [ ] Environment variables configured (.env.production)
- [ ] TLS certificate provisioned (Let's Encrypt via certbot)
- [ ] DNS configured (A record pointing to VPS)
- [ ] Monitoring dashboards ready (Grafana)
- [ ] Alerting rules configured (Telegram alerts)
- [ ] RAG corpus indexed (Qdrant collections populated)
- [ ] Telegram bot webhook set

### Deployment Sequence

```
1. Provision VPS
   └── VPS: AdminVPS or HOSTKEY, Moscow DC, 4vCPU/16GB/200GB SSD
   └── OS: Ubuntu 24.04 LTS
   └── Install: Docker Engine 25+, Docker Compose 2.24+

2. Initial Setup
   └── SSH hardening: key-only, disable password auth, fail2ban
   └── Firewall: ufw allow 22,80,443
   └── Clone repository: git clone <repo> /opt/ai-consultant
   └── Copy .env.production to /opt/ai-consultant/.env

3. Build & Deploy
   └── cd /opt/ai-consultant
   └── docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
   └── docker compose exec api alembic upgrade head
   └── docker compose exec api python scripts/seed_data.py  (initial tenant, agent configs)

4. Index RAG Corpus
   └── docker compose exec api python scripts/index_documents.py --source ./corpus/
   └── Verify: docker compose exec api python scripts/verify_rag.py

5. Configure Telegram Bot
   └── Set webhook: curl -F "url=https://api.domain/webhooks/telegram" \
       https://api.telegram.org/bot<TOKEN>/setWebhook
   └── Verify: curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo

6. TLS Setup
   └── certbot --nginx -d api.domain -d admin.domain
   └── Auto-renewal: systemctl enable certbot.timer

7. Smoke Tests
   └── curl https://api.domain/health → {"status": "ok"}
   └── Send test message to Telegram bot → response received
   └── Login to admin dashboard → metrics page loads
   └── Monitor logs: docker compose logs -f --tail=100

8. Post-Deploy Verification (30 minutes)
   └── Check error rates in Grafana
   └── Verify Telegram bot response time < 30s
   └── Confirm no unhandled exceptions in logs
   └── Test human escalation flow
```

### Rollback Procedure

```
Quick Rollback (< 5 minutes):
  1. docker compose down
  2. git checkout <previous-tag>
  3. docker compose up -d --build
  4. docker compose exec api alembic downgrade -1  (if migration needed)
  5. Verify: curl https://api.domain/health

Full Rollback (database restore):
  1. docker compose down
  2. Restore PostgreSQL: pg_restore -d ai_consultant backup_YYYYMMDD.dump
  3. Restore Qdrant: copy snapshot back to qdrant_data volume
  4. git checkout <previous-tag>
  5. docker compose up -d --build
  6. Verify all services
```

---

## CI/CD Configuration

### GitHub Actions Pipeline

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
      redis:
        image: redis:7
        ports: ['6379:6379']

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check .
      - run: ruff format --check .
      - run: pytest --cov=src --cov-report=xml -v
      - run: bandit -r src/ -ll

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - run: docker compose build
      - run: docker compose -f docker-compose.test.yml up --abort-on-container-exit

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /opt/ai-consultant
            git pull origin main
            docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
            docker compose exec -T api alembic upgrade head
            docker compose exec -T api python scripts/health_check.py
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        args: ['-ll', '-r', 'src/']
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: detect-private-key
      - id: trailing-whitespace
```

---

## Monitoring & Alerting

### Key Metrics

| Metric | Source | Threshold | Alert Channel |
|--------|--------|-----------|--------------|
| API response time (p99) | Prometheus | > 30s | Telegram |
| API error rate | Prometheus | > 2% | Telegram |
| LLM API latency (p95) | Custom metric | > 15s | Telegram |
| LLM API error rate | Custom metric | > 5% | Telegram |
| RAG search latency (p95) | Custom metric | > 3s | Telegram |
| CPU usage | cAdvisor | > 85% for 5min | Telegram |
| Memory usage | cAdvisor | > 90% | Telegram |
| Disk usage | Node Exporter | > 80% | Telegram |
| PostgreSQL connections | pg_stat | > 80% of max | Telegram |
| Qdrant memory | Qdrant metrics | > 80% | Telegram |
| Redis memory | Redis INFO | > 80% | Email |
| Consultation success rate | Custom metric | < 70% | Telegram |
| Human escalation rate | Custom metric | > 40% | Email |
| Daily consultation count | Custom metric | < 10 (anomaly) | Email |

### Health Check Endpoints

```
GET /health
  Response: { "status": "ok", "checks": {
    "database": "ok",
    "vector_db": "ok",
    "redis": "ok",
    "llm_api": "ok",
    "telegram_webhook": "ok"
  }}

GET /health/ready
  Response: { "ready": true }  // For load balancer

GET /metrics
  Response: Prometheus format metrics
```

---

## Logging Strategy

### Log Format

```json
{
  "timestamp": "2026-03-02T10:30:00.123Z",
  "level": "INFO",
  "service": "api",
  "module": "orchestrator",
  "event": "consultation_completed",
  "tenant_id": "uuid",
  "conversation_id": "uuid",
  "agent_type": "architect",
  "confidence": 0.85,
  "response_time_ms": 4200,
  "tokens_input": 1200,
  "tokens_output": 800,
  "rag_docs_retrieved": 5,
  "trace_id": "abc123"
}
```

### Log Levels

| Level | Usage | Examples |
|-------|-------|---------|
| DEBUG | Development only | RAG scores, prompt content, tool call details |
| INFO | Normal operations | Consultation started/completed, lead created, escalation |
| WARNING | Anomalies | Low confidence, stale pricing data, slow LLM response |
| ERROR | Failures | LLM API error, DB connection failure, tool call failure |
| CRITICAL | System down | All LLM providers failing, DB unreachable, disk full |

### Retention

| Storage | Retention | Purpose |
|---------|-----------|---------|
| Container stdout | 7 days (Docker log rotation) | Real-time debugging |
| Loki / log files | 90 days | Operational investigation |
| MinIO (archived) | 1 year | Compliance, audit |
| Anonymized | Permanent | Analytics, model improvement |

---

## Backup Strategy

| Data | Method | Frequency | Retention | Location |
|------|--------|-----------|-----------|----------|
| PostgreSQL | pg_dump → MinIO | Daily full + hourly WAL | 30 days | MinIO + offsite |
| Qdrant | Snapshot API → MinIO | Daily | 14 days | MinIO |
| Redis | RDB snapshot | Every 6 hours | 7 days | Local + MinIO |
| RAG corpus (source) | Git-tracked or MinIO | On change | Permanent | Git / MinIO |
| .env / secrets | Encrypted backup | On change | Permanent | Offsite encrypted |
| Docker volumes | Volume backup script | Weekly | 4 weeks | Offsite |

### Backup Verification

```bash
# Weekly automated restore test
#!/bin/bash
# scripts/backup_verify.sh
docker compose -f docker-compose.test.yml up -d postgres-test
pg_restore -d test_db -h localhost -p 5433 latest_backup.dump
python scripts/verify_data_integrity.py --db test_db
docker compose -f docker-compose.test.yml down -v
```

---

## Environment Configuration

### Required Environment Variables

```bash
# Application
APP_ENV=production          # development | staging | production
APP_DEBUG=false
APP_SECRET_KEY=<random-64-chars>
APP_BASE_URL=https://api.domain

# Database
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/ai_consultant
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Vector DB
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=<optional>

# Redis
REDIS_URL=redis://redis:6379/0

# LLM
ANTHROPIC_API_KEY=<key>
LLM_MODEL=claude-sonnet-4-6
LLM_FALLBACK_MODEL=claude-haiku-4-5-20251001
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.3

# Telegram
TELEGRAM_BOT_TOKEN=<token>
TELEGRAM_WEBHOOK_URL=https://api.domain/webhooks/telegram
TELEGRAM_WEBHOOK_SECRET=<random-32-chars>

# CRM (optional)
BITRIX24_WEBHOOK_URL=<url>
AMOCRM_API_KEY=<key>
AMOCRM_SUBDOMAIN=<subdomain>

# Monitoring
GRAFANA_ADMIN_PASSWORD=<password>

# MinIO
MINIO_ROOT_USER=<user>
MINIO_ROOT_PASSWORD=<password>
MINIO_URL=http://minio:9000
```

---

## Handoff Checklists

### For Development Team

- [ ] Repository access (GitHub)
- [ ] Development environment setup (Docker Compose dev profile)
- [ ] `.env.development` template
- [ ] Code review guidelines (PR template)
- [ ] Branch strategy: `main` (production), `develop` (staging), `feature/*`
- [ ] Architecture.md and Pseudocode.md read and understood
- [ ] MCP tool development guide
- [ ] Agent prompt engineering guide

### For QA Team

- [ ] Test environment access (staging VPS)
- [ ] Test data setup script (`scripts/seed_test_data.py`)
- [ ] Test Telegram bot (separate bot for staging)
- [ ] Bug reporting template (GitHub Issues)
- [ ] Gherkin scenarios in Refinement.md as test basis
- [ ] Performance test scripts (Locust)
- [ ] RAG quality testing procedure

### For Operations Team

- [ ] VPS SSH access
- [ ] Docker Compose commands cheat sheet
- [ ] Grafana dashboard access
- [ ] Alerting Telegram group membership
- [ ] Runbook: restart services
- [ ] Runbook: rollback deployment
- [ ] Runbook: restore from backup
- [ ] Runbook: scale resources (VPS upgrade)
- [ ] Runbook: RAG corpus update
- [ ] Escalation contacts (dev team Telegram group)

### For Cloud.ru Client Team

- [ ] Telegram bot link and access
- [ ] Admin dashboard credentials
- [ ] ROI metrics explanation
- [ ] Escalation SLA (human SA response time)
- [ ] Feedback mechanism (thumbs up/down in chat)
- [ ] Support contact for technical issues
- [ ] Pilot success criteria document
