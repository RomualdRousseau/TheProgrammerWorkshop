from metaball.palettes import generate_fire_palette

APP_NAME = "Tutorial3 - Metaball"

WINDOW_WIDTH = 1024  # px
WINDOW_HEIGHT = 1024  # px
FRAME_RATE = 60  # fps

EPSILON = 1e-5

FIELD_WIDTH = 64  # unit
FIELD_HEIGHT = 64  # unit

METABALLS_COUNT = 5
METABALLS_PALETTE = generate_fire_palette  # or generate_hsv_palette

METABALL_RADIUS = 4  # unit
METABALL_SPEED = 50  # unit.s-1
