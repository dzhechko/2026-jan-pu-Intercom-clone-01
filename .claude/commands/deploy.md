# /deploy $ARGUMENTS — Deployment Workflow

## Usage

- `/deploy` — deploy to staging (default)
- `/deploy staging` — deploy to staging VPS
- `/deploy production` — deploy to production VPS
- `/deploy rollback` — rollback to previous version

## Pre-Deploy Checks

1. Run test suite: `pytest tests/ -v --cov=src --cov-fail-under=80`
2. Run linting: `ruff check . && ruff format --check .`
3. Run security scan: `bandit -r src/ -ll`
4. Verify Docker build: `docker compose build`
5. Check environment variables against `.env.example`

## Deploy Steps

### Staging

```bash
# 1. Build images
docker compose -f docker-compose.yml -f docker-compose.staging.yml build

# 2. Run migrations
docker compose exec api alembic upgrade head

# 3. Deploy
docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d

# 4. Health check
curl -f https://staging.api.example.com/health/ready

# 5. Smoke test
pytest tests/e2e/test_consultation_flow.py -v --env=staging
```

### Production

```bash
# 1. Tag release
git tag -a v$(date +%Y%m%d-%H%M) -m "Release $(date +%Y%m%d-%H%M)"

# 2. Build images
docker compose -f docker-compose.yml -f docker-compose.prod.yml build

# 3. Backup database
docker compose exec postgres pg_dump -U app cloud_consultant > backup_$(date +%Y%m%d).sql

# 4. Run migrations
docker compose exec api alembic upgrade head

# 5. Rolling deploy
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --no-deps api

# 6. Health check (wait 30s for startup)
sleep 30 && curl -f https://api.example.com/health/ready

# 7. Verify metrics
curl -s https://api.example.com/metrics | grep response_time_p99
```

### Rollback

```bash
# Quick rollback (last working image)
docker compose -f docker-compose.yml -f docker-compose.prod.yml down api
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d api --no-deps

# Full rollback (with DB)
alembic downgrade -1
docker compose up -d
```

## Environment Matrix

| Variable | Staging | Production |
|----------|---------|------------|
| `DEBUG` | true | false |
| `LOG_LEVEL` | DEBUG | INFO |
| `RATE_LIMIT_PER_MIN` | 100 | 30 |
| `LLM_MODEL` | claude-sonnet | claude-sonnet |
| `DB_POOL_SIZE` | 5 | 20 |
