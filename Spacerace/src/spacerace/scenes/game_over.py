
import pyray as pr

from spacerace import (
    ACTION_KEYPRESS,
    ACTION_NONE,
    ACTION_TIMEOUT,
    GAME_OVER_TIMEOUT,
    PLAYER1_RAIL,
    PLAYER2_RAIL,
    PLAYERS_START,
)
from spacerace.scenes.context import Context
from spacerace.utils.graphic import draw_text_centered


def init():
    Context.timer = GAME_OVER_TIMEOUT
    Context.player1.reset()
    Context.player2.reset()


def release():
    pass


def update(dt: float):
    Context.timer = max(0.0, Context.timer - dt)

    for asteroid in Context.asteroids:
        asteroid.update(dt)


def draw():
    pr.clear_background(pr.BLACK)

    for entity in Context.entities:
        entity.draw()

    draw_text_centered(f"{Context.score1}", PLAYER1_RAIL - 50, PLAYERS_START, 100)
    draw_text_centered(f"{Context.score2}", PLAYER2_RAIL + 50, PLAYERS_START, 100)

    if Context.score1 > Context.score2:
        draw_text_centered("Player 1 wins !", pr.get_screen_width() // 2, pr.get_screen_height() // 2, 20)
    elif Context.score2 > Context.score1:
        draw_text_centered("Player 2 wins !", pr.get_screen_width() // 2, pr.get_screen_height() // 2, 20)
    else:
        draw_text_centered("Players are even", pr.get_screen_width() // 2, pr.get_screen_height() // 2, 20)


def get_action() -> str:
    if Context.timer == 0.0:
        return ACTION_TIMEOUT
    elif Context.timer < GAME_OVER_TIMEOUT // 2 and pr.get_key_pressed():
        return ACTION_KEYPRESS
    else:
        return ACTION_NONE
