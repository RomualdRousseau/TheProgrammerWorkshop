"""Deployment & hardware settings. Only the engine layer may import this module."""

from pathlib import Path

WINDOW_SIZE: int = 512  # physical window size in pixels (square)
FPS: int = 60
WINDOW_TITLE: str = "Space Race"
ASSET_DIR: Path = Path(__file__).resolve().parents[3] / "assets"

# Audio settings
AUDIO_SAMPLE_RATE: int = 44100
AUDIO_CHUNK_FRAMES: int = 1024
P1_BASE_FREQ: float = 220.0  # A3
P2_BASE_FREQ: float = 330.0  # E4
PITCH_RANGE_OCTAVES: float = 1.0  # freq at progress 1.0 = base * 2
AUDIO_AMPLITUDE: float = 0.1
