from dataclasses import dataclass

import pyray as pr

from cartpole.cart import Cart
from cartpole.config import (
    CAMERA_ZOOM,
    CART_INITIAL_POSITION,
    DEG_TO_RAD,
    FRAME_RATE,
    KD,
    KI,
    KP,
    MICRO_STEPS,
    RAD_TO_DEG,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from cartpole.pole import Pole

BOARD_WIDTH = WINDOW_WIDTH / CAMERA_ZOOM
BOARD_HEIGHT = WINDOW_HEIGHT / CAMERA_ZOOM


@dataclass
class State:
    camera: pr.Camera2D
    bg_texture: pr.Texture2D
    cart: Cart
    pole: Pole
    last_err: float
    sum_err: float


def init() -> State:
    offset = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    camera = pr.Camera2D(offset, (0, 0), 0, CAMERA_ZOOM)
    bg_texture = pr.load_texture("./assets/textures/circus.png")
    cart = Cart(pr.Vector2(*CART_INITIAL_POSITION))
    pole = Pole(cart.body)
    return State(camera, bg_texture, cart, pole, 0.0, 0.0)


def release(state: State) -> None:
    pr.unload_texture(state.cart.sprite.texture)
    pr.unload_texture(state.bg_texture)


def update(state: State) -> State:
    dt = pr.get_frame_time()
    if dt <= 0 or dt >= 2 / FRAME_RATE:
        return state
    dt /= MICRO_STEPS

    (
        camera,
        cart,
        pole,
        last_err,
        sum_err,
    ) = state.camera, state.cart, state.pole, state.last_err, state.sum_err

    for _ in range(MICRO_STEPS):
        u, last_err, sum_err = control_pid(pole, last_err, sum_err, dt + 1e-6, 0.0)
        cart.body.apply_force(u)
        cart.update(dt)
        pole.update(dt)

    camera.target.x = min(max(cart.body.pos.x, -0.5 * BOARD_WIDTH), 0.5 * BOARD_WIDTH)

    return State(
        state.camera,
        state.bg_texture,
        state.cart,
        state.pole,
        last_err,
        sum_err,
    )


def draw(state: State) -> None:
    pr.clear_background(pr.BLACK)
    pr.begin_mode_2d(state.camera)

    bg_texture_ratio = state.bg_texture.width / state.bg_texture.height
    pr.draw_texture_pro(
        state.bg_texture,
        (0, 0, state.bg_texture.width, state.bg_texture.height),
        (
            -0.5 * BOARD_WIDTH * bg_texture_ratio,
            -0.5 * BOARD_HEIGHT,
            BOARD_WIDTH * bg_texture_ratio,
            BOARD_HEIGHT,
        ),
        (0, 0),
        0.0,
        pr.WHITE,
    )

    state.pole.draw()
    state.cart.draw()

    pr.end_mode_2d()
    pr.draw_fps(10, 10)
    pr.draw_text(f"{state.pole.get_angle() * RAD_TO_DEG:.01f} deg", 10, 30, 20, pr.RAYWHITE)


def control_pid(
    pole: Pole, last_err: float, sum_err: float, dt: float, desired_angle: float
) -> tuple[pr.Vector2, float, float]:
    err = desired_angle * DEG_TO_RAD - pole.get_angle()
    ierr = sum_err + err
    derr = err - last_err
    u = pr.Vector2(KP * err + KI + ierr * dt + KD * derr / dt, 0)
    return (u, err, sum_err + err)
