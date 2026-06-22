# Advanced Fun Challenge 2: Escape Room Builder & Solver

## Quick Pitch

A designer has spent three weekends building "The Lighthouse Keeper's Vault" — a gorgeous room full of hidden keys, coded drawers, and a final door that only opens with a badge from a safe. Then the first paying team gets stuck at minute four because the clue that reveals the safe code is locked behind a puzzle they can never reach. Build the tool that catches that dead end *before* a real team is trapped: model the room as a graph, then prove whether it's actually solvable.

## At a Glance

| | |
|---|---|
| Level | Advanced |
| Type | Fun |
| Suggested team size | 3-4 |
| Time box | Full day, or an ambitious half-day |
| Recommended scope | Room + object + dependency model, a validation engine, and tests on graph logic |

## Learning Goals

- Use Copilot agent mode to build and reason about a dependency graph and traversal logic.
- Keep a validation engine pure and let Copilot generate adversarial graph test cases.
- Coordinate multi-file edits across model, graph, and API layers.
- Document the graph model and validation rules so the agent can extend them safely.
- Practice explaining *why* something fails, not just whether it passes — surfacing unreachable nodes and cycles.

## Constraints

- The graph validation engine must be isolated from API and database code and testable on its own.
- Validation must be fully rule-based; no LLM may be required inside the running product.
- A room cannot be published unless the engine proves it is solvable.
- Unsolvable rooms must return a concrete reason (unreachable object, cycle, missing start, or final blocker), not a bare "no".
- Hint ordering and playtest scoring rules live in their own modules, separate from the graph.

## Non-Goals

