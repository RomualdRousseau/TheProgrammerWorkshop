"""Constants defining the immutable laws of the world."""

WINDOW_WIDTH: int = 512
WINDOW_HEIGHT: int = 512
PLAYER_SIZE: int = 32
PLAYER_SPEED: float = 300.0  # max pixels per second
FRICTION_DECAY: float = 12.0  # friction damping factor
MAX_TRAIL_LENGTH: int = 6  # motion trail history count

MIN_X: float = 0.0
MAX_X: float = float(WINDOW_WIDTH - PLAYER_SIZE)  # 480.0
MIN_Y: float = 0.0
MAX_Y: float = float(WINDOW_HEIGHT - PLAYER_SIZE)  # 480.0
