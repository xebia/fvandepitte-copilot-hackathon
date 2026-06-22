# Foundation Fun Challenge 1: Movie Night Decider

## Quick Pitch

It's Friday night, six friends are sprawled across a couch, and twenty minutes have already vanished into the "I don't care, you pick" loop. Someone wants something funny, someone else is half-asleep and wants short, and one person keeps vetoing anything with subtitles. The Movie Night Decider ends the standoff: everyone tosses in suggestions, casts honest votes, and the app crunches the numbers into a single, defensible winner — runtime limits and all.

## At a Glance

| | |
|---|---|
| Level | Foundation |
| Type | Fun |
| Suggested team size | 2-3 |
| Time box | ~3-4 hours |
| Recommended scope | A working API that creates a movie night, collects suggestions and votes, and computes a winner with tie-breakers |

## Learning Goals

- Practice translating fuzzy social rules (votes, vetoes, tie-breakers) into precise, testable logic with Copilot.
- Use a test-first loop to lock down the scoring and tie-breaker algorithm before wiring up endpoints.
- Drive the build with small, issue-sized increments rather than one big push.
- Explore the domain with Copilot by asking it to enumerate edge cases (changed votes, duplicate titles, over-length runtimes).
- Produce clear agent instructions and a README so a teammate could run the project cold.

## Constraints

- The winner must be computed from the documented scoring table and tie-breaker order — no hand-wavy "vibes" ranking.
- Only participants marked as available may influence the final result.
- Each participant gets exactly one vote per suggestion (changeable, never stacked).
- A suggestion's runtime may not exceed the movie night's maximum runtime.
- State changes follow the status lifecycle (`OPEN` → `VOTING` → `DECIDED`, or `CANCELLED`).

## Non-Goals

- No authentication, accounts, or user identity beyond a participant name.
- No real streaming integration or movie metadata lookups — data is entered by hand.
- No production infrastructure (no containers, queues, or cloud deploy required).
- No polished front-end; a UI is a stretch goal only.
- No recommendation/ML engine — the winner is deterministic scoring, not prediction.

## Domain Rules

### Movie Night

A movie night has:

- Title
- Date
- Host name
- Description
- Maximum runtime in minutes
- Preferred mood: `FUNNY`, `ACTION`, `RELAXED`, `SCARY`, `DRAMA`, `ANYTHING`
- Status: `OPEN`, `VOTING`, `DECIDED`, `CANCELLED`

### Participants

Participants have:

- Name
- Optional email
- Snack preference
- Availability: `yes`, `no`, `maybe`

Rules:

- Only available participants count in final voting.
- Duplicate names are not allowed within the same movie night.

### Suggestions

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

### Voting

Participants can vote `LOVE_IT`, `OKAY`, or `NOPE`.

Rules:

- One vote per participant per suggestion.
- A participant can change their vote.
- A movie with too many `NOPE` votes should be penalized.

### Winner Calculation

Scoring:

| Vote | Points |
|---|---:|
| `LOVE_IT` | +3 |
| `OKAY` | +1 |
| `NOPE` | -2 |

Tie-breakers, applied in order:

1. Fewest `NOPE` votes.
2. Shortest runtime.
3. Earliest submitted suggestion.

## Required Endpoints or Flows

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

## Starter Data

Use this shared baseline so every team's demo starts from the same couch. One movie night (`max runtime: 130 min`, mood `ANYTHING`) with these suggestions:

| Title | Suggested by | Genre | Runtime | Platform | Age rating |
|---|---|---|---:|---|---|
| The Grand Budapest Hotel | Lena | Comedy | 99 | Disney+ | 12 |
| Mad Max: Fury Road | Tomas | Action | 120 | Netflix | 16 |
| Paddington 2 | Sofie | Family | 103 | Prime | 6 |
| Hereditary | Marie | Horror | 127 | Netflix | 18 |
| Spirited Away | Lena | Animation | 125 | Netflix | 9 |
| Knives Out | Dries | Mystery | 130 | Prime | 12 |
| The Irishman | Tomas | Drama | 209 | Netflix | 16 |

Note: *The Irishman* (209 min) exceeds the 130-minute cap and should be rejected — a built-in test case for your runtime rule.

Sample participants: Lena (available, popcorn), Tomas (available, nachos), Sofie (available, none), Marie (maybe), Dries (available, candy), Wout (not available).

## Test Expectations

- Adding a duplicate participant to the same movie night is rejected.
- A suggestion longer than the night's maximum runtime is rejected.
- A participant cannot register two simultaneous votes on the same suggestion; re-voting replaces the prior vote.
- Winner calculation produces the correct score from the points table.
- Tie-breaker logic resolves equal scores using fewest `NOPE`, then shortest runtime, then earliest submission.

## Curveball

Halfway through the session, the host announces the streaming subscription for one platform just expired — any suggestion on that platform is now unwatchable. Teams must filter out (or flag) those suggestions *before* recomputing the winner, without breaking existing votes or tie-breakers. The cleanest solutions treat this as a soft constraint rather than deleting data.

## Scoring Rubric

| Category | Points | What we're looking for |
|---|---:|---|
| Domain correctness | 30 | Scoring, vetoes, runtime cap, and tie-breakers behave exactly as specified. |
| Testing depth | 25 | Decision logic and edge cases (re-votes, ties, over-length) are covered, not just happy paths. |
| Architecture & clarity | 20 | Voting/scoring logic is separated from transport; code reads cleanly. |
| Demo quality | 15 | The team can drive a movie night end-to-end and explain the winner. |
| Copilot usage story | 10 | Clear account of how Copilot helped explore rules and generate tests. |

## Demo Script

1. Create a movie night with a 130-minute cap, then add the starter participants (including one unavailable person).
2. Submit several starter suggestions and show *The Irishman* being rejected for exceeding the runtime cap.
3. Cast votes from available participants, then change one participant's vote to prove the one-vote rule.
4. Call the results endpoint and walk through how the winning score was computed.
5. Trigger a tie scenario (or the platform curveball) and show the tie-breaker / filter resolving it, then `decide` to lock the winner.

## Stretch Ideas

- Add a simple UI for suggesting and voting.
- Add anonymous voting so peer pressure doesn't skew results.
- Add a veto option that can hard-block a suggestion.
- Add a random pick mode for when the group truly can't decide.
- Add watch history so the same movie isn't picked twice across nights.
- Add a "mood match" bonus that nudges suggestions matching the night's preferred mood.
