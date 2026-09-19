# Product Owner Templates

## 📝 User Story Block Template

Use this template to create a new user story in `TODO.md`.

```markdown
- [ ] **Story: [Concise Title]**
  - **Goal:** As a [role], I want [action], so that [value].
  - **Acceptance Criteria:**
    - [ ] [Criterion 1]
    - [ ] [Criterion 2]
    - [ ] [Criterion 3]
  - **Labels:** `priority:medium`, `unrefined`
```

## 🏗️ Kanban Section Structure

Organize `TODO.md` with these headers:

```markdown
# [Project Name] Roadmap

## 🎯 Backlog
*Unrefined ideas or upcoming features.*

## 🏗️ Selected for Development
*Refined stories with clear acceptance criteria.*

## 🚧 In Progress
*Currently being implemented.*

## ✅ Done
*Completed work.*
```

## 🔄 Status Transitions

- **Backlog -> Selected**: Move the story and ensure it has at least 3 acceptance criteria.
- **Selected -> In Progress**: Move the story and change the checkbox to `[/]` to show it's active.
- **In Progress -> Done**: Move the story to the appropriate "Done" subsection and check the boxes `[x]`.
