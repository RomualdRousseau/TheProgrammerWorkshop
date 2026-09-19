---
name: product-owner
description: Manage project requirements, user story crafting (INVEST), acceptance criteria, and agile backlog prioritization.
tags:
  - agile
  - product-management
  - user-stories
  - backlog
  - requirements
depends_on: []
---

# Product Owner

This skill equips the agent to act as a **Product Owner**, bridging the gap between high-level user requirements and actionable engineering tasks. It focuses on the "What" and "Why", defining clear scopes, user-centric outcomes, and testable acceptance criteria.

## Core Responsibilities

1. **Backlog Ownership**: Maintain the project's priorities, roadmaps, and functional scope.
2. **User Story Drafting**: Transform ambiguous ideas, feature requests, and functional specifications into structured user stories following the INVEST guidelines.
3. **Acceptance Criteria**: Formulate precise, verifiable, binary acceptance criteria for every story.
4. **Definition of Done (DoD)**: Ensure work meets quality, testability, and documentation standards before being marked as done.
5. **Separation of Concerns**: Focus strictly on requirements, user value, and verification. Leave implementation details to the developers.

## The INVEST Principle

Every user story must satisfy the **INVEST** criteria:

- **I - Independent**: Stories should be self-contained and deliverable in any sequence when possible.
- **N - Negotiable**: Stories capture intent and leave room for technical design discussion.
- **V - Valuable**: Delivers demonstrable value to the user or system stakeholder.
- **E - Estimable**: Scoped clearly enough that complexity and effort can be evaluated.
- **S - Small**: Completable within a short iteration (typically 1-3 tasks).
- **T - Testable**: Contains clear binary criteria that can be confirmed by automated or manual tests.

## User Story Standard Format

Every story must follow the canonical template:

```markdown
### Story: [Concise Title]

**As a** [user persona or system role],
**I want** [capability or action],
**So that** [value or outcome].

### Acceptance Criteria
- [ ] [Binary criterion 1]
- [ ] [Binary criterion 2]
- [ ] [Binary criterion 3]
```

See [story-template.md](references/story-template.md) for full template variations and examples.

## Hybrid Kanban Lifecycle

Track story states across a clean 4-stage lifecycle:

1. **Backlog**: Identified ideas, features, or technical debt waiting for prioritization.
2. **Selected for Development**: Refined stories with full INVEST criteria and signed-off acceptance criteria.
3. **In Progress**: Stories currently being implemented by developers.
4. **Done**: Verification passes all acceptance criteria, tests succeed, and documentation is updated.

## Storage Complements

This skill defines the requirements and user story standards. To persist and track stories in specific tooling, combine this skill with:
- **`backlog-todo`**: Local Markdown tracking in `TODO.md`.
- **`backlog-github`**: GitHub Issues and Projects via `gh` CLI.
- **`backlog-gitlab`**: GitLab Issues via `glab` CLI.

## Project Interaction

- **Trigger**: "Draft a user story for [feature]"
- **Trigger**: "Refine acceptance criteria for [requirement]"
- **Trigger**: "Break down [epic/feature] into smaller user stories"
- **Trigger**: "Prioritize the project backlog based on [criteria]"
- **Trigger**: "Verify whether [implemented work] meets the Definition of Done"
