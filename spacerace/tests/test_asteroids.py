"""Story 3: asteroid lanes — headless physics tests."""

import random
from dataclasses import replace

from spacerace.core import constant
from spacerace.core.input import InputCommand
from spacerace.core.physics import make_asteroids, move_asteroid, update_asteroids
from spacerace.core.state import Asteroid
from spacerace.game import gameplay


def test_init_creates_expected_number_of_asteroids() -> None:
    state = gameplay.init(seed=42)

    assert len(state.asteroids) == constant.ASTEROID_COUNT


def test_asteroids_are_two_pixels_wide_and_one_pixel_tall() -> None:
    state = gameplay.init(seed=42)

    for asteroid in state.asteroids:
        assert asteroid.width == constant.ASTEROID_WIDTH
        assert asteroid.height == constant.ASTEROID_HEIGHT


def test_asteroids_spawn_in_the_middle_band() -> None:
    state = gameplay.init(seed=42)

    for asteroid in state.asteroids:
        assert asteroid.y >= constant.SAFE_ZONE_HEIGHT
        assert (
            asteroid.y + asteroid.height
            <= constant.SCREEN_SIZE - constant.SAFE_ZONE_HEIGHT
        )


def test_asteroids_move_in_both_directions() -> None:
    state = gameplay.init(seed=42)

    rights = [a for a in state.asteroids if a.velocity_x > 0]
    lefts = [a for a in state.asteroids if a.velocity_x < 0]

    assert rights
    assert lefts


def test_asteroid_speeds_are_within_range() -> None:
    state = gameplay.init(seed=42)

    for asteroid in state.asteroids:
        speed = abs(asteroid.velocity_x)
        assert constant.ASTEROID_SPEED_MIN <= speed <= constant.ASTEROID_SPEED_MAX


def test_asteroids_move_with_dt() -> None:
    asteroid = Asteroid(x=10.0, y=20.0, width=2, height=1, velocity_x=30.0)

    new = move_asteroid(asteroid, dt=1.0)

    assert new.x == 40.0
    assert new.y == asteroid.y


def test_initial_asteroids_are_on_screen() -> None:
    state = gameplay.init(seed=42)

    for asteroid in state.asteroids:
        assert 0.0 <= asteroid.x
        assert asteroid.x + asteroid.width <= float(constant.SCREEN_SIZE)


def test_initial_asteroids_have_varied_x_positions() -> None:
    state = gameplay.init(seed=42)

    xs = {asteroid.x for asteroid in state.asteroids}
    assert len(xs) > 1


def test_off_screen_asteroid_respawns_after_update() -> None:
    state = gameplay.init(seed=42)
    # Replace one asteroid with one that is already off the right edge.
    off_screen = Asteroid(
        x=float(constant.SCREEN_SIZE) + 10.0,
        y=50.0,
        width=constant.ASTEROID_WIDTH,
        height=constant.ASTEROID_HEIGHT,
        velocity_x=30.0,
    )
    state = replace(state, asteroids=(off_screen,) + state.asteroids[1:])

    new_state = gameplay.update(InputCommand(), state, dt=0.0)

    respawned = new_state.asteroids[0]
    assert respawned is not off_screen
    assert respawned.y >= constant.SAFE_ZONE_HEIGHT
    assert (
        respawned.y + respawned.height
        <= constant.SCREEN_SIZE - constant.SAFE_ZONE_HEIGHT
    )
    assert respawned.width == constant.ASTEROID_WIDTH
    assert respawned.height == constant.ASTEROID_HEIGHT
    # Respawns start just off an edge so they drift back into view.
    assert respawned.x < 0.0 or respawned.x >= float(constant.SCREEN_SIZE)


def test_init_is_deterministic_with_same_seed() -> None:
    state_a = gameplay.init(seed=42)
    state_b = gameplay.init(seed=42)

    assert state_a == state_b


def test_update_is_deterministic_with_same_state() -> None:
    state = gameplay.init(seed=42)

    new_a = gameplay.update(InputCommand(), state, dt=1.0)
    new_b = gameplay.update(InputCommand(), state, dt=1.0)

    assert new_a == new_b


def test_make_asteroids_advances_rng_state() -> None:
    rng_state = random.Random(0).getstate()

    asteroids, new_rng_state = make_asteroids(rng_state)

    assert len(asteroids) == constant.ASTEROID_COUNT
    assert new_rng_state != rng_state


def test_update_asteroids_advances_rng_state_on_respawn() -> None:
    rng_state = random.Random(0).getstate()
    off_screen = Asteroid(
        x=float(constant.SCREEN_SIZE) + 10.0,
        y=50.0,
        width=constant.ASTEROID_WIDTH,
        height=constant.ASTEROID_HEIGHT,
        velocity_x=30.0,
    )

    asteroids, new_rng_state = update_asteroids((off_screen,), rng_state, dt=0.0)

    assert len(asteroids) == 1
    assert new_rng_state != rng_state
