"""Laws of the world: immutable constants of the Space Race universe."""

SCREEN_SIZE: int = 256  # logical playfield size in pixels (square)
SCALE: int = 2  # integer upscale factor from logical screen to window

PLAYER_SPEED: float = 120.0  # vertical rocket speed in pixels per second
PLAYER_WIDTH: int = 16  # rocket sprite footprint in logical pixels
PLAYER_HEIGHT: int = 18

P1_START_X: float = 56.0  # player 1 lane, left half of the field
P2_START_X: float = 184.0  # player 2 lane, right half of the field
START_Y: float = 224.0  # both rockets launch from the bottom row

RESPAWN_DELAY: float = 0.5  # seconds a rocket stays hidden after a hit
GOAL_ROW: int = 0  # reaching this y row (top) awards a point
MATCH_DURATION: float = 60.0  # seconds per match
TITLE_INACTIVITY_TIMEOUT: float = 15.0  # seconds before title enters demo (Story 8)

# Asteroid layout
SAFE_ZONE_HEIGHT: int = 48  # top and bottom safe rows in logical pixels
ASTEROID_COUNT: int = 20  # number of small asteroids on screen
ASTEROID_WIDTH: int = 2
ASTEROID_HEIGHT: int = 1
ASTEROID_SPEED_MIN: float = 30.0  # pixels per second
ASTEROID_SPEED_MAX: float = 90.0  # pixels per second
