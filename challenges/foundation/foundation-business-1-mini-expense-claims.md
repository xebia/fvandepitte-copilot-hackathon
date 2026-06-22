# Foundation Business Challenge 1: Mini Expense Claims

## Quick Pitch

It's the Monday after a sales kickoff in Lisbon, and seventeen people just got back with crumpled hotel receipts, taxi fares, and one suspiciously large dinner bill. Right now those expenses live in a spreadsheet that nobody trusts and an inbox that nobody reads. Your job is to give the team a small, dependable system where employees submit claims, managers approve or reject with a clear paper trail, and finance can pull a clean export without chasing anyone down the hallway.

## At a Glance

| | |
|---|---|
| Level | Foundation |
| Type | Business |
| Suggested team size | 2-3 |
| Time box | ~3-4 hours |
| Recommended scope | Claim lifecycle (submit → approve/reject → pay), validation rules, summary report, CSV export |

## Learning Goals

- Practice using Copilot to explore an unfamiliar business domain and turn fuzzy rules into explicit code.
- Drive development from GitHub issues, letting each issue map to a slice of the claim lifecycle.
- Use a test-first rhythm for the validation rules where the edge cases actually live.
- Model an explicit state machine instead of scattering boolean flags across the codebase.
- Tell a clear story about where Copilot helped and where you pushed back on its suggestions.

## Constraints

- Model claim status explicitly as a state machine; illegal transitions (e.g. editing an approved claim) must be rejected, not silently allowed.
- Validation rules live in the domain layer, not in controllers or UI code.
- Every state-changing action must be reachable through the API; no "fix it in the database" shortcuts.
- The summary report and CSV export must be derived from the same source of truth as the claims themselves.

## Non-Goals

- No authentication or real user accounts; pass the actor (employee, manager, finance) as input.
- No real payment integration; "paid" is a status, not a bank transfer.
- No production infrastructure, containers, or cloud deployment.
- No polished UI; a minimal page or API client is enough unless you reach the stretch goals.
- No receipt OCR or file storage beyond a URL or filename string.

## Domain Rules

### Claim Fields

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

### Submission Rules

- Amount must be greater than 0.
- Expenses over 250 require manager approval.
- Food expenses over 50 require a note.
- Claims cannot be submitted without a description.

### Manager Review Rules

- Rejected claims require a reason.
- Approved claims cannot be edited.
- Paid claims cannot be changed.

### Finance Overview

Finance can view:

- All approved claims.
- Total amount by department.
- Total amount by category.
- Claims waiting for payment.

## Required Endpoints or Flows

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

## Starter Data

Seed your system with these claims so every team demos against the same baseline.

| ID | Employee | Department | Category | Amount | Currency | Description | Status |
|---|---|---|---|---:|---|---|---|
| 1 | Aïsha Khan | Sales | HOTEL | 320.00 | EUR | 2 nights, Lisbon kickoff | SUBMITTED |
| 2 | Tom De Vries | Engineering | SUPPLIES | 45.00 | EUR | USB-C dock | APPROVED |
| 3 | Marie Lefevre | Sales | FOOD | 82.50 | EUR | Client dinner (note: team of 4) | SUBMITTED |
| 4 | Jonas Berg | Marketing | TRAVEL | 18.00 | EUR | Airport taxi | DRAFT |
| 5 | Priya Nair | Engineering | FOOD | 12.00 | EUR | Lunch | APPROVED |
| 6 | Carlos Mendez | Sales | OTHER | 260.00 | EUR | Conference pass | REJECTED |
| 7 | Lena Vogel | Finance | TRAVEL | 95.40 | EUR | Train, Brussels ↔ Paris | PAID |
| 8 | Sven Larsen | Marketing | FOOD | 60.00 | EUR | Working lunch (missing note) | DRAFT |

## Test Expectations

Your suite should prove the rules hold under pressure:

- A claim amount of zero or below is rejected.
- A food expense over 50 without a note cannot be submitted (record 8 should fail until a note is added).
- Rejecting a claim without a reason is rejected.
- An approved claim cannot be edited.
- The summary report calculates totals by department and by category correctly against the starter data.

## Curveball

At T+90 minutes, finance announces a policy change effective immediately: any claim over 250 now requires **two** approvals — the direct manager and a finance sign-off — before it can be marked paid. Existing single-approved high-value claims must drop back to a "needs finance approval" state rather than staying approved. Adapt your state machine and tests without breaking the lower-value flow.

## Scoring Rubric

| Category | Points | What we're looking for |
|---|---:|---|
| Domain correctness | 30 | All validation and lifecycle rules enforced, including the over-250 and food-over-50 cases. |
| Testing depth | 25 | Edge cases covered, not just happy paths; rejection and illegal-edit cases tested. |
| Architecture & clarity | 20 | Validation isolated in the domain layer; status modeled as an explicit state machine. |
| Demo quality | 15 | A claim walks end-to-end from submission to paid, with the summary and CSV shown live. |
| Copilot usage story | 10 | Clear account of where Copilot accelerated work and where you corrected it. |

## Demo Script

1. Submit claim #3 (the 82.50 food dinner) and show the note requirement being satisfied.
2. As a manager, reject claim #6 with a reason, then show that re-editing it is blocked.
3. Approve claim #1, mark it paid, and confirm a paid claim can no longer be changed.
4. Open the summary report and point out totals by department and category.
5. Download the approved-claims CSV and open it to prove the export matches the report.

## Stretch Ideas

- Add role-based access so only managers can approve and only finance can mark paid.
- Add a receipt upload mock.
- Add an audit trail recording who changed each claim and when.
- Add monthly budget warnings per department.
- Add a dashboard UI.
- Add multi-currency normalization so the summary report can total in a single base currency.
- Add a "resubmit" path that lets an employee fix and re-send a rejected claim.
