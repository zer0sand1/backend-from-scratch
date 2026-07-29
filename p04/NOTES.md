# NOTES — P04 teaching session notes

## Project layout

- **Teaching workspace (this dir root).** Holds `MISSION.md`, `ROADMAP.md`, `GOALS.md`,
  `TIL.md`, `NOTES.md`, `RESOURCES.md`, plus `lessons/`, `reference/`,
  `learning-records/`, `assets/`.
- **Project code lives in `./project/`** (i.e. `Desktop/p04-auth/project/`). Keep
  teaching files and project files separate. FastAPI app, alembic migrations,
  tests, venv all live under `project/`. If the user wants a different path later,
  update this note and `GOALS.md` paths.

## Teaching preferences (confirmed at kickoff)

- **Code-heavy, minimal prose.** Runnable snippets + verification commands over
  long explanation. Don't write paragraphs the user could have read in MDN.
- **RFC / OWASP / repo citations everywhere.** Every non-trivial claim carries a
  link to a primary source. No blog-tier hand-waving, no "common wisdom."
  `RESOURCES.md` is the allow-list of trusted sources.
- **Don't spoon-feed debugging.** When milestone code fails grilling, point the
  user at the area + a question — don't paste the fix. "What does
  `bcrypt.compareSync` return for the empty-string secret? Find it and tell me"
  beats handing them the patch. This is the user's explicit preference.

## Milestone workflow (the agreed loop)

Repeat at the end of every one of the 7 milestones:

1. **User finishes M<N>.** All `/verify/` commands in `GOALS.md` for that
   milestone must pass on the user's machine.
2. **User signals "M<N> done, review my code."** User includes the path/URL where
   the milestone code lives.
3. **Teacher reads the code.** (Files via Read tool, or `gh` diff against the
   previous milestone tag.) Teacher checks it against `GOALS.md` verifications
   and against the spec implied by that milestone's lessons.
4. **Teacher invokes the `grill-me` skill live** — a real-time interview in chat.
   Roughly 5–10 questions, escalating in depth, drawing out whether the user
   understands *why* their own code works, not just that it runs.
5. **User answers inline.** Teacher may follow up.
6. **Teacher decides pass / fail.** On pass: write a new section in `TIL.md`
   under the milestone with what was verified, what the user genuinely now
   understands, and any **knowledge gaps** the grilling exposed. On fail: keep
   grilling or send back to a specific lesson, then re-grill on a separate day.
7. **Teacher unlocks the next milestone's lesson(s)** by writing the next
   `lessons/000X-…html` file and saying *"ready for M<N+1>."*

The same loop cycles through M1 → M7. The final M7 grilling session is the longest
and covers the whole project.

## Preferences / quirks to remember

- User has completed P01–P03 — don't re-teach FastAPI routing, Pydantic,
  SQLAlchemy, Alembic, PG connection pooling. (See `learning-records/0001-*`.)
- User is on Windows (WSL paths noted as `/mnt/c/Users/pinku/Desktop/…`).
- User is self-paced, no team, no deadline — but the grill-me skill is the spike
  of difficulty that prevents illusory fluency.

## Open questions to revisit

- Community engagement preference (`RESOURCES.md` wisdom section) — user has not
  yet said whether they want forum pointers for P04. Re-ask around M4 once the
  project is taking shape.