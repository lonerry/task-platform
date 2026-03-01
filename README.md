# Task Platform

Платформа управления задачами на базе микросервисной архитектуры с event-driven взаимодействием через Kafka.

## Архитектура

```
                    ┌─────────────────┐
                    │  Auth Service   │  JWT (access/refresh)
                    │  :8006          │
                    └────────┬────────┘
                             │
         ┌───────────────────▼───────────────────┐
         │           Task Service                 │  CRUD задач, публикует события
         │           :8001                       │
         └───────────────────┬───────────────────┘
                             │
                    ┌────────▼────────┐
                    │     Kafka       │  tasks_created, tasks_updated, tasks_deleted
                    │     :9092       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │ Analytics   │  │ Notification│  │   (другие    │
    │ Service     │  │ Service     │  │  консьюмеры)│
    │ :8002       │  │ :8003       │  │             │
    │ Статистика  │  │ Telegram    │  └─────────────┘
    │ по статусам │  │ уведомления │
    └─────────────┘  └─────────────┘
```

## Сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| **auth-service** | 8006 | Регистрация, логин, JWT, выдача ролей |
| **task-service** | 8001 | CRUD задач, публикация событий в Kafka |
| **analytics-service** | 8002 | Консьюмер Kafka, агрегация статистики по статусам, REST API |
| **notification-service** | 8003 | Консьюмер Kafka, отправка уведомлений в Telegram |

## Стек

- **Python 3.11**, FastAPI, Uvicorn
- **PostgreSQL** (отдельные схемы: auth, tasks, analytics)
- **Kafka** (Confluent), FastStream
- **Dishka** — dependency injection (HTTP + Kafka)
- **Pydantic** — валидация и схемы
- **Alembic** — миграции (auth, task, analytics)
- **Prometheus** + **Grafana** — метрики
- **Docker**, **uv** — сборка и зависимости

## Быстрый старт

### 1. Инфраструктура (Kafka, PostgreSQL, Prometheus, Grafana, Kafdrop)

```bash
cd infrastructure/infrastructure-main
docker-compose up -d
```

Сервисы появятся в сети `task-management`. Kafdrop: http://localhost:9000

### 2. Сервисы приложения

Каждый сервис поднимается отдельно из своей папки. Нужны `.env` с переменными (см. примеры ниже).

**Auth:**
```bash
cd services/auth-service
cp .env.example .env   # при необходимости
docker-compose up -d
# или: uv sync && uv run python src/main.py
```

**Task:**
```bash
cd services/task-service
docker-compose up -d
```

**Analytics:**
```bash
cd services/analytics-service
docker-compose up -d
```

**Notification:**
```bash
cd services/notification-service
# В .env задать TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
docker-compose up -d
```

### 3. Переменные окружения (примеры)

- **auth-service:** `POSTGRES_*`, JWT-секреты, `ADMIN_EMAIL`, `ADMIN_PASSWORD`
- **task-service:** `POSTGRES_*`, `KAFKA_BOOTSTRAP_SERVERS`, JWT для проверки токенов
- **analytics-service:** `POSTGRES_*`, `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`
- **notification-service:** `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

Все сервисы ожидают Kafka по адресу `kafka:9092` и PostgreSQL при использовании своих `docker-compose` (внешняя сеть `task-management`).

## API

- **Auth:** регистрация, логин, refresh, me, назначение ролей (admin).
- **Tasks:** CRUD задач (требуется JWT от auth-service).
- **Analytics:** `GET /task-stats` — общая статистика по задачам (total_tasks, stats_by_status).

Документация: Swagger/ReDoc на `/docs` и `/redoc` у каждого сервиса (если не отключено в PROD).

## Мониторинг

- **Prometheus:** сбор метрик с `/metrics` каждого сервиса (см. `infrastructure/infrastructure-main/prometheus.yml`).
- **Grafana:** дашборды по данным Prometheus (порт 3000, логин/пароль по умолчанию).
- **Kafdrop:** просмотр топиков и consumer groups Kafka.

## Структура репозитория

```
task-platform/
├── infrastructure/infrastructure-main/   # Docker Compose: Kafka, PostgreSQL, Prometheus, Grafana, Kafdrop
├── services/
│   ├── auth-service/
│   ├── task-service/
│   ├── analytics-service/
│   └── notification-service/
└── README.md
```

В каждом сервисе: `src/` (api, core, domain, infrastructure, schemas, services), `Dockerfile`, `docker-compose.yml`, `pyproject.toml`, при необходимости `alembic/` и `.env`.

## Лицензия

MIT
