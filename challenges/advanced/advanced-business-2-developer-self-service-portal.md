# Advanced Business Challenge 2: Developer Self-Service Portal

## Quick Pitch

A new team just spun up and they need a repo, a staging environment, two CI workflows, and admin access — and right now that means a Slack thread, three approvals nobody can find, and a platform engineer copy-pasting branch protection rules from memory at 6pm. Build the self-service portal that turns that mess into a real workflow: developers file structured requests, policies catch the dangerous ones, the right people approve, and the system hands back a concrete provisioning plan instead of a shrug. It's platform engineering as a product.

## At a Glance

| | |
|---|---|
| **Level** | Advanced |
| **Type** | Business |
| **Suggested team size** | 3-4 |
| **Time box** | Full day (ambitious half-day) |
| **Recommended scope** | Request lifecycle + policy engine + approval workflow + provisioning plan + audit trail, with a template library |

## Learning Goals

- Use Copilot agent mode to model an explicit state machine and keep transitions consistent across many files.
- Encode platform governance as a rules engine driven from a written policy doc that Copilot can read.
- Separate the policy engine, approval engine, and provisioning-plan generator so each is independently testable.
- Use Copilot to scaffold reusable templates and the docs that make the repo agent-ready for future work.
- Build a test strategy that locks down approval gates and policy rejections before any UI exists.

## Constraints

- Request status transitions must be **explicit and validated** — no jumping from `DRAFT` to `PROVISIONED`.
- The policy engine must be deterministic and return a structured pass/fail with reasons, not a boolean.
- A request cannot be provisioned until **all** required approvals for its type are complete.
- Every state change is recorded in the audit trail with actor, previous status, and new status.
- Secrets are never stored or echoed in plain text, including in the audit trail and provisioning plan.

## Non-Goals

- No real GitHub API calls — a generated provisioning plan is the deliverable, not real repos.
- No real identity provider or SSO; assume requester and approver identities are passed in.
- No billing, quota, or cost enforcement.
- No live infrastructure provisioning, Terraform runs, or cloud credentials.

## Domain Rules

### Request Catalog

Users create platform requests. Request types:

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
- Risk level: `LOW`, `MEDIUM`, `HIGH`
- Status: `DRAFT`, `SUBMITTED`, `NEEDS_INFO`, `APPROVED`, `REJECTED`, `PROVISIONED`
- Created date
- Updated date

### Policy Validation

Rule-based validation. Example policies:

- Repository names must follow naming convention.
- Production environment requests require team lead approval.
- Admin access requires security approval.
- Runner requests must specify OS and resource size.
- Secrets cannot be submitted as plain text.
- Public repositories are not allowed.

### Approval Workflow

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

### Provisioning Plan

After approval, the system generates a provisioning plan (no real GitHub integration required for the MVP). The plan includes:

- Actions to execute.
- Required GitHub settings.
- Recommended branch protection.
- Required workflows.
- Security notes.
- Manual follow-up steps.

### Audit Trail

Every state change is recorded. Audit fields:

- Request ID
- Actor
- Action
- Previous status
- New status
- Reason
- Timestamp

### Template Library

Reusable templates the portal ships with:

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

## Required Endpoints or Flows

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

## Architecture Expectations

Keep these concerns in separate, independently testable modules:

- Request lifecycle
- Policy engine
- Approval engine
- Provisioning plan generator
- Template catalog
- Audit trail

The request lifecycle should be an explicit state machine: each transition is a named operation that validates the current status, applies policy/approval checks, and emits an audit record.

## Agent-Ready Deliverables

The repo should contain:

- `docs/domain-model.md`
- `docs/policies.md`
- `docs/approval-workflows.md`
- `docs/provisioning-plan-format.md`
- `docs/architecture.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`

Suggested issues:

1. Create request catalog model and API.
2. Add policy validation engine.
3. Add approval workflow.
4. Add provisioning plan generator.
5. Add template library.
6. Add audit trail.
7. Add API tests and CI.
8. Add agent-ready repo documentation.

