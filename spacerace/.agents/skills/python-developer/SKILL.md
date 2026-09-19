---
name: python-developer
description: Foundational standards for high-integrity Python development, enforcing safety rules (Power of 10), TDD, BDD, property testing, and clean code principles.
tags:
  - python
  - development
  - tdd
  - power-of-10
  - clean-code
depends_on: []
---

# Python Developer

This skill serves as the foundational source of truth for high-integrity Python development across all domains. It enforces strict safety rules, deterministic coding standards, test-driven development, and rigorous testing practices.

## 1. Control & Safety (The Power of 10)

All Python code must strictly follow the Power of 10 safety rules to ensure reliability, predictability, and memory safety:

1. **No Recursion:** All tree or graph traversals must use iterative stacks.
2. **Hard Loop Bounds:** Every `while` loop must be guarded by `MAX_ITERATIONS` or `TIMEOUT_SECONDS`.
3. **Memory Discipline:** Use `__slots__` for high-throughput classes to ensure deterministic memory usage.
4. **Validation at Boundary:** Use `TypeGuard` at presentation/entry boundaries. Internal layers assume validated data.
5. **Pure Functions:** Business logic must be I/O-free and deterministic. Push side effects to infrastructure edges.
6. **Dependency Injection:** Collaborators and external clients must be passed in via constructors, never instantiated internally.
7. **No Magic:** Forbidden: `eval()`, `exec()`, `getattr()` for sensitive logic, and dynamic runtime imports.
8. **Immutable Invariants:** State transitions must be provably immutable against malformed input.
9. **Fail-Closed:** Logic must default to "Access Denied" or "Operation Aborted" upon any ambiguity or exception.
10. **Protocol Interfaces:** Decouple components using `typing.Protocol` rather than tight inheritance.

For detailed rules and code examples, consult [code-rules.md](references/code-rules.md).

## 2. Testing & Verification

### Behavioral TDD

All business logic must be developed using a **Test-First** approach:

1. **Red:** Write a failing test that defines the expected behavior.
2. **Green:** Implement the minimum code to pass the test.
3. **Refactor:** Clean up the code while ensuring tests stay green.

### Vanilla BDD with Pytest

Use standard `pytest` functions structured by behavior. Every test scenario must follow the **Given / When / Then** pattern:

- **Given:** The initial context, state, or mock setup.
- **When:** The specific action or event being tested.
- **Then:** The expected outcome, side effect, or invariant check.

### Systematic Bug Reproduction

If a bug is reported, a fix is incomplete without an automated reproduction test:

1. Create a test case that reproduces the reported bug (it must fail in the current state).
2. Implement the fix.
3. Verify the test now passes. The test remains in the suite as a permanent regression safeguard.

### Technical Testing Standards

- **Property-Based Testing:** Use `Hypothesis` to test invariants across randomized inputs.
- **Strict Mocking:** All mocks must use `spec=True` to guarantee adherence to the real interface.
- **Exhaustive Unit Coverage:** Pure functions must have exhaustive unit test coverage via TDD.

Consult [tooling.md](references/tooling.md) for environment configuration and testing patterns.

## 3. Configuration vs. Constants

### Constants
Constants are **Immutable Truths** that are globally valid across all layers.
- **Import Policy:** Can be imported by any layer or module.
- **Examples:** `TAX_RATE`, `MAX_ITERATIONS`, `SUPPORTED_FORMATS`.

### Configuration
Configuration represents **Environmental Variables** that change based on the deployment context (Dev / Staging / Prod).
- **Import Policy:** Never import raw environment configurations into pure domain or business logic.
- **Injection Pattern:** Values must be injected into services or components via constructors at the application entry point or composition root.
- **Examples:** `DATABASE_URL`, `API_KEY`, `LOG_LEVEL`.

## 4. Operational Workflow & Git Discipline

### Conventional Commits

Format: `<type>(<scope>): <subject>`

- `feat`: New functionality or user-facing feature.
- `fix`: Bug fix.
- `refactor`: Structural change without logic change.
- `test`: Adding or updating tests.
- `docs`: Documentation updates.
- `chore`: Tooling, dependency, or configuration changes.

Commit early and atomically as soon as tests pass for a logical unit of work.

## 5. Tooling

- Package & Dependency Management: Use `uv` (`uv add`, `uv run`).
- Code Formatting & Linting: Use `ruff` (`ruff check`, `ruff format`).
- Testing: Use `pytest` with `hypothesis`.

## Project Interaction

- **Trigger**: "Enforce the Power of 10 rules for [module]"
- **Trigger**: "Write a TDD test suite for [feature]"
- **Trigger**: "Reproduce bug [description] with a failing test"
- **Trigger**: "Add property-based tests using Hypothesis for [function]"
- **Trigger**: "Audit code safety and typing in [file]"
