"""Raylib-backed audio engine: generates ship engine beeps from a high-level state.

Audio is best-effort: if the audio device cannot be initialized (e.g. headless
or no sound hardware), the game continues silently.
"""

from __future__ import annotations

import math

import pyray as pr

from spacerace.core.state import AudioState
from spacerace.engine import config

_stream: pr.AudioStream | None = None
_p1_phase: float = 0.0
_p2_phase: float = 0.0


def init() -> None:
    """Initialize the audio device and streaming buffer."""
    global _stream
    pr.init_audio_device()
    if not pr.is_audio_device_ready():
        return
    _stream = pr.load_audio_stream(config.AUDIO_SAMPLE_RATE, 16, 2)
    pr.play_audio_stream(_stream)


def close() -> None:
    """Release the audio stream and device."""
    global _stream
    if _stream is not None:
        pr.unload_audio_stream(_stream)
        _stream = None
    if pr.is_audio_device_ready():
        pr.close_audio_device()


def update(state: AudioState) -> None:
    """Feed the audio stream with the next chunk of generated samples."""
    if _stream is None or not pr.is_audio_stream_processed(_stream):
        return
    samples = _generate_samples(state, config.AUDIO_CHUNK_FRAMES)
    buffer = pr.ffi.new("short[]", samples)
    pr.update_audio_stream(_stream, buffer, config.AUDIO_CHUNK_FRAMES)


def _generate_samples(state: AudioState, frames: int) -> list[int]:
    """Generate a stereo int16 buffer from the current audio state."""
    global _p1_phase, _p2_phase
    max_int16 = 32767
    samples: list[int] = []
    p1_freq = _progress_to_freq(state.p1_progress, config.P1_BASE_FREQ)
    p2_freq = _progress_to_freq(state.p2_progress, config.P2_BASE_FREQ)

    for _ in range(frames):
        p1_sample = 0.0
        p2_sample = 0.0
        if p1_freq is not None:
            _p1_phase = (_p1_phase + p1_freq / config.AUDIO_SAMPLE_RATE) % 1.0
            p1_sample = math.sin(_p1_phase * 2.0 * math.pi)
        if p2_freq is not None:
            _p2_phase = (_p2_phase + p2_freq / config.AUDIO_SAMPLE_RATE) % 1.0
            p2_sample = math.sin(_p2_phase * 2.0 * math.pi)

        left = config.AUDIO_AMPLITUDE * (p1_sample * 0.8 + p2_sample * 0.2)
        right = config.AUDIO_AMPLITUDE * (p1_sample * 0.2 + p2_sample * 0.8)
        samples.append(int(max(-1.0, min(1.0, left)) * max_int16))
        samples.append(int(max(-1.0, min(1.0, right)) * max_int16))

    return samples


def _progress_to_freq(progress: float | None, base_freq: float) -> float | None:
    """Map ascent progress to frequency; ``None`` means silent."""
    if progress is None:
        return None
    return base_freq * (2.0 ** (config.PITCH_RANGE_OCTAVES * progress))
