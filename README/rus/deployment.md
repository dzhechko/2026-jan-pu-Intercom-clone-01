# Развертывание AI-Консультант Cloud.ru

## Системные требования

### Минимальные

| Параметр | Значение |
|----------|----------|
| ОС | Ubuntu 24.04 LTS |
| CPU | 4 vCPU |
| RAM | 16 ГБ |
| Диск | 200 ГБ SSD |
| Docker | 25+ |
| Docker Compose | 2.24+ |

### Рекомендуемые (продакшн)

| Параметр | Значение |
|----------|----------|
| ОС | Ubuntu 24.04 LTS |
| CPU | 8 vCPU |
| RAM | 32 ГБ |
| Диск | 500 ГБ SSD NVMe |
| Docker | 25+ |
| Docker Compose | 2.24+ |

### Требования к размещению

Сервер должен располагаться в московском ДЦ для соответствия 152-ФЗ (персональные данные граждан РФ). Рекомендуемые хостинг-провайдеры: AdminVPS, HOSTKEY, Selectel.

---

## Быстрый старт (разработка)

### 1. Клонирование репозитория

```bash
git clone <repository-url> cloud-consultant
cd cloud-consultant
```

### 2. Настройка переменных окружения

```bash
cp .env.example .env
```

Обязательно заполните следующие переменные в `.env`:

```bash
# Claude API (основная LLM)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# JWT-секрет (минимум 32 символа)
JWT_SECRET_KEY=ваш-секретный-ключ-не-менее-32-символов

# Telegram-бот (если используется)
TELEGRAM_BOT_TOKEN=123456:ABC-DEF
TELEGRAM_WEBHOOK_SECRET=ваш-секрет-вебхука
TELEGRAM_WEBHOOK_URL=https://ваш-домен.ru/api/webhooks/telegram
```

Остальные переменные имеют значения по умолчанию для dev-окружения.

### 3. Запуск контейнеров

```bash
docker compose up -d
```

Docker Compose поднимет 7 сервисов:

| Сервис | Порт | Описание |
|--------|------|----------|
| api | 8001 | FastAPI backend |
| admin | 3000 | React-панель администратора |
| postgres | 5432 | PostgreSQL 16 |
| qdrant | 6333, 6334 | Векторная БД |
| redis | 6379 | Кеш и очереди |
| minio | 9000, 9001 | S3-совместимое хранилище |
| nginx | 8888 (HTTP), 8443 (HTTPS) | Реверс-прокси |

### 4. Инициализация базы данных

```bash
# Через Alembic (рекомендуется)
docker compose exec api alembic upgrade head

# Или через SQLAlchemy create_all (для быстрого старта)
docker compose exec api python -c "
from src.models.base import Base
from src.core.database import sync_engine
Base.metadata.create_all(sync_engine)
"
```

### 5. Проверка работоспособности

```bash
# Health-check API
curl http://localhost:8001/health

# Readiness-check (зависимости)
curl http://localhost:8001/health/ready

# Swagger-документация
# Откройте в браузере: http://localhost:8001/docs

# Панель администратора
# Откройте в браузере: http://localhost:3000
```

---

## Продакшн-развертывание

### TLS-сертификат (Let's Encrypt)

```bash
# Установите certbot
apt-get install -y certbot

# Получите сертификат
certbot certonly --standalone -d ваш-домен.ru

# Скопируйте сертификаты
mkdir -p nginx/ssl
cp /etc/letsencrypt/live/ваш-домен.ru/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/ваш-домен.ru/privkey.pem nginx/ssl/
```

### Настройка Nginx для TLS

Добавьте в `nginx/nginx.conf` блок HTTPS-сервера:

```nginx
server {
    listen 443 ssl http2;
    server_name ваш-домен.ru;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;

    # ... остальные location-блоки
}

server {
    listen 80;
    server_name ваш-домен.ru;
    return 301 https://$host$request_uri;
}
```

