import pyray as pr

RESOURCES = {
    "title": "data/title.png",
    "spaceship": "data/spaceship.png",
}


class Resources:
    textures: dict[str, pr.Texture] = {}


def release_resources():
    for name in Resources.textures.keys():
        pr.unload_texture(Resources.textures[name])
    Resources.textures = {}


def get_texture(name: str) -> pr.Texture:
    if not Resources.textures.get(name):
        Resources.textures[name] = pr.load_texture(RESOURCES[name])
    return Resources.textures[name]
