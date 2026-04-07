"""
Rendering logic and visual components.
"""

import pyray as pr
import pytmx

from permanence_env.game.state import GameState
from permanence_env.utils.constant import (
    GRID_CELL_SIZE,
    GRID_OFFSET_X,
    GRID_OFFSET_Y,
    GRID_SIZE,
    TARGET_RECT_SIZE,
)
from permanence_env.utils.loader import get_tile_texture, load_tmx_map

# Load map (path assumed for now, ideally managed in config)
# NOTE: This assumes 'assets/tilemaps/room.tmx' exists.
game_map = load_tmx_map("assets/tilemaps/room.tmx")


def draw_grid() -> None:
    """
    Draw the NxN grid background inside borders.
    """
    grid_px_size = GRID_SIZE * GRID_CELL_SIZE

    for i in range(GRID_SIZE + 1):
        # Vertical lines
        x = GRID_OFFSET_X + i * GRID_CELL_SIZE
        pr.draw_line(x, GRID_OFFSET_Y, x, GRID_OFFSET_Y + grid_px_size, pr.LIGHTGRAY)

        # Horizontal lines
        y = GRID_OFFSET_Y + i * GRID_CELL_SIZE
        pr.draw_line(GRID_OFFSET_X, y, GRID_OFFSET_X + grid_px_size, y, pr.LIGHTGRAY)


def draw_game(state: GameState) -> None:
    """
    Draw the game state using two-layer rendering.
    """
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)

    # 1) Layer 1 (Background): Grid, highlights, and rectangle
    draw_grid()

    # Highlight ball cell
    ball_grid_x = int(state.ball.pos.x // GRID_CELL_SIZE)
    ball_grid_y = int(state.ball.pos.y // GRID_CELL_SIZE)
    pr.draw_rectangle(
        GRID_OFFSET_X + ball_grid_x * GRID_CELL_SIZE,
        GRID_OFFSET_Y + ball_grid_y * GRID_CELL_SIZE,
        GRID_CELL_SIZE,
        GRID_CELL_SIZE,
        pr.fade(pr.BLUE, 0.2),
    )

    # Highlight target cell
    target_grid_x = int(state.target.wp1_pos.x // GRID_CELL_SIZE)
    target_grid_y = int(state.target.wp1_pos.y // GRID_CELL_SIZE)
    pr.draw_rectangle(
        GRID_OFFSET_X + target_grid_x * GRID_CELL_SIZE,
        GRID_OFFSET_Y + target_grid_y * GRID_CELL_SIZE,
        GRID_CELL_SIZE,
        GRID_CELL_SIZE,
        pr.fade(pr.GREEN, 0.2),
    )

    # Calculate rectangle screen position
    rect_x = GRID_OFFSET_X + state.target.grid_x * GRID_CELL_SIZE
    rect_y = GRID_OFFSET_Y + state.target.grid_y * GRID_CELL_SIZE
    rect_size = TARGET_RECT_SIZE * GRID_CELL_SIZE

    # Highlight rectangle area
    pr.draw_rectangle(
        rect_x,
        rect_y,
        rect_size,
        rect_size,
        pr.fade(pr.RED, 0.2),
    )

    # 2) Layer 2 (Foreground): Ball, Target Point, Rectangle Outline, TMX Map
    if state.show_layer2:
        # Render TMX Map layers
        # Tilemap covers entire screen (0,0 to SCREEN_WIDTH, SCREEN_HEIGHT)
        for layer in game_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_data = game_map.get_tile_image_by_gid(gid)
                    if tile_data:
                        image_path, source, _ = tile_data
                        texture = get_tile_texture(image_path)
                        # TMX tiles are typically positioned at (x,y) * GRID_CELL_SIZE
                        dest = (
                            x * GRID_CELL_SIZE,
                            y * GRID_CELL_SIZE,
                            GRID_CELL_SIZE,
                            GRID_CELL_SIZE,
                        )

                        pr.draw_texture_pro(
                            texture, source, dest, pr.vector2_zero(), 0.0, pr.WHITE
                        )

        # Draw Animated Ball
        ball_texture = get_tile_texture("assets/images/ball.png")
        # Assuming 3 frames horizontally
        frame_width = ball_texture.width / 3
        ball_source = (
            state.ball.animation_frame * frame_width,
            0,
            frame_width,
            ball_texture.height,
        )
        # Center the ball on its position relative to the grid offset
        ball_dest = (
            GRID_OFFSET_X + state.ball.pos.x - frame_width / 2,
            GRID_OFFSET_Y + state.ball.pos.y - ball_texture.height / 2,
            GRID_CELL_SIZE,
            GRID_CELL_SIZE,
        )
        pr.draw_texture_pro(
            ball_texture,
            ball_source,
            ball_dest,
            pr.vector2_zero(),
            0.0,
            pr.WHITE,
        )

        # Draw table sprite
        table_texture = get_tile_texture("assets/images/table.png")
        pr.draw_texture_pro(
            table_texture,
            (0, 0, table_texture.width, table_texture.height),
            (
                rect_x - GRID_CELL_SIZE,
                rect_y - GRID_CELL_SIZE,
                rect_size + 2 * GRID_CELL_SIZE,
                rect_size + 2 * GRID_CELL_SIZE,
            ),
            pr.vector2_zero(),
            0.0,
            pr.WHITE,
        )

        # Draw Target Point
        pr.draw_circle_v(
            pr.Vector2(
                GRID_OFFSET_X + state.target.wp1_pos.x,
                GRID_OFFSET_Y + state.target.wp1_pos.y,
            ),
            3,
            pr.GREEN,
        )

    pr.end_drawing()
