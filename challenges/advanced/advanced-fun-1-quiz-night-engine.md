# Advanced Fun Challenge 1: Quiz Night Engine

## Quick Pitch

It's Friday night at the local pub. Forty people are crammed around twelve tables, the host has a microphone and a dodgy spreadsheet, and an argument has just broken out over whether "Reykjavik" counts when a team wrote "Reikiavik". The host needs a real engine: rounds, timers, jokers, fair scoring, and a scoreboard nobody can dispute. Build the thing that lets a host run quiz night without losing the room.

## At a Glance

| | |
|---|---|
| Level | Advanced |
| Type | Fun |
| Suggested team size | 3-4 |
| Time box | Full day, or an ambitious half-day |
| Recommended scope | Quiz lifecycle + scoring engine + scoreboard, with tests on scoring and state |

## Learning Goals

- Drive Copilot agent mode across a multi-module backend instead of single-file snippets.
- Isolate a pure scoring engine and let Copilot generate thorough tests against it.
- Use multi-file edits to keep lifecycle, write paths, and read models in sync.
- Capture domain rules in `docs/` and `.github/copilot-instructions.md` so the agent stays on-rules.
- Reason about state machines and edge cases (late answers, ties, jokers) with Copilot as a pair.

## Constraints

- The scoring engine must be a pure, separately testable module with no HTTP or database dependencies.
- Quiz state transitions must be explicit and enforced (`DRAFT` → `OPEN` → `IN_PROGRESS` → `FINISHED`).
- A finished quiz is immutable; no further writes are accepted.
- Tie-breakers must be deterministic and applied in the defined order.
- Answer correctness rules (case-insensitive text, number tolerance, late = 0) live in the engine, not scattered across controllers.

## Non-Goals

- No real-time websockets; a polling scoreboard endpoint is sufficient.
- No authentication or user accounts.
- No production-grade host or player UI (those are stretch goals).
- No media hosting; image/audio question types stay as placeholder fields at most.

## Domain Rules

### Quiz Event

A quiz event has:

- Name
- Host
- Date
- Location
- Status: `DRAFT`, `OPEN`, `IN_PROGRESS`, `FINISHED`
- Current round
- Current question

Rules:

- A quiz cannot start without at least 2 teams.
- A quiz cannot start without at least 1 round.
- Finished quizzes cannot be modified.

### Teams

Team fields:

- Team name
- Members
- Contact person
- Joker used: yes / no
- Total score

Rules:

- Team names must be unique per quiz.
- Team size can be limited.
- A team can use only one joker.

### Rounds

A round has:

- Name
- Category
- Question type: `TEXT`, `MULTIPLE_CHOICE`, `NUMBER`, `TRUE_FALSE`
- Points per question
- Allows joker: yes / no

### Questions and Answers

Question fields:

- Round
- Question text
- Correct answer
- Options, if multiple choice
- Time limit in seconds
- Explanation

Answer fields:

- Team
- Question
- Submitted answer
- Submitted at
- Is correct
- Points awarded

Rules:

- Answers after the time limit are marked late.
- Late answers receive 0 points.
- Case-insensitive matching is enough for text answers.
- Number answers can support a tolerance range.

### Scoring Engine

The scoring engine calculates:

- Points per answer.
- Joker multiplier.
- Round totals.
- Overall ranking.
- Tie-breaker result.

Tie-breakers, applied in order:

1. Most perfect rounds.
2. Most correct answers.
3. Earliest final answer submitted.

### Live Scoreboard

The app exposes:

- Current ranking.
- Round ranking.
- Team details.
- Score history.

## Required Endpoints or Flows

```txt
POST   /quizzes
GET    /quizzes
GET    /quizzes/{id}

POST   /quizzes/{id}/teams
GET    /quizzes/{id}/teams

POST   /quizzes/{id}/rounds
GET    /quizzes/{id}/rounds

POST   /rounds/{id}/questions
GET    /rounds/{id}/questions

POST   /questions/{id}/answers
POST   /teams/{id}/use-joker

POST   /quizzes/{id}/start
POST   /quizzes/{id}/next-question
POST   /quizzes/{id}/finish

GET    /quizzes/{id}/scoreboard
GET    /quizzes/{id}/score-history
```

