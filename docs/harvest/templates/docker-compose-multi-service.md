# Template: Docker Compose Multi-Service Stack

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Docker Compose configuration for a full-stack application with: Python/FastAPI API backend, React frontend, PostgreSQL database, Redis cache, Qdrant vector database, MinIO object storage, and Nginx reverse proxy. All values are parameterized for reuse across projects.

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `{{PROJECT_NAME}}` | Project identifier used in service names and DB name | `my-app` |
| `{{API_PORT}}` | Port the API backend listens on | `8000` |
| `{{FRONTEND_PORT}}` | Port the frontend dev server listens on | `3000` |
| `{{DB_NAME}}` | PostgreSQL database name | `app_db` |
| `{{DB_USER}}` | PostgreSQL username | `app` |
| `{{DB_PASSWORD}}` | PostgreSQL password | `change_me_in_production` |
| `{{POSTGRES_VERSION}}` | PostgreSQL image tag | `16-alpine` |
| `{{REDIS_MAX_MEMORY}}` | Redis maximum memory allocation | `256mb` |
| `{{QDRANT_VERSION}}` | Qdrant image tag | `v1.12.1` |
| `{{NGINX_VERSION}}` | Nginx image tag | `1.27-alpine` |
| `{{MINIO_USER}}` | MinIO root username | `minioadmin` |
| `{{MINIO_PASSWORD}}` | MinIO root password | `change_me_in_production` |

## Template

```yaml
version: "3.9"

services:
  # === API Backend ===
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "{{API_PORT}}:{{API_PORT}}"
    environment:
      - DATABASE_URL=postgresql+asyncpg://{{DB_USER}}:{{DB_PASSWORD}}@postgres:5432/{{DB_NAME}}
      - REDIS_URL=redis://redis:6379/0
      - QDRANT_HOST=qdrant
      - QDRANT_PORT=6333
      - MINIO_ENDPOINT=minio:9000
      - MINIO_ROOT_USER={{MINIO_USER}}
      - MINIO_ROOT_PASSWORD={{MINIO_PASSWORD}}
    env_file:
      - .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      qdrant:
        condition: service_started
    networks:
      - backend
      - frontend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{{API_PORT}}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s

  # === Frontend ===
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "{{FRONTEND_PORT}}:{{FRONTEND_PORT}}"
    environment:
      - VITE_API_URL=http://api:{{API_PORT}}
    depends_on:
      - api
    networks:
      - frontend
    restart: unless-stopped

  # === PostgreSQL ===
  postgres:
    image: postgres:{{POSTGRES_VERSION}}
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: {{DB_NAME}}
      POSTGRES_USER: {{DB_USER}}
      POSTGRES_PASSWORD: {{DB_PASSWORD}}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U {{DB_USER}} -d {{DB_NAME}}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # === Qdrant Vector Database ===
  qdrant:
    image: qdrant/qdrant:{{QDRANT_VERSION}}
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - backend
    restart: unless-stopped

  # === Redis ===
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes --maxmemory {{REDIS_MAX_MEMORY}} --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # === MinIO Object Storage ===
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: {{MINIO_USER}}
      MINIO_ROOT_PASSWORD: {{MINIO_PASSWORD}}
    volumes:
      - minio_data:/data
    networks:
      - backend
    restart: unless-stopped

  # === Nginx Reverse Proxy ===
  nginx:
    image: nginx:{{NGINX_VERSION}}
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
      - frontend
    networks:
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
  qdrant_data:
  redis_data:
  minio_data:

networks:
  backend:
    driver: bridge
  frontend:
    driver: bridge
```

## Usage

1. Copy this template into your project root as `docker-compose.yml`.
2. Replace all `{{PLACEHOLDER}}` values with your project-specific settings.
3. Create an `.env` file for secrets that should not be in the compose file.
4. Create the `nginx/nginx.conf` file (see the Nginx reverse proxy template).
5. Run `docker compose up -d`.

## Notes

- The `backend` network isolates database, cache, and vector DB traffic from the public-facing `frontend` network.
- Health checks ensure services start in dependency order. The API waits for PostgreSQL and Redis to be healthy.
- Qdrant uses `service_started` rather than a health check because Qdrant does not ship with a CLI health probe by default. For stricter checks, add a curl-based health check against `http://qdrant:6333/healthz`.
- MinIO console is accessible at port 9001 for development. Remove or restrict in production.
- For production, move secrets out of `environment` blocks and into Docker secrets or a dedicated secret manager.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
