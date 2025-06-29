import pyray as pr

from tinyrpg.engine.base.resources import load_sound


def play_sound(name: str):
    sound = load_sound(f"sound-{name}")
    if not pr.is_sound_playing(sound):
        pr.play_sound(sound)


def stop_sound(name: str):
    pr.stop_sound(load_sound(f"sound-{name}"))
