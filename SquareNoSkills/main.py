"""
Green Square Game using Raylib in Python.

Specifications:
- 512x512 window with a black background.
- Green square of size 32x32 pixels.
- Controlled via arrow keys with smooth movement.
- Square is strictly clamped to the 512x512 window area.
- Runs at 60 FPS.
- Closes on window close button or Escape key.
"""

import pyray as rl

# Constants for screen dimensions and game settings
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
SQUARE_SIZE = 32
MOVEMENT_SPEED = 300.0  # Pixels per second for smooth movement


def main() -> None:
    # Initialize game window (512x512 pixels)
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Green Square - Raylib Game")

    # Target frame rate: 60 FPS
    rl.set_target_fps(60)

    # Center the square initially in the window
    square_x = float((SCREEN_WIDTH - SQUARE_SIZE) // 2)
    square_y = float((SCREEN_HEIGHT - SQUARE_SIZE) // 2)

    # Main game loop (runs until close button or ESC is pressed)
    while not rl.window_should_close():
        # Get frame delta time in seconds for frame-rate independent smooth movement
        delta_time = rl.get_frame_time()

        # Handle arrow key movement controls
        if rl.is_key_down(rl.KEY_LEFT):
            square_x -= MOVEMENT_SPEED * delta_time
        if rl.is_key_down(rl.KEY_RIGHT):
            square_x += MOVEMENT_SPEED * delta_time
        if rl.is_key_down(rl.KEY_UP):
            square_y -= MOVEMENT_SPEED * delta_time
        if rl.is_key_down(rl.KEY_DOWN):
            square_y += MOVEMENT_SPEED * delta_time

        # Keep the square strictly within the window boundaries
        max_x = float(SCREEN_WIDTH - SQUARE_SIZE)
        max_y = float(SCREEN_HEIGHT - SQUARE_SIZE)
        square_x = max(0.0, min(square_x, max_x))
        square_y = max(0.0, min(square_y, max_y))

        # Begin rendering
        rl.begin_drawing()

        # Fill background with black color
        rl.clear_background(rl.BLACK)

        # Draw the green square (32x32 pixels)
        rl.draw_rectangle(
            int(square_x),
            int(square_y),
            SQUARE_SIZE,
            SQUARE_SIZE,
            rl.GREEN
        )

        # End rendering frame
        rl.end_drawing()

    # Close raylib window and cleanup resources
    rl.close_window()


if __name__ == "__main__":
    main()
