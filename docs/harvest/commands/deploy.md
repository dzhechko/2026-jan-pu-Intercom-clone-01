# Command: /deploy

## Maturity: Alpha v1.0

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

---

## When to Use

- When deploying a tested and reviewed build to staging or production
- When performing a scheduled release after a feature freeze
- When hotfixing production and needing a fast, safe deploy with rollback
- As the final step in a CI/CD pipeline after all quality gates pass

## When NOT to Use

- For local development environment setup (use project-specific bootstrap scripts)
- When infrastructure changes are needed (new services, DB schema changes not covered by migrations) -- handle infrastructure provisioning separately first
- When deploying to environments not defined in the environment matrix
- During active incident response where manual control is preferred over automation

## Prerequisites

- Docker and Docker Compose installed on the deployment target
- SSH access to the deployment target (for remote deploys) or local Docker socket access
- Environment configuration file (`.env.staging` or `.env.production`) present on the target
- A working health check endpoint on each service being deployed
- Database migration tooling configured (e.g., Alembic, Flyway, Prisma Migrate)
- Previous deployment artifacts retained for rollback (at minimum, the prior Docker image tags)

## Command Specification

### Purpose

Execute a zero-downtime deployment of containerized services via Docker Compose, with pre-deploy quality gates, automated database migrations, health check verification, and automatic rollback on failure.

### Invocation

```
/deploy [environment]
```

Where `[environment]` is one of the configured targets (e.g., `staging`, `production`). Defaults to `staging` if omitted.

### Deployment Pipeline

```
Phase 1: Pre-Deploy Verification
  ├── Lint check
  ├── Security scan
  ├── Test suite (unit + integration)
  └── Docker image build verification

Phase 2: Deployment Execution
  ├── Snapshot current state (image tags, config hash)
  ├── Pull new images
  ├── Run database migrations
  ├── Restart services (rolling or recreate, per config)
  └── Wait for readiness

Phase 3: Post-Deploy Verification
  ├── Health check all services
  ├── Smoke test critical endpoints
  └── Verify migration state

Phase 4: Rollback (on failure only)
  ├── Restore previous image tags
  ├── Rollback database migration (if supported)
  ├── Restart services with previous config
  └── Health check after rollback
```

### Phase 1: Pre-Deploy Verification

All checks must pass before deployment proceeds. Any failure aborts the deploy.

| Check | Command (configurable) | Fail Condition |
|-------|----------------------|----------------|
| Lint | Project linter | Any error-level finding |
| Security | Project security scanner | Any high/critical severity |
| Tests | Project test runner | Any test failure |
| Build | `docker compose build` | Non-zero exit code |

For production deployments, an additional confirmation prompt is displayed:

```
WARNING: Deploying to PRODUCTION
  Branch: main
  Commit: abc1234
  Images: [list of services and tags]
  Confirm? [y/N]
```

### Phase 2: Deployment Execution

1. **Snapshot**: Record current image tags, compose file hash, and migration version. Store in `.deploy-state/[environment]/last-good.json`.

2. **Pull Images**: Execute `docker compose pull` for all services. On failure, abort without modifying running services.

3. **Run Migrations**: Execute the project's migration tool (e.g., `alembic upgrade head`). Migrations run inside a dedicated container with database access. If migration fails, abort and do NOT restart services.

4. **Restart Services**: Execute `docker compose up -d` with the appropriate strategy:
   - `rolling` (default for production): restart services one at a time with health check between each
   - `recreate` (default for staging): stop all, then start all

5. **Wait for Readiness**: Poll health check endpoints until all services report healthy or timeout is reached.

### Phase 3: Post-Deploy Verification

| Check | Method | Timeout |
|-------|--------|---------|
| Health endpoints | HTTP GET to each service's `/health` | 60s per service |
| Smoke tests | Configurable HTTP requests to critical endpoints | 30s per request |
| Migration state | Verify migration tool reports current version | 10s |

