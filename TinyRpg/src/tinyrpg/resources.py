import pyray as pr
from pytmx import TiledMap

RESOURCES = {
    "level1": "data/maps/levels/level1.tmx",
    "player": "data/textures/player.png",
    "chop": "data/sounds/chop.wav",
    "step": "data/sounds/step.wav",
}


class CachedResources:
    maps: dict[str, TiledMap] = {}
    textures: dict[str, pr.Texture] = {}
    sounds: dict[str, pr.Sound] = {}


def load_tile_texture(name: str) -> pr.Texture:
    value = CachedResources.textures.get(name)
    if not value:
        value = pr.load_texture(name)
        CachedResources.textures[name] = value
    return value


def load_texture(name: str) -> pr.Texture:
    value = CachedResources.textures.get(name)
    if not value:
        value = pr.load_texture(RESOURCES[name])
        CachedResources.textures[name] = value
    return value


def load_sound(name: str) -> pr.Sound:
    value = CachedResources.sounds.get(name)
    if not value:
        value = pr.load_sound(RESOURCES[name])
        CachedResources.sounds[name] = value
    return value


def unload_resources():
    CachedResources.maps.clear()

    for texture in CachedResources.textures.values():
        pr.unload_texture(texture)
    CachedResources.textures.clear()

    for sound in CachedResources.sounds.values():
        pr.unload_sound(sound)
    CachedResources.sounds.clear()
