import pyray as pr

RESOURCES = {
    "title": "data/title.png",
    "spaceship": "data/spaceship.png",
    "explosion": "data/explosion.wav",
}


class Resources:
    textures: dict[str, pr.Texture] = {}
    sounds: dict[str, pr.Sound] = {}


def release_resources():
    for name in Resources.textures.keys():
        pr.unload_texture(Resources.textures[name])
    Resources.textures = {}

    for name in Resources.sounds.keys():
        pr.unload_sound(Resources.sounds[name])
    Resources.sounds = {}


def get_texture(name: str) -> pr.Texture:
    if not Resources.textures.get(name):
        Resources.textures[name] = pr.load_texture(RESOURCES[name])
    return Resources.textures[name]


def get_sound(name: str) -> pr.Sound:
    if not Resources.sounds.get(name):
        Resources.sounds[name] = pr.load_sound(RESOURCES[name])
    return Resources.sounds[name]
