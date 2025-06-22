import pyray as pr
from pytmx import TiledMap

from tinyrpg.engine.game.map import Map, MapTile

RESOURCES = {
    "level1_map": "data/maps/levels/level1.tmx",
    "level1_music": "data/maps/musics/level1.wav",
    "skeleton": "data/textures/enemies/skeleton.png",
    "player": "data/textures/characters/player.png",
    "portrait-player": "data/textures/portraits/player.png",
    "grace": "data/textures/characters/grace.png",
    "portrait-grace": "data/textures/portraits/grace.png",
    "sword": "data/textures/objects/sword.png",
    "shield": "data/textures/objects/shield.png",
    "gem": "data/textures/objects/gem.png",
    "chest": "data/textures/objects/chest.png",
    "potion": "data/textures/objects/potion.png",
    "step": "data/sounds/step.wav",
    "hit": "data/sounds/hit.wav",
    "hurt": "data/sounds/hurt.wav",
    "key": "data/sounds/key.wav",
    "pick": "data/sounds/pick.wav",
    "open": "data/sounds/open.wav",
}


class CachedResources:
    maps: dict[str, Map] = {}
    textures: dict[str, pr.Texture] = {}
    musics: dict[str, pr.Music] = {}
    sounds: dict[str, pr.Sound] = {}


def load_map(name: str) -> Map:
    def image_loader(filename, colorkey, **kwargs):
        tile_texture = load_tile_texture(filename)

        def extract_image(rect, flags):
            return MapTile(tile_texture, pr.Rectangle(*rect))

        return extract_image

    value = CachedResources.maps.get(name)
    if not value:
        value = Map(TiledMap(RESOURCES[name], image_loader=image_loader, allow_duplicate_names=True))
        CachedResources.maps[name] = value
    return value


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


def load_music(name: str) -> pr.Music:
    value = CachedResources.musics.get(name)
    if not value:
        value = pr.load_music_stream(RESOURCES[name])
        CachedResources.musics[name] = value
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

    for music in CachedResources.musics.values():
        pr.unload_music_stream(music)
    CachedResources.musics.clear()

    for sound in CachedResources.sounds.values():
        pr.unload_sound(sound)
    CachedResources.sounds.clear()