### Продакшн-переменные окружения

```bash
# Обязательно измените для продакшна:
DEBUG=false
JWT_SECRET_KEY=<криптографически стойкий ключ 64+ символов>
MINIO_ROOT_USER=<надежный логин>
MINIO_ROOT_PASSWORD=<надежный пароль>
CORS_ORIGINS=["https://ваш-домен.ru"]
LOG_LEVEL=WARNING
```

### Запуск в продакшн-режиме

```bash
docker compose -f docker-compose.yml up -d --build
```

---

## Справочник переменных окружения

| Переменная | Описание | Обязательная | По умолчанию |
|------------|----------|:------------:|--------------|
| `ANTHROPIC_API_KEY` | Ключ API Claude | Да | - |
| `LLM_MODEL` | Основная модель LLM | Нет | claude-sonnet-4-20250514 |
| `LLM_FALLBACK_MODEL` | Резервная модель | Нет | - |
| `DATABASE_URL` | Строка подключения PostgreSQL | Нет | postgresql+asyncpg://app:app_secret@postgres:5432/cloud_consultant |
| `DB_POOL_SIZE` | Размер пула соединений БД | Нет | 20 |
| `DB_MAX_OVERFLOW` | Макс. дополнительных соединений | Нет | 10 |
| `REDIS_URL` | URL Redis | Нет | redis://redis:6379/0 |
| `QDRANT_HOST` | Хост Qdrant | Нет | qdrant |
| `QDRANT_PORT` | Порт Qdrant | Нет | 6333 |
| `QDRANT_API_KEY` | API-ключ Qdrant | Нет | - |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота | При использовании Telegram | - |
| `TELEGRAM_WEBHOOK_SECRET` | Секрет для верификации вебхуков | При использовании Telegram | - |
| `TELEGRAM_WEBHOOK_URL` | Публичный URL вебхука | При использовании Telegram | - |
| `JWT_SECRET_KEY` | Секрет подписи JWT | Да | change-me-... |
| `JWT_ALGORITHM` | Алгоритм JWT | Нет | HS256 |
| `JWT_EXPIRE_MINUTES` | Время жизни токена (мин) | Нет | 60 |
| `MINIO_ROOT_USER` | Логин MinIO | Нет | minioadmin |
| `MINIO_ROOT_PASSWORD` | Пароль MinIO | Нет | minioadmin |
| `MINIO_ENDPOINT` | Адрес MinIO | Нет | minio:9000 |
| `BITRIX24_WEBHOOK_URL` | URL вебхука Bitrix24 | Нет | - |
| `AMOCRM_API_KEY` | API-ключ amoCRM | Нет | - |
| `SENTRY_DSN` | DSN для Sentry | Нет | - |
| `LOG_LEVEL` | Уровень логирования | Нет | INFO |
| `DEBUG` | Режим отладки | Нет | false |
| `RATE_LIMIT_PER_MIN` | Лимит запросов в минуту | Нет | 30 |
| `CORS_ORIGINS` | Разрешенные источники CORS | Нет | ["http://localhost:3000"] |

---

## Обновление системы

```bash
# 1. Получение обновлений
git pull origin main

# 2. Пересборка и перезапуск контейнеров
docker compose up -d --build

# 3. Применение миграций БД
docker compose exec api alembic upgrade head

# 4. Проверка работоспособности
curl http://localhost:8001/health
```

---

## Откат на предыдущую версию

```bash
# 1. Остановка контейнеров
docker compose down

# 2. Откат кода
git checkout <предыдущий-тег-или-коммит>

# 3. Откат миграций (если нужно)
docker compose up -d postgres
docker compose exec api alembic downgrade -1

# 4. Запуск на старой версии
docker compose up -d --build
```

---

## Проверка логов

```bash
# Все сервисы
docker compose logs -f

# Конкретный сервис
docker compose logs -f api

# Последние 100 строк
docker compose logs --tail=100 api
```
