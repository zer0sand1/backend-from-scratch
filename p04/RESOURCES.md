# P04 — Authentication & Authorization Resources

## Knowledge

- [RFC 7519 — JSON Web Token (JWT)](https://www.rfc-editor.org/rfc/rfc7519)
  The primary spec for JWT. Use for: the canonical definition of registered claims (`iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, `jti`), the header/payload/signature structure, and the exact rules for validation. Read before writing the JWT issuer.
- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
  The OAuth2 spec. Use for: the four grant types (authorization code, implicit, client credentials, password), the `/token` endpoint behaviour, and the exact error responses FastAPI's `OAuth2PasswordBearer` is modeled on.
- [OWASP — Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
  Field-tested guidance on login flows, lockout, session IDs. Use for: deciding login rate-limit thresholds and which anti-automation controls belong in P04.
- [OWASP — Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
  Use for: picking bcrypt vs argon2, choosing a work factor, why MD5/SHA-* are wrong for passwords, and the case for pepper.
- [Coda Hale — "How To Safely Store A Password"](https://codahale.com/how-to-safely-store-a-password-in-a-database/)
  The classic 2010 article that introduced bcrypt to most web devs. Use for: the *why* of bcrypt — adaptive cost, salt built into the hash, blowfish-derived key schedule. Still the single best 5-page explainer on the topic.
- [passlib CryptContext documentation](https://passlib.readthedocs.io/en/stable/narr/context.html)
  The library FastAPI's tutorial uses for bcrypt. Use for: `CryptContext(schemes=["bcrypt"], deprecated="auto")`, `hash()`, `verify()` semantics, and how to migrate schemes later without re-hashing everything.
- [FastAPI Security Tutorial — OAuth2 with Password (and Bearer)](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
  Official FastAPI docs. Use for: the exact `OAuth2PasswordBearer` / `OAuth2PasswordRequestForm` wiring and `Depends(get_current_user)` pattern the project will mirror.
- [Auth0 — "Critical vulnerabilities in JSON Web Token libraries" (Tim McLean, 2015)](https://www.chosenplaintext.ca/2015/03/31/jwt-algorithm-confusion.html)
  Use for: the `alg=none` attack and algorithm-confusion attacks. Essential reading *before* picking a JWT library — explains why you must pin the algorithm server-side and never trust the token header.

## Wisdom (Communities)

- [r/FastAPI](https://www.reddit.com/r/FastAPI/)
  Higher-signal than general Python subreddits for FastAPI-specific auth patterns. Use for: comparing `python-jose` vs `pyjwt`, dependency-injection idioms for `get_current_user`.
- [r/netsec](https://www.reddit.com/r/netsec/) and [r/cybersecurity](https://www.reddit.com/r/cybersecurity/)
  Use for: when an auth design choice feels "weird" (rotate vs revoke, where to store refresh tokens on a SPA, JWT vs opaque session cookies). Read threads before asking — most debates have already happened here.
- [OWASP Slack](https://owasp.org/slack/) (channel `#thyboardinghouse`)
  Use for: vetting a non-obvious threat model (e.g. refresh-token theft via XSS vs CSRF) against people who do this professionally.

## Gaps
- No single trusted source yet on **refresh-token rotation + the Redis denylist pattern** in FastAPI specifically. The FastAPI tutorial stops at a single access token. We will derive Lesson 4 from RFC 6749 §10.4 + §6 + the Redis pattern, then sanity-check against community threads.

## User preference on communities
- TBD — user has not yet said whether they want to engage forums or keep it solo. Re-ask in a later session.