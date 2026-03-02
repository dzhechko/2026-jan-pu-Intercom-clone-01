# Pattern: Multi-Tenant Data Isolation

## Maturity: 🔴 Alpha
## Used in: ai-consultant-cloud-ru
## Extracted: 2026-03-02
## Version: v1.0

---

## Intent

Ensure strict data isolation between tenants (customers, organizations, accounts) in a shared infrastructure. Every data access path -- relational database queries, vector database searches, file storage, cache lookups -- must be scoped to the requesting tenant. This prevents cross-tenant data leakage, which is both a security vulnerability and a compliance violation in multi-customer platforms.

## When to Use

- SaaS platforms serving multiple customers on shared infrastructure
- Any system where different organizations share the same database or service instances
- Platforms subject to data protection regulations (GDPR, CCPA, industry-specific rules)
- AI systems where training data, embeddings, or search results must not cross tenant boundaries
- Marketplaces, white-label products, or agency platforms with client-level separation

## When NOT to Use

- Single-tenant applications (one customer, one deployment)
- Internal tools used by a single organization with no customer data separation requirements
- Systems where all data is intentionally shared (public datasets, open platforms)
- Early prototypes where multi-tenancy is not yet a requirement (but plan for it)

## Structure (pseudocode)

```
# --- Database Layer ---

# Every table includes tenant_id
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    channel VARCHAR(50),
    created_at TIMESTAMP,
    INDEX idx_conversations_tenant (tenant_id)
);

# Base query class enforces tenant filtering
class TenantScopedQuery:
    def __init__(self, session, tenant_id):
        self.session = session
        self.tenant_id = tenant_id

    def query(self, model):
        return self.session.query(model).filter(
            model.tenant_id == self.tenant_id
        )

# --- Middleware Layer ---

function tenant_middleware(request, next):
    tenant_id = extract_tenant_id(request)  # from JWT, API key, or subdomain
    if not tenant_id:
        return 401 Unauthorized

    request.state.tenant_id = tenant_id
    return next(request)

# --- Vector Database Layer ---

function vector_search(tenant_id, query_embedding, top_k):
    collection_name = f"docs_{tenant_id}"  # per-tenant collection
    return vector_db.search(
        collection=collection_name,
        vector=query_embedding,
        limit=top_k
    )

# --- Cache Layer ---

function cache_get(tenant_id, key):
    scoped_key = f"tenant:{tenant_id}:{key}"
    return redis.get(scoped_key)

# --- File Storage Layer ---

function upload_file(tenant_id, file):
    path = f"/{tenant_id}/uploads/{file.name}"
    return storage.put(path, file.content)
```

## Implementation Variants

| Variant | Isolation Level | Trade-off |
|---------|----------------|-----------|
| A - Column-level (shared tables) | `tenant_id` column on every table, filtered in queries | Simplest ops, cheapest, but relies on query discipline |
| B - Schema-level | Separate database schema per tenant | Stronger isolation, easier per-tenant backup, moderate ops cost |
| C - Database-level | Separate database instance per tenant | Strongest isolation, independent scaling, highest ops cost |
| D - Hybrid | Column-level for most data, separate collections for sensitive stores (vector DB, files) | Balances isolation strength with operational simplicity |

## Trade-offs

| Dimension | Benefit | Cost |
|-----------|---------|------|
| Security | Data leakage between tenants is structurally prevented | Every query path must be audited for tenant filtering |
| Compliance | Meets data residency and isolation requirements | Per-tenant data deletion (right to erasure) requires tenant-aware purge logic |
| Simplicity (column-level) | Single database, simple deployment | One missed WHERE clause = data leak |
| Scalability (DB-level) | Independent scaling per tenant | Connection pool management, migration coordination across N databases |
| Cost | Shared infrastructure reduces per-tenant cost | Noisy neighbor risk on shared resources |
| Observability | Tenant-scoped metrics enable per-customer SLA tracking | Log volume and metric cardinality increase with tenant count |

## Gotchas

1. **The forgotten JOIN** -- When joining tables, both sides must be tenant-scoped. A common bug: `SELECT * FROM messages JOIN conversations ON messages.conversation_id = conversations.id` without filtering both tables by `tenant_id`. Use a base query class or ORM mixin that automatically applies the filter.

2. **Migration across tenants** -- With column-level isolation, a single `ALTER TABLE` affects all tenants simultaneously. With schema/DB-level, migrations must be applied to each tenant's schema independently. Plan migration strategy before choosing the isolation variant.

3. **Tenant ID in every layer** -- It is not enough to filter at the API layer. Background jobs, event handlers, scheduled tasks, and admin tools must all carry and enforce `tenant_id`. A common leak vector is a cron job that processes "all records" without tenant scoping.

4. **Vector DB collection proliferation** -- Per-tenant vector collections are clean for isolation but create operational overhead: collection creation on tenant onboarding, index maintenance, and memory usage. For tenants with very few documents, consider shared collections with tenant metadata filtering (weaker isolation but better resource usage).

5. **Cache key collisions** -- Without tenant-scoped cache keys, Tenant A's cached data can be served to Tenant B. Always prefix cache keys with `tenant:{id}:`. This applies to all caching layers: Redis, in-memory, CDN.

6. **Admin/superuser access** -- Admin users who need cross-tenant visibility (for support, debugging) require a separate access path that explicitly bypasses tenant filtering. This path must be heavily audited and logged.

7. **Tenant deletion complexity** -- Deleting a tenant requires purging data from every store: relational DB, vector DB, cache, file storage, message queues, logs. Build a tenant deletion checklist and automate it from day one.

## Related Artifacts

- Pattern: Hybrid RAG Search with RRF (vector search must be tenant-scoped)
- Pattern: Multi-Agent Orchestrator Pipeline (tenant context must flow through the entire pipeline)
- Pattern: Non-Blocking Side Effects (side effects like CRM sync must carry tenant context)

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
