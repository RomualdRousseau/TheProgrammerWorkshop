import pyray as pr

from spacerace import (
    ACTION_NONE,
    ACTION_TIMEOUT,
    ASTEROID_COUNT,
    ASTEROIDS_END_ZONE,
    ASTEROIDS_START_ZONE,
    GAME_TIMEOUT,
    PLAYER1_CONTROLS,
    PLAYER1_RAIL,
    PLAYER2_CONTROLS,
    PLAYER2_RAIL,
    PLAYERS_START,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from spacerace.entities.asteriod import Asteroid
from spacerace.entities.entity import check_collisions
from spacerace.entities.player import Player
from spacerace.scenes.context import Context
from spacerace.utils.graphic import draw_text_centered
from spacerace.utils.resources import get_music, release_resources


def init():
    Context.timer = GAME_TIMEOUT

    Context.score1 = 0
    Context.player1 = Player(PLAYER1_RAIL, PLAYERS_START, PLAYER1_CONTROLS)

    Context.score2 = 0
    Context.player2 = Player(PLAYER2_RAIL, PLAYERS_START, PLAYER2_CONTROLS)

    rail_step = (ASTEROIDS_END_ZONE - ASTEROIDS_START_ZONE) // ASTEROID_COUNT
    Context.asteroids = [Asteroid(y) for y in range(ASTEROIDS_START_ZONE, ASTEROIDS_END_ZONE, rail_step)]

    Context.entities = [*Context.asteroids, Context.player1, Context.player2]

    Context.music = get_music("theme")
    pr.play_music_stream(Context.music)


def release():
    pr.stop_music_stream(Context.music)
    release_resources()


def update(dt: float):
    #
    # Physic
    #
    for entity in Context.entities:
        entity.update(dt)

    check_collisions(Context.entities)

    #
    # Gameplay
    #
    Context.timer = max(0.0, Context.timer - dt)

    if Context.player1.y < ASTEROIDS_START_ZONE:
        Context.player1.reset()
        Context.score1 += 1

    if Context.player2.y < ASTEROIDS_START_ZONE:
        Context.player2.reset()
        Context.score2 += 1

    #
    # Music
    #
    pr.update_music_stream(Context.music)


def draw():
    pr.clear_background(pr.BLACK)

    for entity in Context.entities:
        entity.draw()

    time_ratio = Context.timer / GAME_TIMEOUT
    pr.draw_rectangle(
        WINDOW_WIDTH // 2 - 2,
        int(WINDOW_HEIGHT * time_ratio) + 1,
        4,
        int(WINDOW_HEIGHT * (1.0 - time_ratio)) + 1,
        pr.RAYWHITE,
    )

    draw_text_centered(f"{Context.score1}", PLAYER1_RAIL - 50, PLAYERS_START, 100)
    draw_text_centered(f"{Context.score2}", PLAYER2_RAIL + 50, PLAYERS_START, 100)


def get_action() -> str:
    if Context.timer == 0.0:
        return ACTION_TIMEOUT
    else:
        return ACTION_NONE
