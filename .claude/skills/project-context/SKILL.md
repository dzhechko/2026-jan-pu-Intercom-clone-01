# Project Context Skill — AI-Консультант Cloud.ru

## Domain Knowledge

### What is AI-Консультант Cloud.ru?

A multi-agent AI platform for pre-sales cloud consulting, deployed as a white-label solution starting with Cloud.ru (Russia's #1 IaaS+PaaS provider, 32.5% market share, ₽49.4B revenue).

### Target Users

| Segment | Role | Need |
|---------|------|------|
| Primary | CTO/VP Engineering (100-1000 employees) | Cloud migration architecture advice |
| Secondary | IT Directors (government/enterprise) | Compliance consulting (152-ФЗ, ФСТЭК) |
| Tertiary | DevOps/Cloud Engineers | Technical cost optimization |

### Core Problem

Russian CTOs spend 2-4 weeks getting cloud architecture recommendations via manual meetings with Solution Architects (SAs). The AI consultant replaces the first 70-80% of this process with instant, RAG-grounded answers.

### Business Model

- **Pilot**: Free 3 months (lead generation mode)
- **Production**: ₽500K/month per cloud provider tenant
- **Enterprise**: ₽1-2M/month (custom integrations, SLA)
- **Target**: 5 paying tenants by Month 12, ₽78M ARR by Year 2

### Key Metrics

| Metric | MVP Target (M3) | Production Target (M6) |
|--------|-----------------|----------------------|
| Response accuracy | >85% | >90% |
| Response time (p50) | <5s | <3s |
| Conversations/day | 50 | 200 |
| Escalation rate | <20% | <15% |
| Lead conversion | >15% | >25% |

### Agent System

6 specialized AI agents, each with its own RAG corpus and MCP tools:

1. **Architect Agent** — Cloud architecture recommendations (VMware migration, Kubernetes, hybrid)
2. **Cost Calculator Agent** — TCO comparison across 3+ Russian cloud providers
3. **Compliance Agent** — 152-ФЗ, ФСТЭК, КИИ regulatory guidance
4. **Migration Agent** — Step-by-step migration planning
5. **AI Factory Agent** — GPU/ML workload consulting
6. **Human Escalation Agent** — Handoff to human SA when confidence < 0.6

### Russian Cloud Market Context

- Total market: ₽416.5B (2024), growing 30%+ annually
- Top providers: Cloud.ru, Yandex Cloud, VK Cloud, Selectel, МТС Cloud
- Key regulation: 152-ФЗ (personal data), ФСТЭК (security certification), КИИ (critical infrastructure)
- All data must stay in Russian DCs (data sovereignty)
- Import substitution trend: VMware → local alternatives

### Competitive Landscape

- No direct competitor in Russian market for AI cloud consulting
- International: Qualified.com (B2B sales AI), Intercom Fin (support AI), AWS Q (but no Russian cloud)
- Indirect: Manual SA teams at cloud providers
