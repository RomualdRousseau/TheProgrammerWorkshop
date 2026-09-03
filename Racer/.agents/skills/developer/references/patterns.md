# Design Patterns for Environments & Simulations

These patterns facilitate building modular, testable, and high-performance simulations that serve both as interactive "games" and as Gymnasium-compliant RL environments.

## 1. The Scene Pattern (State Machine & Orchestration)

The Scene pattern acts as the glue between gameplay logic, rendering, and the state machine. It manages the lifecycle of a specific "mode" of the simulation.

### Scene Structure
A Scene object (or module) coordinates three primary components:
1.  **State**: The data representation.
2.  **Gameplay**: The transition logic.
3.  **Renderer**: The visual representation.

```python
class Scene:
    def __init__(self):
        self.state = init_state()
        self.status = "running" # State Machine logic

    def update(self, dt, actions):
        if self.status == "running":
            self.state = update_gameplay(self.state, dt, actions)
            if check_win(self.state):
                self.status = "finished"

    def draw(self):
        draw_renderer(self.state)
```

## 2. The Router Pattern (Scene Management)

Use a dispatch-based router to switch between different scenes (e.g., `MenuScene`, `BattleScene`) without complex `if/elif` chains.

```python
SCENES = {
    "menu": MenuScene(),
    "playing": LevelOneScene(),
}

def main_loop():
    current_scene = SCENES["menu"]
    while not should_close():
        current_scene.update(dt, actions)
        current_scene.draw()
```

## 3. RL Transition Patterns (Gymnasium Integration)

When wrapping a simulation for RL, map the internal Scene logic to the Gymnasium lifecycle.

| Gym Method | Simulation Mapping | Responsibility |
|------------|--------------------|----------------|
| `reset()`  | `Scene.init_state()` | Re-initialize variables and return initial observation. |
| `step()`   | `Scene.update()`    | Apply action, advance simulation, and calculate reward/done. |
| `render()` | `Scene.draw()`      | Trigger Raylib drawing if in "human" mode. |

### Reward Shaping Pattern
Keep reward logic pure and separate from state transitions.
```python
def calculate_reward(state, action, next_state):
    reward = 0
    # Sparse: Goal reached
    if next_state.reached_goal: reward += 10
    # Dense: Progress toward goal
    reward += (state.dist_to_goal - next_state.dist_to_goal)
    return reward
```

## 4. Command Pattern (Input Decoupling)

Decouple input (Keyboard for humans, Actions for agents) from the simulation logic.

```python
class InputAdapter(Protocol):
    def get_actions(self) -> list[Action]: ...

class AgentAdapter:
    def __init__(self, agent): self.agent = agent
    def get_actions(self): return [self.agent.predict()]
```

## 5. Component-Lite (Dataclasses)

Use simple nested dataclasses with `__slots__` for deterministic memory and high-speed attribute access.

```python
@dataclass(slots=True)
class Entity:
    pos: pr.Vector2
    velocity: pr.Vector2
    mass: float
```
