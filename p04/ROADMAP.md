# ROADMAP — P04 Authentication & Authorization

Bird's-eye view of where we're going on top of the
[backend roadmap](https://zer0sand1.github.io/backend-roadmap/) Phase 2 / Project 04.

## The big picture

After P01–P03 we have an API that anyone on the internet can call as anonymous anyone.
P04 turns it into an API with **identities**: people own things, admins manage people,
and only the right caller gets through the door. It is the security floor under every
later project — you cannot talk sensibly about rate limits, websockets, e-commerce, or
webhooks on top of an unauthenticated API.

P04 = **AuthN (who are you?) + AuthZ (are you allowed?) + tokens (proof you can carry
around) + rate-limiting login (so attackers can't brute-force AuthN).** Everything else
in the spec is mechanics in service of those four ideas.

```
            ┌──── M1 ── Users + bcrypt + register ─────────────────────────┐
AuthN       │                                                              │
            ├──── M2 ── Login + sign first JWT (HS256 access, 15min) ──────┤
            │                                                              │
            ├──── M3 ── get_current_user Depends + 401 cases ──────────────┘
            │
AuthZ       ├──── M4 ── Refresh tokens + rotation + Redis revocation ──┐
            │                                                          │
            └──── M5 ── RBAC + URL ownership + 401 vs 403 ─────────────┘
            │
Defense     ├──── M6 ── Redis login rate limit (5/min/IP, 429)
            │
Hardening   └──── M7 ── alg=none defence, secret hygiene, timing, full walkthrough
```

## How lessons map to milestones

Lessons (in `lessons/`) teach the *concept*. Milestones (in `GOALS.md`) are the *code
checkpoint* you must ship and verify before the next lesson. Roughly one lesson per
milestone, but some milestones need two lessons behind them (e.g. M4 = lessons on JWT
anatomy + refresh rotation). Lessons iterate faster than milestones.

```
M1  ← Lesson 0001 (authn/authz + bcrypt)
M2  ← Lesson 0002 (register/login)  + Lesson 0003 (JWT anatomy, alg=none)
M3  ← Lesson 0004 (FastAPI Depends auth)
M4  ← Lesson 0005 (access vs refresh)  + Lesson 0006 (rotation, revocation)
M5  ← Lesson 0007 (RBAC + ownership, 401 vs 403)
M6  ← Lesson 0008 (Redis token-bucket)
M7  ← Lesson 0009 (security hardening)
```

## What's NOT in P04

- Building your own OAuth2 *provider* (we only consume the password grant).
- WebAuthn / passkeys, SAML, OIDC discovery, multi-tenant ABAC/ReBAC.
- Frontend / cookie-based session flow for a SPA. API-only.

## Out the other side

When M7 verifies, you should be able to walk an interviewer through your P04 repo,
point at code, and answer the four questions:

1. *Where does the password go on the wire?* (bcrypt hash column, plaintext never logged)
2. *What does the token contain, and why can I trust it?* (signed JWT, HS256, pinned alg)
3. *Why two tokens?* (access = stateless + short; refresh = revocable + long)
4. *What stops login brute-force?* (Redis token bucket, 5/min/IP, 429)

That's the green light to start P05 Rate Limiter.