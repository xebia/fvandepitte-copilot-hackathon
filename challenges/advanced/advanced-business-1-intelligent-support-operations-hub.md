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
