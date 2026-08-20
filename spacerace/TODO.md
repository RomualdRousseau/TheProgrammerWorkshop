# Space Race Roadmap

## 🎯 Backlog

_Unrefined ideas or upcoming features (post-brief)._

- [ ] **Story: Juiciness pass**
  - **Goal:** As a player, I want visible celebration and impact effects, so that scoring feels rewarding and hits feel costly.
  - **Acceptance Criteria:**
    - [ ] Explosion particle burst and screen flash when a rocket is hit
    - [ ] Score popup at the goal line when a player scores
    - [ ] Engine exhaust flicker while a rocket thrusts
  - **Labels:** `priority:low`, `unrefined`
- [ ] **Story: Audio**
  - **Goal:** As a player, I want sound effects, so that game events have audible feedback.
  - **Acceptance Criteria:**
    - [ ] Explosion and score sounds; countdown beeps near match end (ship engine beeps are covered by Story 9)
  - **Labels:** `priority:low`, `unrefined`
- [ ] **Story: Match start countdown**
  - **Goal:** As a player, I want a 3-2-1-GO countdown, so that both players start fairly.
  - **Labels:** `priority:low`, `unrefined`
- [ ] **Story: Smarter demo bot**
  - **Goal:** As a player, I want the demo to look skillful, so that the attract loop is engaging. (Drop-in `InputSource` replacement — no game-logic changes.)
  - **Labels:** `priority:low`, `unrefined`
- [ ] **Story: Randomized lanes & difficulty ramp**
  - **Goal:** As a player, I want variety between matches, so that the game stays fresh. (Seeded RNG per match; optional speed ramp over match time.)
  - **Labels:** `priority:low`, `unrefined`
- [ ] **Story: Single-player mode vs bot**
  - **Goal:** As a solo player, I want to race against the computer, so that I can play alone. (Reuse the bot `InputSource` for P2.)
  - **Labels:** `priority:low`, `unrefined`
- [ ] **Story: External configuration**
  - **Goal:** As a designer, I want durations/speeds in a config file, so that I can tune the game without editing code.
  - **Labels:** `priority:low`, `unrefined`

## 🏗️ Selected for Development

_Refined stories with clear acceptance criteria, in implementation order._

- [ ] **Story 8: Demo mode (attract loop)**
  - **Goal:** As a player, I want the game to play itself after idle time on the title, so that it feels alive like an arcade cabinet.
  - **Acceptance Criteria:**
    - [ ] Title inactivity (15 s, reset by any mapped key) enters Demo with a fresh `PlayState`
    - [ ] Demo reuses the exact playing logic and renderer; only the input source differs — a seeded `RandomBot` (decision interval ~0.15 s, never confirms); `Space` still comes from the keyboard and starts a normal match immediately
    - [ ] Demo duration (30 s) expiry returns to Title
    - [ ] Bot is replaceable: it implements the `InputSource` protocol; seeded RNG injected for determinism
    - [ ] TDD: headless tests for all demo transitions and bot determinism (same seed → same commands)
  - **Labels:** `priority:high`
- [ ] **Story 9: Ship engine beeps — pitch rises with altitude**
  - **Goal:** As a player, I want each ship to emit the original game's signature beep whose pitch climbs as the ship ascends, so that I can hear the race's progress like on the 1973 cabinet.
  - **Acceptance Criteria:**
    - [ ] Each ship emits a continuous beep while a match is active (Main Game and Demo); pitch rises smoothly from low at the start row to high at the goal row, correlated with the ship's vertical position
    - [ ] The two ships are distinguishable by ear (e.g., P1 panned left / P2 panned right, or distinct base tones)
    - [ ] A ship's beep is silent while the ship is hidden/respawning; no beeps on the Title or Game Over screens
    - [ ] Tones are generated in code (sine wave via raylib audio streams) — no audio asset files required
    - [ ] Audio lives entirely in the engine layer, driven by the high-level representation passed to it; the altitude→progress mapping is a pure core function with headless tests; the full suite still passes without audio hardware
  - **Labels:** `priority:medium`

## 🚧 In Progress

_Currently being implemented._

## ✅ Done

_Completed work._

