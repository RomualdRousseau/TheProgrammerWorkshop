---
name: python-game-developer
description: Raylib game development using Python. Use when building minimal, modular, visually-debuggable games with a strict separation between simulation logic and rendering.
---

# Raylib Game Development

This skill provides a foundation for building games using Python and `raylib` for simulation and visualization.

## Core Philosophy

1.  **Module-Based First**: Start with module-level functions and minimal state. Only introduce classes when the game genuinely complexifies.
2.  **Layered Architecture**: Split the project into three layers:
    -   `core/` — data, physics, input, and graphics abstractions (no rendering code)
    -   `game/` — gameplay logic; imports only from `core`
    -   `engine/` — Raylib adapters implementing the `core` protocols
3.  **Engine Injection**: `main.py` wires the system, injecting the concrete implementations into the game layer. This lets tests swap the real adapters for mocks.
4.  **Simulation/Visualization Split**: Keep physics and state updates separate from Raylib drawing. The simulation must be testable without a graphics context.
5.  **Headless-Ready (Strict)**: Logic in `core/` and `game/` must never import from `engine/` or `pyray`.
6.  **Simple Before Object-Oriented**: Prefer plain functions and dataclasses. The Scene pattern is valid for complex state machines, but start with module-level functions and refactor only when needed.
7.  **Decouple Input and Graphics**: Always decouple the input implementation and the graphical implementation instead of creating a monolithic "engine". Keeping them separate allows independent mocking/testing and simplifies implementation swapping.
8.  **High-Level Representation Rendering**: Rendering protocols must define high-level, semantic representation draws (e.g., `render_game(state)`) rather than exposing low-level primitives (like line/rectangle draws) to the game logic. This gives any concrete implementation the liberty to enhance and polish graphics (e.g., adding shaders, rich UI styling, particles) without changing a single line of game logic.

## Project Structure

See [structure.md](references/structure.md) for the full package layout.

```text
ProjectName/
├── pyproject.toml
├── justfile
├── README.md
├── TODO.md
├── src/project_name/
│   ├── __init__.py
│   ├── main.py              # Entry point; wires input and graphics adapters into game
│   ├── core/
│   │   ├── __init__.py
│   │   ├── constant.py      # World constants (immutable laws)
│   │   ├── math.py          # Vector/wrap helpers
│   │   ├── physics.py       # Pure state transition functions
│   │   ├── input.py         # InputEngine protocol
│   │   ├── render.py        # RenderEngine protocol
│   │   └── state.py         # Dataclasses with __slots__
│   ├── game/
│   │   ├── __init__.py
│   │   └── gameplay.py      # Module-level Gameplay functions
│   └── engine/
│       ├── raylib_input.py  # Module-level Raylib input implementation
│       └── raylib_render.py # Module-level Raylib rendering implementation
└── tests/
```

## Testing & Verification

### Behavioral TDD (Core & Game Layers)

All simulation logic in `core/` and `game/` must be developed using a **Test-First** approach:

1.  **Red**: Write a failing test for a physics rule or state transition.
2.  **Green**: Implement the minimum logic to pass the test.
3.  **Refactor**: Optimize for efficiency while maintaining correctness.

### Vanilla BDD for Scenarios

Use `pytest` to describe gameplay behaviors using the **Given / When / Then** pattern:

- **Given**: A player at a specific position with a specific velocity.
- **When**: A specific input is applied.
- **Then**: The resulting position, velocity, and game status must match expectations.

### Headless Validation (Engine Injection)

Logic tests **must never require a hardware window**. The `game/` and `core/` layers receive decoupled graphics and input objects via **Dependency Injection**.
- During testing, inject a `MockInput` and a `MockGraphics` implementing their respective protocols.
- Verify that logic correctly reads input and triggers the expected high-level rendering representations without needing actual hardware or window context.

## Configuration & Constants

### Constants (`core/constant.py`)

Constants define the **"Laws of the World."**
- **Location**: Kept in `core/` to maintain locality with the physics engine.
- **Examples**: `GRAVITY`, `MAX_SPEED`, `SCREEN_SIZE`, `PLAYER_SPEED`.
- **Policy**: Immutable and importable by any layer.

### Configuration (`engine/config.py`)

Configuration represents **Deployment & Hardware Settings.**
- **Location**: Kept in `engine/` as it concerns rendering and environment setup.
- **Examples**: `SCREEN_WIDTH`, `FPS`, `ASSET_PATH`.
- **Injection Policy**: Business logic in `core/` and `game/` **must never** import this. Values are passed in via constructors or module setup during initialization.

## Key Workflows

### Gameplay Loop Design

Every game follows the same loop in `main.py`:

```python
graphics.init()
player = game.init()

while not graphics.should_quit():
    dt = graphics.get_frame_time()
    graphics.begin_frame()
    player = game.update(graphics, input, player, dt)
    graphics.render(player)
    graphics.end_frame()

graphics.close()
```

### Visual Debugging with Raylib

- Use `render_mode="human"` equivalents (direct play mode) to visually inspect behavior.
- Implement high-level debug render hooks (such as `render_debug_overlay(state)`) on the graphics interface to visualize velocities, collision boxes, or state variables.

## Tooling & CLI

- **Dependencies**: `uv add raylib pytest`.
- **Raylib Note**: Although the package name is `raylib`, it must be imported as `pyray`. Always use the `pr` alias for consistency.

```python
import pyray as pr
```

- **Task Runner**: Use `just` for common commands (`just play`, `just test`, `just sync`).
- **Entry Point**: Define the play command in `pyproject.toml` under `[project.scripts]` rather than using a CLI framework for simple games.

```toml
[project.scripts]
spacerace-play = "spacerace.main:run"
```

## Project Interaction

- **Trigger**: "Build a Raylib game where [mechanic]"
- **Trigger**: "Implement the simulation logic for [mechanic]"
- **Trigger**: "Add a Raylib debug overlay for [state/variable]"
- **Trigger**: "Add [input/control] to move [entity]"
- **Trigger**: "Refactor the game into the core/game/engine layers"
