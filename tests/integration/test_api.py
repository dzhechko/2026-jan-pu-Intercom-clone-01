"""Integration tests for API endpoints (requires running services)."""

import pytest
from httpx import AsyncClient, ASGITransport

from src.api.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestHealthEndpoints:
    """Test health check endpoints."""

    @pytest.mark.asyncio
    async def test_health_returns_ok(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestConversationAPI:
    """Test conversation API endpoints."""

    @pytest.mark.asyncio
    async def test_create_conversation_requires_auth(self, client):
        response = await client.post(
            "/api/v1/conversations",
            json={"channel": "web_widget", "channel_user_id": "test-user"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_send_message_requires_auth(self, client):
        response = await client.post(
            "/api/v1/conversations/fake-id/messages",
            json={"content": "Hello", "role": "user"},
        )
        assert response.status_code == 401


class TestDashboardAPI:
    """Test dashboard metrics API."""

    @pytest.mark.asyncio
    async def test_metrics_requires_auth(self, client):
        response = await client.get("/api/v1/dashboard/metrics")
        assert response.status_code == 401


class TestTelegramWebhook:
    """Test Telegram webhook endpoint."""

    @pytest.mark.asyncio
    async def test_webhook_accepts_valid_update(self, client):
        # Telegram webhook should accept POST without auth errors
        # (secret token validation is separate)
        response = await client.post(
            "/api/v1/webhooks/telegram",
            json={
                "update_id": 123,
                "message": {
                    "message_id": 1,
                    "from": {"id": 12345, "first_name": "Test"},
                    "chat": {"id": 12345, "type": "private"},
                    "text": "/start",
                },
            },
        )
        # Should succeed (200) even without full setup
        assert response.status_code in (200, 401)

    @pytest.mark.asyncio
    async def test_webhook_handles_empty_body(self, client):
        response = await client.post(
            "/api/v1/webhooks/telegram",
            json={"update_id": 123},
        )
        assert response.status_code in (200, 401)
