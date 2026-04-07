from raylib import *


def main():
    # Window initialization
    init_window(800, 450, b"Raylib Python - Functional Template")
    set_target_fps(60)

    # State initialization (using dictionaries or dataclasses)
    player = {"pos": [400, 225], "color": RAYWHITE}

    # Main loop
    while not window_should_close():
        # Input/Update (Logic)
        if is_key_down(KEY_RIGHT):
            player["pos"][0] += 2
        if is_key_down(KEY_LEFT):
            player["pos"][0] -= 2
        if is_key_down(KEY_UP):
            player["pos"][1] -= 2
        if is_key_down(KEY_DOWN):
            player["pos"][1] += 2

        # Drawing (Rendering)
        begin_drawing()
        clear_background(BLACK)

        draw_text(b"Move with arrows!", 10, 10, 20, DARKGRAY)
        draw_circle_v(player["pos"], 20, player["color"])

        end_drawing()

    close_window()


if __name__ == "__main__":
    main()
