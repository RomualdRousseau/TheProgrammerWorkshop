# 🤖 Racer-Agents

> The training pipeline for Racer. Take the environment, throw an agent at it, watch it learn to dodge cars better than you.

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Stable Baselines3](https://img.shields.io/badge/SB3-RL%20Library-red.svg)](https://stable-baselines3.readthedocs.io/)
[![pytest](https://img.shields.io/badge/pytest-tested-green.svg)](https://docs.pytest.org/)

---

## What is it?

The RL agent training and evaluation suite for the [Racer environment](../racer-env/). Built on top of [Stable Baselines 3](https://stable-baselines3.readthedocs.io/), it provides a unified interface for training, snapshotting, and watching agents play.

The goal: agents that can consistently survive 90 seconds and rack up high scores.

---

## The Agent Pipeline

```
┌─────────────┐    train    ┌─────────────┐   snapshot   ┌─────────────┐
│  racer-env  │ ───────────→│    Agent    │ ───────────→│   Model     │
│  (Gymnasium)│             │  (SB3 DQN   │   every K    │   .zip      │
│             │             │   or PPO)   │   steps      │             │
└─────────────┘             └─────────────┘              └─────────────┘
                                    ↑                            │
                                    └──────── evaluate / watch ──┘
```

1. **Train**: Feed the Gymnasium env to an SB3 algorithm. Save checkpoints.
2. **Evaluate**: Run N episodes, report mean reward and survival rate.
3. **Watch**: Load a saved model and render it playing in real time.

---

## Planned Agents

| Agent | Algorithm | Status | Purpose |
|-------|-----------|--------|---------|
| Random | — | ✅ Done | Baseline. Expected to die fast. |
| DQN | Deep Q-Network | 📋 Planned | Value-based, discrete actions. Natural fit. |
| PPO | Proximal Policy Optimization | 📋 Planned | Policy gradient, robust and sample-efficient. |

More algorithms may be added once the interface is stable.

---

## Agent Interface

All agents implement a common interface so they can be swapped in and out:

```python
class Agent:
    def act(self, observation) -> int:
        """Return an action from the discrete action space."""
        ...

    def train(self, env, total_timesteps: int, **kwargs):
        """Train the agent on the given environment."""
        ...

    def save(self, path: str):
        """Persist the model to disk."""
        ...

    def load(self, path: str):
        """Load a model from disk."""
        ...
```

SB3 wrappers will adapt `BaseAlgorithm` to this contract.

---

## Planned CLI Commands

```bash
# Train a DQN agent, saving snapshots every 10k steps
uv run python -m racer_agents train --algo=dqn --timesteps=100000 --snapshot-every=10000

# Watch a trained model play
uv run python -m racer_agents watch --model=models/dqn_final.zip

# Evaluate a model over 100 episodes
uv run python -m racer_agents evaluate --model=models/dqn_final.zip --episodes=100
```

Or via the root `justfile` (once implemented):

```bash
just agents train --algo=dqn
just agents watch --model=models/dqn_final.zip
```

---

## Training Workflow

```bash
# 1. Make sure the environment is installed
uv sync

# 2. Train
uv run python -m racer_agents train --algo=dqn --timesteps=500000

# 3. Check the logs and snapshots in models/
ls models/

# 4. Watch the best one
uv run python -m racer_agents watch --model=models/dqn_best.zip
```

---

## Testing

Tests follow the same GWT pattern as `racer-env`:

```python
def test_random_agent_chooses_valid_actions():
    # Given
    agent = RandomAgent()

    # When
    action = agent.act(dummy_observation())

    # Then
    assert action in [0, 1, 2]  # IDLE, LEFT, RIGHT
```

Run tests:

```bash
just test
```

Coverage target: **80%+** for core agent logic.

---

## Dependencies

- `racer-env` — The Gymnasium environment (workspace dependency)
- `stable-baselines3>=2.3.0` — The RL algorithms
- `fire>=0.6.0` — CLI generation

---

## Status

🚧 **Package initialized. Implementation pending.**

This package is waiting on the `racer-env` Gymnasium wrapper (`env/gym_env.py`) to be completed. Once the environment exposes `reset()` and `step()`, agent development begins.

---

## Package Details

- **Name**: `racer-agents`
- **Version**: `0.1.0`
- **Python**: `3.11`
- **Dependencies**: `racer-env`, `stable-baselines3`, `fire`
