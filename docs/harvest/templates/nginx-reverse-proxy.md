# Template: Nginx Reverse Proxy Configuration

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Nginx configuration for a reverse proxy that routes traffic to an API backend and a frontend application. Includes rate limiting zones (API, auth, webhook), security headers, upstream definitions, and SSL/TLS readiness. Designed to sit in front of Docker Compose services.

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `{{API_UPSTREAM}}` | API backend host:port | `api:8000` |
| `{{FRONTEND_UPSTREAM}}` | Frontend host:port | `frontend:3000` |
| `{{DOMAIN}}` | Server name / domain | `example.com` |
| `{{RATE_LIMIT_API}}` | Rate limit for API endpoints (requests/minute) | `30r/m` |
| `{{RATE_LIMIT_AUTH}}` | Rate limit for auth endpoints (requests/minute) | `5r/m` |
| `{{RATE_LIMIT_WEBHOOK}}` | Rate limit for webhook endpoints (requests/minute) | `100r/m` |
| `{{MAX_BODY_SIZE}}` | Maximum client request body size | `10m` |
| `{{SSL_CERT_PATH}}` | Path to SSL certificate file | `/etc/nginx/ssl/fullchain.pem` |
| `{{SSL_KEY_PATH}}` | Path to SSL private key file | `/etc/nginx/ssl/privkey.pem` |

## Template

```nginx
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time';

    access_log /var/log/nginx/access.log main;
    sendfile on;
    keepalive_timeout 65;

    # --- Rate Limiting Zones ---
    limit_req_zone $binary_remote_addr zone=api:10m rate={{RATE_LIMIT_API}};
    limit_req_zone $binary_remote_addr zone=auth:10m rate={{RATE_LIMIT_AUTH}};
    limit_req_zone $binary_remote_addr zone=webhook:10m rate={{RATE_LIMIT_WEBHOOK}};

    # --- Upstream Servers ---
    upstream api_backend {
        server {{API_UPSTREAM}};
    }

    upstream app_frontend {
        server {{FRONTEND_UPSTREAM}};
    }

    # --- HTTP: Redirect to HTTPS (uncomment for production) ---
    # server {
    #     listen 80;
    #     server_name {{DOMAIN}};
    #     return 301 https://$host$request_uri;
    # }

    # --- Main Server Block ---
    # For HTTP-only (development), use listen 80.
    # For HTTPS (production), uncomment the ssl lines and the redirect block above.
    server {
        listen 80;
        # listen 443 ssl http2;
        server_name {{DOMAIN}};

        # --- SSL/TLS (uncomment for production) ---
        # ssl_certificate     {{SSL_CERT_PATH}};
        # ssl_certificate_key {{SSL_KEY_PATH}};
        # ssl_protocols       TLSv1.2 TLSv1.3;
        # ssl_ciphers         HIGH:!aNULL:!MD5;
        # ssl_prefer_server_ciphers on;
        # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # --- Security Headers ---
        add_header X-Content-Type-Options nosniff always;
        add_header X-Frame-Options DENY always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;

        # --- Max Body Size ---
        client_max_body_size {{MAX_BODY_SIZE}};

        # --- API Routes ---
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://api_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 60s;
        }

        # --- Auth Endpoints (stricter rate limit) ---
        location /api/v1/auth/ {
            limit_req zone=auth burst=3 nodelay;
            proxy_pass http://api_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # --- Webhook Endpoints ---
        location /api/v1/webhooks/ {
            limit_req zone=webhook burst=50 nodelay;
            proxy_pass http://api_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # --- Health Checks (no rate limit) ---
        location /health {
            proxy_pass http://api_backend;
        }

        # --- Frontend (catch-all) ---
        location / {
            proxy_pass http://app_frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## Usage

1. Copy this template to `nginx/nginx.conf` in your project.
2. Replace all `{{PLACEHOLDER}}` values.
3. For development, use the HTTP-only configuration (default).
4. For production, uncomment the SSL lines, the HTTPS redirect block, and the HSTS header.
5. Mount the config read-only in your Docker Compose Nginx service.

## Notes

- Rate limiting uses `$binary_remote_addr` (compact IP storage) with a 10MB shared memory zone, supporting roughly 160,000 unique IP addresses per zone.
- The `burst` parameter allows temporary spikes. `nodelay` processes burst requests immediately rather than queuing them.
- The `/api/v1/auth/` location block must appear before the generic `/api/` block because Nginx matches the most specific prefix first.
- `proxy_read_timeout 60s` on the API block prevents Nginx from closing connections during long-running LLM or search requests.
- For WebSocket support (e.g., real-time chat), add `proxy_http_version 1.1;` and `proxy_set_header Upgrade $http_upgrade;` to the relevant location block.
- The `X-Frame-Options DENY` header prevents the site from being embedded in iframes (clickjacking protection). Change to `SAMEORIGIN` if you need iframe embedding within your own domain.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
