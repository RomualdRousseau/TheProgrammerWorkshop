import random

import pyray as pr

from racer_env.core.config import Config
from racer_env.core.constant import (
    OBSTACLE_MAX_SPEED,
    OBSTACLE_MIN_SPEED,
    OBSTACLE_SIZE,
    PLAYER_SIZE,
    PLAYER_SPEED,
    SPAWN_INTERVAL,
)
from racer_env.core.input import Action, InputHandler
from racer_env.game.state import Entity, GameState


def init_gameplay_state() -> GameState:
    """Creates a fresh game state."""
    player = Entity(
        position=pr.Vector2(
            float(Config.SCREEN_WIDTH // 2 - PLAYER_SIZE // 2),
            float(Config.SCREEN_HEIGHT - PLAYER_SIZE - 10),
        ),
        velocity=pr.Vector2(0.0, 0.0),
        width=float(PLAYER_SIZE),
        height=float(PLAYER_SIZE),
    )
    return GameState(player=player)


def update_gameplay(dt: float, state: GameState, inputs: InputHandler) -> GameState:
    """Core simulation logic shared between different scenes."""
    if state.game_over or state.won:
        return state

    # 1. Update Timer
    state.timer += dt
    if state.timer >= Config.GAME_TIMER:
        state.won = True
        return state

    # 2. Handle Player Movement
    action = inputs.get_action()
    if action == Action.LEFT:
        state.player.position.x -= PLAYER_SPEED * dt
    elif action == Action.RIGHT:
        state.player.position.x += PLAYER_SPEED * dt

    # Clamp player position
    state.player.position.x = max(
        0.0,
        min(float(Config.SCREEN_WIDTH - state.player.width), state.player.position.x),
    )

    # 3. Spawn Obstacles
    state.spawn_timer += dt
    if state.spawn_timer >= SPAWN_INTERVAL:
        state.spawn_timer = 0.0
        x_pos = random.uniform(0.0, float(Config.SCREEN_WIDTH - OBSTACLE_SIZE))
        speed = random.uniform(OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED)
        state.obstacles.append(
            Entity(
                position=pr.Vector2(x_pos, -float(OBSTACLE_SIZE)),
                velocity=pr.Vector2(0.0, speed),
                width=float(OBSTACLE_SIZE),
                height=float(OBSTACLE_SIZE),
            )
        )

    # 4. Update Obstacles & Collisions
    for obs in state.obstacles[:]:
        obs.position.y += obs.velocity.y * dt

        # Collision detection
        if pr.check_collision_recs(state.player.rect, obs.rect):
            state.game_over = True
            return state

        # Score tracking & removal
        if obs.position.y > Config.SCREEN_HEIGHT:
            state.obstacles.remove(obs)
            state.score += 1

    return state
