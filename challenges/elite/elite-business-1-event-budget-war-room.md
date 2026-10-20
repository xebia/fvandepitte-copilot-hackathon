# Elite Business Challenge 1: Event Budget War Room

## Quick Pitch

The events team runs a dozen conferences, meetups, and launches a year, all drawing from the same shared budget pots. Today the planning meeting looks like this: three spreadsheets open side by side, someone shouting "catering for the summit just went over", and nobody able to say what cutting the marketing pot by ten percent would actually do. Build the war room: one screen where money visibly flows from pots to events to categories, where rebalancing is a drag instead of a formula, and where a what-if scenario can be forked, compared, and promoted without touching the live plan until it is ready.

## At a Glance

| | |
|---|---|
| Level | Elite |
| Type | Business |
| Suggested team size | 3-4 |
| Time box | Full day minimum |
| Recommended scope | Allocation engine + event lifecycle + interactive visual war room + scenario what-if mode, with deep tests on the engine |

## Learning Goals

- Drive Copilot agent mode across both a strict backend engine and a demanding interactive frontend.
- Isolate a pure allocation and validation engine and let Copilot generate thorough tests against it.
- Use Copilot to build non-trivial visualizations (flow diagrams, burn charts) and review the generated code critically.
- Model scenario forking and comparison, a genuinely hard read-model problem.
- Capture money-handling rules in `docs/` and `.github/copilot-instructions.md` so agents never improvise with rounding or floors.

## Constraints

- The allocation and validation engine must be a pure, separately testable module with no HTTP, UI, or database dependencies.
- The graphical war room is core scope, not a stretch goal; a forms-and-tables UI does not satisfy this challenge.
- All money is stored and computed in integer cents; rounding happens once, at defined boundaries, using banker's rounding.
- Pots can never go negative, in the live plan or in any scenario.
- Every pot has a contingency floor percentage; allocations that would breach the floor are rejected with the exact amount available.
- Reallocations above an approval threshold require an explicit approval step before they take effect.
- Event lifecycle must be explicit and enforced (`PLANNING` → `APPROVED` → `EXECUTION` → `CLOSED`), with per-state write rules.
- Scenarios never mutate the live plan; promotion is the only path from scenario to live, and it must re-validate everything against the current live state.

## Non-Goals

- No authentication or user roles; a simple "acting as" selector is enough for the approval flow.
- No real accounting integration, invoicing, or payment processing; actuals are entered manually or seeded.
- No multi-currency conversion; a single currency with correct cent handling is the challenge.
- No real-time collaboration; last-write-wins with the scenario conflict check is sufficient.
- No historical fiscal-year reporting; the war room shows the current planning cycle.

## Domain Rules

### Budget Pots

A pot has:

- Name
- Total budget in cents
- Contingency floor percentage
- Allocations to events

Rules:

- Sum of a pot's allocations can never exceed its total budget.
- The unallocated remainder of a pot can never drop below its contingency floor (floor percentage × total budget).
- Validation errors must state the pot, the rule, and the maximum amount still allocatable.

### Events

An event has:

- Name
- Date
- Status: `PLANNING`, `APPROVED`, `EXECUTION`, `CLOSED`
- Allocations per category
- Commitments and actuals per category

Category set: `VENUE`, `CATERING`, `MARKETING`, `SPEAKERS`, `CONTINGENCY`.

Lifecycle rules:

- `PLANNING`: allocations fully editable.
- `APPROVED`: allocations editable only through the approval flow.
- `EXECUTION`: allocations locked; only commitments and actuals may be recorded.
- `CLOSED`: fully immutable; unspent allocation returns to its source pot on close.
- Status can only move forward, one step at a time.

### Allocations, Commitments, Actuals

- An allocation reserves money from one pot to one event category.
- A commitment records a contractual obligation against an allocation (a signed venue contract, for example).
- An actual records money actually spent.
- Commitments and actuals can never exceed the category allocation; the engine rejects the write and reports the available headroom.
- Burn rate per category = actuals / allocation; health per category: `OK` (< 80%), `WARNING` (80-100%), `OVER` would be rejected, so it can never appear in live data, only in scenario previews.

### Reallocation and Approval

- Moving money between categories within one event, or between events within one pot, is a reallocation.
- A reallocation at or above the approval threshold (configurable, seeded at 5 000.00, i.e. 500 000 cents) enters `PENDING_APPROVAL` and has no effect until approved.
- Approving applies the move atomically with full re-validation; rejecting discards it.
- Reallocations out of a category are capped by that category's uncommitted remainder.

### Scenarios

- A scenario is a fork of the complete live plan at a point in time.
- Scenario edits follow all engine rules except approval thresholds (scenarios are sandboxes).
- A scenario comparison shows, per pot, event, and category: live value, scenario value, and delta.
- Promoting a scenario re-validates every change against the current live plan; if live has changed incompatibly since the fork, promotion fails with a conflict report listing each conflicting item.
- Promotion applies all changes atomically or not at all.

### The War Room (Graphical Requirements)

The UI must include, as core scope:

1. **Flow view**: a sankey or equivalent flow diagram showing money from pots to events to categories, with widths proportional to amounts, updating live after every change.
2. **Interactive rebalancing**: dragging a flow or using +/- controls on it adjusts an allocation, with invalid moves (floor breach, locked event, headroom) visibly rejected and explained inline.
3. **Burn view**: per event, burn-up or burn-down per category showing allocation, commitments, and actuals, with `OK`/`WARNING` health coloring.
4. **Scenario mode**: a visible toggle between live and scenario, a side-by-side or overlay diff of the flow view, and a promote button that surfaces the conflict report on failure.

Server-rendered SVG, a charting library, or hand-rolled canvas are all acceptable; the bar is interactivity and correctness, not visual polish.

