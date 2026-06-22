# Foundation Business Challenge 1: Mini Expense Claims

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
