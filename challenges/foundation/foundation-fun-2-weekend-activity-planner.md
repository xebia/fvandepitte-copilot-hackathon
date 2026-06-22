# Foundation Fun Challenge 2: Weekend Activity Planner

## Concept

Build an app that helps a group decide what to do during the weekend. Users suggest activities, add constraints like budget and weather suitability, vote, and generate a simple plan.

## Target Users

- Families
- Friend groups
- Couples
- Student groups

## Core Features

### 1. Create a Weekend Plan

A plan has:

- Name
- Date
- Location or city
- Group name
- Budget per person
- Preferred activity type:
  - `INDOOR`
  - `OUTDOOR`
  - `FOOD`
  - `CULTURE`
  - `SPORT`
  - `RELAXED`
  - `ANY`
- Status:
  - `OPEN`
  - `VOTING`
  - `PLANNED`
  - `CANCELLED`

### 2. Add People

Each person has:

- Name
- Age group:
  - `CHILD`
  - `TEEN`
  - `ADULT`
  - `SENIOR`
- Budget limit
- Mobility notes
- Availability

Rules:

- Activities must be suitable for all required age groups.
- People marked unavailable should not count in voting.

### 3. Add Activity Ideas

Activity fields:

- Name
- Description
- Type
- Indoor or outdoor
- Estimated cost per person
- Duration in minutes
- Minimum age
- Location
- Requires booking:
  - yes
  - no

Rules:

- Activity cost should not exceed the group budget unless marked as over budget.
- Outdoor activities should show a warning if the plan is marked as bad-weather-safe.

### 4. Voting

Users vote on activities:

- `YES`
- `MAYBE`
- `NO`

Rules:

- One vote per person per activity.
- Activities with `NO` votes from children or mobility-constrained people should be flagged.

### 5. Plan Generation

The app creates a suggested schedule.

Example output:

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

## Required API Endpoints

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

## Required Tests

- Activity over budget is flagged.
- Minimum age rule works.
- Vote ranking works.
- Unavailable people do not affect results.
- Generated schedule does not exceed available time.

## Suggested GitHub Issues

1. Create weekend plan model.
2. Add people and constraints.
3. Add activity ideas.
4. Add voting and ranking.
5. Add schedule generation.
6. Add tests and agent-ready docs.

## Acceptance Criteria

A successful solution:

- Lets users create a plan.
- Lets users add people and activities.
- Handles votes and ranking.
- Generates a basic schedule.
- Flags budget and suitability issues.
- Has useful tests and CI.

## Stretch Goals

- Add child-friendly filter.
- Add rainy-day mode.
- Add map links as plain URLs.
- Add export to calendar format.
- Add surprise-me randomizer.
