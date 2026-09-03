import os


class Config:
    """Central configuration for the Racer environment."""

    # Screen Settings
    SCREEN_WIDTH = int(os.getenv("RACER_SCREEN_WIDTH", 512))
    SCREEN_HEIGHT = int(os.getenv("RACER_SCREEN_HEIGHT", 512))
    TARGET_FPS = int(os.getenv("RACER_TARGET_FPS", 60))

    # Game Rules
    GAME_TIMER = float(os.getenv("RACER_TIMER", 90.0))
