# Administrator Guide

## Logging In

### Development Environment

Open the admin dashboard at `http://localhost:3000` and log in with the default credentials:

| Field | Value |
|-------|-------|
| Email | `admin@cloud.ru` |
| Password | `admin123admin` |

After login, you receive a JWT token (valid for 60 minutes by default). The dashboard stores it automatically and refreshes as needed.

### Production Environment

In production, set the `ADMIN_PASSWORD_HASH` environment variable to a bcrypt hash of your chosen password. The default development password will be disabled when this variable is configured.

Generate a password hash:

```bash
python3 -c "from passlib.hash import bcrypt; print(bcrypt.hash('your-secure-password'))"
```

---

## Dashboard Overview

The main dashboard (`/`) displays key performance metrics for the selected time period (today, 7 days, or 30 days).

### Metric Cards

| Metric | Description |
|--------|-------------|
| Total Consultations | Number of AI-handled conversations in the period |
| Leads Generated | Qualified leads extracted from consultations |
| Avg Response Time | Mean response latency in milliseconds |
| Escalation Rate | Percentage of conversations escalated to a human SA |
| Satisfaction Score | Average user satisfaction rating (0.00 - 5.00) |
| Conversion Rate | Ratio of leads generated to total consultations |

### Daily Trend Chart

A line chart showing the number of consultations and leads per day over the selected period. Use this to spot usage patterns and growth trends.

### Top Intents Bar Chart

Displays the five most frequent user intents (e.g., architecture review, cost estimation, compliance check) with their percentage share.

---

## Managing Conversations

Navigate to `/conversations` to view all conversations in a paginated table.

### Conversation Fields

| Column | Description |
|--------|-------------|
| ID | Unique conversation identifier (UUID) |
| Channel | Source channel: `telegram`, `web_widget`, or `crm` |
| Status | `active`, `completed`, `escalated`, or `archived` |
| Intent | Detected user intent (from context) |
| Created At | Timestamp of conversation start |

### Filtering

Use the page controls to navigate through conversations. The table shows 20 items per page by default.

---

## Managing Leads

Navigate to `/leads` to view qualified leads extracted from conversations.

### Lead Fields

| Column | Description |
|--------|-------------|
| Contact | Contact information (name, email, phone) stored as JSON |
| Qualification | Lead status: `cold`, `warm`, `hot`, or `qualified` |
| Intent | The primary intent that generated the lead |
| Estimated Deal Value | Projected deal amount in rubles |
| Created At | When the lead was first identified |

Leads are automatically created by the orchestrator when a conversation meets qualification criteria (company name mentioned, budget discussed, timeline established).

---

## Agent Configuration

Agents are configured through two mechanisms:

### 1. System Prompt Files

Each agent has a markdown prompt file in `prompts/`:

| Agent | File |
|-------|------|
| Architect | `prompts/architect.md` |
| Cost Calculator | `prompts/cost_calculator.md` |
| Compliance (152-FZ) | `prompts/compliance.md` |
| Migration | `prompts/migration.md` |
| AI Factory | `prompts/ai_factory.md` |
| Human Escalation | `prompts/human_escalation.md` |

To modify an agent's behavior, edit the corresponding prompt file and restart the API service:

```bash
docker compose restart api
```

### 2. Database Configuration (Per-Tenant)

The `agent_configs` table stores per-tenant overrides:

| Field | Description |
|-------|-------------|
| `agent_type` | Agent identifier (e.g., `architect`, `cost_calculator`) |
| `system_prompt` | Override prompt text (if null, uses the file-based prompt) |
| `confidence_threshold` | Minimum confidence to respond without escalation (default: 0.60) |
| `max_turns` | Maximum conversation turns before auto-escalation (default: 20) |
| `rag_collections` | Array of Qdrant collection names for RAG retrieval |
| `tools` | Array of MCP tool names available to this agent |
| `enabled` | Whether the agent is active for this tenant |

### Adding a New Agent

1. Create a prompt file: `prompts/new_agent.md`
2. Insert a row into `agent_configs` for each tenant that should use the agent
3. Register the agent type in the orchestrator routing table
4. Restart the API

