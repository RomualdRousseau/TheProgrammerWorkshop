# Permanence Environment - Grid Physics Ball

A functional, modular game prototype built with Python and Raylib. The simulation features a ball that uses Euler integration to move toward a randomly placed target rectangle on a grid.

## Core Philosophy

- **Pythonic & Functional**: Prefers modules and functions over deep class hierarchies.
- **Explicit State**: Game state is managed via immutable-ish dataclasses passed explicitly to logic and rendering functions.
- **Modular Architecture**:
  - `core`: Central engine logic (Physics) and application configuration.
  - `game`: Domain-specific state definitions and orchestration.
  - `ui`: Rendering logic and visual components.
  - `utils`: Shared constants, assets loading, and helper functions.

## Features

- **Grid-based Movement**: 20x20 playable grid within a bordered screen (1-cell sides/bottom, 4-cells top).
- **Euler Physics**: Real-time integration considering mass, friction, and acceleration (force-based).
- **Sprite Animation**:
  - **Animated Ball**: 3-frame animation at 3 FPS.
  - **Table Sprite**: Replaces the target rectangle for a polished look.
- **Randomized Simulation**:
  - Random ball starting position, mass, and friction.
  - Random target placement (constrained within a 2-cell playable border).
  - Random target point within the table area.
- **Toggleable Visualization**: Toggle Layer 2 (ball and target point) visibility with the **Spacebar**.
- **Tilemap Support**: Integrated loading and rendering of tiled map layers using TMX files (covers the full screen).

## Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) (Astral's fast Python package manager)
- [just](https://github.com/casey/just) (Command runner)

### Installation

```bash
just sync
```

### Running the Simulation

```bash
just run
```

### Configuration

You can customize the simulation using environment variables:

- `TARGET_FPS`: Adjust the simulation speed (default: 60).

Example:

```bash
TARGET_FPS=30 just run
```

## Development

### Code Quality & Testing

We maintain **100% test coverage** and enforce strict type safety.

```bash
just format       # Auto-format with Ruff
just check        # Run format-check, lint, typecheck, and tests
just coverage     # Run tests and generate coverage report
just clean        # Clean caches with pyclean
```

### Key Conventions

- **Justfile**: Always use `just <recipe>` for common tasks.
- **Pyray Alias**: Always `import pyray as pr`.
- **Absolute Imports**: All imports must use the absolute package path (`permanence_env...`).
- **No Wildcards**: Explicit imports are required for clarity and type safety.
