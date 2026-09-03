---
name: developer
description: AI Environment development using Python, Raylib, and Gymnasium. Use when building high-performance, visually-debuggable RL environments, focusing on MDP design and simulation integrity.
---

# Gymnasium & Raylib Environment Development

This skill provides a foundation for building Reinforcement Learning (RL) environments using `gymnasium` for the API and `raylib` for high-performance simulation and visualization.

## Core Philosophy

1.  **Gymnasium First**: The environment must strictly adhere to the `gym.Env` interface (`reset`, `step`, `render`, `close`).
2.  **Inheritance of Standards**: This skill **inherits and enforces** all "Power of 10" rules and hexagonal architecture principles defined in the core `python-app` developer skill.
3.  **Simulation/Visualization Split**: Keep the simulation logic (physics, state updates) separate from the Raylib rendering logic. The environment must run "headless" at maximum speed.
4.  **Scene-Based Orchestration**: Use the **Scene Pattern** to coordinate `game/logic`, `ui/renderer`, and state-machine transitions between game modes and RL phases.

## Environment Structure

### The `gym.Env` Wrapper & Scenes

```python
import gymnasium as gym
from gymnasium import spaces
import pyray as pr

class MyEnv(gym.Env):
    def __init__(self, render_mode=None):
        self.render_mode = render_mode
        self.scene = MainEnvScene() # Coordinates state, logic, and renderer
        self.observation_space = spaces.Box(...)
        self.action_space = spaces.Discrete(...)

    def step(self, action):
        # Maps step() to scene.update()
        self.scene.update(dt, action)
        reward = calculate_reward(self.scene.state)
        return self._get_obs(), reward, self.scene.terminated, False, {}
```

## 3. Testing & Verification

### Behavioral TDD (Core & Game Layers)

All simulation logic in `core/` (physics) and `game/` (gameplay) must be developed using a **Test-First** approach:

1.  **Red**: Write a failing test for a physics rule or state transition.
2.  **Green**: Implement the minimum logic to pass the test.
3.  **Refactor**: Optimize for efficiency while maintaining correctness.

### Vanilla BDD for Scenarios

Use `pytest` to describe environment behaviors using the **Given / When / Then** pattern. This verifies the MDP (Markov Decision Process) transitions:

- **Given**: An agent in a specific state (position, velocity).
- **When**: A specific action is taken.
- **Then**: The resulting state, reward, and termination status must match expectations.

### Headless Validation (Engine Injection)

Logic tests **must never require a hardware window**. To achieve this, the `game/` and `core/` layers must receive an `Engine` instance via **Dependency Injection**.
- During testing, inject a `NullEngine` or `Mock(spec=Engine)`.
- Verify that logic correctly calls the engine (e.g., `engine.play_sound()`) without needing the actual hardware.

## 4. Configuration & Constants

### Constants (`core/constant.py`)

Constants define the **"Laws of the World."**
- **Location**: Kept in `core/` to maintain locality with the physics engine.
- **Examples**: `GRAVITY`, `MAX_SPEED`, `REWARD_TARGET`.
- **Policy**: Immutable and importable by any layer.

### Configuration (`engine/config.py`)

Configuration represents **Deployment & Hardware Settings.**
- **Location**: Kept in `engine/` for simplicity, as it primarily concerns rendering and environment setup.
- **Examples**: `SCREEN_WIDTH`, `FPS`, `ASSET_PATH`.
- **Injection Policy**: Business logic in `core/` and `game/` **must never** import this. Values are passed in via constructors during the setup of the `env/` or `game/` scenes.

## 5. Key Workflows

### Reward Engineering

- **Sparse vs. Dense**: Prefer sparse rewards with well-defined terminal states, or use potential-based reward shaping.
- **Invariants**: Use `Hypothesis` to verify that rewards are bounded.

### Observation Space Design

- **Normalization**: Always normalize observations to `[0, 1]` or `[-1, 1]`.
- **Type Safety**: Use `np.float32` for observations.

### Visual Debugging with Raylib

- Use `render_mode="human"` to visually inspect agent behavior.
- Use `Scene.draw()` to implement debug overlays (vectors for velocities, heatmaps for rewards).

## Tooling & CLI

- **Dependencies**: `uv add raylib gymnasium numpy fire`.
- **Raylib Note**: Although the package name is `raylib`, it must be imported as `pyray`. Always use the `pr` alias for consistency.

```python
import pyray as pr
```

- **CLI Framework**: Use `python-fire` in `src/package/__main__.py` to expose the environment and agent tasks.

### Command Structure

```python
import fire

class CLI:
    def play(self):
        """Run the environment with human controls (Raylib)."""
        # Initialize env with render_mode="human"
        ...

    def test_env(self):
        """Run a random agent to verify the Gymnasium interface."""
        # Initialize env and run N episodes with random actions
        ...

    def train(self, agent_type="ppo"):
        """Train a specific agent on the environment."""
        ...

    def eval(self, model_path):
        """Evaluate a trained agent."""
        ...

if __name__ == "__main__":
    fire.Fire(CLI)
```

## Project Interaction

- **Trigger**: "Build a new Gymnasium environment for [task]"
- **Trigger**: "Implement the simulation logic for [mechanic]"
- **Trigger**: "Add a Raylib debug overlay for [state/variable]"
- **Trigger**: "Verify the Gymnasium interface with a random agent"
- **Trigger**: "Implement the reward function for [goal]"
