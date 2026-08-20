"""Raylib-backed audio engine: generates ship engine tones from a high-level state.

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
_p1_freq: float = 0.0
_p2_freq: float = 0.0
_p1_amp: float = 0.0
_p2_amp: float = 0.0


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
    """Generate a stereo int16 buffer with smooth, continuous sine tones."""
    global _p1_phase, _p2_phase, _p1_freq, _p2_freq, _p1_amp, _p2_amp
    max_int16 = 32767
    samples: list[int] = []

    p1_target_freq = _progress_to_freq(state.p1_progress, config.P1_BASE_FREQ)
    p2_target_freq = _progress_to_freq(state.p2_progress, config.P2_BASE_FREQ)
    p1_target_amp = 1.0 if state.p1_progress is not None else 0.0
    p2_target_amp = 1.0 if state.p2_progress is not None else 0.0

    # Fade from 0 to full amplitude over 1 ms to avoid clicks.
    fade_step = 1.0 / (0.001 * config.AUDIO_SAMPLE_RATE)

    for i in range(frames):
        t = i / frames
        freq1 = _p1_freq + (p1_target_freq - _p1_freq) * t
        freq2 = _p2_freq + (p2_target_freq - _p2_freq) * t

        _p1_phase = (_p1_phase + freq1 / config.AUDIO_SAMPLE_RATE) % 1.0
        _p2_phase = (_p2_phase + freq2 / config.AUDIO_SAMPLE_RATE) % 1.0

        _p1_amp = _move_toward(_p1_amp, p1_target_amp, fade_step)
        _p2_amp = _move_toward(_p2_amp, p2_target_amp, fade_step)

        p1_sample = math.sin(_p1_phase * 2.0 * math.pi) * _p1_amp
        p2_sample = math.sin(_p2_phase * 2.0 * math.pi) * _p2_amp

        left = config.AUDIO_AMPLITUDE * (p1_sample * 0.8 + p2_sample * 0.2)
        right = config.AUDIO_AMPLITUDE * (p1_sample * 0.2 + p2_sample * 0.8)
        samples.append(int(max(-1.0, min(1.0, left)) * max_int16))
        samples.append(int(max(-1.0, min(1.0, right)) * max_int16))

    _p1_freq = p1_target_freq
    _p2_freq = p2_target_freq
    return samples


def _progress_to_freq(progress: float | None, base_freq: float) -> float:
    """Map ascent progress to frequency; silent progress maps to 0 Hz."""
    if progress is None:
        return 0.0
    return base_freq * (2.0 ** (config.PITCH_RANGE_OCTAVES * progress))


def _move_toward(current: float, target: float, step: float) -> float:
    """Move ``current`` toward ``target`` by at most ``step``."""
    if current < target:
        return min(current + step, target)
    return max(current - step, target)