- [x] **Story 7: Game Over screen**
  - **Goal:** As a player, when time expires I want to see the frozen final screen, so that the match has closure.
  - **Acceptance Criteria:**
    - [x] Match timer expiry transitions to Game Over, freezing the final `PlayState`; rendering shows exactly the last game frame (scores + timer at 0), no overlay text
    - [x] `Space` returns to Title; `GAMEOVER_TIMEOUT` (10 s) returns automatically; the timeout is independent of the match timer
    - [x] Title → new match afterwards resets everything
    - [x] TDD: headless tests for expiry transition, both return paths, timeout independence
  - **Labels:** `priority:high`
  - **Implemented:** `core/state.py` (`Scene.GAMEOVER`, `GameOverState`, `AppState.gameover`); `core/constant.py` (`GAMEOVER_TIMEOUT=10.0`); `game/scenes.py` (`_update_playing` transitions to GAMEOVER when `match_timer` reaches 0; `_update_gameover` returns to title on Space or timeout; `_go_to_title()` ensures a fresh title state); `scenes.draw` renders the frozen final frame via `gameplay.draw` for GAMEOVER. 6 new headless tests in `tests/test_scenes.py` cover expiry transition, Space/timeout return paths, timeout independence, full reset on new match, and frozen-frame drawing. 53 tests total pass.
- [x] **Story 6: Title screen & scene router**
  - **Goal:** As a player, I want a title screen where Space starts a match, so that the game has a proper entry point.
  - **Acceptance Criteria:**
    - [x] App boots into Title showing `title.png` (native 512×512); edge-triggered `Space` starts a fresh match
    - [x] Router (`AppState` + explicit dispatch) introduced; entering PLAYING constructs a fully fresh `PlayState` (players, scores, timer, asteroids, effects)
    - [x] Inactivity timer starts ticking on the title (transition lands in Story 8); any mapped key resets it
    - [x] TDD: headless tests for title→playing transition and full state reset
  - **Labels:** `priority:high`
  - **Implemented:** `core/state.py` (`Scene` enum, `TitleState`, `AppState`); `core/constant.py` (`TITLE_INACTIVITY_TIMEOUT=15.0`); `core/render.py` (`render_title` protocol method); `game/scenes.py` (router with `init/update/draw`, title inactivity handling, Space → fresh `PlayState`); `engine/raylib_render.py` (loads `title.png`, `render_title` draws it natively to the window); `main.py` now drives `scenes`. 8 new headless tests in `tests/test_scenes.py`. 47 tests total pass.
