# Тестовое задание DevOps: nginx → backend в Docker

Простое веб-приложение (Python, `http.server`), доступное через reverse proxy **nginx**.
Оба сервиса запускаются в Docker-контейнерах через Docker Compose.

## Архитектура

```
            HTTP :80                 docker-сеть (app-network)
 ┌────────┐         ┌───────────────┐      proxy_pass       ┌──────────────────┐
 │ Клиент │ ──────▶ │  nginx        │ ────────────────────▶ │  backend         │
 │ (curl) │         │  em-nginx     │   http://backend:8080 │  em-backend      │
 └────────┘         └───────────────┘                       │  python :8080    │
                     единственный                           └──────────────────┘
                     опубликованный порт                     порт наружу
                                                             НЕ публикуется
```

- **backend** — HTTP-сервер на Python (стандартная библиотека, без зависимостей), слушает порт `8080` **только внутри docker-сети**, отвечает на `/` текстом `Hello from Effective Mobile!`. Запускается не от root.
- **nginx** — официальный образ `nginx:1.27-alpine`, принимает запросы на порт `80` хоста и проксирует их на backend по имени сервиса (`upstream backend { server backend:8080; }`). Конфигурация подключается через volume и заменяет дефолтный конфиг.
- Сервисы общаются по отдельной bridge-сети `app-network`; IP-адреса нигде не захардкожены — используется DNS docker-сети по именам сервисов.

## Структура проекта

```
├── backend/
│   ├── Dockerfile        # образ backend (python:3.12-alpine, non-root)
│   └── app.py            # HTTP-сервер на http.server
├── nginx/
│   └── nginx.conf        # конфиг reverse proxy (upstream + proxy_pass)
├── docker-compose.yml    # два сервиса, сеть, публикация только 80 порта
├── .env.example          # пример настроек (порт nginx)
└── README.md
```

## Как запустить

Требуются Docker и Docker Compose.

```bash
git clone <repo-url>
cd <repo-dir>

# (опционально) настроить порт nginx; по умолчанию 80
cp .env.example .env

docker compose up -d --build
```

## Как проверить

```bash
curl http://localhost
```

Ожидаемый ответ:

```
Hello from Effective Mobile!
```

Убедиться, что backend **не доступен** с хоста напрямую (запрос должен завершиться ошибкой соединения):

```bash
curl http://localhost:8080
```

Остановить:

```bash
docker compose down
```

## Технологии

- Docker / Docker Compose
- nginx 1.27 (официальный alpine-образ)
- Python 3.12 (стандартная библиотека `http.server`, без внешних зависимостей)
