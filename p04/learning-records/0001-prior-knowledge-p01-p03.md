# Prior knowledge established: P01–P03 complete

User has finished projects P01 (raw HTTP server), P02 (FastAPI + Pydantic + OpenAPI REST API), and P03 (URL shortener with SQLAlchemy, Alembic, PostgreSQL, indexing, pooling). They报到 starting P04 directly. This sets the floor for everything in P04:

- They already know FastAPI route handlers, Pydantic request/response models, `HTTPException`, status codes, and how to layer a REST design.
- They already know SQLAlchemy models, Alembic migrations, `Session` injection via `Depends`, foreign keys, and the P03 schema (URL shortener tables). P04 extends that schema with a `users` table and a `user_id` FK on URLs.
- They have written testable Python and shipped endpoints to a local PostgreSQL.

**Implications for teaching P04**:
- Do **not** re-teach FastAPI routing, `Depends`, Pydantic, or SQLAlchemy model patterns — treat as known. New primitives to introduce: bcrypt via `passlib`, JWT via `python-jose` or `pyjwt`, FastAPI `OAuth2PasswordBearer`, Redis-backed login rate limiting, refresh-token storage/revocation.
- The user's own P03 codebase is the substrate. Every lesson should end with "go add this to your P03 codebase and verify with `curl`" — that is the built-in feedback loop.
- They have not yet worked with Redis, secrets management, or signed tokens — expect genuine first-principles teaching on bcrypt structure and JWT signature mechanics, even if the user is confident on adjacent topics.