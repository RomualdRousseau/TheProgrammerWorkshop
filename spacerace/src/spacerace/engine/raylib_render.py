"""Raylib-backed render engine.

The 256x256 logical world is drawn into a render texture, then blitted
upscaled x2 to the physical window with point filtering for crisp pixels.
The game is rendered strictly in black and white.
"""

import pyray as pr

from spacerace.core import constant
from spacerace.core.state import PlayState
from spacerace.engine import config

_render_texture: pr.RenderTexture
_spaceship: pr.Texture

# The spaceship source image is 32x33 with the 16x18 rocket drawn in the
# center (8 px of padding on every side); it is rendered at original size.
_SPRITE_SCALE: float = 1.0
_SPRITE_OFFSET: float = 8.0  # content padding inside the source image
_SCORE_FONT_SIZE: int = 20
_SCORE_MARGIN: int = 40
_TIMER_BAR_WIDTH: int = 2


def init() -> None:
    """Open the window, create the render target, and load assets."""
    global _render_texture, _spaceship
    pr.init_window(config.WINDOW_SIZE, config.WINDOW_SIZE, config.WINDOW_TITLE)
    pr.set_target_fps(config.FPS)
    _render_texture = pr.load_render_texture(constant.SCREEN_SIZE, constant.SCREEN_SIZE)
    pr.set_texture_filter(
        _render_texture.texture, pr.TextureFilter.TEXTURE_FILTER_POINT
    )
    _spaceship = pr.load_texture(str(config.ASSET_DIR / "spaceship.png"))
    pr.set_texture_filter(_spaceship, pr.TextureFilter.TEXTURE_FILTER_POINT)


def should_quit() -> bool:
    """Return True when the user asks to quit (Esc key or window close)."""
    return pr.window_should_close()


def get_frame_time() -> float:
    """Return the elapsed time in seconds since the previous frame."""
    return pr.get_frame_time()


def begin_frame() -> None:
    """Start drawing the world into the 128x128 render target."""
    pr.begin_texture_mode(_render_texture)
    pr.clear_background(pr.BLACK)


def end_frame() -> None:
    """Blit the render target upscaled to the window and present it."""
    pr.end_texture_mode()
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    source = pr.Rectangle(
        0.0, 0.0, float(constant.SCREEN_SIZE), -float(constant.SCREEN_SIZE)
    )
    destination = pr.Rectangle(
        0.0, 0.0, float(config.WINDOW_SIZE), float(config.WINDOW_SIZE)
    )
    pr.draw_texture_pro(
        _render_texture.texture,
        source,
        destination,
        pr.Vector2(0.0, 0.0),
        0.0,
        pr.WHITE,
    )
    pr.end_drawing()


def render_play(state: PlayState) -> None:
    """Render a live match: asteroids, rockets, and HUD in white on black."""
    for asteroid in state.asteroids:
        pr.draw_rectangle(
            int(asteroid.x),
            int(asteroid.y),
            asteroid.width,
            asteroid.height,
            pr.WHITE,
        )
    for player in state.players:
        if player.respawn_timer > 0:
            continue
        pr.draw_texture_ex(
            _spaceship,
            pr.Vector2(player.x - _SPRITE_OFFSET, player.y - _SPRITE_OFFSET),
            0.0,
            _SPRITE_SCALE,
            pr.WHITE,
        )
    _draw_hud(state)


def _draw_hud(state: PlayState) -> None:
    """Draw the original-style timer bar and side scores."""
    _draw_timer(state)
    _draw_scores(state)


def _draw_timer(state: PlayState) -> None:
    """Draw a vertical bar in the center that shrinks from top to bottom."""
    ratio = state.match_timer / constant.MATCH_DURATION
    height = int(constant.SCREEN_SIZE * ratio)
    x = (constant.SCREEN_SIZE - _TIMER_BAR_WIDTH) // 2
    y = constant.SCREEN_SIZE - height
    pr.draw_rectangle(x, y, _TIMER_BAR_WIDTH, height, pr.WHITE)


def _draw_scores(state: PlayState) -> None:
    """Draw each score beside its player's start lane, ship-sized font."""
    p1_score = str(state.scores[0])
    p2_score = str(state.scores[1])
    y = int(constant.START_Y + constant.PLAYER_HEIGHT / 2 - _SCORE_FONT_SIZE / 2)

    pr.draw_text(p1_score, _SCORE_MARGIN, y, _SCORE_FONT_SIZE, pr.WHITE)

    p2_width = pr.measure_text(p2_score, _SCORE_FONT_SIZE)
    pr.draw_text(
        p2_score,
        constant.SCREEN_SIZE - _SCORE_MARGIN - p2_width,
        y,
        _SCORE_FONT_SIZE,
        pr.WHITE,
    )


def close() -> None:
    """Release resources and close the window."""
    pr.unload_texture(_spaceship)
    pr.unload_render_texture(_render_texture)
    pr.close_window()
