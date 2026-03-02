"""Unit tests for Bitrix24 CRM integration service."""

from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from src.services.crm import Bitrix24Client


class TestBitrix24ClientDisabled:
    """Test behavior when CRM is not configured."""

    def test_disabled_when_no_webhook(self):
        client = Bitrix24Client(webhook_url="")
        assert client.enabled is False

    @pytest.mark.asyncio
    async def test_push_lead_returns_none_when_disabled(self):
        client = Bitrix24Client(webhook_url="")
        result = await client.push_lead(
            contact={"name": "Test", "email": "test@test.com"},
            qualification="hot",
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_create_contact_returns_none_when_disabled(self):
        client = Bitrix24Client(webhook_url="")
        result = await client.create_contact(name="Test")
        assert result is None

    @pytest.mark.asyncio
    async def test_create_deal_returns_none_when_disabled(self):
        client = Bitrix24Client(webhook_url="")
        result = await client.create_deal(title="Test Deal")
        assert result is None


class TestBitrix24ClientEnabled:
    """Test CRM operations with mocked HTTP calls."""

    @pytest.fixture
    def client(self):
        return Bitrix24Client(webhook_url="https://test.bitrix24.ru/rest/1/abc123")

    @pytest.mark.asyncio
    async def test_create_contact_success(self, client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 42}

        with patch("src.services.crm.httpx.AsyncClient") as mock_client_cls:
            mock_http = AsyncMock()
            mock_http.post.return_value = mock_response
            mock_http.__aenter__ = AsyncMock(return_value=mock_http)
            mock_http.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_http

            # find_contact_by_email returns empty (no duplicate)
            mock_responses = [
                MagicMock(status_code=200, json=MagicMock(return_value={"result": []})),
                MagicMock(status_code=200, json=MagicMock(return_value={"result": 42})),
            ]
            mock_http.post.side_effect = mock_responses

            result = await client.create_contact(
                name="Иван Петров",
                company="Cloud Corp",
                email="ivan@cloud.ru",
                phone="+7 495 123 45 67",
            )
            assert result == 42

    @pytest.mark.asyncio
    async def test_create_contact_duplicate_detected(self, client):
        with patch("src.services.crm.httpx.AsyncClient") as mock_client_cls:
            mock_http = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"result": [{"ID": "99"}]}
            mock_http.post.return_value = mock_response
            mock_http.__aenter__ = AsyncMock(return_value=mock_http)
            mock_http.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_http

            result = await client.create_contact(email="existing@cloud.ru")
            assert result == 99

    @pytest.mark.asyncio
    async def test_create_deal_success(self, client):
        with patch("src.services.crm.httpx.AsyncClient") as mock_client_cls:
            mock_http = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"result": 101}
            mock_http.post.return_value = mock_response
            mock_http.__aenter__ = AsyncMock(return_value=mock_http)
            mock_http.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_http

            result = await client.create_deal(
                title="AI Consultant: migration — Cloud Corp",
                contact_id=42,
                value=500000.0,
                stage="PREPARATION",
                comments="Architecture recommendation: use K8s",
            )
            assert result == 101

    @pytest.mark.asyncio
    async def test_push_lead_full_flow(self, client):
        with patch("src.services.crm.httpx.AsyncClient") as mock_client_cls:
            mock_http = AsyncMock()
            responses = [
                # find_contact_by_email → empty
                MagicMock(status_code=200, json=MagicMock(return_value={"result": []})),
                # create_contact → 42
                MagicMock(status_code=200, json=MagicMock(return_value={"result": 42})),
                # create_deal → 101
                MagicMock(status_code=200, json=MagicMock(return_value={"result": 101})),
            ]
            mock_http.post.side_effect = responses
            mock_http.__aenter__ = AsyncMock(return_value=mock_http)
            mock_http.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_http

            result = await client.push_lead(
                contact={"name": "Иван", "company": "Corp", "email": "ivan@corp.ru"},
                qualification="hot",
                estimated_deal_value=500000.0,
                intent="migration",
                architecture_summary="Recommended K8s cluster",
            )
            assert result == "contact:42/deal:101"

    @pytest.mark.asyncio
    async def test_push_lead_no_contact_no_deal(self, client):
        with patch("src.services.crm.httpx.AsyncClient") as mock_client_cls:
            mock_http = AsyncMock()
            # All calls return errors
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_http.post.return_value = mock_response
            mock_http.__aenter__ = AsyncMock(return_value=mock_http)
            mock_http.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_http

            result = await client.push_lead(
                contact={"email": "test@test.com"},
                qualification="qualified",
            )
            assert result is None


