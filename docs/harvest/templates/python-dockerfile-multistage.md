# Template: Multi-Stage Python Dockerfile

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Multi-stage Dockerfile for Python applications. The builder stage installs dependencies (including compiled C extensions like asyncpg and bcrypt). The runtime stage copies only the installed packages and application code, runs as a non-root user, and includes a health check endpoint.

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `{{PYTHON_VERSION}}` | Python base image tag | `3.12-slim` |
| `{{APP_PORT}}` | Port the application listens on | `8000` |
| `{{WORKERS}}` | Number of uvicorn worker processes | `4` |
| `{{ENTRY_MODULE}}` | Python module path for the ASGI app | `src.api.main:app` |
| `{{APP_DIRS}}` | Application source directories to copy (space-separated COPY lines) | `src/`, `alembic/` |
| `{{REQUIREMENTS_FILE}}` | Pip requirements file name | `requirements.txt` |

## Template

```dockerfile
# === Stage 1: Builder ===
FROM python:{{PYTHON_VERSION}} AS builder

WORKDIR /app

# Install build dependencies for compiled packages (asyncpg, bcrypt, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml {{REQUIREMENTS_FILE}} ./

# Install Python dependencies into /install prefix
RUN pip install --no-cache-dir --prefix=/install -r {{REQUIREMENTS_FILE}}

# === Stage 2: Runtime ===
FROM python:{{PYTHON_VERSION}} AS runtime

WORKDIR /app

# Install runtime-only system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
# Adjust these COPY lines to match your project structure:
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=15s \
    CMD curl -f http://localhost:{{APP_PORT}}/health || exit 1

# Expose application port
EXPOSE {{APP_PORT}}

# Run with uvicorn
CMD ["uvicorn", "{{ENTRY_MODULE}}", "--host", "0.0.0.0", "--port", "{{APP_PORT}}", "--workers", "{{WORKERS}}"]
```

## Usage

1. Copy this template into your project root as `Dockerfile`.
2. Replace all `{{PLACEHOLDER}}` values.
3. Adjust the `COPY` lines in the runtime stage to match your project's directory layout.
4. Add or remove system packages in the builder stage depending on which compiled Python packages you use.
5. Build: `docker build -t my-app .`

## Notes

- The `--prefix=/install` trick installs all Python packages into an isolated directory in the builder stage. The runtime stage copies this entire prefix, avoiding the need to install build tools (gcc, etc.) in the final image.
- `PYTHONUNBUFFERED=1` ensures logs appear immediately in Docker output (no buffering).
- `PYTHONDONTWRITEBYTECODE=1` prevents `.pyc` files from being written, reducing image size slightly.
- The `--no-install-recommends` flag keeps both stages minimal.
- If your application does not use Alembic, remove the `alembic/` and `alembic.ini` COPY lines.
- For production, consider pinning the base image digest (e.g., `python:3.12-slim@sha256:...`) for reproducible builds.
- The health check assumes your application exposes a `/health` endpoint. Adjust the path as needed.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
