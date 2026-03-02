"""Telegram bot webhook handler."""

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database import get_db
from src.core.logging import get_logger
from src.models.conversation import Conversation
from src.models.tenant import Tenant
from src.orchestrator.router import Orchestrator

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])

# Start command greeting
START_GREETING = (
    "Добро пожаловать в AI-Консультант Cloud.ru! 🌐\n\n"
    "Я помогу вам с:\n"
    "• Архитектурой облачных решений\n"
    "• Расчётом стоимости (TCO)\n"
    "• Вопросами compliance (152-ФЗ, ФСТЭК)\n"
    "• Планированием миграции\n\n"
    "Просто опишите вашу задачу, и я начну консультацию."
)


@router.post("/telegram")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
):
    # Verify webhook secret
    if settings.telegram_webhook_secret:
        if x_telegram_bot_api_secret_token != settings.telegram_webhook_secret:
            logger.warning("telegram_invalid_secret", ip=request.client.host if request.client else "unknown")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook secret")

    body = await request.json()
    message = body.get("message", {})
    text = message.get("text", "").strip()
    chat_id = message.get("chat", {}).get("id")
    user_id = message.get("from", {}).get("id")

    if not chat_id or not text:
        return {}

    # Handle /start command
    if text == "/start":
        await _send_telegram_message(chat_id, START_GREETING)
        return {}

    # Handle empty/whitespace messages
    if not text:
        await _send_telegram_message(chat_id, "Пожалуйста, опишите вашу задачу. Чем могу помочь?")
        return {}

    # Find tenant for this bot (use first active tenant for now)
    tenant_result = await db.execute(select(Tenant).limit(1))
    tenant = tenant_result.scalar_one_or_none()
    if not tenant:
        await _send_telegram_message(chat_id, "Сервис временно недоступен.")
        return {}

    # Find or create conversation
    conv_result = await db.execute(
        select(Conversation)
        .where(Conversation.tenant_id == tenant.id)
        .where(Conversation.channel == "telegram")
        .where(Conversation.channel_user_id == str(user_id))
        .where(Conversation.status == "active")
    )
    conversation = conv_result.scalar_one_or_none()

    if not conversation:
        conversation = Conversation(
            tenant_id=tenant.id,
            channel="telegram",
            channel_user_id=str(user_id),
        )
        db.add(conversation)
        await db.flush()

    # Process through orchestrator
    orchestrator = Orchestrator(db, tenant.id)
    response = await orchestrator.process_message(conversation, text)

    # Send response via Telegram
    await _send_telegram_message(chat_id, response.content)

    return {}


async def _send_telegram_message(chat_id: int, text: str) -> None:
    """Send a message via Telegram Bot API."""
    import httpx

    if not settings.telegram_bot_token:
        logger.warning("telegram_bot_token_not_set")
        return

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"

    # Split long messages (Telegram limit: 4096 chars)
    chunks = [text[i : i + 4096] for i in range(0, len(text), 4096)]

    async with httpx.AsyncClient(timeout=10.0) as client:
        for chunk in chunks:
            try:
                resp = await client.post(url, json={"chat_id": chat_id, "text": chunk, "parse_mode": "Markdown"})
                if resp.status_code == 429:
                    # Rate limited — log and skip
                    logger.warning("telegram_rate_limited", chat_id=chat_id)
            except Exception:
                logger.exception("telegram_send_failed", chat_id=chat_id)