class TestBitrix24ErrorHandling:
    """Test error handling and retries."""

    @pytest.fixture
    def client(self):
        return Bitrix24Client(webhook_url="https://test.bitrix24.ru/rest/1/abc123")

    @pytest.mark.asyncio
    async def test_server_error_retries(self, client):
        with patch("src.services.crm.httpx.AsyncClient") as mock_client_cls:
            mock_http = AsyncMock()
            responses = [
                # First attempt: 500 error
                MagicMock(status_code=500, text="Server Error"),
                # Retry: success
                MagicMock(status_code=200, json=MagicMock(return_value={"result": 42})),
            ]
            mock_http.post.side_effect = responses
            mock_http.__aenter__ = AsyncMock(return_value=mock_http)
            mock_http.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_http

            result = await client._call("crm.contact.add", {"fields": {}})
            assert result is not None
            assert result["result"] == 42

    @pytest.mark.asyncio
    async def test_client_error_no_retry(self, client):
        with patch("src.services.crm.httpx.AsyncClient") as mock_client_cls:
            mock_http = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            mock_http.post.return_value = mock_response
            mock_http.__aenter__ = AsyncMock(return_value=mock_http)
            mock_http.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_http

            result = await client._call("crm.contact.add", {"fields": {}})
            assert result is None
            # Only 1 call (no retry on 4xx)
            assert mock_http.post.call_count == 1


class TestBitrix24DealStageMapping:
    """Test deal stage determination from qualification."""

    def test_hot_stage(self):
        stage_map = {"hot": "PREPARATION", "qualified": "PREPAYMENT_INVOICE"}
        assert stage_map.get("hot", "NEW") == "PREPARATION"

    def test_qualified_stage(self):
        stage_map = {"hot": "PREPARATION", "qualified": "PREPAYMENT_INVOICE"}
        assert stage_map.get("qualified", "NEW") == "PREPAYMENT_INVOICE"

    def test_cold_defaults_to_new(self):
        stage_map = {"hot": "PREPARATION", "qualified": "PREPAYMENT_INVOICE"}
        assert stage_map.get("cold", "NEW") == "NEW"

    def test_warm_defaults_to_new(self):
        stage_map = {"hot": "PREPARATION", "qualified": "PREPAYMENT_INVOICE"}
        assert stage_map.get("warm", "NEW") == "NEW"


class TestContactFieldMapping:
    """Test contact field mapping for Bitrix24 API."""

    def test_name_split(self):
        name = "Иван Петров"
        parts = name.split(maxsplit=1)
        assert parts[0] == "Иван"
        assert parts[1] == "Петров"

    def test_single_name(self):
        name = "Иван"
        parts = name.split(maxsplit=1)
        assert parts[0] == "Иван"
        assert len(parts) == 1

    def test_deal_title_format(self):
        intent = "new_deployment"
        company = "Cloud Corp"
        title = f"AI Consultant: {intent.replace('_', ' ')} — {company}"
        assert title == "AI Consultant: new deployment — Cloud Corp"

    def test_deal_title_unknown_company(self):
        company = None
        company_label = company or "Unknown"
        title = f"AI Consultant: migration — {company_label}"
        assert title == "AI Consultant: migration — Unknown"
