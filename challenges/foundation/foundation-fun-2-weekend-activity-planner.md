# Foundation Fun Challenge 2: Weekend Activity Planner

## Quick Pitch

A group chat lights up on Thursday: "What are we doing this weekend?" Twenty messages later there's a budget argument, someone's toddler can't do the climbing gym, and the forecast says rain. The Weekend Activity Planner turns that chaos into a plan — people drop in ideas with costs and age limits, everyone votes, and the app stitches the winners into a schedule that actually fits the day, the wallet, and the weather.

## At a Glance

| | |
|---|---|
| Level | Foundation |
| Type | Fun |
| Suggested team size | 2-3 |
| Time box | ~3-4 hours |
| Recommended scope | An API that builds a plan, captures people and activities with constraints, ranks by vote, and generates a time-boxed schedule |

## Learning Goals

- Practice encoding overlapping real-world constraints (budget, age, weather, availability) into clear validation logic with Copilot.
- Use a test-first loop to nail down ranking and schedule-fitting before building endpoints.
- Break the work into issue-sized slices that each ship a usable capability.
- Use Copilot to surface edge cases — over-budget ideas, under-age participants, schedules that overflow the day.
- Ship agent instructions and a README so the project is runnable by anyone on the team.

## Constraints

- Ranking must be derived from votes using a documented, repeatable rule — not a manual sort.
- Only available people may influence voting and ranking.
- Activity suitability (minimum age, budget) is validated against the people on the plan.
- A generated schedule must fit within the available day and respect activity durations.
- State changes follow the status lifecycle (`OPEN` → `VOTING` → `PLANNED`, or `CANCELLED`).

## Non-Goals

- No authentication or user accounts beyond a person's name.
- No live weather, maps, or booking APIs — values are entered by hand.
- No production infrastructure (no cloud deploy, queues, or containers required).
- No polished front-end; UI and calendar export are stretch goals.
- No route optimization or travel-time modelling between activities.

## Domain Rules

### Weekend Plan

A plan has:

- Name
- Date
- Location or city
- Group name
- Budget per person
- Preferred activity type: `INDOOR`, `OUTDOOR`, `FOOD`, `CULTURE`, `SPORT`, `RELAXED`, `ANY`
- Status: `OPEN`, `VOTING`, `PLANNED`, `CANCELLED`

### People

Each person has:

- Name
- Age group: `CHILD`, `TEEN`, `ADULT`, `SENIOR`
- Budget limit
- Mobility notes
- Availability

Rules:

- Activities must be suitable for all required age groups.
- People marked unavailable should not count in voting.

### Activity Ideas

Activity fields:

- Name
- Description
- Type
- Indoor or outdoor
- Estimated cost per person
- Duration in minutes
- Minimum age
- Location
- Requires booking: `yes`, `no`

Rules:

- Activity cost should not exceed the group budget unless marked as over budget.
- Outdoor activities should show a warning if the plan is marked as bad-weather-safe.

### Voting

Users vote `YES`, `MAYBE`, or `NO` on activities.

Rules:

- One vote per person per activity.
- Activities with `NO` votes from children or mobility-constrained people should be flagged.

### Plan Generation

The app produces a suggested schedule, for example:

```txt
10:00 - Breakfast
11:30 - Museum visit
14:00 - Lunch
15:30 - Indoor playground
```

Rules:

- Total duration should fit within the available day.
- Activities requiring booking should be highlighted.
- The highest-ranked activity should be included first.

## Required Endpoints or Flows

```txt
POST   /plans
GET    /plans
GET    /plans/{id}

POST   /plans/{id}/people
GET    /plans/{id}/people

POST   /plans/{id}/activities
GET    /plans/{id}/activities

POST   /activities/{id}/votes
GET    /plans/{id}/ranking
POST   /plans/{id}/generate-schedule
```

## Starter Data

Shared baseline: one plan in Ghent, `budget per person: €40`, preferred type `ANY`, marked bad-weather-safe. Seed these activities:

| Name | Type | Indoor/Outdoor | Cost/person | Duration (min) | Min age | Requires booking |
|---|---|---|---:|---:|---:|---|
| Museum of Fine Arts | CULTURE | Indoor | 12 | 90 | 0 | no |
| City Bike Tour | SPORT | Outdoor | 25 | 120 | 12 | yes |
| Indoor Climbing Gym | SPORT | Indoor | 22 | 90 | 8 | yes |
| Brunch at De Markt | FOOD | Indoor | 18 | 75 | 0 | no |
| Botanical Garden Walk | RELAXED | Outdoor | 0 | 60 | 0 | no |
| Escape Room "Heist" | CULTURE | Indoor | 28 | 60 | 14 | yes |
| Rooftop Cocktails | FOOD | Outdoor | 45 | 90 | 18 | no |

Notes: *Rooftop Cocktails* (€45) exceeds the €40 budget and is adults-only — built-in tests for the budget and minimum-age rules. The two outdoor activities should raise weather warnings on a bad-weather-safe plan.

Sample people: Anja (ADULT, budget €40), Pieter (ADULT, budget €30), Lily (CHILD, age 7, budget €15), Marc (SENIOR, mobility: limited walking, budget €40), Sara (TEEN, age 15, unavailable).

## Test Expectations

- An activity priced above the group budget is flagged as over budget.
- The minimum-age rule correctly excludes activities for under-age people on the plan.
- Vote-based ranking orders activities as specified.
- Unavailable people do not affect voting or ranking results.
- A generated schedule never exceeds the available time for the day.

## Curveball

Midway through, the facilitator announces the forecast flipped to heavy rain all weekend. The plan must now exclude (or strongly warn on) every outdoor activity, and the schedule has to regenerate from indoor options only — while still honouring budget, age, and the day's time box. Teams that modelled "indoor/outdoor" and weather-safety as first-class data will adapt in minutes; others will scramble.

## Scoring Rubric

| Category | Points | What we're looking for |
|---|---:|---|
| Domain correctness | 30 | Budget, age, availability, ranking, and schedule-fit rules all behave as specified. |
| Testing depth | 25 | Constraint and scheduling edge cases are covered, not just the happy path. |
| Architecture & clarity | 20 | Ranking and schedule generation are isolated from transport and easy to follow. |
| Demo quality | 15 | The team builds a plan end-to-end and explains why each activity made the cut. |
| Copilot usage story | 10 | Clear account of how Copilot helped model constraints and generate tests. |

## Demo Script

1. Create the Ghent plan (€40 budget, bad-weather-safe) and add the starter people, including the unavailable teen.
2. Add the starter activities and show *Rooftop Cocktails* being flagged for both budget and minimum age.
3. Cast votes, including a `NO` from the child, and show that activity getting flagged.
4. Call the ranking endpoint and walk through the resulting order.
5. Generate a schedule that fits the day, then trigger the rain curveball and regenerate with indoor-only activities.

## Stretch Ideas

- Add a child-friendly filter that hides anything above a chosen minimum age.
- Add a rainy-day mode that auto-prefers indoor activities.
- Add map links as plain URLs per activity.
- Add export to a calendar format (e.g. iCal).
- Add a surprise-me randomizer for indecisive groups.
- Add a per-person budget check so an activity over *someone's* limit gets flagged, not just the group's.
- Add a "must include a meal" rule so every generated plan has at least one `FOOD` activity.
