---
name: python-raylib
description: Raylib graphics and simulation in Python, featuring decoupled render protocols, input abstractions, and headless testability.
tags:
  - python
  - game
  - raylib
  - graphics
  - simulation
depends_on:
  - python-developer
---

# Python Raylib

This skill provides design and implementation patterns for 2D graphics, games, and simulations in Python using **Raylib**. Extending `python-developer`, it emphasizes clean decoupling between pure simulation logic and hardware rendering, enabling fast, headless automated testing without a display window.

## 1. Import & Library Conventions

Although the package is installed via `uv add raylib`, it must be imported as `pyray`. Always alias `pyray` as `pr` for consistency:

```python
import pyray as pr
```

Consult [import-practices.md](references/import-practices.md) for detailed import rules and conventions.

## 2. Layered Architecture

Organize simulation and game code into three distinct decoupled layers:

- **`core/`**: Fundamental physics, math, and constants. Pure, deterministic functions with no dependencies on graphics or input devices.
- **`game/`**: Game mechanics, entity state transitions, scoring, and lifecycle management. Decoupled from concrete rendering libraries.
- **`engine/`**: Raylib wrapper and hardware interfacing (display window, keyboard/gamepad polling, sound playback).

Review [structure.md](references/structure.md) for full project layout details.

## 3. Decoupled Render Protocols & Headless Testing

Simulation logic must never directly invoke Raylib drawing functions (e.g. `pr.draw_circle`). Instead, use **Dependency Injection** with abstract protocols:

- **Graphics Protocol**: Defines high-level rendering operations (e.g., `draw_player(state)`, `draw_overlay(info)`).
- **Input Protocol**: Defines input queries (e.g., `is_action_pressed()`, `get_axis_vector()`).

### Headless Testability

In automated tests (`pytest`), pass mock or stub implementations of the graphics and input protocols:

```python
def test_player_moves_on_input():
    # Given
    mock_input = StubInput(move_vector=(1.0, 0.0))
    mock_graphics = NullGraphics()
    player = Player(position=(0, 0))

    # When
    updated_player = update_player(player, mock_input, dt=0.016)

    # Then
    assert updated_player.position[0] > 0
```

This guarantees 100% of game and simulation logic can be verified rapidly in CI without a GPU or display server. Detailed patterns can be found in [patterns.md](references/patterns.md).

## 4. Standard Game Loop

The standard game loop in `main.py` coordinates timing and rendering:

```python
graphics.init()
game_state = init_game()

while not graphics.should_quit():
    dt = graphics.get_frame_time()
    graphics.begin_frame()

    game_state = update_game(game_state, input_handler, dt)
    graphics.render(game_state)

    graphics.end_frame()

graphics.close()
```

## Project Interaction

- **Trigger**: "Build a Raylib simulation or game loop for [concept]"
- **Trigger**: "Decouple game logic from Raylib rendering in [module]"
- **Trigger**: "Add headless unit tests for [game mechanic]"
- **Trigger**: "Implement a debug visual overlay for [state]"
- **Trigger**: "Add input handling for [control scheme]"
