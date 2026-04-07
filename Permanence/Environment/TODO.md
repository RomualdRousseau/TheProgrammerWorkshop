# Backlog

- [ ] Calculate ball exit from target rectangle
- [ ] Save the first n image of the animation, and the exit coordinate in a dataset
- [ ] Convert as a gymnasium environment
- [ ] Define simulation state, final, ...

# To Be Developed (In Progress)

# Done

- [x] Story: As a designer, I want a polished visual experience with sprites and animation.
  - [x] Task: Implement animated ball sprite (3 FPS) with frame-based rendering.
  - [x] Task: Replace target rectangle drawing with a "table" sprite.
  - [x] Task: Implement grid offsets to create screen borders (1-cell sides/bottom, 4-cells top).
  - [x] Task: Ensure the table spawns within a 2-cell playable area border.
- [x] Story: As an architect, I want a clean and logical directory structure.
  - [x] Task: Move `physics.py` from `game/` to `core/` for centralized engine logic.
  - [x] Task: Fix all imports and type hints across the project.
- [x] Story: As a developer, I want a physics-driven ball that moves toward the target.
  - [x] Task: Implement Euler integration with mass and friction in `core/physics.py`.
  - [x] Task: Implement "Move Toward" logic targeting a random point within the rectangle.
  - [x] Task: Implement grid boundary rebounding (bounce on edges, accounting for ball radius).
  - [x] Task: Handle random initial speed and random starting position.
- [x] Story: As a maintainer, I want high-quality, type-safe code.
  - [x] Task: Enforce absolute imports and `pyray as pr` alias.
  - [x] Task: Setup `ruff` for linting and `ty` for type checking.
  - [x] Task: Centralize configuration in `core/config.py` using environment variables.
