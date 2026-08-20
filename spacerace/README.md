# Space Race

A modern adaptation of **Space Race** (Atari, 1973) — a two-player competitive
arcade game written in Python on top of [raylib](https://www.raylib.com/).

## The Game

Two rockets launch from the bottom of the screen. Reach the top to score a
point — but asteroids sweep horizontally across several lanes. Get hit and your
rocket briefly disappears, then respawns at the bottom while the race goes on.
When the match timer expires, the highest score wins.

The game world is a 256×256 pixel-art screen upscaled ×2 to a 512×512
window, rendered strictly in black and white like the 1973 original.

### Controls

| Action          | Player 1 | Player 2 |
| --------------- | -------- | -------- |
| Move up         | `W`      | `↑`      |
| Move down       | `S`      | `↓`      |
| Start / confirm | `Space`  |          |
| Quit            | `Esc`    |          |

### States

- **Title** — press `Space` to start; enters Demo after an inactivity delay.
- **Main Game** — the two-player match against the countdown.
- **Game Over** — the frozen final screen; `Space` or a timeout returns to Title.
- **Demo** — attract mode; the match plays itself; `Space` starts a real game.

## Usage

```bash
just sync         # install dependencies
just play         # run the game
just test         # run the test suite
just check        # run all quality checks (format, lint, types, tests)
just format       # format the code with ruff
just lint         # lint the code with ruff
just typecheck    # type check with ty
just clean        # remove caches
just              # list all recipes
```

Direct `uv` equivalents: `uv sync --extra dev`, `uv run spacerace-play`,
`uv run pytest`, `uv run --extra dev ruff check .`, `uv run --extra dev ty check .`.

## Architecture

```text
src/spacerace/
├── core/      # data, physics, input/render protocols — no rendering
├── game/      # gameplay logic — imports only core
├── engine/    # Raylib adapters — implements core abstractions
└── main.py    # wires engine into game and runs the loop
```

Logic in `core/` and `game/` is 100% headless-testable; hardware calls live
only in `engine/`. See `AGENTS.md` for the full conventions and `TODO.md` for
the development roadmap.
