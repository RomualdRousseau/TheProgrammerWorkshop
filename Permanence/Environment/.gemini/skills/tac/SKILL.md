---
name: tac
description: Game development with Python and Raylib. Use when building 2D/3D games, prototyping mechanics, or structuring Raylib projects using Pythonic, functional, and modular patterns instead of class-heavy architectures.
---

# Python Raylib Game Development

This skill provides a foundation for building games with Python and Raylib, emphasizing modularity, functional design, and Pythonic patterns over traditional class-based hierarchies.

## Core Philosophy

1.  **Prefer Modules to Classes**: Group related functions and state definitions in modules. Use singular, descriptive filenames.
2.  **Explicit State Management**: Pass game state objects (dataclasses) into update and draw functions.
3.  **Delay Abstraction**: Start with simple functions and modules. Only abstract when complexity justifies it.
4.  **Functional Over Object-Oriented**: Use first-class functions for commands and behaviors. **Prefer branchless math** (e.g., adding `EPSILON` to denominators) for cleaner logic.

## Quick Start

1.  **Project Structure**: Refer to [structure.md](references/structure.md) for the modular package layout.
2.  **Import Practices**: Follow [import-practices.md](references/import-practices.md) for naming conventions and absolute imports.
3.  **Patterns**: Use [patterns.md](references/patterns.md) for functional game design patterns.

## Tooling & Workflow

### Task Management
Use the `justfile` for all common tasks:
- `just run`: Start the simulation.
- `just check`: Run formatting, linting, and type checks.
- `just format`: Auto-format with `ruff`.
- `just clean`: Clean caches with `pyclean`.

### Quality Control
Always ensure code passes Astral's quality tools:
- **Linting**: `uv run ruff check src/`
- **Type Checking**: `uv run ty check src/` (Astral's fast type checker)

### Pyray Alias
Always use the `pr` alias for `pyray`:
```python
import pyray as pr
```

## Key Workflows

### Defining Game State
Use `dataclasses` for structured state definitions. Keep constants in `utils/constants.py`.

```python
from dataclasses import dataclass
import pyray as pr

@dataclass
class Ball:
    pos: pr.Vector2
    velocity: pr.Vector2
```

### Separate Logic and Rendering
Decouple logic (physics, AI) from visual representation.

```python
# In game/physics.py
def update_physics(ball, dt):
    ball.pos.x += ball.velocity.x * dt

# In ui/renderer.py
def draw_ball(ball):
    pr.draw_circle_v(ball.pos, 10, pr.BLUE)
```

## Advanced Topics

- **Core Config**: Use `core/config.py` for environment-driven settings (e.g., `os.getenv`).
- **Utilities**: Centralize shared logic and math helpers in `utils/helpers.py`.
- **Absolute Imports**: Maintain absolute paths across the entire project for consistency with `uv`, `ruff`, and `ty`.
