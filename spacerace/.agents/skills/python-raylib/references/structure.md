# Single-Package Game Structure

This structure supports building modular Raylib games that stay simple and testable.

## Root Level

```text
/
├── pyproject.toml       # Project config, dependencies, entry points
├── justfile             # Common commands (play, test, sync)
├── README.md            # Project overview and usage
├── TODO.md              # Project backlog
├── src/
│   └── spacerace/
│       ├── __init__.py
│       ├── main.py      # Entry point: wires engine into game
│       ├── core/        # Data, physics, input abstractions
│       ├── game/        # Gameplay logic (imports only core)
│       └── engine/      # Raylib adapter (implements core abstractions)
└── tests/
    └── test_*.py
```

## Package Internal Structure

```text
spacerace/
├── __init__.py
├── main.py              # Wires engine → game, runs the loop
├── core/
│   ├── __init__.py
│   ├── constant.py      # World constants (immutable laws)
│   ├── math.py          # Vector, wrap, and helper math
│   ├── physics.py       # Pure state transition functions
│   ├── input.py         # InputEngine protocol
│   └── state.py         # Dataclasses (__slots__ mandatory)
├── game/
│   └── __init__.py      # Module-level gameplay functions
│                        # (init, update, draw)
└── engine/
    └── raylib_engine.py # Module-level Raylib implementation
```

## Modular Design Guidelines

1.  **Start with Functions**: Keep `game` and `engine` as modules with top-level functions. Only introduce classes when the game genuinely complexifies.
2.  **Engine as Service (Injection)**:
    - The `engine/` package is a hardware adapter (Raylib).
    - `game/` receives the engine as an object/module argument (e.g., `game.update(engine, state, dt)`).
    - This allows swapping the real `raylib_engine` with a `MockEngine` for testing.
3.  **Headless-Ready (Strict)**:
    - Logic in `core/` and `game/` **must never** import from `engine/` or `pyray`.
    - Simulation must be 100% functional and testable without a graphics context.
    - All hardware calls (drawing, audio, input) are abstracted through the injected engine.
4.  **Absolute Imports**: Maintain absolute paths within the package's `src/` directory for tool compatibility (`uv`, `ruff`, `pytest`).

## When to Add Classes

If a game grows beyond a single screen and needs distinct modes (menu, playing, paused, game over), consider the **Scene Pattern** described in [patterns.md](patterns.md). Until then, module-level functions are enough.
