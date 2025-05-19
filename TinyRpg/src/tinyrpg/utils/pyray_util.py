import pyray as pr
from pytmx import TiledMap


class CachedImages:
    textures: dict[str, pr.Texture] = {}


def load_tiledmap(filename: str) -> TiledMap:
    return TiledMap(filename, image_loader=_pyray_loader)


def unload_tiledmap(tiledmap: TiledMap) -> None:
    for texture in CachedImages.textures.values():
        pr.unload_texture(texture)


def draw_tiledmap(tiledmap: TiledMap, pos: pr.Vector2, size: pr.Vector2) -> None:
    for layer in tiledmap.layers:
        for x, y, (texture, source, _) in layer.tiles():
            pr.draw_texture_pro(
                texture,
                source,
                ((pos.x + x) * size.x, (pos.y + y) * size.y, size.x, size.y),
                (0, 0),
                0,
                pr.WHITE,
            )


def _pyray_loader(filename, colorkey, **kwargs):
    texture = CachedImages.textures.get(filename)
    if not texture:
        texture = pr.load_texture(filename)
        CachedImages.textures[filename] = texture

    def extract_image(rect, flags):
        x, y, width, height = rect
        return (texture, pr.Rectangle(x, y, width, height), flags)

    return extract_image
