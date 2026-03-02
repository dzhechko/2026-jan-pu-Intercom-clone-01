"""Shared test fixtures."""

import pytest


@pytest.fixture
def sample_tenant_data():
    return {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "Cloud.ru",
        "slug": "cloud_ru",
        "api_key_hash": "$2b$12$test_hash",
        "plan": "pilot",
        "config": {"display_name": "AI-Консультант Cloud.ru", "language": "ru"},
    }


@pytest.fixture
def sample_conversation_data(sample_tenant_data):
    return {
        "id": "00000000-0000-0000-0000-000000000002",
        "tenant_id": sample_tenant_data["id"],
        "channel": "telegram",
        "channel_user_id": "123456789",
        "status": "active",
        "context": {},
    }


@pytest.fixture
def sample_message_data(sample_conversation_data):
    return {
        "id": "00000000-0000-0000-0000-000000000003",
        "conversation_id": sample_conversation_data["id"],
        "role": "user",
        "content": "Мне нужно мигрировать 200 серверов VMware в облако",
        "metadata": {},
    }
