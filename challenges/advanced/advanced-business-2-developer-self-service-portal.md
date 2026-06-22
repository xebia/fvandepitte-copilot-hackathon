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
