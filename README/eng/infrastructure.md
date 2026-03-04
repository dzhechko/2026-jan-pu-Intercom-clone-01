# Infrastructure Guide

## Hardware Requirements

### Minimum (Development / Pilot)

| Resource | Specification | Notes |
|----------|---------------|-------|
| CPU | 4 vCPU | Shared between all containers |
| RAM | 16 GB | Qdrant and PostgreSQL are the heaviest consumers |
| Storage | 200 GB SSD | Database, vector storage, document corpus |
| Network | 100 Mbps | Sufficient for pilot with < 50 concurrent users |

### Recommended (Production)

| Resource | Specification | Notes |
|----------|---------------|-------|
| CPU | 8 vCPU | Handles 100+ concurrent users comfortably |
| RAM | 32 GB | Allows larger Qdrant collections and connection pools |
| Storage | 500 GB NVMe SSD | Room for growing corpus and long-term metric storage |
| Network | 1 Gbps | Recommended for multi-channel production traffic |

### Resource Allocation by Service

| Service | CPU | RAM (Minimum) | RAM (Recommended) | Storage |
|---------|-----|---------------|-------------------|---------|
| API (FastAPI) | 1 vCPU | 2 GB | 4 GB | Minimal |
| Admin (React) | 0.5 vCPU | 512 MB | 1 GB | Minimal |
| PostgreSQL 16 | 1 vCPU | 4 GB | 8 GB | 50-200 GB |
| Qdrant | 1 vCPU | 4 GB | 8 GB | 20-100 GB |
| Redis 7 | 0.5 vCPU | 256 MB | 1 GB | Minimal (in-memory) |
| MinIO | 0.5 vCPU | 512 MB | 1 GB | 50-200 GB |
| Nginx | 0.25 vCPU | 128 MB | 256 MB | Minimal |

---

## Network Configuration

### Port Map

| Port | Service | Protocol | Exposure |
|------|---------|----------|----------|
| 80 | Nginx (HTTP redirect) | TCP | Public |
| 443 | Nginx (HTTPS) | TCP | Public |
| 8001 | API (FastAPI) | TCP | Internal or development only |
| 3000 | Admin Dashboard | TCP | Internal or development only |
| 5432 | PostgreSQL | TCP | Internal only |
| 6333 | Qdrant (HTTP API) | TCP | Internal only |
| 6334 | Qdrant (gRPC) | TCP | Internal only |
| 6379 | Redis | TCP | Internal only |
| 9000 | MinIO (S3 API) | TCP | Internal only |
| 9001 | MinIO (Console) | TCP | Internal only |

### Production Firewall Rules

Only expose ports 80 and 443 to the public internet. All other services communicate via Docker's internal bridge networks (`backend` and `frontend`).

```bash
# UFW example
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### Docker Networks

The `docker-compose.yml` defines two isolated networks:

| Network | Services | Purpose |
|---------|----------|---------|
| `backend` | api, postgres, qdrant, redis, minio | Data layer communication |
| `frontend` | api, admin, nginx | Client-facing communication |

The API service is connected to both networks since it needs to serve HTTP requests (frontend) and access data stores (backend).

---

## External Dependencies

### Required

| Dependency | Purpose | Network Access |
|------------|---------|----------------|
| Anthropic API | Claude LLM (primary AI engine) | Outbound HTTPS to `api.anthropic.com` |
| Telegram Bot API | Telegram channel support | Outbound HTTPS to `api.telegram.org` |

### Optional

| Dependency | Purpose | Network Access |
|------------|---------|----------------|
| GigaChat API | Fallback LLM (Russian language optimized) | Outbound HTTPS to GigaChat endpoints |
| Bitrix24 API | CRM integration | Outbound HTTPS to Bitrix24 instance |
| amoCRM API | Alternative CRM integration | Outbound HTTPS to amoCRM instance |
| Sentry | Error tracking and monitoring | Outbound HTTPS to `sentry.io` |

### DNS Requirements

The server must be able to resolve and connect to the external API endpoints listed above. If your hosting environment uses a restrictive outbound firewall, allow HTTPS (port 443) to these domains.

---

## Docker Requirements

### Engine

| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| Docker Engine | 25.0+ | Latest stable |
| Docker Compose | 2.24+ | Latest stable |
| Docker BuildKit | Enabled | Enabled by default in Docker 25+ |

### Installation (Ubuntu 24.04)

```bash
# Remove old versions
sudo apt remove docker docker-engine docker.io containerd runc 2>/dev/null