If any post-deploy check fails, proceed to Phase 4 (Rollback).

### Phase 4: Rollback

Triggered automatically when post-deploy verification fails.

1. **Restore Images**: Read previous image tags from `.deploy-state/[environment]/last-good.json` and update compose configuration.
2. **Rollback Migration**: If the migration tool supports downgrade (e.g., `alembic downgrade -1`), execute it. If not, log a warning -- manual intervention may be needed.
3. **Restart Services**: Bring up services with the previous configuration.
4. **Verify Rollback**: Run health checks again. If rollback also fails, alert and halt -- manual intervention required.

### Environment Matrix

| Environment | Strategy | Confirmation | Rollback | Notifications |
|-------------|----------|-------------|----------|---------------|
| staging | recreate | no | automatic | log only |
| production | rolling | required | automatic | alert channel |

Additional environments can be defined in the deploy configuration file.

### State Files

```
.deploy-state/
├── staging/
│   ├── last-good.json      # Snapshot of last successful deploy
│   ├── deploy-log.jsonl     # Append-only deploy history
│   └── current-version.txt  # Current deployed commit SHA
└── production/
    ├── last-good.json
    ├── deploy-log.jsonl
    └── current-version.txt
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `health_check_timeout` | `60` | Seconds to wait for health check per service |
| `health_check_interval` | `5` | Seconds between health check polls |
| `smoke_test_endpoints` | `[]` | List of URLs to hit after deploy for smoke testing |
| `rollback_on_failure` | `true` | Whether to auto-rollback on health check failure |
| `migration_command` | `alembic upgrade head` | Command to run database migrations |
| `rollback_migration_command` | `alembic downgrade -1` | Command to rollback one migration |
| `restart_strategy` | `{"staging": "recreate", "production": "rolling"}` | Per-environment restart strategy |
| `require_confirmation` | `{"staging": false, "production": true}` | Per-environment confirmation requirement |
| `notification_channel` | `null` | Webhook URL for deploy notifications |

## Variants

| Variant | Description |
|---------|-------------|
| `/deploy staging` | Deploy to staging with recreate strategy, no confirmation |
| `/deploy production` | Deploy to production with rolling strategy, requires confirmation |
| `/deploy --skip-checks` | Skip pre-deploy verification (use only for hotfixes with explicit justification) |
| `/deploy --dry-run` | Execute all phases except actual service restart; report what would happen |
| `/deploy --rollback` | Manually trigger rollback to the last known good state |
| `/deploy --status` | Show current deployment state for all environments |

## Gotchas

- **Migration irreversibility**: Not all database migrations can be rolled back (e.g., column drops, data transforms). Test migration rollback in staging before deploying to production. If a migration is irreversible, the rollback phase will skip the migration step and log a warning.
- **Image tag mutability**: If using `latest` or mutable tags, the snapshot may not accurately capture the previous state. Use immutable tags (commit SHA or semver) for reliable rollback.
- **Health check false positives**: A service may report healthy at the `/health` endpoint while having issues on other endpoints. Configure smoke tests for critical paths, not just the health endpoint.
- **Compose file drift**: If the `docker-compose.yml` has changed between the current and previous deploy, rollback may fail due to incompatible configuration. The snapshot includes the compose file hash to detect this.
- **Disk space**: Old images accumulate on the deployment target. Periodically run `docker system prune` to reclaim space. The deploy command does not auto-prune.
- **Concurrent deploys**: The command does not implement locking. Running two deploys simultaneously to the same environment will cause undefined behavior. Use a CI/CD system with deploy queuing for team environments.
- **Secrets rotation**: If secrets have changed between the snapshot and rollback, the rolled-back services may fail to authenticate. Ensure secret rotation is coordinated with deployments.

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-02 | Initial extraction. Docker Compose deploy with pre-checks, rolling restart, auto-rollback. |
