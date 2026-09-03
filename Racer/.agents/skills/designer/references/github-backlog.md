# GitHub Backlog Workflow

The backlog for **Racer** is managed exclusively through the GitHub project **Racer** and the `gh` CLI. `TODO.md` files are no longer used.

## Project

- **Project**: `Racer` (project #2, owner `@me`)
- **Repository**: `RomualdRousseau/TheProgrammerWorkshop`

## Scope Labels

Every backlog item must have exactly one scope label:

| Label | Use for |
|---|---|
| `racer-all` | Monorepo-level or cross-cutting stories |
| `racer-env` | `racer-env` package stories and features |
| `racer-agents` | `racer-agents` package stories and features |

## Creating a New Backlog Item

Create a repo issue, apply the correct label, and add it to the **Racer** project in one command:

```bash
gh issue create \
  --repo RomualdRousseau/TheProgrammerWorkshop \
  --title "[racer-env] Story: Implement turbo boost" \
  --body "## Acceptance Criteria\n- [ ] ...\n- [ ] ..." \
  --label "racer-env" \
  --project "Racer"
```

If the item is already completed, close it immediately:

```bash
gh issue close <issue-url> --repo RomualdRousseau/TheProgrammerWorkshop
```

## Updating Status

Move items through the board using the GitHub UI or CLI. Do not maintain a local `TODO.md` file.

## Closing Items

When a story is fully implemented and verified:

1. Close the issue with `gh issue close`.
2. Ensure acceptance criteria in the issue body are checked.
3. Update the README or zensical documentation if the change affects user-facing behavior.
