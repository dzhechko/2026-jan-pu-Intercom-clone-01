# Refinement: Cost Calculator Edge Cases

## Edge Case 1: Large Workloads (500+ VMs)

**Trigger:** User submits workload with 500+ VM specs of varied configurations.

**Risk:** Slow response (>30s), token limit exceeded, pricing MCP timeouts.

**Mitigation:**
- Batch VM specs by identical config: group by `(vcpu, ram_gb, disk_type)`, multiply by count.
- Cap at 50 unique SKU lookups per request; aggregate remaining as "estimated".
- Agent prompt instructs batching: "Process large requests (500+ VMs) in logical batches."
- Test: parametrize `test_tco.py` with 1, 50, 500, 1000 VM counts.

## Edge Case 2: Stale Pricing Data

**Trigger:** RAG pricing documents are older than 30 days.

**Risk:** User gets outdated cost estimates, loses trust.

**Mitigation:**
- Check `metadata.last_updated` on RAG results. If > 30 days, add disclaimer.
- Agent prompt: "Flag if pricing data may be outdated (>30 days)."
- Pricing MCP returns `last_updated` timestamp; if stale, response includes caveat.
- Test: mock RAG result with `last_updated = 60 days ago`, assert disclaimer present.

## Edge Case 3: Missing Provider or Unknown SKU

**Trigger:** User requests a provider not in our corpus, or a VM config with no matching SKU.

**Risk:** Hallucinated pricing numbers.

**Mitigation:**
- If `MATCH_SKU` returns null, use `CLOSEST_LARGER_SKU` and flag as "estimated."
- If no SKU exists at all for a provider, exclude that provider and state: "Pricing unavailable for [provider]."
- Agent prompt: "Never hallucinate pricing numbers not in the knowledge base."
- Test: assert that unknown provider returns graceful message, not fake numbers.

## Edge Case 4: Zero or Negative Costs

**Trigger:** Free-tier services, promotional pricing, or calculation bugs produce zero/negative totals.

**Risk:** Misleading comparison (free tier not sustainable at scale).

**Mitigation:**
- If any category cost is 0: note "free tier / promotional" in breakdown.
- If total monthly < 0: clamp to 0, log warning.
- Savings percentage: guard against division by zero when `runner_up.monthly_cost == 0`.
- Test: `test_savings_calculation` with `current_cost = 0` should return 0% (not ZeroDivisionError).

## Edge Case 5: Partial Workload Spec

**Trigger:** User provides incomplete info (e.g., "50 VMs" without RAM/CPU details).

**Risk:** Agent guesses specs and produces inaccurate costs.

**Mitigation:**
- Agent asks 1-2 clarifying questions before calculating (per prompt behavior).
- If forced to estimate, use Cloud.ru's most popular SKU as default and flag explicitly.
- Test: input with missing `vcpu`/`ram_gb` triggers clarification, not silent defaults.

## Test Coverage Targets

| Scenario | Test Location | Status |
|----------|---------------|--------|
| Monthly/annual/3-year conversion | `test_tco.py::test_monthly_to_annual_conversion` | Exists |
| Discount application | `test_tco.py::test_annual_discount_applied` | Exists |
| Cheapest provider selection | `test_tco.py::test_cheapest_provider_selection` | Exists |
| Savings percentage | `test_tco.py::test_savings_calculation` | Exists |
| 500+ VMs batching | Planned | Pending |
| Stale pricing disclaimer | Planned | Pending |
| Missing provider graceful | Planned | Pending |
| Zero cost guard | Planned | Pending |
