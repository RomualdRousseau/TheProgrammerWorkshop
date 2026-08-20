"""Story 1 smoke tests: package skeleton and render harness invariants.

Headless: these tests must never open a window.
"""

from spacerace.core import constant
from spacerace.engine import config


def test_logical_screen_is_256_square() -> None:
    assert constant.SCREEN_SIZE == 256


def test_window_is_integer_upscale_of_world() -> None:
    assert config.WINDOW_SIZE == constant.SCREEN_SIZE * constant.SCALE


def test_entry_point_is_callable() -> None:
    from spacerace.main import run

    assert callable(run)
