import numpy as np
import pyray as pr


def generate_hsv_palette() -> np.ndarray:
    palette = [color_to_tuple(pr.color_from_hsv(x, 1.0, 1.0)) for x in np.linspace(0, 360, 256)]
    return np.array(palette, dtype=np.uint8)


def generate_fire_palette():
    # Define the fire palette using RGB values
    palette = [
        (0, 0, 0, 255),  # Black
        (255, 0, 0, 255),  # Red
        (255, 165, 0, 255),  # Orange
        (255, 255, 0, 255),  # Yellow
        (255, 255, 255, 255),  # White
    ]

    # Interpolate the palette to get smooth transitions
    colors = np.array(palette, dtype=np.uint8)
    x = np.linspace(0, 1, len(colors))
    xp = np.linspace(0, 1, 256)
    fire_colors = np.zeros((256, 4), dtype=np.uint8)
    for i in range(4):
        fire_colors[:, i] = np.interp(xp, x, colors[:, i])
    return fire_colors


def color_to_tuple(color: pr.Color) -> tuple[int, int, int, int]:
    return (int(color.r), int(color.g), int(color.b), 255)
