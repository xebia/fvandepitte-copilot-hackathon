# Advanced Fun Challenge 1: Quiz Night Engine

## Concept

Build a platform for running a quiz night with teams, rounds, questions, scoring, joker rounds, timers, and a live scoreboard.

This challenge is useful for advanced Copilot work because it has state, rules, edge cases, scoring logic, and enough complexity to make tests valuable.

## Target Users

- Quiz host
- Teams
- Players
- Event organizer

## Core Features

### 1. Quiz Event

A quiz event has:

- Name
- Host
- Date
- Location
- Status:
  - `DRAFT`
  - `OPEN`
  - `IN_PROGRESS`
  - `FINISHED`
- Current round
- Current question

Rules:

- A quiz cannot start without at least 2 teams.
- A quiz cannot start without at least 1 round.
- Finished quizzes cannot be modified.

### 2. Teams

Team fields:

- Team name
- Members
- Contact person
- Joker used:
  - yes
  - no
- Total score

Rules:

- Team names must be unique per quiz.
- Team size can be limited.
- A team can use only one joker.

### 3. Rounds

A round has:

- Name
- Category
- Question type:
  - `TEXT`
  - `MULTIPLE_CHOICE`
  - `NUMBER`
  - `TRUE_FALSE`
- Points per question
- Allows joker:
  - yes
  - no

### 4. Questions and Answers

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

- Answers after the time limit should be marked late.
- Late answers receive 0 points.
- Case-insensitive matching is enough for text answers.
- Number answers can support a tolerance range.

### 5. Scoring Engine

The scoring engine should calculate:

- Points per answer.
- Joker multiplier.
- Round totals.
- Overall ranking.
- Tie-breaker result.

Suggested tie-breakers:

1. Most perfect rounds.
2. Most correct answers.
3. Earliest final answer submitted.

### 6. Live Scoreboard

The app should expose:

- Current ranking.
- Round ranking.
- Team details.
- Score history.

This does not need real-time websockets. A polling endpoint is sufficient.

## Required API Endpoints

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

## Required Tests

- Quiz cannot start without teams.
- Team names must be unique.
- Joker can only be used once.
- Late answer receives 0 points.
- Score calculation works.
- Tie-breaker logic works.

## Advanced Architecture Requirements

Separate:

- Quiz lifecycle
- Team management
- Question management
- Answer submission
- Scoring engine
- Scoreboard/read model

## Required Agent-Ready Deliverables

- `docs/domain-model.md`
- `docs/scoring-rules.md`
- `docs/state-transitions.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`

## Suggested GitHub Issues

1. Create quiz lifecycle model.
2. Add teams.
3. Add rounds and questions.
4. Add answer submission.
5. Implement scoring engine.
6. Add scoreboard.
7. Add tests and CI.
8. Add agent-ready documentation.

## Acceptance Criteria

A successful solution:

- Can create and run a quiz.
- Supports teams, rounds, questions, and answers.
- Calculates scores correctly.
- Handles joker logic.
- Provides scoreboard endpoints.
- Has strong tests around scoring and state.

## Stretch Goals

- Add host UI.
- Add player answer UI.
- Add QR-code join page.
- Add question import from CSV.
- Add pub quiz mode with image/audio placeholder fields.
