---
name: backlog-todo
description: Manage project backlog, user stories, and tasks in Markdown format using TODO.md and Kanban state sections.
tags:
  - backlog
  - todo
  - markdown
  - kanban
  - tracking
depends_on:
  - product-owner
---

# Backlog Todo

This skill provides workflows for managing a project's agile backlog and user stories locally in Markdown format (typically `TODO.md`). Extending `product-owner`, it focuses on Kanban state transitions, Markdown formatting, and version-controlled backlog maintenance.

## 1. File Structure: The `TODO.md` File

All project stories and tasks are tracked in a root-level `TODO.md` organized into four Kanban status sections:

1. **`## 🎯 Backlog`**: Unrefined ideas or upcoming features waiting for refinement.
2. **`## 🏗️ Selected for Development`**: Refined stories with agreed acceptance criteria, in implementation order.
3. **`## 🚧 In Progress`**: Actively developed stories.
4. **`## ✅ Done`**: Completed stories where all acceptance criteria and tests pass; grouped under epic subsections.

Refer to [todo-template.md](references/todo-template.md) for the complete file layout.

## 2. Managing Stories in `TODO.md`

### Adding Stories
When a new story is drafted according to `product-owner` standards, append it to `## 🎯 Backlog`:

```markdown
- [ ] **Story: [Concise Title]**
  - **Goal:** As a [role], I want [action], so that [value].
  - **Acceptance Criteria:**
    - [ ] [Criterion 1]
    - [ ] [Criterion 2]
  - **Labels:** `priority:medium`, `unrefined`
```

### Advancing State
- Move the story block between headers as work progresses.
- Check off individual criteria checkboxes (`- [x]`) as they are completed and verified by tests.
- When all criteria are checked and code is committed, move the story block to `## ✅ Done`, under the correct epic subsection.

### Formatting
- Always separate story blocks with exactly one blank line (see [todo-template.md](references/todo-template.md) → Formatting Rules).

## Project Interaction

- **Trigger**: "Initialize the TODO.md backlog for this project"
- **Trigger**: "Move [story] from Backlog to Selected for Development in TODO.md"
- **Trigger**: "Mark [story] as In Progress in TODO.md"
- **Trigger**: "Check off acceptance criteria for [story] in TODO.md"
- **Trigger**: "Archive completed tasks in TODO.md"