---

## System Monitoring

### Health Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Basic liveness (API process running) |
| `GET /health/ready` | Readiness (PostgreSQL, Redis, Qdrant connected) |

### Docker Container Status

```bash
# Overview of all containers
docker compose ps

# CPU and memory usage
docker stats --no-stream

# API logs (last 100 lines)
docker compose logs api --tail 100

# Follow API logs in real time
docker compose logs api -f

# PostgreSQL logs
docker compose logs postgres --tail 50

# Qdrant logs
docker compose logs qdrant --tail 50
```

### Key Metrics to Monitor

| Metric | Warning Threshold | Critical Threshold |
|--------|-------------------|-------------------|
| API response time | > 5 seconds | > 30 seconds |
| Error rate | > 1% | > 5% |
| Disk usage | > 70% | > 85% |
| Memory usage | > 80% | > 90% |
| PostgreSQL connections | > 80% of pool | > 95% of pool |

---

## Backup and Restore

### PostgreSQL Backup

```bash
# Full database backup
docker compose exec -T postgres pg_dump -U app cloud_consultant > backup.sql

# Compressed backup
docker compose exec -T postgres pg_dump -U app -Fc cloud_consultant > backup.dump

# Restore from SQL
docker compose exec -T postgres psql -U app cloud_consultant < backup.sql

# Restore from compressed
docker compose exec -T postgres pg_restore -U app -d cloud_consultant backup.dump
```

### Qdrant Snapshots

```bash
# Create snapshot of all collections
curl -X POST http://localhost:6333/snapshots

# List available snapshots
curl http://localhost:6333/snapshots

# Restore from snapshot (see Qdrant documentation for full procedure)
```

### Automated Backup Schedule

Set up a cron job for daily backups:

```bash
# Daily backup at 2:00 AM
0 2 * * * cd /path/to/project && docker compose exec -T postgres pg_dump -U app cloud_consultant > /backups/pg_$(date +\%Y\%m\%d).sql
```

Recommended backup retention: keep daily backups for 7 days, weekly backups for 4 weeks, monthly backups for 12 months.

---

## Troubleshooting

### API Does Not Start

**Symptoms:** Container exits immediately or health check fails.

1. Check logs: `docker compose logs api --tail 50`
2. Verify `.env` file exists and has required variables
3. Ensure PostgreSQL is healthy: `docker compose exec postgres pg_isready -U app`
4. Ensure Redis is healthy: `docker compose exec redis redis-cli ping`

### Database Connection Errors

**Symptoms:** `ECONNREFUSED` or `connection refused` on port 5432.

1. Check PostgreSQL container status: `docker compose ps postgres`
2. Verify `DATABASE_URL` matches the PostgreSQL service configuration
3. Check if the database exists: `docker compose exec postgres psql -U app -l`
4. Review connection pool settings (`DB_POOL_SIZE`, `DB_MAX_OVERFLOW`)

### Qdrant Search Returns Empty Results

1. Verify collections exist: `curl http://localhost:6333/collections`
2. Check collection point count: `curl http://localhost:6333/collections/{name}`
3. Re-index documents: `docker compose exec api python scripts/index.py`

### Admin Dashboard Shows No Data

1. Confirm the API is reachable from the browser (check CORS settings)
2. Verify `VITE_API_URL` in `admin/.env` points to the correct API URL
3. Check that seed data has been loaded or that real data exists
4. Open browser developer tools and inspect network requests for errors

### Telegram Bot Not Responding

1. Verify `TELEGRAM_BOT_TOKEN` is set correctly
2. Check that `TELEGRAM_WEBHOOK_URL` is publicly accessible over HTTPS
3. Confirm the webhook is registered: check API logs for webhook setup
4. Test manually: `curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`

### High Memory Usage

1. Check Redis memory: `docker compose exec redis redis-cli INFO memory`
2. Review Qdrant memory: `docker stats qdrant`
3. Reduce `DB_POOL_SIZE` if PostgreSQL is consuming excess memory
4. Consider increasing server RAM if usage exceeds 80% consistently
