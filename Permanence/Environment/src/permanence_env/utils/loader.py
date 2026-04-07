"""
Utility for loading game assets, including maps and textures.
"""

import functools

import pyray as pr
import pytmx


def load_tmx_map(map_path: str):
    """Load a TMX map file."""
    return pytmx.TiledMap(map_path)


@functools.lru_cache(maxsize=128)
def get_tile_texture(image_path: str) -> pr.Texture:
    """Load and return a texture from a tileset, cached for performance."""
    return pr.load_texture(image_path)
