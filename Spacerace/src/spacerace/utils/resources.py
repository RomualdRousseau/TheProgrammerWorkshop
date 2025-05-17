from genericpath import exists

import pyray as pr

from spacerace import AUDIO_SAMPLE_RATE, AUDIO_VOLUME, GAME_TIMEOUT
from spacerace.utils.audio import create_wav, generate_ranged_square_wave, generate_square_wave

RESOURCES = {
    "title": "data/title.png",
    "spaceship": "data/spaceship.png",
    "explosion": "data/explosion.wav",
    "theme": "data/theme.wav",
}


class Resources:
    textures: dict[str, pr.Texture] = {}
    musics: dict[str, pr.Music] = {}
    sounds: dict[str, pr.Sound] = {}


def generate_resources():
    if not exists("data/explosion.wav"):
        pr.trace_log(pr.TraceLogLevel.LOG_INFO, "AUDIO: Generate data/explosion.wav")
        explosion = generate_square_wave(440, int(AUDIO_SAMPLE_RATE * 0.1), vol=AUDIO_VOLUME * 5)
        create_wav("data/explosion.wav", explosion)

    if not exists("data/theme.wav"):
        pr.trace_log(pr.TraceLogLevel.LOG_INFO, "AUDIO: Generate data/theme.wav")
        theme = generate_ranged_square_wave(440, 880, int(AUDIO_SAMPLE_RATE * GAME_TIMEOUT), vol=AUDIO_VOLUME)
        create_wav("data/theme.wav", theme)


def release_resources():
    for name in Resources.textures.keys():
        pr.unload_texture(Resources.textures[name])
    Resources.textures = {}

    for name in Resources.musics.keys():
        pr.unload_music_stream(Resources.musics[name])
    Resources.musics = {}

    for name in Resources.sounds.keys():
        pr.unload_sound(Resources.sounds[name])
    Resources.sounds = {}


def get_texture(name: str) -> pr.Texture:
    if not Resources.textures.get(name):
        Resources.textures[name] = pr.load_texture(RESOURCES[name])
    return Resources.textures[name]


def get_music(name: str) -> pr.Music:
    if not Resources.musics.get(name):
        Resources.musics[name] = pr.load_music_stream(RESOURCES[name])
    return Resources.musics[name]


def get_sound(name: str) -> pr.Sound:
    if not Resources.sounds.get(name):
        Resources.sounds[name] = pr.load_sound(RESOURCES[name])
    return Resources.sounds[name]
