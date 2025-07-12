import struct
import wave

import numpy as np

from spacerace import AUDIO_SAMPLE_RATE, AUDIO_VOLUME


def create_wav(filename, samples: np.ndarray, sample_rate: float = AUDIO_SAMPLE_RATE):
    with wave.open(filename, "w") as wav_file:
        wav_file.setparams((1, 2, int(sample_rate), len(samples), "NONE", "not compressed"))
        for sample in samples:
            wav_file.writeframes(struct.pack("<h", sample))  # '<h' is little-endian 16-bit signed int


def generate_sin_wave(
    freq: float, frames: int, vol: float = AUDIO_VOLUME, sample_rate: float = AUDIO_SAMPLE_RATE
) -> np.ndarray:
    time = np.linspace(0, frames / sample_rate, frames)
    sinwave = 32000.0 * vol * np.sin(2.0 * np.pi * freq * time)
    return np.array(sinwave, dtype=np.int16)


def generate_ranged_sin_wave(
    freq1: float, freq2: float, frames: int, vol: float = AUDIO_VOLUME, sample_rate: float = AUDIO_SAMPLE_RATE
) -> np.ndarray:
    time = np.linspace(0, frames / sample_rate, frames)
    freq = np.geomspace(freq1, freq2, frames)
    sinwave = 32000.0 * vol * np.sin(2.0 * np.pi * freq * time)
    return np.array(sinwave, dtype=np.int16)


def generate_square_wave(
    freq: float, frames: int, vol: float = AUDIO_VOLUME, sample_rate: float = AUDIO_SAMPLE_RATE
) -> np.ndarray:
    sinwave = generate_sin_wave(freq, frames, vol, sample_rate)
    return np.array(np.where(sinwave >= 0, -32000.0 * vol, 32000.0 * vol), dtype=np.int16)


def generate_ranged_square_wave(
    freq1: float,
    freq2: float,
    frames: int,
    vol: float = AUDIO_VOLUME,
    sample_rate: float = AUDIO_SAMPLE_RATE,
) -> np.ndarray:
    sinwave = generate_ranged_sin_wave(freq1, freq2, frames, vol, sample_rate)
    return np.array(np.where(sinwave >= 0, -32000.0 * vol, 32000.0 * vol), dtype=np.int16)
