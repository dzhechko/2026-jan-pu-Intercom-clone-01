# Refinement — Migration Agent

## Edge Cases

### 1. Hybrid Cloud Deployment
Customer keeps some workloads on-prem, migrates others.
- Support split-deployment plans (partial migration)
- Include VPN/peering connectivity between on-prem and Cloud.ru
- Estimate egress/ingress costs for cross-environment traffic
- **Test:** "We want to keep Oracle DB on-prem but move web servers"

### 2. Multi-Datacenter Migration
Infrastructure spread across multiple DCs/regions.
- Organize migration waves per-DC to minimize cross-DC data transfer
- Ask which DC to prioritize; handle sequential DC migrations
- Consider data replication lag between source DCs
- **Test:** "We have 3 data centers: Moscow, SPB, and Novosibirsk"

### 3. Legacy Systems (Mainframe, Proprietary OS)
Workloads on unsupported platforms (AS/400, mainframe).
- Detect unsupported platforms and flag immediately
- Recommend professional services engagement
- Escalate to human SA when confidence < 0.6
- **Test:** "We run IBM AS/400 with RPG applications"

### 4. Compliance Constraints (152-FZ, CII)
Customer processes personal data or operates Critical Information Infrastructure.
- Flag 152-FZ early in assessment phase
- Verify target Cloud.ru services hold required certifications
- Include compliance validation in Phase 4 (Validate)
- **Test:** "We process medical records under 152-FZ UZ-1"

### 5. Compressed Timeline Request
Customer demands migration faster than safe estimate.
- Identify parallelizable waves (no dependencies)
- Flag increased risk; never promise below minimum safe threshold
- **Test:** "We must be fully migrated in 4 weeks" (200+ VMs)

### 6. Incomplete Infrastructure Information
Customer lacks full specs or dependency maps.
- Ask targeted follow-ups (max 3 rounds)
- Generate plan with ranges where data is missing (e.g., "2-4 weeks")
- Mark assumptions explicitly; suggest discovery tools
- **Test:** "We have about 100 servers, not sure about specs"

### 7. Mid-Migration Strategy Change
After receiving a plan, customer wants a different strategy for some workloads.
- Regenerate plan for affected workloads only
- Preserve completed waves; recalculate from change point forward
- **Test:** "Let's containerize the web apps instead of moving VMs"

## Testing Matrix

| Edge Case | Test Type | Priority |
|-----------|-----------|----------|
| Hybrid cloud | Unit + Integration | High |
| Multi-DC | Unit | Medium |
| Legacy systems | Unit (escalation) | High |
| Compliance 152-FZ | Unit + Integration | High |
| Compressed timeline | Unit | Medium |
| Incomplete info | Unit | Medium |
| Strategy change | Integration | Medium |

## Confidence Thresholds

| Scenario | Confidence | Action |
|----------|-----------|--------|
| Standard VM migration | >= 0.8 | Full plan |
| Database re-platform | 0.6-0.8 | Plan with caveats |
| Legacy/mainframe | < 0.6 | Escalate to human SA |
| CII workloads | 0.6-0.7 | Plan + compliance flag |
| Unknown workload type | < 0.5 | Escalate immediately |
