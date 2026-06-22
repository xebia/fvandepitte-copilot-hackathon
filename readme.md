# GitHub Copilot Hackathon Challenge Pack

![Repository QR Code](repo-qr-code.png)

## Purpose

This hackathon is designed for participants who already had hands-on sessions with GitHub Copilot and are ready for a more open-ended challenge.

The format is intentionally simple:

> Here is the challenge. Build it. Make it runnable. Make it testable. Make the repository agent-ready.

The goal is not only to build a working application, but also to learn how to use GitHub Copilot in a more advanced and realistic development workflow:

- Exploring an unknown problem domain.
- Creating a project structure from scratch.
- Writing useful issues and acceptance criteria.
- Generating and improving tests.
- Creating documentation that helps both humans and AI coding agents.
- Using Copilot Chat, Copilot Edits, agent mode, custom instructions, and issue-driven development.

The challenges are divided into foundation and advanced levels, with both fun and business-oriented topics.

As an alternative to greenfield projects, participants can also choose a legacy/refactoring track using the Gilded Rose Refactoring Kata.

---

## Common Requirements for Every Challenge

Each team should deliver a GitHub repository that contains a working application and enough supporting material to make the project understandable and maintainable.

Teams can use any programming language, framework, and application style.

### Lightweight Repository Deliverables (3-4 Hour Format)

Every repository should include:

- `README.md` with quick start and assumptions.
- A working core flow for the selected challenge.
- At least 2-3 key GitHub Issues (or a small TODO backlog in `README.md`).
- Basic tests for the most important business logic (a few focused tests are enough).
- Optional but recommended: `.github/copilot-instructions.md` and `AGENTS.md`.
- Optional but recommended: CI workflow.

### Agent-Ready Repository Expectations

The repository should be easy for both humans and AI coding agents to understand.

A good solution should document:

- How to run the application.
- How to run the tests.
- The domain model.
- Important business rules.
- Architectural decisions.
- Known limitations.
- Suggested future improvements.
- What Copilot should and should not do when editing the codebase.

### Copilot Usage Expectations

Teams should be able to explain how they used Copilot during the challenge.

Examples:

- Using Copilot Chat to explore the domain.
- Asking Copilot to propose a project structure.
- Generating a first version of tests.
- Asking Copilot to explain unfamiliar code.
- Using Copilot Edits to apply changes across multiple files.
- Using agent mode to implement a GitHub Issue.
- Creating custom instructions for the repository.
- Reviewing and correcting Copilot-generated code.

---

# Challenge Menu

## Foundation Challenges

| Type | Challenge |
|---|---|
| Fun | [Movie Night Decider](challenges/foundation/foundation-fun-1-movie-night-decider.md) |
| Fun | [Weekend Activity Planner](challenges/foundation/foundation-fun-2-weekend-activity-planner.md) |
| Business | [Mini Expense Claims](challenges/foundation/foundation-business-1-mini-expense-claims.md) |
| Business | [Support Ticket Triage Board](challenges/foundation/foundation-business-2-support-ticket-triage-board.md) |

## Advanced Challenges

| Type | Challenge |
|---|---|
| Fun | [Quiz Night Engine](challenges/advanced/advanced-fun-1-quiz-night-engine.md) |
| Fun | [Escape Room Builder & Solver](challenges/advanced/advanced-fun-2-escape-room-builder-and-solver.md) |
| Business | [Intelligent Support Operations Hub](challenges/advanced/advanced-business-1-intelligent-support-operations-hub.md) |
| Business | [Developer Self-Service Portal](challenges/advanced/advanced-business-2-developer-self-service-portal.md) |

## Alternative Refactoring Track