# Install prerequisites
sudo apt update
sudo apt install -y ca-certificates curl gnupg

# Add Docker's official GPG key and repository
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and Compose
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add current user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker compose version
```

---

## 152-FZ Compliance: Data Residency

Federal Law 152-FZ ("On Personal Data") requires that personal data of Russian citizens be stored and processed on servers physically located in Russia.

### Requirements

| Requirement | Implementation |
|-------------|----------------|
| Server location | Moscow data center (or other Russian DC) |
| Data at rest | All databases (PostgreSQL, Qdrant, Redis, MinIO) on Russian servers |
| Data in transit | TLS 1.3 for all external communications |
| PII handling | Anonymization after 90 days (automated background job) |
| Backups | Stored on the same server or another Russian DC |

### Recommended VPS Providers (Moscow DC)

| Provider | Notes |
|----------|-------|
| AdminVPS | Budget-friendly, Moscow DC available |
| HOSTKEY | Good performance, Russian entity |
| Selectel | Enterprise-grade, multiple Russian DCs |
| Yandex Cloud | Large-scale, native Russian cloud |

### Verification Checklist

- [ ] Server is physically located in Russia (verify with hosting provider)
- [ ] No data replication to servers outside Russia
- [ ] TLS 1.3 configured on Nginx
- [ ] PII anonymization job is active
- [ ] Backup storage is on Russian servers
- [ ] LLM API calls do not transmit raw PII (pre-processing anonymizes sensitive fields)

---

## Storage Considerations

### PostgreSQL Data Growth

| Data Type | Growth Rate (Estimate) | Notes |
|-----------|----------------------|-------|
| Conversations | ~1 KB per conversation | Metadata and context JSON |
| Messages | ~2 KB per message | Content + metadata |
| Leads | ~0.5 KB per lead | Contact info and qualification data |
| Daily Metrics | ~0.2 KB per day per tenant | Aggregated, compact |

At 1,000 consultations per day with an average of 10 messages each, expect approximately 20 MB/day of database growth (about 7 GB/year).

### Qdrant Storage

Vector storage depends on the corpus size and embedding dimensions:

| Metric | Value |
|--------|-------|
| Embedding dimensions | 1,536 (text-embedding-3-small) |
| Bytes per vector | ~6 KB (1,536 x 4 bytes) |
| 10,000 documents | ~60 MB |
| 100,000 documents | ~600 MB |
| 1,000,000 documents | ~6 GB |

### MinIO Object Storage

Used for the original document corpus (PDFs, HTML) and generated reports. Plan storage based on the volume of documentation to index.

---

## Scaling Path

### Phase 1: Single Server (MVP)

All services on one VPS. Suitable for up to 100 concurrent users and 1,000 consultations per day.

### Phase 2: Vertical Scaling

Upgrade server to 8 vCPU, 32 GB RAM, 500 GB SSD. Handles up to 500 concurrent users.

### Phase 3: Horizontal Scaling

| Component | Strategy |
|-----------|----------|
| FastAPI | Multiple container replicas behind Nginx round-robin |
| PostgreSQL | Add PgBouncer for connection pooling; read replicas for dashboard queries |
| Qdrant | Enable cluster mode with sharding by tenant |
| Redis | Redis Cluster for high availability |
| Background Jobs | Separate worker containers (Celery or similar) |

### Phase 4: Full Separation

Extract heavy services (PostgreSQL, Qdrant) to dedicated servers or managed services. The API and admin containers remain on application servers.
