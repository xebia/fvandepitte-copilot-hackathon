# Foundation Fun Challenge 1: Movie Night Decider

## Concept

Build an app that helps a group decide what to watch together. Users can suggest movies or shows, vote on them, add constraints, and let the app pick the best option.

The challenge is familiar enough for everyone to understand quickly, but it still contains useful logic around voting, constraints, scoring, and tie-breakers.

## Target Users

- Friends
- Families
- Student groups
- Small teams planning a fun evening

## Core Features

### 1. Create a Movie Night

A movie night has:

- Title
- Date
- Host name
- Description
- Maximum runtime in minutes
- Preferred mood:
  - `FUNNY`
  - `ACTION`
  - `RELAXED`
  - `SCARY`
  - `DRAMA`
  - `ANYTHING`
- Status:
  - `OPEN`
  - `VOTING`
  - `DECIDED`
  - `CANCELLED`

### 2. Add Participants

Participants have:

- Name
- Optional email
- Snack preference
- Availability:
  - yes
  - no
  - maybe

Rules:

- Only available participants count in final voting.
- Duplicate names are not allowed within the same movie night.

### 3. Suggest Movies or Shows

A suggestion has:

- Title
- Suggested by
- Genre
- Runtime
- Streaming platform
- Age rating
- Description

Rules:

- Runtime cannot exceed the movie night maximum runtime.
- Suggestions must have a title and runtime.
- Duplicate movie titles should be rejected or merged.

### 4. Voting

Participants can vote:

- `LOVE_IT`
- `OKAY`
- `NOPE`

Rules:

- One vote per participant per suggestion.
- A participant can change their vote.
- A movie with too many `NOPE` votes should be penalized.

### 5. Winner Calculation

The app calculates the best option.

Suggested scoring:

| Vote | Points |
|---|---:|
| `LOVE_IT` | +3 |
| `OKAY` | +1 |
| `NOPE` | -2 |

Suggested tie-breakers:

1. Fewest `NOPE` votes.
2. Shortest runtime.
3. Earliest submitted suggestion.

## Required API Endpoints

```txt
POST   /movie-nights
GET    /movie-nights
GET    /movie-nights/{id}
PATCH  /movie-nights/{id}

POST   /movie-nights/{id}/participants
GET    /movie-nights/{id}/participants

POST   /movie-nights/{id}/suggestions
GET    /movie-nights/{id}/suggestions

POST   /suggestions/{id}/votes
GET    /movie-nights/{id}/results
POST   /movie-nights/{id}/decide
```

## Required Tests

- Cannot add duplicate participant.
- Cannot suggest movie longer than max runtime.
- One vote per participant per movie.
- Winner calculation works.
- Tie-breaker logic works.

## Suggested GitHub Issues

1. Create movie night model and API.
2. Add participants.
3. Add movie suggestions.
4. Add voting.
5. Add winner calculation.
6. Add tests, CI, README, and Copilot instructions.

## Acceptance Criteria

A successful solution:

- Can create a movie night.
- Can add participants and suggestions.
- Can collect votes.
- Can calculate and store a winner.
- Has tests for the decision logic.
- Has clear setup and agent instructions.

## Stretch Goals

- Add simple UI.
- Add anonymous voting.
- Add veto option.
- Add random pick mode.
- Add watch history so the same movie is not picked twice.
