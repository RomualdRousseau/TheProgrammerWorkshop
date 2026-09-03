# 🏎️ Racer

> A top-down survival racing game built with Raylib, designed from the ground up to be a **Gymnasium environment** for training Reinforcement Learning agents.

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-enabled-purple.svg)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/badge/ruff-lint%20%26%20format-orange.svg)](https://github.com/astral-sh/ruff)
[![pytest](https://img.shields.io/badge/pytest-tested-green.svg)](https://docs.pytest.org/)
[![Gymnasium](https://img.shields.io/badge/Gymnasium-RL%20Env-lightgrey.svg)](https://gymnasium.farama.org/)

---

## The Vision

Racer is a **playable game** and a **fully instrumented RL environment** in one package. The same code that renders the game on screen also drives the simulation headless for training. No disconnect between "what the human plays" and "what the agent sees."

The core loop is simple but rich enough for RL:
- **Dodge** scrolling obstacle cars for 90 seconds
- **Survive** = win
- **Collide** = game over
- **Score** by passing obstacles

Three actions: **Left**, **Right**, **Idle**. That's it. But the random spawn patterns and varying speeds make it a solid control problem.

---

## Quick Start

```bash
# Clone and sync
just sync

# Play it yourself
just env play

# Watch a random agent stumble around
just env test

# Run the test suite
just test

# Run all checks (lint, typecheck, test)
just check
```

---

## Project Structure

```
racer/
├── racer-env/           # The game + Gymnasium environment
│   ├── src/racer_env/
│   │   ├── core/        # Config, Input abstraction, Scene Manager
│   │   ├── game/        # Physics, collision, game state, scenes
│   │   └── ui/          # Raylib renderer (HUD, screens)
│   └── tests/
├── racer-agents/        # RL training pipeline (Stable Baselines 3)
│   ├── src/racer_agents/
│   └── tests/
├── justfile             # Task runner
├── pyproject.toml       # Workspace configuration
└── README.md            # You are here
```

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Language | Python 3.11 |
| Package Manager | [uv](https://github.com/astral-sh/uv) |
| Renderer | [Raylib](https://www.raylib.com/) (via `raylib` Python bindings) |
| RL Framework | [Gymnasium](https://gymnasium.farama.org/) + [Stable Baselines 3](https://stable-baselines3.readthedocs.io/) |
| Linting | [Ruff](https://github.com/astral-sh/ruff) |
| Type Checking | [ty](https://github.com/astral-sh/ty) |
| Testing | [pytest](https://docs.pytest.org/) + pytest-cov |
| Task Runner | [just](https://github.com/casey/just) |

---

## Development

All tasks are wired through `just`:

| Command | What it does |
|---------|-------------|
| `just sync` | Sync workspace dependencies |
| `just lint` | Run ruff linter and format check |
| `just fix` | Auto-fix lint issues and reformat |
| `just typecheck` | Run static type analysis |
| `just test` | Run tests with coverage |
| `just check` | Run the full pipeline (prek, lint, typecheck, test) |
| `just env play` | Launch the game (human controls) |
| `just env test` | Launch the random agent test |

---

## Roadmap & Status

The full backlog is tracked in the GitHub project [**Racer**](https://github.com/users/RomualdRousseau/projects/2).

| Feature | Status | Notes |
|---------|--------|-------|
| Playable game (human controls) | ✅ Done | Keyboard input, collision, timer, scoring |
| Scene management (Start/Gameplay/Game Over) | ✅ Done | Clean scene transitions with restart |
| Input abstraction (Keyboard / Random / Agent) | ✅ Done | Hexagonal pattern, easy to extend |
| Headless simulation + Gymnasium wrapper | 🚧 In Progress | `engine/` adapter and `env/gym_env.py` |
| Visual polish (sprites, particles) | 📋 Planned | Asset-ready renderer, currently rectangles |
| RL Agents (DQN, PPO) | 📋 Planned | Waiting on Gymnasium interface |
| Configuration (JSON/YAML, env vars) | 📋 Planned | Partial: env vars already supported |

---

## Contributing

This is a monorepo managed with `uv`. Always run `uv sync` after pulling changes. Before committing, run `just check` to make sure everything passes.

## Packages

- [**racer-env**](racer-env/) — The game and Gymnasium environment
- [**racer-agents**](racer-agents/) — The RL training pipeline
