"""Seed script — create initial tenant and agent configurations."""

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import async_session_factory, engine
from src.core.security import hash_password
from src.models.base import Base
from src.models.tenant import Tenant
from src.models.agent_config import AgentConfig


async def seed():
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        # Check if tenant already exists
        result = await session.execute(select(Tenant).where(Tenant.slug == "cloud_ru"))
        existing = result.scalar_one_or_none()

        if existing:
            print("Tenant 'cloud_ru' already exists, skipping seed.")
            return

        # Create Cloud.ru tenant
        tenant = Tenant(
            name="Cloud.ru",
            slug="cloud_ru",
            api_key_hash=hash_password("cloud_ru_dev_api_key"),
            plan="pilot",
            config={
                "display_name": "AI-Консультант Cloud.ru",
                "language": "ru",
                "escalation_hours": {"start": "09:00", "end": "18:00", "timezone": "Europe/Moscow"},
            },
        )
        session.add(tenant)
        await session.flush()

        # Create agent configurations
        agents = [
            AgentConfig(
                tenant_id=tenant.id,
                agent_type="architect",
                confidence_threshold=0.6,
                max_turns=20,
                rag_collections=["cloud_ru_cloud_docs", "cloud_ru_architectures"],
                tools=["rag_search", "pricing_api", "config_api"],
            ),
            AgentConfig(
                tenant_id=tenant.id,
                agent_type="cost_calculator",
                confidence_threshold=0.6,
                max_turns=15,
                rag_collections=["cloud_ru_pricing", "competitor_pricing"],
                tools=["rag_search", "pricing_api"],
            ),
            AgentConfig(
                tenant_id=tenant.id,
                agent_type="compliance",
                confidence_threshold=0.6,
                max_turns=15,
                rag_collections=["cloud_ru_compliance", "regulatory_updates"],
                tools=["rag_search", "compliance_checker"],
            ),
            AgentConfig(
                tenant_id=tenant.id,
                agent_type="human_escalation",
                confidence_threshold=0.0,
                max_turns=5,
                rag_collections=[],
                tools=["notification"],
            ),
        ]

        for agent in agents:
            session.add(agent)

        await session.commit()
        print(f"Seeded tenant '{tenant.name}' (id: {tenant.id}) with {len(agents)} agent configs.")


if __name__ == "__main__":
    asyncio.run(seed())
