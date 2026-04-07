"""
Configuration management for the application.

Loads settings from environment variables with sensible defaults.
"""

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    """
    Application configuration parameters.
    """

    target_fps: int = field(default_factory=lambda: int(os.getenv("TARGET_FPS", "60")))


config = Config()