- [Gilded Rose Refactoring Kata](https://github.com/emilybache/GildedRose-Refactoring-Kata) (alternative to greenfield projects)


---

# Suggested Hackathon Flow

## Opening Briefing

Explain that teams should focus on more than just code generation. The goal is to build a repository that a future developer or coding agent can continue working on.

### Preferred Way of Working

1. Create new folder.
2. Copy the challenge they want to do to that folder.
3. Get started.

### Preferred Way of Working (Gilded Rose Alternative)

1. Create a new folder for your team work.
2. Clone [emilybache/GildedRose-Refactoring-Kata](https://github.com/emilybache/GildedRose-Refactoring-Kata) into that folder.
3. Pick one language folder (for example: `python`, `TypeScript`, `csharp.xUnit`, `Java`).
4. Read the requirements first: [GildedRoseRequirements.md](https://github.com/emilybache/GildedRose-Refactoring-Kata/blob/main/GildedRoseRequirements.md).
5. Run the existing tests and confirm the baseline before changing code.
6. Implement support for `Conjured` items and improve code quality through small, safe refactoring steps.
7. Keep constraints from the kata: do not alter the `Item` class or `Items` property.
8. Work in your own repository/fork and do not submit your solution as a PR to the upstream kata repository.

Suggested framing:

1. Pick a challenge track (greenfield challenge or Gilded Rose kata).
2. Create a repository.
3. Break the work into issues.
4. Add Copilot and agent instructions early.
5. Build the core flow.
6. Add tests and CI.
7. Document what works and what does not.
8. Demo the result and explain how Copilot was used.

## Recommended Time Boxing

For a half-day format:

| Timebox | Activity |
|---|---|
| 20 minutes | Challenge selection and repo setup |
| 30 minutes | Domain model, issues, and architecture sketch |
| 90 minutes | First implementation block |
| 30 minutes | Test and CI focus |
| 45 minutes | Second implementation block |
| 30 minutes | Documentation and agent-readiness cleanup |
| 30 minutes | Demos and wrap-up |

For a full-day format:

| Timebox | Activity |
|---|---|
| 30 minutes | Challenge selection and repo setup |
| 45 minutes | Domain model, issues, architecture, and agent instructions |
| 2 hours | First implementation block |
| 45 minutes | Tests, CI, and refactoring |
| 2 hours | Second implementation block |
| 45 minutes | Documentation, demo prep, and cleanup |
| 60 minutes | Demos and discussion |

---

# Recommended Minimum Done Definition

A team is considered done when:

- The app can be started locally.
- The main happy path works.
- At least 2-3 core business rules are implemented.
- Core logic has at least a small set of automated tests.
- The repository has enough notes so someone else can continue.
- The team can explain what Copilot did well and where human guidance was needed.

---

# Optional Facilitator Notes

## Things to Encourage

Encourage teams to:

- Ask Copilot to explain the domain before coding.
- Ask Copilot to generate edge cases.
- Ask Copilot to write tests before implementation.
- Use issues as the task boundary for agent mode.
- Review generated code critically.
- Keep business logic out of controllers.
- Keep documentation close to the code.
- Add clear naming and folder conventions.

## Things to Watch Out For

Common mistakes:

- Letting Copilot generate too much code without review.
- No tests.
- No clear domain model.
- Business rules hidden inside API controllers.
- README written at the very end and barely useful.
- Large generated code dumps that nobody understands.
- CI added too late.
- No acceptance criteria in issues.

## Suggested Demo Questions

Ask each team:

1. What did you build?
2. What is the most important business or domain rule?
3. How did you use Copilot?
4. What did Copilot get wrong?
5. What did you do to make the repository agent-ready?
6. How would a future coding agent continue the project?
7. What would you improve with more time?

---

# Recommended Default Pairings

If participants struggle to choose, recommend:

## Foundation

- Fun: Movie Night Decider
- Business: Support Ticket Triage Board

## Advanced

- Fun: Quiz Night Engine
- Business: Developer Self-Service Portal

These challenges provide a good balance of familiar domain logic, clear rules, meaningful tests, and realistic Copilot usage.