- [x] **Story 5: Scoring & match timer**
  - **Goal:** As a player, I want to score by reaching the top and race a countdown, so that matches produce a winner.
  - **Acceptance Criteria:**
    - [x] Reaching the goal row awards +1 and resets that rocket to its start; play continues
    - [x] Match timer counts down from `MATCH_DURATION` (60 s)
    - [x] HUD (renderer-level) shows both scores and remaining time — it is part of the game screen, so the frozen Game Over frame shows the final result with no extra text
    - [x] TDD: headless tests for scoring, reset-on-score, countdown
  - **Labels:** `priority:high`
  - **Implemented:** `core/state.py` (`scores`, `match_timer` on `PlayState`); `core/constant.py` (`GOAL_ROW=0`, `MATCH_DURATION=60.0`); `game/gameplay.py` (`_update_player` now returns `(Player, int)` and awards a point when an active rocket reaches `GOAL_ROW`, then resets it to start; match timer counts down and clamps at 0); `engine/raylib_render.py` (`_draw_hud` draws a vertical timer bar in the center that shrinks from bottom to top, and larger P1/P2 scores in ship-sized text closer to each player's start lane). 6 new headless tests in `tests/test_gameplay.py` cover scoring, reset-on-score, hidden-player can't score, timer countdown/clamp, and scoring not affecting the other player. 39 tests total pass.
- [x] **Story 4: Collision & respawn**
  - **Goal:** As a player, when I hit an asteroid I want my rocket to briefly disappear and respawn at the start, so that mistakes cost time but the race never stops.
  - **Acceptance Criteria:**
    - [x] Collision detection between an active rocket and asteroids
    - [x] On hit: rocket is hidden, immobile and non-collidable for `RESPAWN_DELAY` (~0.5 s), then reappears at its start position; the other player and asteroids continue uninterrupted
    - [x] Hidden rockets cannot move, score, or be drawn
    - [x] TDD: full cycle — hit → hidden → timer elapses → respawned at start; no collision while hidden
  - **Labels:** `priority:high`
  - **Implemented:** `core/state.py` (`respawn_timer` on `Player`); `core/constant.py` (`RESPAWN_DELAY=0.5`); `core/physics.py` (`collides` AABB check); `game/gameplay.py` (`_update_player` handles hit → hidden → respawn cycle); `engine/raylib_render.py` skips hidden rockets. 7 new headless tests in `tests/test_gameplay.py` cover hit detection, hidden immobility, no hidden collision, respawn at start, and uninterrupted other player/asteroids. 33 tests total pass.
- [x] **Story 3: Asteroid lanes**
  - **Goal:** As a player, I want asteroids sweeping horizontally across several lanes, so that the climb requires timing and nerve.
  - **Acceptance Criteria:**
    - [x] Fixed deterministic layout: lanes confined to the middle band; start and goal rows are safe zones; per-lane speed, alternating direction, evenly spaced asteroids — identical every match
    - [x] Asteroids move horizontally with dt and wrap seamlessly at screen edges
    - [x] Rendered as 2-px-wide white vertical bars via the render protocol
    - [x] TDD: tests for wrap-around, direction, spacing preservation, deterministic reset
  - **Labels:** `priority:high`
  - **Implemented:** `core/state.py` (`Asteroid` dataclass, `rng_state` in `PlayState`); `core/constant.py` (`ASTEROID_COUNT=20`, `ASTEROID_WIDTH=2`, `ASTEROID_HEIGHT=1`, speed range, `SAFE_ZONE_HEIGHT=48` so the rocket launch row is fully safe); `core/physics.py` (`move_asteroid`, `_is_off_screen`, `_make_asteroid` with `on_screen` flag, `make_asteroids`, `update_asteroids`); `game/gameplay.py` (`init(seed)` for deterministic/random start, `update()` advances asteroids and respawns off-screen ones); `engine/raylib_render.py` draws 2×1 white rectangles. 13 headless tests in `tests/test_asteroids.py` covering size, safe-zone placement, bidirectional movement, speed range, on-screen initial x, varied x, respawn, and deterministic update. 26 tests total pass.
- [x] **Story 2: Player rockets — movement & rendering**
  - **Goal:** As a player, I want to move my rocket vertically with responsive keys, so that I can race to the top.
  - **Acceptance Criteria:**
    - [x] P1 moves with `W`/`S`, P2 with `↑`/`↓`; vertical-only, dt-based, speed from constants
    - [x] Movement clamped inside the 128×128 field; players move independently
    - [x] Both rockets drawn with `spaceship.png`, tinted per player (P1 light, P2 yellow)
    - [x] TDD: headless tests (scripted mock input) cover up/down movement, clamping, independence
  - **Labels:** `priority:high`
  - **Implemented:** `core/input.py` (`InputCommand`, `InputSource` protocol), `core/render.py` (`RenderEngine` protocol), `core/state.py` (`Player`, `PlayState`), `core/math.py` (`clamp`), `core/physics.py` (`move_player`, clamped), `game/gameplay.py` (init/update/draw), `engine/raylib_input.py` (keyboard polling), sprite rendering at original size (16×18 rocket) in white on black; `main.py` loop with dt clamp. 10 new headless tests (13 total). Verified visually: both rockets render at the expected positions on the 128×128 field.
- [x] **Story 1: Project bootstrap & rendering harness**
  - **Goal:** As a developer, I want a scaffolded project with tooling and a 128×128→512×512 pixel-perfect render pipeline, so that every later story has a tested, visible foundation.
  - **Acceptance Criteria:**
    - [x] `pyproject.toml` (raylib dep, `dev` extra with pytest, `spacerace-play` script entry), `justfile` (`play/test/sync/clean`), src-layout `core/game/engine` packages exist
    - [x] `just sync` and `just test` succeed (headless smoke test); `uv run spacerace-play` opens a 512×512 "Space Race" window at 60 FPS and closes cleanly via Esc/window close
    - [x] All drawing goes through a 128×128 render texture upscaled ×4 with point filtering
    - [x] `README.md` and `TODO.md` (this backlog) created
  - **Labels:** `priority:high`, `foundational`
  - **Implemented:** uv/hatchling src-layout package; `engine/config.py` (512×512 window, 60 FPS, asset dir); `engine/raylib_render.py` (128×128 render texture → ×4 point-filtered blit); `main.py` frame loop; 3 headless smoke tests (3 passed). Verified: window runs at 60 FPS on raylib 6.0.
