"""Pure state-transition functions: the physics of the Space Race world."""

import random
from dataclasses import replace

from spacerace.core import constant
from spacerace.core.math import clamp
from spacerace.core.state import Asteroid, Player


def move_player(player: Player, velocity_y: float, dt: float) -> Player:
    """Move a rocket vertically, clamped so it never leaves the field."""
    max_y = float(constant.SCREEN_SIZE - constant.PLAYER_HEIGHT)
    y = clamp(player.y + velocity_y * dt, 0.0, max_y)
    return replace(player, y=y)


def collides(player: Player, asteroid: Asteroid) -> bool:
    """Return True when the player's footprint overlaps the asteroid."""
    return (
        player.x < asteroid.x + asteroid.width
        and player.x + constant.PLAYER_WIDTH > asteroid.x
        and player.y < asteroid.y + asteroid.height
        and player.y + constant.PLAYER_HEIGHT > asteroid.y
    )


def move_asteroid(asteroid: Asteroid, dt: float) -> Asteroid:
    """Move an asteroid horizontally."""
    x = asteroid.x + asteroid.velocity_x * dt
    return replace(asteroid, x=x)


def _is_off_screen(asteroid: Asteroid) -> bool:
    """Return True when an asteroid has fully left the playfield."""
    return (asteroid.velocity_x > 0 and asteroid.x >= constant.SCREEN_SIZE) or (
        asteroid.velocity_x < 0 and asteroid.x + asteroid.width <= 0
    )


def _make_asteroid(rng: random.Random, *, on_screen: bool) -> Asteroid:
    """Create one random asteroid.

    When ``on_screen`` is True the asteroid is placed at a random x inside the
    playfield (used for the initial swarm). When False it is placed just off
    the appropriate edge so it drifts back in (used for respawns).
    """
    direction = rng.choice((-1, 1))
    speed = rng.uniform(constant.ASTEROID_SPEED_MIN, constant.ASTEROID_SPEED_MAX)
    y = rng.randint(
        constant.SAFE_ZONE_HEIGHT,
        constant.SCREEN_SIZE - constant.SAFE_ZONE_HEIGHT - constant.ASTEROID_HEIGHT,
    )
    if on_screen:
        x = rng.uniform(0.0, float(constant.SCREEN_SIZE - constant.ASTEROID_WIDTH))
    else:
        x = (
            float(constant.SCREEN_SIZE)
            if direction == -1
            else -float(constant.ASTEROID_WIDTH)
        )
    return Asteroid(
        x=x,
        y=float(y),
        width=constant.ASTEROID_WIDTH,
        height=constant.ASTEROID_HEIGHT,
        velocity_x=direction * speed,
    )


def make_asteroids(rng_state: tuple) -> tuple[tuple[Asteroid, ...], tuple]:
    """Build the initial asteroid swarm using the supplied RNG state."""
    rng = random.Random()
    rng.setstate(rng_state)
    asteroids = tuple(
        _make_asteroid(rng, on_screen=True) for _ in range(constant.ASTEROID_COUNT)
    )
    return asteroids, rng.getstate()


def update_asteroids(
    asteroids: tuple[Asteroid, ...], rng_state: tuple, dt: float
) -> tuple[tuple[Asteroid, ...], tuple]:
    """Advance asteroids and respawn any that have left the screen."""
    rng = random.Random()
    rng.setstate(rng_state)
    new_asteroids: list[Asteroid] = []
    for asteroid in asteroids:
        moved = move_asteroid(asteroid, dt)
        if _is_off_screen(moved):
            moved = _make_asteroid(rng, on_screen=False)
        new_asteroids.append(moved)
    return tuple(new_asteroids), rng.getstate()
