"""Index documents into Qdrant for RAG search."""

import asyncio
from pathlib import Path

from src.rag.indexer import DocumentIndexer


SAMPLE_DOCS = [
    {
        "collection": "cloud_ru_cloud_docs",
        "title": "Cloud Servers — Виртуальные машины Cloud.ru",
        "content": (
            "Cloud Servers — сервис виртуальных машин Cloud.ru. "
            "Поддерживает конфигурации от 1 vCPU / 1 GB RAM до 128 vCPU / 512 GB RAM. "
            "Типы дисков: SSD (до 100 000 IOPS), HDD (до 5 000 IOPS). "
            "Поддержка Windows и Linux. Автоматическое масштабирование. "
            "SLA 99.95%. Размещение в дата-центрах Москвы."
        ),
        "metadata": {"source_url": "https://cloud.ru/docs/cloud-servers", "category": "compute", "provider": "cloud_ru"},
    },
    {
        "collection": "cloud_ru_cloud_docs",
        "title": "Cloud Containers — Managed Kubernetes",
        "content": (
            "Cloud Containers — управляемый Kubernetes в Cloud.ru. "
            "Сертифицирован CNCF. Автоматическое масштабирование нод. "
            "Интеграция с Container Registry, Monitoring, Logging. "
            "Поддержка GPU-нод для ML-задач. "
            "SLA 99.95%. Network Policies, Pod Security Standards."
        ),
        "metadata": {"source_url": "https://cloud.ru/docs/cloud-containers", "category": "containers", "provider": "cloud_ru"},
    },
    {
        "collection": "cloud_ru_cloud_docs",
        "title": "VPC — Virtual Private Cloud",
        "content": (
            "VPC — изолированная виртуальная сеть в Cloud.ru. "
            "Поддержка подсетей, маршрутизации, NAT Gateway, VPN. "
            "Security Groups и Network ACL. "
            "Peering между VPC. Интеграция с DDoS Protection. "
            "IPv4 и IPv6 поддержка."
        ),
        "metadata": {"source_url": "https://cloud.ru/docs/vpc", "category": "networking", "provider": "cloud_ru"},
    },
    {
        "collection": "cloud_ru_compliance",
        "title": "Соответствие 152-ФЗ",
        "content": (
            "Cloud.ru соответствует требованиям 152-ФЗ «О персональных данных». "
            "Аттестат соответствия УЗ-1 (максимальный уровень защищённости). "
            "Дата-центры расположены на территории РФ. "
            "Шифрование данных at-rest (AES-256) и in-transit (TLS 1.3). "
            "Сертификаты ФСТЭК и ФСБ. Регулярный аудит безопасности."
        ),
        "metadata": {"source_url": "https://cloud.ru/compliance/152fz", "category": "compliance", "provider": "cloud_ru"},
    },
]


async def index():
    indexer = DocumentIndexer()

    # Use a placeholder tenant ID for seed data
    tenant_id = "00000000-0000-0000-0000-000000000001"

    for doc in SAMPLE_DOCS:
        try:
            ids = await indexer.index_document(
                collection_name=doc["collection"],
                tenant_id=tenant_id,
                title=doc["title"],
                content=doc["content"],
                metadata=doc["metadata"],
            )
            print(f"Indexed: {doc['title']} ({len(ids)} chunks)")
        except Exception as e:
            print(f"Failed to index {doc['title']}: {e}")

    await indexer.close()
    print("\nDocument indexing complete.")


if __name__ == "__main__":
    asyncio.run(index())
