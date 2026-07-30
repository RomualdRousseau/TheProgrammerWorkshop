# GreenSquare Roadmap

## 🎯 Backlog
*Unrefined ideas or upcoming features.*

- [ ] **Story: Sound & Audio Cues**
  - **Goal:** As a player, I want audio feedback on movement, so that moving feels tactile.
  - **Acceptance Criteria:**
    - [ ] Subdued tick/hum plays during movement
    - [ ] Soft bump sound when hitting screen edge
  - **Labels:** `priority:low`, `unrefined`

## 🏗️ Selected for Development
*Refined stories with clear acceptance criteria.*

## 🚧 In Progress
*Currently being implemented.*

## ✅ Done
*Completed work.*

- [x] **Story 1: Project Setup & Package Scaffold**
  - **Goal:** As a developer, I want a clean Python package structure with Raylib and pytest setup, so that the project is ready for development.
  - **Acceptance Criteria:**
    - [x] `pyproject.toml`, `justfile`, `README.md` configured for `greensquare` package
    - [x] Source layout `src/greensquare/` with `core/`, `game/`, and `engine/` subpackages created
    - [x] Dependencies synced and `pytest` runs without error
  - **Labels:** `priority:high`, `refined`

- [x] **Story 2: Core Physics & Headless Simulation**
  - **Goal:** As a player, I want precise 2D movement clamped to window bounds, so that the green square stays on screen.
  - **Acceptance Criteria:**
    - [x] `PlayerState` dataclass defined with position `(x, y)` and velocity
    - [x] Pure physics update function handles directional input and delta time
    - [x] Square position clamped to `[0, 512 - 32]` on both axes
    - [x] 100% headless pytest coverage for movement and bounding logic
  - **Labels:** `priority:high`, `refined`

- [x] **Story 3: Tooling Setup (Linting, Formatting & Type Checking)**
  - **Goal:** As a developer, I want `just lint` and `just format` recipes using `uvx ruff` and `uvx ty`, so that code quality, style, and type safety are automatically enforced.
  - **Acceptance Criteria:**
    - [x] Add `lint` recipe to `justfile` running `uvx ruff check .` and `uvx ty check`
    - [x] Add `format` recipe to `justfile` running `uvx ruff format .`
    - [x] Verify `just lint` and `just format` run cleanly without errors
  - **Labels:** `priority:high`, `refined`

- [x] **Story 4: Raylib Engine Adapters & Main Game Loop**
  - **Goal:** As a player, I want to control a 32x32 green square in a 512x512 window with arrow keys or close with ESC, so that I can play the game.
  - **Acceptance Criteria:**
    - [x] `RaylibInput` implements `InputEngine` protocol (arrow keys, ESC, window close)
    - [x] `RaylibRender` renders 512x512 black background and 32x32 green square
    - [x] `main.py` composition root wires engine into gameplay loop at 60 FPS
  - **Labels:** `priority:high`, `refined`

- [x] **Story 5: Visual Polish & Movement Juice**
  - **Goal:** As a player, I want smooth movement easing, soft shadow, and motion trail, so that controlling the square feels polished and satisfying.
  - **Acceptance Criteria:**
    - [x] Acceleration and deceleration friction easing applied to movement
    - [x] Soft drop shadow rendered offset behind player
    - [x] Fading motion trail rendered during movement
  - **Labels:** `priority:medium`, `refined`

- [x] **Story 6: Setup Pre-commit Hooks using `prek`**
  - **Goal:** As a developer, I want git pre-commit hooks configured via `prek`, so that code formatting, linting, and type checking run automatically on every commit.
  - **Acceptance Criteria:**
    - [x] Create `.pre-commit-config.yaml` with trailing whitespace, EOF fixer, `ruff`, `ruff-format`, and `ty check` hooks.
    - [x] Add `hooks` recipe to `justfile` running `uvx prek install`.
    - [x] Run `uvx prek run --all-files` and verify all hooks execute and pass cleanly.
  - **Labels:** `priority:medium`, `refined`
