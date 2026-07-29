# GOALS — P04 Milestones

Seven small verifiable milestones. Each milestone ships code in your project at
`./project/` (sibling of this teaching workspace root), has a single sentence goal,
a list of files you can expect to touch, and an explicit **verification** block —
concrete shell commands whose output is the proof you're done. Don't move on until
every verification line passes.

Review happens after each milestone per the workflow recorded in
[`NOTES.md`](./NOTES.md): you mark the milestone done → I review code → I invoke the
`grill-me` skill live in chat → you answer → I append gaps to [`TIL.md`](./TIL.md).

---

## M1 — Users, bcrypt, register

**Goal:** The API can create users whose passwords are stored as bcrypt hashes,
with no admin endpoint, no login, no tokens yet.

**Touches:** `project/app/models.py` (new `User`), `project/app/security.py`
(`hash_password`, `verify_password`), `project/app/schemas.py` (`UserCreate`,
`UserRead`), `project/alembic/versions/xxxx_users.py`, `project/app/main.py`
(`POST /register`), `project/requirements.txt` (pin `passlib[bcrypt]`, `bcrypt`).

**Verify:**
- `pip install -r requirements.txt` clean (no `bcrypt`/`passlib` conflict).
- `alembic upgrade head` creates `users` table.
- `curl -s -XPOST localhost:8000/register -d '{"email":"a@b.c","password":"hunter2"}' -H 'Content-Type: application/json'` returns 201 with the user JSON and **no password field**.
- `psql -d <db> -c "SELECT email, hashed_password FROM users;"` shows a string starting `$2b$12$…` — never `hunter2`.
- Two users with the same password → different `hashed_password` rows.

---

## M2 — Login + first signed JWT (access token only)

**Goal:** `POST /login` validates credentials and returns a single HS256-signed
access token. Refresh tokens come in M4 — do NOT build them here.

**Touches:** `project/app/security.py` (new `create_access_token`), `project/app/main.py`
(`POST /token` or `/login`, using `OAuth2PasswordBearer`), `project/.env`
(`JWT_SECRET`, `JWT_ALG=HS256`, `ACCESS_TOKEN_EXPIRE_MINUTES=15`). PyJWT or python-jose.

**Verify:**
- `curl -XPOST localhost:8000/login -d 'username=a@b.c&password=hunter2'` returns
  `{"access_token":"eyJ…","token_type":"bearer"}`.
- Paste the token at <https://jwt.io>, enter your secret → header `alg:HS256`,
  payload has `sub`, `iat`, `exp`; `exp - iat == 900` (15 min).
- Wrong password → 401 with no `hashed_password` echoed in the response body.
- Secret is loaded from env, never hardcoded in `security.py` (grep check:
  `grep -RIn "secret" project/app/ | grep -v env` returns nothing literal).

---

## M3 — Bearer auth dependency + 401 cases

**Goal:** Add a `get_current_user` FastAPI dependency. Protect `GET /me` and the
non-login URL endpoints. Missing, malformed, expired, or signed-with-wrong-secret
tokens all return 401.

**Touches:** `project/app/security.py` (`get_current_user` via `Depends`), `project/app/main.py`
(protect `/me`, list/create URL routes), `project/app/exceptions.py` if you want a shared
401 handler.

**Verify:**
- `curl localhost:8000/me` → 401.
- `curl localhost:8000/me -H "Authorization: Bearer not.a.jwt"` → 401.
- `curl localhost:8000/me -H "Authorization: Bearer <valid>"` → 200 user JSON.
- Sign a token with `exp = now - 1` → 401.
- Sign a token with a different secret → 401.
- (Pin alg: attempt a token with `alg:none` header; it must also 401. We'll
  harden deliberately in M7, but this code path must exist now.)

---

## M4 — Refresh tokens + rotation + revocation

**Goal:** `POST /login` also issues a 7-day refresh token (separate signing key or
`type:refresh` claim). `POST /refresh` accepts a refresh token, mints a new access
token, and **rotates**: the presented refresh is denied on second use. Rotation is
enforced by a Redis set of revoked refresh-token `jti`s.

**Touches:** `project/app/security.py` (`create_refresh_token`, decode split,
`is_revoked`), `project/app/main.py` (`POST /refresh`), `project/app/redis_client.py`
(new — Redis connection), `project/.env` (`REDIS_URL`, `REFRESH_TOKEN_EXPIRE_DAYS=7`).

