# 🏎️ Racer-Env

> The Raylib-powered racing game that doubles as a **Gymnasium environment**. Play it. Train on it. The same code does both.

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Gymnasium](https://img.shields.io/badge/Gymnasium-RL%20Env-lightgrey.svg)](https://gymnasium.farama.org/)
[![Raylib](https://img.shields.io/badge/Raylib-5.0-green.svg)](https://www.raylib.com/)
[![pytest](https://img.shields.io/badge/pytest-tested-green.svg)](https://docs.pytest.org/)

---

## What is it?

A top-down survival racing game where you dodge scrolling obstacle cars for 90 seconds. But under the hood, it's architected as a clean simulation + renderer split so it can run **headless for training** or **rendered for humans**.

The game is the environment. The environment is the game.

---

## Game Mechanics

- **Player Car**: 64×64. Moves left and right at the bottom of a 512×512 screen.
- **Obstacles**: Spawn every second at random horizontal positions with random downward speeds (200–400 px/s).
- **Collision**: Instant game over.
- **Timer**: Survive 90 seconds = you win.
- **Score**: Each obstacle that scrolls off the bottom = +1 point.
- **Controls**: LEFT / RIGHT arrows (human). Agents use the same action space.

---

## Architecture

```
racer_env/
├── core/
│   ├── config.py         # Centralized config (env vars supported)
│   ├── constant.py       # Game constants (speeds, sizes, intervals)
│   ├── input.py          # Input abstraction: Keyboard, Random, Agent
│   └── scene_manager.py  # Scene transition protocol & manager
├── game/
│   ├── state.py          # Entity & GameState dataclasses
│   ├── gameplay.py       # Core physics, collision, spawning, scoring
│   └── scenes.py         # StartScene, GameScene, GameOverScene, SimulationScene
└── ui/
    └── renderer.py       # Raylib drawing (HUD, screens, rectangles)
```

### Design Principles

- **Simulation is I/O-free**: `gameplay.py` knows nothing about rendering.
- **Renderer is optional**: `ui/renderer.py` can be swapped or skipped for headless mode.
- **Scenes are composable**: The Scene Manager handles transitions (Start → Gameplay → Game Over → Restart).
- **Input is polymorphic**: `KeyboardInput`, `RandomInput`, and `AgentInput` all implement the same `InputHandler` protocol.

---

## Action Space

Discrete 3:

| Action | Value | Effect |
|--------|-------|--------|
| `IDLE` | 0 | Do nothing |
| `LEFT` | 1 | Move player car left |
| `RIGHT` | 2 | Move player car right |

(Keyboard players also get `START` to begin / restart.)

---

## Observation Space

🚧 **In Progress** — The Gymnasium wrapper is actively being built. Planned modes:

| Mode | Shape | Description |
|------|-------|-------------|
| State-based | `(N,)` vector | Player position + obstacle positions/velocities |
| Pixel-based | `(H, W, 3)` | Raw rendered frame from Raylib |

---

## Reward Function

🚧 **In Progress** — Tentative design:

- `+0.1` per step survived (encourages longevity)
- `+1.0` per obstacle passed (encourages scoring)
- `-10.0` on collision (strong penalty for dying)
- `+10.0` on timer completion (win bonus)

---

## Configuration

Set via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `RACER_SCREEN_WIDTH` | `512` | Window width |
| `RACER_SCREEN_HEIGHT` | `512` | Window height |
| `RACER_TARGET_FPS` | `60` | Frame rate cap |
| `RACER_TIMER` | `90.0` | Survival timer in seconds |

JSON/YAML file support is on the roadmap.

---

## CLI Usage

```bash
# Human play mode (keyboard)
uv run python -m racer_env play

# Random agent test mode
uv run python -m racer_env test
```

Or via the root `justfile`:

```bash
just env play
just env test
```

---

## Scene Flow

```
┌─────────────┐    START     ┌─────────────┐   GAME_OVER   ┌─────────────┐
│  StartScene │ ───────────→ │  GameScene  │ ───────────→ │ GameOverScene│
└─────────────┘              └─────────────┘   or WON      └─────────────┘
                                    ↑                            │
                                    └──────── START ─────────────┘
```

- **StartScene**: "Press SPACE to Start"
- **GameScene**: Active gameplay with physics, spawning, collision
- **GameOverScene**: Displays final score. Press SPACE to restart.

---

## Testing

Tests use `pytest` with a **Given/When/Then (GWT)** structure:

```python
def test_player_cannot_move_off_screen():
    # Given
    state = starting_game_state()

    # When
    state.player.position.x = -1000
    next_state = clamp_player_position(state)

    # Then
    assert next_state.player.position.x == 0
```

Run tests:

```bash
just test
```

Coverage target: **80%+** for `core/` and `game/`.

---

## Package Details

- **Name**: `racer-env`
- **Version**: `0.1.0`
- **Python**: `3.11`
- **Dependencies**: `gymnasium`, `raylib`, `numpy`, `fire`, `pyyaml`
