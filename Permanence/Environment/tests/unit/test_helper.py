from permanence_env.utils.helper import get_random_target_pos
from permanence_env.utils.constant import GRID_CELL_SIZE, TARGET_RECT_SIZE

def test_get_random_target_pos_bounds():
    """Verify generated position is within the expected target rectangle."""
    grid_x, grid_y = 5, 5
    for _ in range(100):
        pos = get_random_target_pos(grid_x, grid_y)
        min_x = grid_x * GRID_CELL_SIZE
        max_x = (grid_x + TARGET_RECT_SIZE) * GRID_CELL_SIZE
        min_y = grid_y * GRID_CELL_SIZE
        max_y = (grid_y + TARGET_RECT_SIZE) * GRID_CELL_SIZE
        
        assert min_x <= pos.x <= max_x
        assert min_y <= pos.y <= max_y
