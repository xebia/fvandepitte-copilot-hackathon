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
