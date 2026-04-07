# Raylib Project Structure

Prefer a modular, package-based structure where your code is organized into a main package with specialized sub-modules.

```text
src/your_project_name/
├── __init__.py
├── __main__.py          # Entry point, initializes window and main loop
├── core/
│   ├── __init__.py
│   ├── physics.py       # Domain: Physics integration and logic
│   └── config.py        # Configuration from env vars (e.g., TARGET_FPS)
├── game/
│   ├── __init__.py
│   └── state.py         # Domain: Dataclasses and state definitions
├── ui/
│   ├── __init__.py
│   └── renderer.py      # Domain: Raylib drawing and visual components
└── utils/
    ├── __init__.py
    ├── constant.py      # Immutable values (Colors, GRID_SIZE, WINDOW_TITLE)
    └── helper.py        # Shared stateless logic (Random, math helpers)
```

## Modular Design Guidelines

1.  **Package as Module**: Always run the application with `uv run -m package_name`.
2.  **Separate Config and Constants**:
    - `core/config.py`: For dynamic settings that can change via environment variables.
    - `utils/constants.py`: For hardcoded, immutable values.
3.  **Flat Domain Modules**: Group related functions and state definitions in singular files within domain-specific directories (`game/`, `ui/`).
4.  **Absolute Imports**: Always use absolute paths from the project root.
