# Snippet: Async SQLAlchemy 2.0 Session Factory (Python)

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Sets up an async SQLAlchemy 2.0 database connection with `create_async_engine`, an `async_sessionmaker` factory, and an async generator for dependency injection (e.g., FastAPI's `Depends`). The session auto-commits on success and rolls back on exception.

## Dependencies

- `sqlalchemy[asyncio]>=2.0.29`
- `asyncpg>=0.29.0` (PostgreSQL async driver)

## Code

```python
"""Async database connection and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Configuration -- replace these with your settings source
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"
POOL_SIZE = 20
MAX_OVERFLOW = 10
DEBUG_ECHO = False

engine = create_async_engine(
    DATABASE_URL,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    echo=DEBUG_ECHO,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session.

    Commits on successful exit, rolls back on exception.
    Use as a FastAPI dependency: db: AsyncSession = Depends(get_db)
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

## Usage Example

```python
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/items/{item_id}")
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/items/")
async def create_item(data: ItemCreate, db: AsyncSession = Depends(get_db)):
    item = Item(**data.model_dump())
    db.add(item)
    # commit happens automatically when get_db() exits without exception
    await db.flush()  # flush to get the generated ID
    await db.refresh(item)
    return item
```

## Notes

- `expire_on_commit=False` prevents SQLAlchemy from expiring all attributes after commit. Without this, accessing any attribute after commit triggers a lazy load, which fails in async mode (no implicit IO).
- The `get_db` generator pattern works with FastAPI's `Depends()` and any other async dependency injection framework.
- `pool_size` controls the number of persistent connections. `max_overflow` allows temporary connections above the pool size during traffic spikes. Total max connections = `pool_size + max_overflow`.
- For production, load `DATABASE_URL`, `POOL_SIZE`, etc. from environment variables or a settings class (e.g., pydantic-settings `BaseSettings`).
- The `echo=True` flag logs all SQL statements -- useful for development, but disable it in production.
- To dispose of the engine (e.g., during shutdown), call `await engine.dispose()`.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