## Architecture Expectations

Keep these concerns separated so they can evolve and be tested independently:

- Quiz lifecycle
- Team management
- Question management
- Answer submission
- Scoring engine
- Scoreboard / read model

The scoring engine in particular must be reachable in tests without spinning up the API or a database.

## Agent-Ready Deliverables

The repository should contain:

- `docs/domain-model.md`
- `docs/scoring-rules.md`
- `docs/state-transitions.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`

Suggested GitHub issues to seed the board:

1. Create quiz lifecycle model.
2. Add teams.
3. Add rounds and questions.
4. Add answer submission.
5. Implement scoring engine.
6. Add scoreboard.
7. Add tests and CI.
8. Add agent-ready documentation.

## Starter Data

Seed one quiz so every team demos against the same baseline.

**Quiz:** "The Pub Quiz Championship" — host Maya, status `OPEN`.

Teams:

| Team name | Contact | Joker used | Total score |
|---|---|---|---|
| The Quizzly Bears | Tom | no | 0 |
| Les Quizerables | Anaïs | no | 0 |
| Sherlock Homies | Dev | no | 0 |
| Trivia Newton John | Priya | no | 0 |

Rounds:

| Round | Category | Type | Points | Allows joker |
|---|---|---|---|---|
| Geography Warmup | Geography | `TEXT` | 10 | no |
| Pop Culture | Movies | `MULTIPLE_CHOICE` | 15 | yes |
| Numbers Game | Science | `NUMBER` | 20 | yes |

Questions:

| Round | Question | Correct answer | Time limit | Notes |
|---|---|---|---|---|
| Geography Warmup | Capital of Iceland? | Reykjavik | 30s | text, case-insensitive |
| Pop Culture | Director of *Inception*? | Christopher Nolan | 20s | options: Nolan / Spielberg / Villeneuve / Fincher |
| Numbers Game | Boiling point of water in °C at sea level? | 100 | 25s | tolerance ±1 |

## Test Expectations

The suite should prove, at minimum:

- A quiz cannot start without teams.
- Team names must be unique within a quiz.
- A joker can only be used once per team.
- A late answer receives 0 points.
- Score calculation produces correct round totals and overall ranking.
- Tie-breaker logic resolves equal scores in the defined order.

Aim for the scoring engine to have the deepest coverage, including joker multipliers and all three tie-breaker levels.

## Curveball

Two hours in, the facilitator announces a new house rule: the host can declare a "double points" final round on the fly, and any team that has **not** yet used its joker may stack the joker on top of the double. Teams must support a round-level points multiplier set at runtime and prove the joker-plus-double interaction still resolves correctly in the scoring engine — without breaking existing tie-breaker tests.

## Scoring Rubric

| Criteria | Points | Note |
|---|---|---|
| Domain correctness | 25 | Lifecycle, joker, late-answer, and tie-breaker rules behave exactly as specified. |
| Testing depth | 20 | Scoring engine and state transitions are covered, including edge cases. |
| Architecture & clarity | 25 | Scoring engine is a clean, dependency-free module; concerns are separated. |
| Demo quality | 15 | A full quiz runs end to end and the scoreboard tells a clear story. |
| Copilot/agent usage story | 15 | Team can show how agent mode and the docs drove multi-file work. |

## Demo Script

1. **0:00–0:45** — Open "The Pub Quiz Championship", show the four seeded teams and three rounds, then start the quiz (proving the 2-team / 1-round guards).
2. **0:45–2:00** — Submit answers for two questions: one correct, one late, and one team uses its joker. Walk through how the scoring engine awarded points.
3. **2:00–3:00** — Hit the scoreboard endpoint to show live ranking, then force a tie and show the tie-breaker resolving it. Close with a one-line note on how Copilot generated the scoring tests.

## Stretch Ideas

- Add a host UI.
- Add a player answer UI.
- Add a QR-code join page.
- Add question import from CSV.
- Add pub quiz mode with image/audio placeholder fields.
- Add a "fastest finger" speed bonus that rewards the earliest correct answer per question.
- Add an audience side-bet leaderboard that runs alongside the official scoreboard.
