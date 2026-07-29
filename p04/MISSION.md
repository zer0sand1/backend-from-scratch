# Mission: Authentication & Authorization (Backend Roadmap P04)

## Why
P04 is the security foundation that every real backend needs. By the end of this project I want the URL shortener from P03 to have real users — sign-up, login, protected routes, and admin/user roles — so that I can show a hiring manager a backend that won't embarrass them on a security review. Without this, every later project in the roadmap (rate limiting, websockets, e-commerce) sits on top of an API that anyone on the internet can call as anyone.

## Success looks like
- `POST /register` stores users with bcrypt-hashed passwords (never plaintext in the DB).
- `POST /login` returns a short-lived **access token** (15 min) and a long-lived **refresh token** (7 days).
- `GET /me` works only with a valid Bearer token; expired or missing tokens return `401`.
- `POST /refresh` rotates the refresh token and issues a new access token.
- User A gets `403` when trying to delete User B's short URL; admin can manage all users (RBAC).
- Login is rate-limited (5 attempts/min/IP) using Redis.
- I can explain — without notes — the difference between authentication and authorization, why we hash with bcrypt, and why access + refresh tokens exist as a pair.

## Constraints
- Stack is fixed by the roadmap: **Python + FastAPI + PostgreSQL + Redis + SQLAlchemy/Alembic**.
- Self-paced, side project. No team, no deadline, no budget for paid courses.
- I have completed P01–P03, so I already know: raw HTTP, FastAPI routes + Pydantic, REST design, SQLAlchemy models, Alembic migrations, PostgreSQL indexing and connection pooling.
- Type every line myself. Read RFCs and source, not just tutorials.

## Out of scope
- Frontend / web UI — this project is API-only.
- OAuth2 *provider* implementation (being an IdP). P04 only consumes/implements the OAuth2 password grant flow on the server; building a full OAuth2 server is out of scope.
- WebAuthn / passkeys, SAML, OIDC discovery — flagged for "later".
- Multi-tenant authorization, ABAC, ReBAC models — RBAC is enough for P04.