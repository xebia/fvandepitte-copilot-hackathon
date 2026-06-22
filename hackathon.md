# GitHub Copilot Advanced Hackathon Challenge Pack

## Purpose

This hackathon is designed for participants who already had hands-on sessions with GitHub Copilot and are ready for a more open-ended challenge.

The format is intentionally simple:

> Here is the challenge. Build it. Make it runnable. Make it testable. Make the repository agent-ready.

The goal is not only to build a working application, but also to learn how to use GitHub Copilot in a more advanced and realistic development workflow:

- Exploring an unknown problem domain.
- Creating a project structure from scratch.
- Writing useful issues and acceptance criteria.
- Generating and improving tests.
- Creating documentation that helps both humans and AI coding agents.
- Using Copilot Chat, Copilot Edits, agent mode, custom instructions, and issue-driven development.

The challenges are divided into beginner and advanced levels, with both fun and business-oriented topics.

---

## Common Requirements for Every Challenge

Each team should deliver a GitHub repository that contains a working application and enough supporting material to make the project understandable and maintainable.

### Technical Scope

Teams can choose between:

- Java, preferably Spring Boot.
- Python, preferably FastAPI or Django.
- A simple frontend is optional.
- API-only, CLI, or simple web UI solutions are all acceptable.

### Required Repository Deliverables

Every repository should include:

- `README.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`
- `docs/architecture.md`
- `docs/testing.md`
- At least 5 well-written GitHub Issues used as implementation backlog.
- GitHub Actions workflow for build and test.
- Unit tests for core logic.
- At least one integration or API test.
- Seed or demo data.

### Agent-Ready Repository Expectations

The repository should be easy for both humans and AI coding agents to understand.

A good solution should document:

- How to run the application.
- How to run the tests.
- The domain model.
- Important business rules.
- Architectural decisions.
- Known limitations.
- Suggested future improvements.
- What Copilot should and should not do when editing the codebase.

### Copilot Usage Expectations

Teams should be able to explain how they used Copilot during the challenge.

Examples:

- Using Copilot Chat to explore the domain.
- Asking Copilot to propose a project structure.
- Generating a first version of tests.
- Asking Copilot to explain unfamiliar code.
- Using Copilot Edits to apply changes across multiple files.
- Using agent mode to implement a GitHub Issue.
- Creating custom instructions for the repository.
- Reviewing and correcting Copilot-generated code.

---

# Challenge Menu

## Beginner Challenges

