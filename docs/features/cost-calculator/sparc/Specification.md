# Specification: Cost Calculator Data Model

## WorkloadSpec (Input)

```python
class WorkloadSpec:
    vms: list[VMSpec]                 # VM configurations
    storage: StorageSpec | None       # Additional object/block storage
    networking: NetworkSpec | None    # Egress traffic
    managed_services: list[str]       # e.g. ["kubernetes", "postgresql", "redis"]
    period: Literal["monthly", "annual", "three_year"]

class VMSpec:
    count: int          # Number of identical VMs
    vcpu: int           # vCPUs per VM
    ram_gb: int         # RAM in GB per VM
    disk_gb: int        # Disk size per VM
    disk_type: str      # "ssd" | "hdd" | "nvme"

class StorageSpec:
    type: str           # "object" | "block"
    size_tb: float

class NetworkSpec:
    egress_gb_month: float   # Outbound traffic per month
```

## TCOComparison (Output)

```python
class TCOComparison:
    workload_description: str
    providers: list[ProviderCost]
    recommended: str                  # Provider name with lowest monthly cost
    savings_vs_current: float | None  # Percentage savings if current cost given

class ProviderCost:
    name: str                         # "Cloud.ru" | "Yandex Cloud" | "VK Cloud"
    monthly_cost: float               # Total monthly in rubles
    annual_cost: float                # monthly * 12, after annual discount
    three_year_cost: float            # monthly * 36, after 3-year discount
    breakdown: list[CostCategory]

class CostCategory:
    category: str   # "Compute" | "Storage" | "Networking" | "Managed Services"
    cost: float     # Monthly cost in rubles
```

## Provider Discount Configuration

| Provider | Annual Discount | 3-Year Discount | Source |
|----------|:-:|:-:|--------|
| Cloud.ru | 15% | 30% | RAG corpus / Pricing MCP |
| Yandex Cloud | 10-20% | 20-35% | RAG corpus |
| VK Cloud | 10-15% | 20-30% | RAG corpus |

Discounts are loaded at runtime from the Pricing MCP server or RAG pricing collection. If unavailable, hardcoded defaults above are used with a staleness warning.

## Pricing SKU Matching

SKU lookup order:
1. Exact match on `(provider, vcpu, ram_gb)`
2. Closest larger SKU if exact not found (flag as "estimated")
3. If no match at all, return `null` and note missing pricing

Collections queried: `pricing`, `cloud_ru_docs`.
