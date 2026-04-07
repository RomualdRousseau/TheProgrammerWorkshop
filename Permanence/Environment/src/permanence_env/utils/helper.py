import random
import pyray as pr
from permanence_env.utils.constant import GRID_CELL_SIZE, TARGET_RECT_SIZE


def get_random_target_pos(rect_grid_x: int, rect_grid_y: int) -> pr.Vector2:
    """Generate a random target position within a grid rectangle."""
    return pr.Vector2(
        (rect_grid_x + random.uniform(0, TARGET_RECT_SIZE)) * GRID_CELL_SIZE,
        (rect_grid_y + random.uniform(0, TARGET_RECT_SIZE)) * GRID_CELL_SIZE,
    )