- No real-time multiplayer play session is required.
- No authentication or user accounts.
- No visual drag-and-drop editor (that's a stretch goal).
- No 3D or rich media; objects are described in text and tags.

## Domain Rules

### Escape Room Design

An escape room has:

- Name
- Theme
- Difficulty: `EASY`, `MEDIUM`, `HARD`, `EXPERT`
- Description
- Time limit in minutes
- Status: `DRAFT`, `READY_FOR_TEST`, `PUBLISHED`, `ARCHIVED`

Rules:

- A room cannot be published if it is not solvable.
- A room must have at least one start object.
- A room must have exactly one final exit object.

### Objects

Objects can be: `CLUE`, `ITEM`, `LOCK`, `PUZZLE`, `DOOR`, `CONTAINER`, `EXIT`.

Each object has:

- Name
- Type
- Description
- Initial state: `VISIBLE`, `HIDDEN`, `LOCKED`, `SOLVED`
- Location
- Tags

Examples: a key, a locked drawer, a code written under a table, a puzzle box, a final door.

### Dependencies

Designers define how objects interact.

Dependency fields:

- Source object
- Target object
- Dependency type: `UNLOCKS`, `REVEALS`, `SOLVES`, `REQUIRES`
- Condition text

Examples:

- Key unlocks drawer.
- Solving puzzle reveals code.
- Code unlocks safe.
- Safe contains exit badge.
- Exit badge opens final door.

### Solvability Checker

The engine determines whether the room can be solved from its initial state and returns:

- Solvable: yes / no
- Ordered solving path.
- Unreachable objects.
- Circular dependencies.
- Missing starting clues.
- Final blocker, if unsolvable.

### Hint System

Each puzzle or lock can have hints:

- Gentle hint.
- Strong hint.
- Almost-solution hint.

Rules:

- Hints are returned in order.
- The app tracks how many hints were requested.
- Hint usage can reduce final player score.

### Playtest Run

A playtest run tracks:

- Room
- Team name
- Started at
- Finished at
- Hints used
- Solved: yes / no
- Notes

The app calculates:

- Completion time.
- Hint penalty.
- Final score.

## Required Endpoints or Flows

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

## Architecture Expectations

Keep these concerns separated so they can evolve and be tested independently:

- Room lifecycle
- Object model
- Dependency graph
- Validation engine
- Hint system
- Playtest scoring

The graph validation must be isolated from API and database code.

## Agent-Ready Deliverables

The repository should contain:

- `docs/domain-model.md`
- `docs/graph-model.md`
- `docs/validation-rules.md`
- `docs/playtest-scoring.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`

Suggested GitHub issues to seed the board:

1. Create room lifecycle model.
2. Add objects.
3. Add dependency graph.
4. Implement solvability checker.
5. Add hints.
6. Add playtest runs and scoring.
7. Add tests and CI.
8. Add agent-ready docs.

## Starter Data

Seed "The Lighthouse Keeper's Vault" — theme nautical, difficulty `HARD`, 60-minute limit, status `DRAFT` — so every team validates the same room.

Objects:

| Name | Type | Initial state | Location |
|---|---|---|---|
| Brass Key | `ITEM` | `VISIBLE` | On the desk |
| Locked Drawer | `CONTAINER` | `LOCKED` | Under the desk |
| Tide Puzzle | `PUZZLE` | `VISIBLE` | Wall panel |
| Hidden Code | `CLUE` | `HIDDEN` | Behind the panel |
| Wall Safe | `CONTAINER` | `LOCKED` | Behind the painting |
| Exit Badge | `ITEM` | `LOCKED` | Inside the safe |
| Lighthouse Door | `EXIT` | `LOCKED` | North wall |

Dependencies:

| Source | Type | Target | Condition |
|---|---|---|---|
| Brass Key | `UNLOCKS` | Locked Drawer | Insert and turn the key |
| Tide Puzzle | `REVEALS` | Hidden Code | Arrange tides high to low |
| Hidden Code | `UNLOCKS` | Wall Safe | Enter 4-digit code |
| Wall Safe | `REQUIRES` | Exit Badge | Safe contains the badge |
| Exit Badge | `UNLOCKS` | Lighthouse Door | Tap badge on the reader |

This baseline is solvable. The curveball below makes it interesting.

## Test Expectations

The suite should prove, at minimum:

- A room cannot be published if it is unsolvable.
- The engine detects an unreachable object.
- The engine detects a circular dependency.
- The engine detects a missing start object.
- The engine produces the correct ordered solving path for a valid room.
- The hint penalty affects the final playtest score.

Aim for the validation engine to have the deepest coverage, including cycles, orphaned nodes, and the "everything but the last door" near-miss.

## Curveball

Halfway through, the facilitator hands teams a "designer change request": remove the **Brass Key → Locked Drawer** dependency and instead make the **Hidden Code** live *inside* the Locked Drawer. Now the only path to the safe runs through a drawer that nothing unlocks — the room is quietly unsolvable. Teams must catch it with `validate`, report the exact final blocker, and refuse to publish, all without hand-editing the test fixtures to make it pass.

## Scoring Rubric

| Criteria | Points | Note |
|---|---|---|
| Domain correctness | 25 | Publish guard, start/exit rules, and dependency semantics behave as specified. |
| Testing depth | 20 | Graph engine covers cycles, unreachable nodes, missing start, and valid paths. |
| Architecture & clarity | 25 | Validation engine is isolated from API/DB; modules are cleanly separated. |
| Demo quality | 15 | A valid room validates and an unsolvable one explains exactly why. |
| Copilot/agent usage story | 15 | Team can show how agent mode and the docs drove graph and test work. |

## Demo Script

1. **0:00–1:00** — Open "The Lighthouse Keeper's Vault", show its seven objects and five dependencies, then run `validate` to prove it's solvable and print the ordered solution path.
2. **1:00–2:15** — Apply the curveball change live (move the code into the unlocked drawer), re-run `validate`, and show the engine reporting the unreachable object and final blocker.
3. **2:15–3:00** — Attempt to publish and show it rejected, then run a playtest with two hints used and show the hint penalty applied to the final score. Close with how Copilot generated the adversarial graph tests.

## Stretch Ideas

- Visual graph view.
- Import/export room as JSON.
- Difficulty score calculation.
- Player mode.
- Generate a printable room plan.
- Suggest the minimum dependency to add that would make an unsolvable room solvable.
- Estimate expected solve time from path length and difficulty.