## Starter Data

Seed every team from the same request set so policy and approval behaviour is comparable.

| ID | Requester | Team | Type | Justification (excerpt) | Risk | Status |
|---|---|---|---|---|---|---|
| REQ-2001 | a.dubois | payments | New repository | `payments-core` service repo | LOW | SUBMITTED |
| REQ-2002 | a.dubois | payments | Deployment environment | production env for payments-core | HIGH | SUBMITTED |
| REQ-2003 | m.peeters | data | Access request | admin access to data-lake | HIGH | SUBMITTED |
| REQ-2004 | s.khan | web | New repository | `Public_Website` marketing site | MEDIUM | DRAFT |
| REQ-2005 | s.khan | web | Runner request | self-hosted runner, no OS specified | MEDIUM | DRAFT |
| REQ-2006 | l.rossi | platform | Secret request | `DB_PASSWORD=hunter2` for staging | HIGH | SUBMITTED |
| REQ-2007 | j.novak | mobile | CI/CD workflow template | reuse Java service workflow | LOW | APPROVED |
| REQ-2008 | t.garcia | data | New team | create `data-governance` team | LOW | NEEDS_INFO |

This set deliberately includes a naming-convention violation (REQ-2004 `Public_Website` is non-conforming and public), a runner request missing its OS/size (REQ-2005), a plain-text secret that must be rejected (REQ-2006), and an admin access request that needs security approval (REQ-2003).

## Test Expectations

The suite should prove the governance rules hold:

- Repository naming policy rejects non-conforming names.
- Public repository requests are rejected.
- Production environment requests require team lead approval before they can proceed.
- Admin access requests require security approval.
- A request cannot be provisioned before all required approvals are complete.
- The audit trail records every state change with previous and new status.
- Provisioning plan generation produces the documented sections for an approved request.

## Curveball

Mid-afternoon, security drops a new mandate: **every `HIGH` risk request now also requires a second, independent security reviewer, and any request older than 24 hours in `NEEDS_INFO` must auto-expire to `REJECTED` with a system-generated reason.** Teams whose approval engine is data-driven (a table of required approvals) absorb this in minutes; teams who wrote `if requestType == ...` branches throughout the API will be hunting for every gate.

## Scoring Rubric

| Category | Points | What we're looking for |
|---|---|---|
| Domain correctness | 25 | Policies, approvals, and state transitions behave correctly on the starter requests. |
| Testing depth | 20 | Naming, public-repo, approval-gate, and cannot-provision-early cases are all tested. |
| Architecture & clarity | 25 | Explicit state machine; policy, approval, and plan generators are cleanly separated. |
| Demo quality | 15 | A clear walkthrough of one request from submit to provisioning plan. |
| Copilot / agent usage story | 15 | Evidence that `docs/policies.md` and friends drove agent-mode generation. |

## Demo Script

1. **(0:00)** Submit REQ-2004 and show the naming + public-repo policy rejecting it with reasons.
2. **(0:30)** Fix and resubmit a valid repo request; show it move to `SUBMITTED`.
3. **(1:00)** Try to provision REQ-2002 early and show the approval gate blocking it.
4. **(1:30)** Add the required Team lead + Security approvals, then provision it.
5. **(2:00)** Open the generated provisioning plan and highlight branch protection + security notes.
6. **(2:40)** Show `/requests/{id}/audit` with the full state history, then name the `docs/` file Copilot used.

## Stretch Ideas

- Generate GitHub Issues from approved requests.
- Add GitHub Actions workflow scaffolding.
- Add repo settings as YAML.
- Add a simulated GitHub API adapter.
- Add a dashboard for the platform team.
- Implement the curveball's auto-expiry sweep as a scheduled job with its own audit action.
- Add a policy-as-code format so new policies can be added without touching the engine.
