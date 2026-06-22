# Foundation Business Challenge 2: Support Ticket Triage Board

## Quick Pitch

It's 9:02 on a Tuesday and the support queue already has a customer who can't log in, someone furious about a double charge, and a polite feature request that's been ignored for a week. Without triage, the loudest email wins and the urgent login outage quietly breaches its SLA. Build the board that brings order to the chaos: customers raise tickets, agents categorize and assign them, and everyone can see at a glance what's on fire and what's about to be.

## At a Glance

| | |
|---|---|
| Level | Foundation |
| Type | Business |
| Suggested team size | 2-3 |
| Time box | ~3-4 hours |
| Recommended scope | Ticket lifecycle, assignment, SLA calculation, comment history, SLA report |

## Learning Goals

- Use Copilot to translate a support domain into clean models and explicit status transitions.
- Slice the work into GitHub issues that each deliver a usable piece of the board.
- Practice test-first development on the SLA math, where off-by-one and timezone bugs hide.
- Model ticket status and assignment rules as first-class domain logic rather than UI conditions.
- Capture a short, honest story of how Copilot shaped your SLA and validation code.

## Constraints

- Model ticket status explicitly; transitions like editing a closed ticket must be rejected in the domain layer.
- SLA calculation lives in one well-tested place, not duplicated across endpoints.
- Assignment rules (single active assignee, no reassigning closed tickets) are enforced in code, not assumed.
- Comments are append-only; existing comments cannot be edited or deleted through the API.

## Non-Goals

- No authentication; pass the acting agent or customer as input.
- No real email sending or inbound email parsing.
- No production infrastructure or cloud deployment.
- No polished UI; an API or minimal board view is enough unless you reach the stretch goals.
- No full business-calendar engine with public holidays unless you choose it as a stretch.

## Domain Rules

### Ticket Fields

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

### Ticket Rules

- Subject and description are required.
- Urgent tickets must have an assigned agent.
- Closed tickets cannot be edited.

### Assignment Rules

- A ticket can only have one active assignee.
- Resolved tickets can still be reassigned.
- Closed tickets cannot be reassigned.

### SLA Targets

| Priority | SLA |
|---|---:|
| `LOW` | 5 business days |
| `MEDIUM` | 3 business days |
| `HIGH` | 1 business day |
| `URGENT` | 4 hours |

For each ticket the app should show:

- SLA due date.
- Whether the ticket is overdue.
- Time remaining.

### Comment Rules

Comment fields:

- Ticket ID
- Author
- Message
- Created date
- Internal or external flag

## Required Endpoints or Flows

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

## Starter Data

Seed the board with these tickets so every team's SLA report and overdue detection can be compared directly. Assume "now" is the time you run your demo.

| ID | Customer | Subject | Category | Priority | Status | Assigned Agent | Created |
|---|---|---|---|---|---|---|---|
| 1 | Aïsha Khan | Cannot log in to portal | ACCOUNT | URGENT | IN_PROGRESS | Nora | 2 hours ago |
| 2 | Tom De Vries | Charged twice this month | BILLING | HIGH | OPEN | — | yesterday |
| 3 | Marie Lefevre | Export button does nothing | TECHNICAL | MEDIUM | OPEN | Sam | 4 days ago |
| 4 | Jonas Berg | Add dark mode please | FEATURE_REQUEST | LOW | WAITING_FOR_CUSTOMER | Sam | 6 days ago |
| 5 | Priya Nair | Invoice PDF is blank | BILLING | MEDIUM | IN_PROGRESS | Nora | 1 day ago |
| 6 | Carlos Mendez | API returns 500 on upload | TECHNICAL | HIGH | OPEN | — | 30 hours ago |
| 7 | Lena Vogel | Change account email | ACCOUNT | LOW | RESOLVED | Sam | 3 days ago |
| 8 | Sven Larsen | App crashes on startup | TECHNICAL | URGENT | OPEN | — | 10 minutes ago |

## Test Expectations

Your suite should prove the board behaves under the awkward cases:

- A ticket without a subject or description is rejected.
- A closed ticket cannot be edited.
- An urgent ticket cannot be saved without an assignee (ticket 8 should fail until assigned).
- The SLA due date is calculated correctly per priority against the starter data.
- Overdue tickets are detected (tickets 2 and 6 should surface as breaching or close to it).

## Curveball

At T+90 minutes, the support manager introduces a "VIP" flag: any ticket from a customer on the VIP list is automatically promoted one priority level (LOW→MEDIUM, MEDIUM→HIGH, HIGH→URGENT) and its SLA recalculated accordingly. URGENT VIP tickets must additionally appear at the top of the SLA report regardless of due date. Fold this into your SLA logic and tests without breaking existing priorities.

## Scoring Rubric

| Category | Points | What we're looking for |
|---|---:|---|
| Domain correctness | 30 | Validation, assignment, and SLA rules all enforced, including urgent-needs-assignee. |
| Testing depth | 25 | SLA math and overdue detection tested across priorities, not just one happy case. |
| Architecture & clarity | 20 | SLA logic centralized; status and assignment modeled as explicit domain rules. |
| Demo quality | 15 | A ticket moves through assignment, comments, and the SLA report live. |
| Copilot usage story | 10 | Clear account of where Copilot helped with SLA/validation and where you corrected it. |

## Demo Script

1. Create ticket #8 (urgent crash) and show it can't be saved until an agent is assigned.
2. Assign it to Nora, then add an internal comment and an external comment.
3. Open the SLA report and point out the overdue billing ticket (#2) and the urgent items at the top.
4. Resolve ticket #7 and show it can still be reassigned, then close it and show reassignment is now blocked.
5. Attempt to edit the closed ticket and show the domain layer rejecting it.

## Stretch Ideas

- Add a simple UI board grouped by status.
- Add search by customer email.
- Add canned responses for common categories.
- Add ticket tags.
- Add rule-based category suggestion from the subject and description.
- Add a real business-calendar SLA that skips weekends and configurable holidays.
- Add an SLA breach alert feed that lists tickets crossing their due date in the next hour.
