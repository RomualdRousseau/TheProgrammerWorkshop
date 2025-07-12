import pyray as pr
from pytmx import TiledMap

from tinyrpg.engine.base.database import get_database
from tinyrpg.engine.game.map import Map, MapTile


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
        file_path = get_database().select_dict("resources")["maps"][name]
        value = Map(TiledMap(file_path, image_loader=image_loader, allow_duplicate_names=True))
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
        file_path = get_database().select_dict("resources")["textures"][name]
        value = pr.load_texture(file_path)
        CachedResources.textures[name] = value
    return value


def load_music(name: str) -> pr.Music:
    value = CachedResources.musics.get(name)
    if not value:
        file_path = get_database().select_dict("resources")["musics"][name]
        value = pr.load_music_stream(file_path)
        CachedResources.musics[name] = value
    return value


def load_sound(name: str) -> pr.Sound:
    value = CachedResources.sounds.get(name)
    if not value:
        file_path = get_database().select_dict("resources")["sounds"][name]
        value = pr.load_sound(file_path)
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
