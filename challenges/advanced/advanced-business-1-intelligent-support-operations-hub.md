# Advanced Business Challenge 1: Intelligent Support Operations Hub

## Quick Pitch

It's Monday at 9:03 and the support inbox already has 140 unread tickets. Three of them are the same enterprise customer screaming about the same outage, two are quietly ticking toward an SLA breach nobody noticed, and one junior agent is about to route a `data loss` report to the billing team. Your job is to build the operations brain that sees all of this at once: it ingests the flood, classifies it, spots the duplicates, and flags the tickets about to go critical — while keeping a paper trail for every automated decision it makes.

## At a Glance

| | |
|---|---|
| **Level** | Advanced |
| **Type** | Business |
| **Suggested team size** | 3-4 |
| **Time box** | Full day (ambitious half-day) |
| **Recommended scope** | Ingestion + classification + duplicate detection + SLA engine + audit trail, with queues on top |

## Learning Goals

- Use Copilot agent mode to scaffold and wire together six separate engines (ingestion, classification, duplicates, SLA, queues, audit) across many files in one coordinated effort.
- Drive a rules-based decision system from a written spec, keeping the rules in `docs/` so Copilot can read them and stay consistent.
- Design a read model (work queues) that is deliberately separate from the write model (tickets and suggestions).
- Build an audit-first mindset where every automated suggestion is explainable and reversible.
- Use Copilot to generate a layered test suite that pins down business rules before the UI exists.

## Constraints

- Every automated suggestion must carry a human-readable **reason** — no silent decisions.
- The classification, duplicate, and SLA engines must be deterministic and unit-testable; no ML or external model calls in the core.
- Work queues are a **read model** derived from tickets; they must not be the source of truth.
- State changes and suggestions must be recorded in the audit trail before they are treated as final.
- Suggestions are advisory: a human accept/reject step gates anything that mutates a ticket.

## Non-Goals

- No real email/CSV provider integration — importing from a pasted JSON/CSV blob is enough.
- No machine learning, embeddings, or LLM dependency in the MVP scoring path.
- No real-time websocket dashboard — polling or a refresh button is fine.
- No multi-tenant auth or user management; assume a trusted internal operator.

## Domain Rules

### Ticket

Tickets can be created manually or imported from JSON or CSV. Fields:

- External ID
- Customer
- Customer tier: `FREE`, `STANDARD`, `PREMIUM`, `ENTERPRISE`
- Subject
- Description
- Product area
- Severity: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- Status
- Created date
- Updated date
- Assigned team
- Assigned agent

### Classification Engine

A rule-based system that suggests product area, severity, assigned team, and SLA target. Example rules:

- Description contains `cannot login` → Product area `IDENTITY`
- Customer tier `ENTERPRISE` and severity `HIGH` → SLA 4 hours
- Subject contains `invoice` → Product area `BILLING`
- Description contains `data loss` → Severity `CRITICAL`

### Duplicate Detection

Detect potential duplicate tickets with a deterministic similarity algorithm (no ML required):

- Normalize title and description.
- Compare keywords.
- Find tickets with shared important terms.
- Return a duplicate score.

### SLA Risk Engine

The app calculates:

- SLA due date.
- Time remaining.
- SLA status: `SAFE`, `AT_RISK`, `BREACHED`.
- Reason for risk.

### Work Queue

Support managers can view queues by team, by customer tier, by severity, by SLA status, and by duplicate group.

### Audit Trail

Every automated suggestion must be auditable. Audit record:

- Ticket ID
- Action type
- Suggested value
- Reason
- Timestamp
- Accepted or rejected by human

## Required Endpoints or Flows

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

## Architecture Expectations

Keep these concerns in separate, independently testable modules:

- Ingestion
- Classification
- Duplicate detection
- SLA engine
- Queue / read model
- Audit trail

The queue read model should be projected from the ticket store rather than mutated directly, and the three decision engines should be callable in isolation so tests can exercise them without the API layer.

## Agent-Ready Deliverables

The repo should contain:

- `docs/domain-model.md`
- `docs/classification-rules.md`
- `docs/sla-rules.md`
- `docs/architecture.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`
- GitHub Issues for each major feature.

Suggested issues:

