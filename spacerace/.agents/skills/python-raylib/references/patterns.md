# Design Patterns for Raylib Games

These patterns facilitate building modular, testable, and visually-debuggable games.

## 1. Module-Function Pattern (Default)

Start every game with module-level functions and minimal state. This is the recommended default for simple games.

```python
# game/__init__.py
from spacerace.core.physics import move
from spacerace.core.state import Player


def init() -> Player:
    return Player()


def update(engine, player, dt):
    dx = 0.0
    dy = 0.0
    if engine.is_left():
        dx -= 1.0
    if engine.is_right():
        dx += 1.0
    if engine.is_up():
        dy -= 1.0
    if engine.is_down():
        dy += 1.0
    return move(player, dx, dy, dt)


def draw(engine, player):
    engine.draw_square(player.x, player.y, player.size, engine.COLOR_PLAYER)
```

Use this pattern until the game has multiple modes or complex state-machine transitions.

## 2. The Scene Pattern (When the Game Complexifies)

When a game grows beyond a single screen (e.g., menu, playing, paused, game over), use the Scene pattern to coordinate state, logic, and rendering per mode.

A Scene object (or module) coordinates three primary components:
1.  **State**: The data representation.
2.  **Gameplay**: The transition logic.
3.  **Renderer**: The visual representation.

```python
class Scene:
    def __init__(self):
        self.state = init_state()
        self.status = "running"

    def update(self, dt, engine):
        if self.status == "running":
            self.state = update_gameplay(engine, self.state, dt)
            if check_win(self.state):
                self.status = "finished"

    def draw(self, engine):
        draw_renderer(engine, self.state)
```

Refactor into Scenes only when module-level functions become unwieldy.

## 3. The Router Pattern (Scene Management)

Use a dispatch-based router to switch between different scenes without complex `if/elif` chains.

```python
SCENES = {
    "menu": MenuScene(),
    "playing": LevelOneScene(),
}


def main_loop():
    current_scene = SCENES["menu"]
    while not engine.should_quit():
        current_scene.update(dt, engine)
        current_scene.draw(engine)
```

## 4. Command Pattern (Input Decoupling)

Decouple input (keyboard for humans) from the simulation logic.

```python
# core/input.py
from typing import Protocol


class InputEngine(Protocol):
    def is_up(self) -> bool: ...
    def is_down(self) -> bool: ...
    def is_left(self) -> bool: ...
    def is_right(self) -> bool: ...
    def should_quit(self) -> bool: ...
```

The engine module implements this protocol with Raylib key checks. The game layer receives the engine object and polls it.

## 5. Component-Lite (Dataclasses)

Use simple dataclasses with `__slots__` for deterministic memory and high-speed attribute access.

```python
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Player:
    x: float
    y: float
    size: float
```

Keep state immutable where possible; return updated copies from physics functions.
