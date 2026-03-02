# Pseudocode: Cost Calculator Algorithms

## calculate_tco(workload, providers) -> TCOComparison

```
INPUT:  workload: WorkloadSpec, providers: list[str]
OUTPUT: TCOComparison

FOR EACH provider IN providers:
    pricing = LOAD_PRICING(provider)     # RAG + MCP lookup

    compute_cost = 0
    FOR EACH vm IN workload.vms:
        sku = MATCH_SKU(provider, vm.vcpu, vm.ram_gb)
        IF sku IS NULL:
            sku = CLOSEST_LARGER_SKU(provider, vm)
            FLAG "estimated"
        compute_cost += sku.price_monthly * vm.count

    storage_cost = SUM(vm.disk_gb * DISK_PRICE(provider, vm.disk_type) * vm.count
                       FOR vm IN workload.vms)
    IF workload.storage:
        storage_cost += workload.storage.size_tb * 1024 * STORAGE_PRICE(provider, workload.storage.type)

    network_cost = 0
    IF workload.networking:
        network_cost = CALC_EGRESS(provider, workload.networking.egress_gb_month)

    managed_cost = SUM(MANAGED_SKU_PRICE(provider, svc) FOR svc IN workload.managed_services)

    total_monthly = compute_cost + storage_cost + network_cost + managed_cost
    total_monthly = apply_discounts(total_monthly, provider, workload.period)

    APPEND ProviderCost(provider, total_monthly, breakdown=[compute, storage, network, managed])

SORT results BY monthly_cost ASC
RETURN TCOComparison(providers=results, recommended=results[0].name)
```

## apply_discounts(monthly, provider, period) -> float

```
INPUT:  monthly: float, provider: str, period: str
OUTPUT: discounted monthly cost

discounts = LOAD_DISCOUNT_TABLE(provider)  # from MCP or defaults

MATCH period:
    "monthly"    -> RETURN monthly
    "annual"     -> RETURN monthly * (1 - discounts.annual)     # typically 0.10-0.20
    "three_year" -> RETURN monthly * (1 - discounts.three_year) # typically 0.20-0.40
```

## compare_providers(tco: TCOComparison) -> str

```
INPUT:  tco: TCOComparison
OUTPUT: formatted markdown comparison table

header = "| Provider | Monthly | Annual | 3-Year | Breakdown |"
FOR EACH p IN tco.providers:
    row = format_row(p.name, p.monthly_cost, p.annual_cost, p.three_year_cost, p.breakdown)

cheapest = tco.providers[0]
runner_up = tco.providers[1]
savings_pct = (runner_up.monthly_cost - cheapest.monthly_cost) / runner_up.monthly_cost * 100

APPEND f"Recommended: {cheapest.name} (saves {savings_pct:.1f}% vs {runner_up.name})"
RETURN table
```

## find_cheapest(providers: list[ProviderCost]) -> ProviderCost

```
INPUT:  providers: list[ProviderCost]
OUTPUT: ProviderCost with lowest monthly_cost

RETURN MIN(providers, key=lambda p: p.monthly_cost)
```
Complexity: O(p * v) where p = number of providers, v = number of VM specs.
