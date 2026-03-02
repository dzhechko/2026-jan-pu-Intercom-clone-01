"""Application configuration using pydantic-settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "AI-Консультант Cloud.ru"
    debug: bool = False
    log_level: str = "INFO"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Database
    database_url: str = "postgresql+asyncpg://app:app_secret@localhost:5432/cloud_consultant"
    db_pool_size: int = 20
    db_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: str | None = None

    # LLM
    anthropic_api_key: str = ""
    llm_model: str = "claude-sonnet-4-20250514"
    llm_fallback_model: str | None = None

    # Telegram
    telegram_bot_token: str = ""
    telegram_webhook_secret: str = ""
    telegram_webhook_url: str = ""

    # Auth
    jwt_secret_key: str = Field(default="change-me-to-at-least-32-characters-long-secret", min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    admin_email: str = "admin@cloud.ru"
    admin_password_hash: str = ""  # bcrypt hash; if empty, uses default dev password

    # MinIO
    minio_endpoint: str = "localhost:9000"
    minio_root_user: str = "minioadmin"
    minio_root_password: str = "minioadmin"

    # CRM Integration
    bitrix24_webhook_url: str = ""  # Empty = disabled. Format: https://{domain}.bitrix24.ru/rest/{user_id}/{secret}/

    # Rate Limiting
    rate_limit_per_min: int = 30

    # Sentry
    sentry_dsn: str | None = None


settings = Settings()
