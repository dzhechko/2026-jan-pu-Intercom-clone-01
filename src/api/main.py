"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.log_level)
    logger.info("app_starting", debug=settings.debug)
    yield
    logger.info("app_shutting_down")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
from src.api.routes.auth import router as auth_router  # noqa: E402
from src.api.routes.conversations import router as conversations_router  # noqa: E402
from src.api.routes.dashboard import router as dashboard_router  # noqa: E402
from src.api.webhooks.telegram import router as telegram_router  # noqa: E402

app.include_router(auth_router)
app.include_router(conversations_router)
app.include_router(dashboard_router)
app.include_router(telegram_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/ready")
async def health_ready():
    # Check database and Redis connectivity
    checks = {"database": "ok", "redis": "ok", "qdrant": "ok"}

    try:
        from src.core.database import engine

        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        checks["database"] = "error"

    try:
        import redis.asyncio as aioredis

        r = aioredis.from_url(settings.redis_url)
        await r.ping()
        await r.aclose()
    except Exception:
        checks["redis"] = "error"

    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ready" if all_ok else "degraded", "checks": checks}


# Import text for health check query
from sqlalchemy import text  # noqa: E402