1. Create ticket ingestion model and API.
2. Add JSON/CSV import.
3. Implement classification engine.
4. Implement duplicate detection.
5. Implement SLA risk engine.
6. Add work queues.
7. Add audit trail.
8. Add reports and CI.

## Starter Data

Seed everyone from the same baseline. Times are illustrative; assume "now" is `2026-06-22T09:00Z`.

| External ID | Customer | Tier | Subject | Description (excerpt) | Severity | Status | Team |
|---|---|---|---|---|---|---|---|
| TCK-1001 | Northwind Logistics | ENTERPRISE | Cannot login after password reset | users `cannot login`, SSO loop | HIGH | OPEN | — |
| TCK-1002 | Northwind Logistics | ENTERPRISE | Login broken for whole team | nobody can sign in, SSO loop | HIGH | OPEN | — |
| TCK-1003 | Acme Retail | STANDARD | Invoice shows wrong VAT | `invoice` total incorrect | MEDIUM | OPEN | — |
| TCK-1004 | Globex | PREMIUM | Nightly export deleted records | possible `data loss` after sync | HIGH | OPEN | — |
| TCK-1005 | Initech | FREE | How do I export to CSV? | feature question | LOW | OPEN | — |
| TCK-1006 | Umbrella Health | ENTERPRISE | Dashboard slow at peak | latency over 8s | MEDIUM | IN_PROGRESS | PLATFORM |
| TCK-1007 | Acme Retail | STANDARD | Duplicate invoice emails | `invoice` sent twice | LOW | OPEN | — |
| TCK-1008 | Globex | PREMIUM | Billing portal 500 error | `invoice` page crashes | HIGH | OPEN | — |

This set deliberately includes a near-duplicate pair (TCK-1001 / TCK-1002), a `data loss` ticket that should escalate to `CRITICAL`, and several `invoice` tickets that should classify into `BILLING`.

## Test Expectations

The suite should prove the business rules hold:

- Classification rules produce the expected product area, severity, team, and SLA — with the matching reason.
- Duplicate scoring ranks the near-duplicate pair above unrelated tickets.
- SLA calculation returns the correct due date and `SAFE` / `AT_RISK` / `BREACHED` status.
- Audit records are created for every suggestion.
- The accept / reject suggestion flow mutates the ticket only on accept.
- Import validation rejects malformed records without partially importing.

## Curveball

Two hours in, the facilitator announces a new business rule from "the VP of Support": **any `ENTERPRISE` ticket left unassigned for more than 30 minutes must auto-escalate one severity level and re-enter the SLA engine** — and the audit trail has to show that the escalation was system-triggered, not human. Teams that kept their engines separate and audit-first will slot this in cleanly; teams that hardcoded classification into the API will feel it.

## Scoring Rubric

| Category | Points | What we're looking for |
|---|---|---|
| Domain correctness | 25 | Classification, duplicate scoring, and SLA status match the documented rules on the starter data. |
| Testing depth | 20 | Each engine has isolated tests plus an accept/reject and import-validation test. |
| Architecture & clarity | 25 | Clean separation of the six concerns; queues are a read model, not the source of truth. |
| Demo quality | 15 | A coherent walkthrough showing a ticket go from ingestion to audited suggestion. |
| Copilot / agent usage story | 15 | Evidence that `docs/` rules drove agent-mode generation and multi-file edits. |

## Demo Script

1. **(0:00)** Import the starter JSON; show the 8 tickets land in the queue.
2. **(0:30)** Classify TCK-1004 and point out it jumps to `CRITICAL` with the `data loss` reason.
3. **(1:00)** Open TCK-1002's duplicates and show TCK-1001 surfacing with a high score.
4. **(1:30)** Show the SLA queue flagging the enterprise tickets as `AT_RISK`, with the reason.
5. **(2:00)** Accept one suggestion, reject another, then open `/audit` to show both recorded with who/what/why.
6. **(2:40)** Close on `/reports/operations-summary` and call out which `docs/` file Copilot read to build it.

## Stretch Ideas

- Add a human feedback loop that promotes accepted suggestions into refined rules.
- Add a dashboard UI over the queues.
- Add webhook simulation for inbound ticket events.
- Add LLM-based classification behind the existing interface (without replacing the deterministic core).
- Add OpenAPI documentation generated from the endpoints.
- Add the auto-escalation curveball as a scheduled background sweep with its own audit action type.
