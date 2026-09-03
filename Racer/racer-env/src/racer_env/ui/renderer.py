import pyray as pr

from racer_env.game.state import GameState


def draw_start_scene() -> None:
    """Render the start screen."""
    pr.clear_background(pr.BLACK)
    pr.draw_text("RACER RL", 120, 150, 60, pr.RAYWHITE)
    pr.draw_text("Press SPACE to Start", 150, 250, 20, pr.GREEN)
    pr.draw_text("Controls: LEFT/RIGHT arrows", 140, 450, 15, pr.GRAY)


def draw_game_scene(state: GameState) -> None:
    """Render the game world during active play."""
    # Clear background
    pr.clear_background(pr.BLACK)

    # Draw Player (White rectangle)
    pr.draw_rectangle_rec(state.player.rect, pr.WHITE)

    # Draw Obstacles (Red rectangles for visibility)
    for obs in state.obstacles:
        pr.draw_rectangle_rec(obs.rect, pr.RED)

    # Draw HUD
    pr.draw_text(f"Score: {state.score}", 10, 10, 20, pr.GREEN)
    pr.draw_text(f"Time: {int(state.timer)}s", 10, 35, 20, pr.RAYWHITE)


def draw_game_over_scene(state: GameState) -> None:
    """Render the game over screen (Win or Loss)."""
    pr.clear_background(pr.BLACK)

    if state.game_over:
        pr.draw_text("GAME OVER!", 150, 200, 40, pr.RED)
    elif state.won:
        pr.draw_text("YOU WIN!", 170, 200, 40, pr.GOLD)

    pr.draw_text(f"Final Score: {state.score}", 180, 280, 20, pr.RAYWHITE)
    pr.draw_text("Press SPACE to restart", 140, 350, 20, pr.GRAY)
