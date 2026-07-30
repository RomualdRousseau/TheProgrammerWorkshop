# GreenSquare

GreenSquare is a 2D Python game built with Raylib (`pyray`). A 32x32 green square moves within a 512x512 bounded window via arrow keys, featuring smooth physics movement, drop shadow, and motion trails.

## Tech Stack

- **Language**: Python 3.12+
- **Renderer**: Raylib (`pyray`)
- **Package Manager**: `uv`
- **Task Runner**: `just`
- **Testing**: `pytest`

## Quick Start

### Installation

```bash
just sync
# or
uv sync --extra dev
```

### Play Game

```bash
just play
# or
uv run greensquare-play
```

### Run Tests

```bash
just test
# or
uv run pytest
```

## Architecture

The project follows a strict three-layer decoupled architecture:

- `src/greensquare/core/`: World constants, physics functions, state dataclasses, and input/render protocol abstractions.
- `src/greensquare/game/`: Gameplay logic (imports only `core`).
- `src/greensquare/engine/`: Raylib adapter implementing `core` input and rendering interfaces.
- `src/greensquare/main.py`: Composition root wiring engine adapters into the game layer.
