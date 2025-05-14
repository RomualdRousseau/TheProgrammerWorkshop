import pyray as pr


RESOURCES = {
    "hero": (lambda: pr.load_texture("data/textures/hero.png"), pr.unload_texture)
}


class Resources:
    cache: dict[str, pr.Texture] = {}


def load_resource(name: str) -> pr.Texture:
    value = Resources.cache.get(name)
    if not value:
        load_func, _ = RESOURCES[name]
        value = load_func()
        Resources.cache[name] = value
    return value


def unload_resources():
    for name in Resources.cache.keys():
        _, unload_func = RESOURCES[name]
        value = Resources.cache[name]
        unload_func(value)
    Resources.cache.clear()
