# Foundation Business Challenge 2: Support Ticket Triage Board

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
