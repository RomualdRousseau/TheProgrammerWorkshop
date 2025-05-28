import pyray as pr
from pytmx import TiledMap

from tinyrpg.utils.draw import DrawTextureCommand, emit_draw_command


class CachedTextures:
    textures: dict[str, pr.Texture] = {}


def load_tiledmap(filename: str) -> TiledMap:
    def _pyray_loader(filename, colorkey, **kwargs):
        texture = CachedTextures.textures.get(filename)
        if not texture:
            texture = pr.load_texture(filename)
            CachedTextures.textures[filename] = texture

        def extract_image(rect, flags):
            x, y, width, height = rect
            return (texture, pr.Rectangle(x, y, width, height), flags)

        return extract_image

    return TiledMap(filename, image_loader=_pyray_loader)


def unload_tiledmap(tiledmap: TiledMap) -> None:
    for texture in CachedTextures.textures.values():
        pr.unload_texture(texture)
    CachedTextures.textures.clear()


def draw_tiledmap(tiledmap: TiledMap, pos: pr.Vector2, size: pr.Vector2) -> None:
    origin = pr.vector2_zero()
    for i_layer, layer in enumerate(tiledmap.layers):
        for x, y, (texture, source, _) in layer.tiles():
            dest = pr.Rectangle((pos.x + x) * size.x, (pos.y + y) * size.y, size.x, size.y)
            emit_draw_command(DrawTextureCommand(i_layer, 1.0, texture, source, dest, origin, 0.0))
