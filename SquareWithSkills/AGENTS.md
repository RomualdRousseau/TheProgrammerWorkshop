# Python Game — Agent Guide

This document helps any coding assistant understand the project, its conventions, and how to work with it.

## Project Overview

GreenSquare is a 2D Python game built with Raylib (`pyray`). A 32x32 green square moves within a 512x512 bounded window via arrow keys, featuring smooth physics movement, drop shadow, and motion trails.

## Tech Stack

- **Language**: Python 3.12+
- **Renderer**: [raylib](https://www.raylib.com/) (imported as `pyray`)
- **Package Manager**: [uv](https://docs.astral.sh/uv/)
- **Task Runner**: [just](https://just.systems/)
- **Testing**: [pytest](https://docs.pytest.org/)

## Common Commands

```bash
just play   # Run the game
just test   # Run the test suite
just sync   # Install dependencies
just clean  # Remove __pycache__ and .pytest_cache
just        # List all recipes
```

Direct `uv` equivalents are also available:

```bash
uv run greensquare-play
uv run pytest
uv sync --extra dev
```

## Architecture

The project follows a strict three-layer architecture:

```text
src/greensquare/
├── core/      # Data, physics, math, input protocol — no rendering
├── game/      # Gameplay logic — imports only core
├── engine/    # Raylib adapter — implements core abstractions
└── main.py    # Wires engine into game and runs the loop
```

### Layer Rules

1. **`core/`** contains the "Laws of the World": constants, state dataclasses, pure physics functions, and the `InputEngine` protocol.
   - Must never import from `engine/` or `pyray`.
   - Must be 100% testable without a window.

2. **`game/`** contains gameplay logic as module-level functions.
   - Imports only from `core/`.
   - Receives the engine object as an argument (`game.update(engine, player, dt)`, `game.draw(engine, player)`).

3. **`engine/`** contains the Raylib-backed implementation.
   - Implements the `InputEngine` protocol from `core/`.
   - Handles window creation, input polling, and drawing primitives.

4. **`main.py`** is the composition root.
   - Creates the engine.
   - Passes it into the game layer.
   - Runs the frame loop.

### When to Introduce Classes

Start with module-level functions. Only introduce classes (e.g., Scene objects) when the game genuinely complexifies — multiple screens, modes, or complex state machines.

## Coding Conventions

- **Absolute imports only** (`from greensquare.core.state import PlayerState`).
- **No wildcard imports**.
- Import `pyray` as `pr`.
- Use `dataclass(slots=True, frozen=True)` for state containers.
- Keep physics and state-transition functions pure.
- Inject dependencies; never instantiate Raylib or hardware collaborators inside `core/` or `game/`.

## Testing

All physics and gameplay logic must be testable headlessly.

- Tests live in `tests/`.
- Use mocks or simple objects that satisfy the `InputEngine` protocol.
- Never open a Raylib window in a test.

```bash
just test
```

## Backlog & Documentation

- Project stories and tasks are tracked in `TODO.md`.
- Use the python-game-designer todo template for new stories.
- Keep `README.md` up to date with usage instructions.
- Keep `AGENTS.md` up to date when workflows, structure, or conventions change.

## Adding a New Feature

1. Check `TODO.md` for existing stories.
2. If none exists, draft a user story with clear acceptance criteria.
3. Implement the smallest change that satisfies the story.
4. Add or update tests in `tests/`.
5. Run `just test` to verify.
6. Update `README.md` and `AGENTS.md` if the change affects usage or conventions.

## Development Process

Before writing any code:

1. Create the project documentation.
2. Create the initial backlog.
3. Break the work into small user stories with clear acceptance criteria.
4. Present the implementation plan for approval.

After the plan is approved, implement **one user story at a time**.

After each story:

- Explain what was implemented.
- Run any appropriate verification.
- Stop and wait for confirmation before continuing to the next story.

Never implement multiple stories in a single step unless explicitly requested.

## Key Decisions

- **Module-level functions for game and engine**: Classes are reserved for future complexity.
- **Engine injection**: The engine is passed as an object/module into the game layer so tests can swap it for a mock.