**Verify:**
- `POST /login` returns `{"access_token":…,"refresh_token":…,"token_type":"bearer"}`.
  At `jwt.io`, refresh token's `exp - iat == 7 * 86400`.
- `curl -XPOST localhost:8000/refresh -d 'refresh_token=<rt>'` → new access_token.
- Calling `POST /refresh` again with the **same** previously-used refresh token → 401.
- Calling `POST /refresh` with an actually-expired refresh token (mint one with
  `exp = now - 1`) → 401.
- After logout (if you build it) or rotation: `redis-cli SMEMBERS revoked:refresh`
  shows the revoked `jti`.

---

## M5 — RBAC + URL ownership + 401 vs 403

**Goal:** URLs gain a `user_id` foreign key. Only the owner (or an admin) may
update or delete a URL. Admins get `GET /admin/users` and a user-deactivate
endpoint. AuthN failures return 401; AuthZ failures return 403 — never the inverse.

**Touches:** `project/alembic/versions/yyyy_urls_user_fk.py` (add `user_id` FK to
`urls`), `project/app/models.py` (`User.role: Literal["user","admin"]`), `project/app/security.py`
(`get_current_active_user`, `require_role("admin")` deps), `project/app/main.py`
(wire ownership checks and admin endpoints).

**Verify:**
- After `POST /shorten` as User A, `SELECT short_code, user_id FROM urls;` shows A's id.
- User B hits `DELETE /urls/<a-s-code>` → **403** (not 404, not 401).
- User A hits own `DELETE /urls/<a-s-code>` → 204.
- Promote User B's row to `role='admin'`; B hits `DELETE /urls/<a-s-code>` → 204.
- Curl `GET /admin/users` as `role='user'` → 403; as admin → 200 list.
- Admin `POST /admin/users/<id>/deactivate` flips `is_active=false`; that user's
  next `/login` → 403 (*after* credentials check — see M7 timing).

---

## M6 — Redis login rate limit (5/min/IP, 429)

**Goal:** Login attempts are throttled per IP at 5/min. Over-limit returns 429 with
`Retry-After`. Implemented as a Redis sliding-window counter; not a naive `time.sleep`.

**Touches:** `project/app/rate_limit.py` (new), `project/app/main.py` (wrap `/login`),
`project/.env` (`LOGIN_RATE_LIMIT_PER_MIN=5`).

**Verify:**
- 6th wrong-password login inside 60 sec from the same IP → 429 with `Retry-After`
  header populated.
- After waiting the window, the 7th attempt is allowed again.
- Rate limit is per IP, not per account: hammering user A from a fresh IP is allowed
  but still limited by that IP's counter.
- Switching to rate-user-not-IP *deliberately left as a M7 grilling question* — do
  not implement it; we'll talk about the tradeoff.

---

## M7 — Security hardening pass + end-to-end walkthrough

**Goal:** Close the obvious holes that earlier milestones skipped under "ship it."
Specifically: pin algorithm server-side so `alg:none` and `alg=RS256` token
confusion fail; constant-time secret comparison; never leak existence of an account
through login error timing; secrets live in env only; serialization never echoes
`hashed_password`.

**Touches:** `project/app/security.py` (alg allowlist),
`project/app/schemas.py` (`hashed_password` excluded from every response model —
Pydantic `Field(exclude=True)`), `project/.gitignore` (`.env`), `project/README.md`
(end-to-end walkthrough section).

**Verify:**
- A token whose header is `{"alg":"none","typ":"JWT"}` and an empty signature → 401
  (explicitly rejected by alg allowlist).
- A token signed with an RSA public key against `alg=RS256` while server expects
  HS256 → 401 (algorithm-confusion attack from McLean 2015 fails).
- `curl -XPOST localhost:8000/login -d 'username=doesnotexist@x.y&password=…'` and
  `curl -XPOST localhost:8000/login -d 'username=real@x.y&password=wrong'` — both
  take a comparable wall-clock time (within a few ms). Difference should not
  betray which account exists.
- `git grep -n "hashed_password"` includes only model definition and security code;
  no serializer includes it.
- `.env` is in `.gitignore` and is not staged in any commit.
- README has a section "End-to-end walkthrough" reproducing the full register →
  login → /me → /shorten → /refresh → DELETE flow with curl commands and expected
  outputs.

---

## When all seven verify

- Push to GitHub.
- `cd` into `project/`, run the README walkthrough end-to-end against a fresh DB.
- Book the final grilling session (the longest).
- Mark the milestone complete. You are ready for P05 — rate limiter & API
  gateway middleware.