## Required Endpoints or Flows

```txt
GET    /pots
POST   /pots
GET    /pots/{id}

GET    /events
POST   /events
GET    /events/{id}
POST   /events/{id}/advance-status

POST   /events/{id}/allocations
POST   /events/{id}/commitments
POST   /events/{id}/actuals

POST   /reallocations
GET    /reallocations?status=PENDING_APPROVAL
POST   /reallocations/{id}/approve
POST   /reallocations/{id}/reject

POST   /scenarios
GET    /scenarios/{id}
POST   /scenarios/{id}/allocations
GET    /scenarios/{id}/diff
POST   /scenarios/{id}/promote

GET    /warroom/flow
GET    /warroom/burn
```

## Architecture Expectations

Keep these concerns separated so they can evolve and be tested independently:

- Allocation and validation engine (pure, money math lives only here)
- Event lifecycle
- Approval workflow
- Scenario store, diff, and promotion
- War room read models (flow and burn projections)
- UI shell

The engine must be reachable in tests without the API, database, or UI. The flow and burn views must consume read-model endpoints, never recompute money math in the frontend.

## Agent-Ready Deliverables

The repository should contain:

- `docs/domain-model.md`
- `docs/money-rules.md` (cents, rounding, floors, thresholds)
- `docs/state-transitions.md`
- `docs/scenario-semantics.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`

Suggested GitHub issues to seed the board:

1. Create pots, events, and the allocation engine.
2. Enforce contingency floors and integer-cent money rules.
3. Implement the event lifecycle with per-state write rules.
4. Add commitments, actuals, and burn health.
5. Add the reallocation approval workflow.
6. Add scenarios: fork, diff, promote with conflict check.
7. Build the flow view with interactive rebalancing.
8. Build the burn view and scenario diff overlay.
9. Add tests and CI.
10. Add agent-ready documentation.

## Starter Data

Seed one planning cycle so every team demos against the same baseline.

Pots:

| Pot | Budget | Contingency floor |
|---|---|---|
| Flagship Events | 250 000.00 | 10% |
| Community | 60 000.00 | 15% |
| Launches | 120 000.00 | 10% |

Events:

| Event | Pot | Status | Date |
|---|---|---|---|
| DevSummit 2026 | Flagship Events | `EXECUTION` | 2026-03-12 |
| Spring Meetup Series | Community | `APPROVED` | 2026-04-20 |
| Product X Launch | Launches | `PLANNING` | 2026-05-08 |

Seed DevSummit with allocations across all five categories, commitments on `VENUE` and `SPEAKERS`, and actuals putting `CATERING` at 85% burn (`WARNING`). Seed Spring Meetup with allocations only, and Product X Launch with a partial draft, leaving each pot with visible unallocated headroom above its floor.

## Test Expectations

The suite should prove, at minimum:

- A pot never goes negative and allocations stop exactly at the contingency floor, with the available amount reported.
- All money math is integer cents; a dedicated test locks in the rounding behavior.
- Per-state write rules: allocation edits rejected in `EXECUTION`, everything rejected in `CLOSED`, status only moves forward.
- Closing an event returns unspent allocation to the source pot.
- Commitments and actuals cannot exceed their category allocation.
- A reallocation at the threshold requires approval and has no effect until approved.
- Scenario promotion applies atomically, and promotion after a conflicting live change fails with a conflict report naming the item.
- Flow read model: amounts in the projection sum consistently at every level (pots = events = categories).

Aim for the allocation engine and scenario promotion to have the deepest coverage, including floor-boundary and rounding edge cases.

## Curveball

Two hours in, the facilitator announces that finance has imposed a 15% across-the-board budget cut on every pot, effective immediately. Teams must implement an auto-rebalance that proportionally shrinks allocations to fit the new pot totals while respecting two hard limits: contingency floors still hold, and locked allocations (events in `EXECUTION`) cannot be touched, so their share of the cut falls on the remaining events. Where the cut cannot be fully absorbed, the operation must produce an exceptions report instead of silently going negative. The result should arrive as a scenario, visible in the diff overlay, ready for review before promotion.

## Scoring Rubric

| Criteria | Points | Note |
|---|---|---|
| Domain correctness | 25 | Floors, cents, lifecycle locks, approvals, and scenario semantics behave exactly as specified. |
| Testing depth | 20 | Engine and promotion are covered, including floor-boundary, rounding, and conflict cases. |
| Architecture & clarity | 20 | Money math lives only in the pure engine; read models feed the UI; concerns are separated. |
| Demo quality & visuals | 20 | The war room tells the money story at a glance and rebalancing feels direct and safe. |
| Copilot/agent usage story | 15 | Team can show how docs and agent mode drove both engine and visualization work. |

## Demo Script

1. **0:00-0:45**: Open the flow view, walk the money from the three pots through the events to categories, and point out the `CATERING` warning on DevSummit in the burn view.
2. **0:45-2:00**: Drag a rebalance on Product X Launch, then attempt two illegal moves: breaching the Community pot floor and editing a locked DevSummit allocation, showing both rejected inline with reasons. Trigger a reallocation above the threshold and approve it.
3. **2:00-3:00**: Fork a scenario, make two changes, show the diff overlay, promote it, and show one promotion failing with a conflict report. Close with how Copilot built the flow diagram and what had to be corrected.

## Stretch Ideas

- Add an undo/redo timeline for the live plan.
- Add CSV import for actuals.
- Add a per-pot forecast line projecting burn to event date.
- Add keyboard-driven rebalancing for accessibility.
- Add a presenter mode that animates the money flow for stakeholder meetings.
- Add soft multi-user support: show a banner when the live plan changed under an open scenario.
