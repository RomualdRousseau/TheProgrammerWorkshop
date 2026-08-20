"""Deployment & hardware settings. Only the engine layer may import this module."""

from pathlib import Path

WINDOW_SIZE: int = 512  # physical window size in pixels (square)
FPS: int = 60
WINDOW_TITLE: str = "Space Race"
ASSET_DIR: Path = Path(__file__).resolve().parents[3] / "assets"
