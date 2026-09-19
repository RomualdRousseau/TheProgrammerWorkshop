# Standard Tooling Templates

To maintain consistency across projects, use these templates for task management and automated quality control.

## 1. Justfile Template

Every module or sub-project should have its own `justfile`. Use this template as a starting point.

```just
# Set default recipe to list all commands
default: list

# List all available recipes
list:
    @just --list

# Run the application/simulation
run:
    uv run -m my_project run

# Run all quality checks
check:
    uvx prek run --all-files

# Run all tests
test:
    uv run --group dev python -m pytest tests/

# Format the source code
format:
    uv run --group dev ruff format .

# Check formatting without making changes
format-check:
    uv run --group dev ruff format . --check

# Lint the source code
lint:
    uv run --group dev ruff check .

# Auto-fix linting issues where possible
fix:
    uv run --group dev ruff check . --fix

# Type check the source code
typecheck:
    uv run --group dev ty check .

# Clean up caches
clean:
    uvx pyclean . -d all
```

## 2. Pre-commit Configuration

Use Astral's tools (`ruff` and `ty`) for fast and reliable pre-commit checks.

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=1000]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: ty-check
        name: ty-check
        entry: uv run --no-env-file ty check
        language: system
        types: [python]
        pass_filenames: false
        stages: [pre-commit]
```

## 3. Prek Integration

If using `prek` for managing hooks, ensure it runs standard linting and type checking on every commit.

```bash
# Install hooks
uv run --no-env-file prek install

# Run hooks manually
uv run --no-env-file prek run --all-files
```

## 4. Modern Git Tooling

Maintain high repository standards with structured commit messages and automated validation.

### Commit Messages

Use clear, concise messages focused on "why" rather than "what". Group related changes into single, logical commits.

- **Feature**: `feat: implement A*-based pathfinding for agents`
- **Fix**: `fix: resolve race condition in physics integration`
- **Refactor**: `refactor: move renderer logic to ui/renderer.py`

### Automated Quality Control

Integrate with GitHub Actions to validate every pull request and commit:

```yaml
# .github/workflows/ci.yml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run prek run --all-files
      - run: just test
```

### Git Hooks

Always use `pre-commit` or `prek` to ensure that no broken code (lint errors, type errors) is ever committed to the repository.
