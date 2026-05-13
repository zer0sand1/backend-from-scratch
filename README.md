
# Backend Engineering Roadmap

I'm following the Backend Engineering Roadmap — 18 projects from HTTP fundamentals to production-ready microservices. Each builds on the last, introducing one first-principle concept at a time.

**Timeline**: 5–7 months | **Languages**: Python (primary), TypeScript (secondary)

---

## Phase 1 — Foundations (TCP, HTTP, REST, web frameworks)

1. **Custom HTTP Server from Scratch** — Raw sockets, parse HTTP/1.1, build a router with no frameworks
2. **RESTful Library Management API** — FastAPI, Pydantic, OpenAPI, clean RESTful design
3. **URL Shortener with PostgreSQL** — SQLAlchemy, Alembic, indexing, connection pooling

## Phase 2 — Access & Control (Auth, rate limiting, middleware)

4. **Authentication & Authorization** — JWT, bcrypt, OAuth2, RBAC, refresh tokens
5. **Rate Limiter & API Gateway Middleware** — Redis, token bucket, sliding window, ASGI middleware

## Phase 3 — Real-time & Async (WebSockets, pub/sub, async processing)

6. **Real-time Chat with WebSockets** — Full-duplex, rooms, Redis Pub/Sub, connection management
7. **File Upload Service with Async Processing** — Celery, image thumbnails, content-addressable storage, CDN simulation

## Phase 4 — Reliability & Correctness (Transactions, concurrency, testing)

8. **E-commerce Order Service** — ACID, optimistic/pessimistic locking, idempotency, saga pattern
9. **Testing Deep-Dive** — pytest, fixtures, mocking, integration tests, testcontainers

## Phase 5 — Events & Communication (Search, message queues, webhooks, gRPC)

10. **Full-Text Search Engine** — Inverted indexes, TF-IDF, BM25, fuzzy search, type-ahead
11. **Background Job Worker with RabbitMQ** — Message queues, worker pools, retry, dead letter queues
12. **Webhook Delivery System** — Event-driven, HMAC signatures, retry with backoff, idempotency
13. **gRPC Microservice** — Protocol Buffers, inter-service RPC, streaming

## Phase 6 — Performance & Visibility (Caching, monitoring, tracing)

14. **Caching Layer & CDN Simulator** — LRU, cache-aside, write-through, thundering herd, TTL
15. **Observability Stack** — Prometheus, Grafana, OpenTelemetry, structured logging

## Phase 7 — TypeScript & Modern APIs

16. **TypeScript + Express REST API with Prisma** — Express, Prisma ORM, Zod validation
17. **GraphQL API Wrapper** — Apollo, DataLoader, subscriptions, code-first schema

## Phase 8 — Production (Containerization, CI/CD, cloud)

18. **Docker, CI/CD & Cloud Deployment** — Multi-service Docker Compose, GitHub Actions, deploy to Render/Fly.io

---

## Technology Stack

**Core (know deeply)**: Python, TypeScript, FastAPI, PostgreSQL, Redis, SQLAlchemy, Docker, Docker Compose, Git, REST APIs, pytest

**Nice-to-have**: RabbitMQ, Celery, JWT/OAuth2, Prometheus, OpenTelemetry, GraphQL, WebSockets, gRPC, Nginx, GitHub Actions, Express, Prisma

---

## Concept Dependency Map

- TCP/Sockets → HTTP → REST → FastAPI → Database CRUD → Auth
- HTTP → Middleware → Rate Limiting → Caching
- Database → Transactions → Concurrency Control → Idempotency
- WebSockets → Pub/Sub → Real-time
- Message Queues → Async Workers → Webhooks → Event-Driven
- Protocol Buffers → gRPC → Service Communication
- Search Indexes → Tokenization → Ranking (TF-IDF/BM25)
- Logging + Metrics + Tracing → Observability
- REST → GraphQL → DataLoader
- Docker + Compose + Actions → Cloud Deploy

---

## My Approach

1. **Build, don't copy** — type every line, read errors, use debuggers, understand before moving on.
2. **Read deeply** — when stuck, search for *why* not *how*. Read RFCs, source code, engineering blogs.
3. **Verify every goal** — each project has concrete verification goals; don't move on until they pass.
4. **Portfolio ready** — push every project to GitHub with good READMEs, be ready to explain design choices.
>>>>>>> 59969c0 (Step 1: TCP server binds, listens, accepts connections, sends HTTP response)