| Type | Challenge |
|---|---|
| Fun | [Movie Night Decider](#beginner-fun-challenge-1-movie-night-decider) |
| Fun | [Weekend Activity Planner](#beginner-fun-challenge-2-weekend-activity-planner) |
| Business | [Mini Expense Claims](#beginner-business-challenge-1-mini-expense-claims) |
| Business | [Support Ticket Triage Board](#beginner-business-challenge-2-support-ticket-triage-board) |

## Advanced Challenges

| Type | Challenge |
|---|---|
| Fun | [Quiz Night Engine](#advanced-fun-challenge-1-quiz-night-engine) |
| Fun | [Escape Room Builder & Solver](#advanced-fun-challenge-2-escape-room-builder--solver) |
| Business | [Intelligent Support Operations Hub](#advanced-business-challenge-1-intelligent-support-operations-hub) |
| Business | [Developer Self-Service Portal](#advanced-business-challenge-2-developer-self-service-portal) |

---

# Beginner Fun Challenge 1: Movie Night Decider

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

---

# Beginner Fun Challenge 2: Weekend Activity Planner

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

---

# Beginner Business Challenge 1: Mini Expense Claims

## Concept

Build a lightweight expense claim system for employees. Employees submit expenses, managers approve or reject them, and finance can export approved claims.

## Target Users

- Employee
- Manager
- Finance user

## Core Features

### 1. Submit Expense Claim

Employees can create claims.

Claim fields:

- Employee name
- Department
- Date
- Category:
  - `TRAVEL`
  - `FOOD`
  - `HOTEL`
  - `SUPPLIES`
  - `OTHER`
- Amount
- Currency
- Description
- Receipt URL or filename
- Status:
  - `DRAFT`
  - `SUBMITTED`
  - `APPROVED`
  - `REJECTED`
  - `PAID`

Rules:

- Amount must be greater than 0.
- Expenses over 250 require manager approval.
- Food expenses over 50 require a note.
- Claims cannot be submitted without a description.

### 2. Manager Review

Managers can approve or reject submitted claims.

Rules:

- Rejected claims require a reason.
- Approved claims cannot be edited.
- Paid claims cannot be changed.

### 3. Finance Overview

Finance can view:

- All approved claims.
- Total amount by department.
- Total amount by category.
- Claims waiting for payment.

### 4. Export

Provide a simple CSV export for approved claims.

## Required API Endpoints

```txt
GET    /claims
POST   /claims
GET    /claims/{id}
PATCH  /claims/{id}
POST   /claims/{id}/submit
POST   /claims/{id}/approve
POST   /claims/{id}/reject
POST   /claims/{id}/mark-paid

GET    /reports/summary
GET    /exports/approved-claims.csv
```

## Required Tests

- Claim amount must be positive.
- Food over 50 requires note.
- Rejection requires reason.
- Approved claim cannot be edited.
- Summary report calculates totals correctly.

## Suggested GitHub Issues

1. Create claim domain model and API.
2. Add validation rules.
3. Add manager approval workflow.
4. Add finance summary report.
5. Add CSV export and tests.

## Acceptance Criteria

A successful solution:

- Supports claim creation and submission.
- Supports approve, reject, and pay workflow.
- Enforces validation rules.
- Produces a summary report.
- Exports approved claims as CSV.

## Stretch Goals

- Add role-based access.
- Add receipt upload mock.
- Add audit trail.
- Add monthly budget warnings.
- Add dashboard UI.

---

# Beginner Business Challenge 2: Support Ticket Triage Board

## Concept

Build a basic support ticket triage system. Customers submit tickets, support agents categorize them, and the system tracks priority and SLA status.

## Target Users

- Customer
- Support agent
- Support manager

## Core Features

### 1. Ticket Creation

Ticket fields:

- Customer name
- Customer email
- Subject
- Description
- Category:
  - `BILLING`
  - `TECHNICAL`
  - `ACCOUNT`
  - `FEATURE_REQUEST`
  - `OTHER`
- Priority:
  - `LOW`
  - `MEDIUM`
  - `HIGH`
  - `URGENT`
- Status:
  - `OPEN`
  - `IN_PROGRESS`
  - `WAITING_FOR_CUSTOMER`
  - `RESOLVED`
  - `CLOSED`
- Created date
- Assigned agent

Rules:

- Subject and description are required.
- Urgent tickets must have an assigned agent.
- Closed tickets cannot be edited.

### 2. Ticket Assignment

Support agents can assign tickets to themselves or others.

Rules:

- A ticket can only have one active assignee.
- Resolved tickets can still be reassigned.
- Closed tickets cannot be reassigned.

### 3. SLA Calculation

Each priority has an SLA target:

| Priority | SLA |
|---|---:|
| `LOW` | 5 business days |
| `MEDIUM` | 3 business days |
| `HIGH` | 1 business day |
| `URGENT` | 4 hours |

The app should show:

- SLA due date.
- Whether the ticket is overdue.
- Time remaining.

### 4. Comment History

Agents can add comments.

Comment fields:

- Ticket ID
- Author
- Message
- Created date
- Internal or external flag

## Required API Endpoints

```txt
GET    /tickets
POST   /tickets
GET    /tickets/{id}
PATCH  /tickets/{id}
POST   /tickets/{id}/assign
POST   /tickets/{id}/comments
GET    /tickets/{id}/comments

GET    /reports/sla
```

## Required Tests

- Ticket requires subject and description.
- Closed ticket cannot be edited.
- Urgent ticket requires assignee.
- SLA due date is calculated correctly.
- Overdue tickets are detected.

## Suggested GitHub Issues

1. Create ticket model and API.
2. Add assignment workflow.
3. Add SLA calculation.
4. Add comments.
5. Add SLA report and tests.

## Acceptance Criteria

A successful solution:

- Supports ticket creation and assignment.
- Tracks status changes.
- Calculates SLA status.
- Supports comments.
- Has tests and CI.

## Stretch Goals

- Add simple UI board.
- Add search by customer email.
- Add canned responses.
- Add ticket tags.
- Add rule-based category suggestion.

---

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

---

# Advanced Fun Challenge 2: Escape Room Builder & Solver

## Concept

Build an app where users can design escape rooms with puzzles, locks, clues, objects, and dependencies. The system should validate whether the escape room is solvable.

## Target Users

- Escape room designer
- Playtester
- Event host
- Puzzle enthusiast

## Core Features

### 1. Escape Room Design

An escape room has:

- Name
- Theme
- Difficulty:
  - `EASY`
  - `MEDIUM`
  - `HARD`
  - `EXPERT`
- Description
- Time limit in minutes
- Status:
  - `DRAFT`
  - `READY_FOR_TEST`
  - `PUBLISHED`
  - `ARCHIVED`

Rules:

- A room cannot be published if it is not solvable.
- A room must have at least one start object.
- A room must have exactly one final exit object.

### 2. Objects

Objects can be:

- `CLUE`
- `ITEM`
- `LOCK`
- `PUZZLE`
- `DOOR`
- `CONTAINER`
- `EXIT`

Each object has:

- Name
- Type
- Description
- Initial state:
  - `VISIBLE`
  - `HIDDEN`
  - `LOCKED`
  - `SOLVED`
- Location
- Tags

Examples:

- A key.
- A locked drawer.
- A code written under a table.
- A puzzle box.
- A final door.

### 3. Dependencies

Designers define how objects interact.

Dependency fields:

- Source object
- Target object
- Dependency type:
  - `UNLOCKS`
  - `REVEALS`
  - `SOLVES`
  - `REQUIRES`
- Condition text

Examples:

- Key unlocks drawer.
- Solving puzzle reveals code.
- Code unlocks safe.
- Safe contains exit badge.
- Exit badge opens final door.

### 4. Solvability Checker

The app must determine whether the room can be solved from the initial state.

It should return:

- Solvable:
  - yes
  - no
- Ordered solving path.
- Unreachable objects.
- Circular dependencies.
- Missing starting clues.
- Final blocker, if unsolvable.

This should be rule-based. No LLM is required inside the product.

### 5. Hint System

Each puzzle or lock can have hints:

- Gentle hint.
- Strong hint.
- Almost-solution hint.

Rules:

- Hints are returned in order.
- The app tracks how many hints were requested.
- Hint usage can reduce final player score.

### 6. Playtest Run

A playtest run tracks:

- Room
- Team name
- Started at
- Finished at
- Hints used
- Solved:
  - yes
  - no
- Notes

The app should calculate:

- Completion time.
- Hint penalty.
- Final score.

## Required API Endpoints

```txt
POST   /rooms
GET    /rooms
GET    /rooms/{id}
PATCH  /rooms/{id}

POST   /rooms/{id}/objects
GET    /rooms/{id}/objects
PATCH  /objects/{id}

POST   /rooms/{id}/dependencies
GET    /rooms/{id}/dependencies

POST   /rooms/{id}/validate
GET    /rooms/{id}/solution-path
POST   /rooms/{id}/publish

POST   /objects/{id}/hints
GET    /objects/{id}/hints

POST   /rooms/{id}/playtests
PATCH  /playtests/{id}
GET    /playtests/{id}/score
```

## Required Tests

- Room cannot publish if unsolvable.
- Detects unreachable object.
- Detects circular dependency.
- Detects missing start object.
- Produces correct solving path.
- Hint penalty affects final score.

## Advanced Architecture Requirements

Separate:

- Room lifecycle
- Object model
- Dependency graph
- Validation engine
- Hint system
- Playtest scoring

The graph validation should be isolated from API and database code.

## Required Agent-Ready Deliverables

- `docs/domain-model.md`
- `docs/graph-model.md`
- `docs/validation-rules.md`
- `docs/playtest-scoring.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`

## Suggested GitHub Issues

1. Create room lifecycle model.
2. Add objects.
3. Add dependency graph.
4. Implement solvability checker.
5. Add hints.
6. Add playtest runs and scoring.
7. Add tests and CI.
8. Add agent-ready docs.

## Acceptance Criteria

A successful solution:

- Lets users model an escape room.
- Supports object dependencies.
- Validates if the room is solvable.
- Explains why invalid rooms are broken.
- Supports hints and playtest scoring.
- Has strong tests around graph logic.

## Stretch Goals

- Visual graph view.
- Import/export room as JSON.
- Difficulty score calculation.
- Player mode.
- Generate a printable room plan.

---

# Advanced Business Challenge 1: Intelligent Support Operations Hub

## Concept

Build a support operations platform that ingests customer tickets, classifies them, detects duplicates, suggests routing, and tracks SLA risk.

This challenge goes beyond a basic ticket board. It focuses on operational intelligence, automation, auditability, and rule-based decision support.

## Target Users

- Support agent
- Support manager
- Product owner
- Customer success manager

## Core Features

### 1. Ticket Ingestion

Tickets can be created manually or imported from JSON or CSV.

Ticket fields:

- External ID
- Customer
- Customer tier:
  - `FREE`
  - `STANDARD`
  - `PREMIUM`
  - `ENTERPRISE`
- Subject
- Description
- Product area
- Severity:
  - `LOW`
  - `MEDIUM`
  - `HIGH`
  - `CRITICAL`
- Status
- Created date
- Updated date
- Assigned team
- Assigned agent

### 2. Classification Engine

Implement a rule-based classification system.

The system should suggest:

- Product area
- Severity
- Assigned team
- SLA target

Example rules:

- Description contains `cannot login` → Product area `IDENTITY`
- Customer tier `ENTERPRISE` and severity `HIGH` → SLA 4 hours
- Subject contains `invoice` → Product area `BILLING`
- Description contains `data loss` → Severity `CRITICAL`

### 3. Duplicate Detection

Detect potential duplicate tickets.

Minimum approach:

- Normalize title and description.
- Compare keywords.
- Find tickets with shared important terms.
- Return duplicate score.

No machine learning is required. A deterministic similarity algorithm is enough.

### 4. SLA Risk Engine

The app should calculate:

- SLA due date.
- Time remaining.
- SLA status:
  - `SAFE`
  - `AT_RISK`
  - `BREACHED`
- Reason for risk.

### 5. Work Queue

Support managers can view queues:

- By team.
- By customer tier.
- By severity.
- By SLA status.
- By duplicate group.

### 6. Audit Trail

Every automated suggestion must be auditable.

Audit record:

- Ticket ID
- Action type
- Suggested value
- Reason
- Timestamp
- Accepted or rejected by human

## Required API Endpoints

```txt
POST   /tickets
POST   /tickets/import
GET    /tickets
GET    /tickets/{id}
PATCH  /tickets/{id}

POST   /tickets/{id}/classify
GET    /tickets/{id}/duplicates
GET    /tickets/{id}/sla

GET    /queues/team/{team}
GET    /queues/sla-risk
GET    /queues/duplicates

POST   /tickets/{id}/suggestions/{suggestionId}/accept
POST   /tickets/{id}/suggestions/{suggestionId}/reject

GET    /audit
GET    /reports/operations-summary
```

## Required Tests

- Classification rules.
- Duplicate scoring.
- SLA calculation.
- Audit trail creation.
- Accept or reject suggestion flow.
- Import validation.

## Advanced Architecture Requirements

Separate:

- Ingestion
- Classification
- Duplicate detection
- SLA engine
- Queue/read model
- Audit trail

## Required Agent-Ready Deliverables

- `docs/domain-model.md`
- `docs/classification-rules.md`
- `docs/sla-rules.md`
- `docs/architecture.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`
- GitHub Issues for each major feature.

## Suggested GitHub Issues

1. Create ticket ingestion model and API.
2. Add JSON/CSV import.
3. Implement classification engine.
4. Implement duplicate detection.
5. Implement SLA risk engine.
6. Add work queues.
7. Add audit trail.
8. Add reports and CI.

## Acceptance Criteria

A successful solution:

- Imports and stores tickets.
- Suggests classification with reasons.
- Detects possible duplicates.
- Calculates SLA risk.
- Provides work queues.
- Records audit trail for suggestions.
- Has test coverage around business rules.

## Stretch Goals

- Add human feedback loop to improve rules.
- Add dashboard UI.
- Add webhook simulation.
- Add LLM-based classification behind an interface.
- Add OpenAPI documentation.

---

# Advanced Business Challenge 2: Developer Self-Service Portal

## Concept

Build a developer platform portal where teams can request new repositories, environments, permissions, and CI/CD templates.

This challenge is especially relevant for GitHub Copilot, GitHub Enterprise, platform engineering, and developer productivity audiences.

## Target Users

- Developer
- Team lead
- Platform engineer
- Security reviewer

## Core Features

### 1. Request Catalog

Users can create platform requests.

Request types:

- New repository
- New team
- Access request
- Deployment environment
- CI/CD workflow template
- Secret or variable request
- Runner request

Each request has:

- Requester
- Team
- Request type
- Business justification
- Risk level:
  - `LOW`
  - `MEDIUM`
  - `HIGH`
- Status:
  - `DRAFT`
  - `SUBMITTED`
  - `NEEDS_INFO`
  - `APPROVED`
  - `REJECTED`
  - `PROVISIONED`
- Created date
- Updated date

### 2. Policy Validation

Implement rule-based validation.

Example policies:

- Repository names must follow naming convention.
- Production environment requests require team lead approval.
- Admin access requires security approval.
- Runner requests must specify OS and resource size.
- Secrets cannot be submitted as plain text.
- Public repositories are not allowed.

### 3. Approval Workflow

Each request type has required approvals.

| Request Type | Required Approvals |
|---|---|
| New repository | Platform |
| Access request | Team lead |
| Production environment | Team lead + Security |
| Runner request | Platform + Security |
| Secret request | Security |

Rules:

- Request cannot be provisioned before all approvals are complete.
- Rejected requests require a reason.
- Requests needing information can be resubmitted.

### 4. Provisioning Plan

After approval, the system generates a provisioning plan.

The plan should include:

- Actions to execute.
- Required GitHub settings.
- Recommended branch protection.
- Required workflows.
- Security notes.
- Manual follow-up steps.

No real GitHub API integration is required for the MVP. A generated plan is enough.

### 5. Audit Trail

Every state change must be recorded.

Audit fields:

- Request ID
- Actor
- Action
- Previous status
- New status
- Reason
- Timestamp

### 6. Template Library

The portal should include reusable templates:

- Java service repo
- Python service repo
- Static website
- Internal library
- GitHub Actions workflow template

Each template has:

- Name
- Description
- Recommended settings
- Required files
- Default branch protection
- Default CI workflow

## Required API Endpoints

```txt
POST   /requests
GET    /requests
GET    /requests/{id}
PATCH  /requests/{id}

POST   /requests/{id}/submit
POST   /requests/{id}/approve
POST   /requests/{id}/reject
POST   /requests/{id}/needs-info
POST   /requests/{id}/provision

POST   /requests/{id}/validate
GET    /requests/{id}/provisioning-plan
GET    /requests/{id}/audit

GET    /templates
GET    /templates/{id}
```

## Required Tests

- Repository naming policy.
- Public repository rejection.
- Production environment approval rules.
- Admin access security approval rule.
- Cannot provision before approvals.
- Audit trail records state changes.
- Provisioning plan generation.

## Advanced Architecture Requirements

Separate:

- Request lifecycle
- Policy engine
- Approval engine
- Provisioning plan generator
- Template catalog
- Audit trail

## Required Agent-Ready Deliverables

- `docs/domain-model.md`
- `docs/policies.md`
- `docs/approval-workflows.md`
- `docs/provisioning-plan-format.md`
- `docs/architecture.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`

## Suggested GitHub Issues

1. Create request catalog model and API.
2. Add policy validation engine.
3. Add approval workflow.
4. Add provisioning plan generator.
5. Add template library.
6. Add audit trail.
7. Add API tests and CI.
8. Add agent-ready repo documentation.

## Acceptance Criteria

A successful solution:

- Supports multiple request types.
- Validates requests against policies.
- Handles approval workflows.
- Generates provisioning plans.
- Tracks audit trail.
- Includes reusable templates.
- Is well documented for future Copilot or agent work.

## Stretch Goals

- Generate GitHub Issues from approved requests.
- Add GitHub Actions workflow scaffolding.
- Add repo settings as YAML.
- Add simulated GitHub API adapter.
- Add dashboard for platform team.

---

# Suggested Scoring Rubric

Use the same rubric for every challenge.

| Category | Points | What Good Looks Like |
|---|---:|---|
| Product completeness | 20 | Core features work and the demo flow is clear. |
| Business/domain logic | 20 | Rules are implemented cleanly and tested. |
| Agent readiness | 20 | Copilot instructions, `AGENTS.md`, docs, and issues are useful. |
| Code quality | 15 | Clear structure, good names, understandable architecture. |
| Tests and CI | 15 | Meaningful automated tests and GitHub Actions. |
| Copilot usage story | 10 | Team can explain how Copilot helped and where they had to steer it. |

Total: 100 points.

---

# Suggested Hackathon Flow

## Opening Briefing

Explain that teams should focus on more than just code generation. The goal is to build a repository that a future developer or coding agent can continue working on.

Suggested framing:

1. Pick a challenge.
2. Create a repository.
3. Break the work into issues.
4. Add Copilot and agent instructions early.
5. Build the core flow.
6. Add tests and CI.
7. Document what works and what does not.
8. Demo the result and explain how Copilot was used.

## Recommended Time Boxing

For a half-day format:

| Timebox | Activity |
|---|---|
| 20 minutes | Challenge selection and repo setup |
| 30 minutes | Domain model, issues, and architecture sketch |
| 90 minutes | First implementation block |
| 30 minutes | Test and CI focus |
| 45 minutes | Second implementation block |
| 30 minutes | Documentation and agent-readiness cleanup |
| 30 minutes | Demos and scoring |

For a full-day format:

| Timebox | Activity |
|---|---|
| 30 minutes | Challenge selection and repo setup |
| 45 minutes | Domain model, issues, architecture, and agent instructions |
| 2 hours | First implementation block |
| 45 minutes | Tests, CI, and refactoring |
| 2 hours | Second implementation block |
| 45 minutes | Documentation, demo prep, and cleanup |
| 60 minutes | Demos, scoring, and discussion |

---

# Recommended Minimum Done Definition

A team is considered done when:

- The app can be started locally.
- The main happy path works.
- At least 5 core business rules are implemented.
- Core logic has automated tests.
- CI runs successfully.
- The repository contains useful Copilot and agent instructions.
- The team can explain what Copilot did well and where human guidance was needed.

---

# Optional Facilitator Notes

## Things to Encourage

Encourage teams to:

- Ask Copilot to explain the domain before coding.
- Ask Copilot to generate edge cases.
- Ask Copilot to write tests before implementation.
- Use issues as the task boundary for agent mode.
- Review generated code critically.
- Keep business logic out of controllers.
- Keep documentation close to the code.
- Add clear naming and folder conventions.

## Things to Watch Out For

Common mistakes:

- Letting Copilot generate too much code without review.
- No tests.
- No clear domain model.
- Business rules hidden inside API controllers.
- README written at the very end and barely useful.
- Large generated code dumps that nobody understands.
- CI added too late.
- No acceptance criteria in issues.

## Suggested Demo Questions

Ask each team:

1. What did you build?
2. What is the most important business or domain rule?
3. How did you use Copilot?
4. What did Copilot get wrong?
5. What did you do to make the repository agent-ready?
6. How would a future coding agent continue the project?
7. What would you improve with more time?

---

# Recommended Default Pairings

If participants struggle to choose, recommend:

## Beginner

- Fun: Movie Night Decider
- Business: Support Ticket Triage Board

## Advanced

- Fun: Quiz Night Engine
- Business: Developer Self-Service Portal

These challenges provide a good balance of familiar domain logic, clear rules, meaningful tests, and realistic Copilot usage.
