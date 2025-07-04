import io
import os

from tinyrpg.engine import PRPickler, PRUnpickler, Scene, get_player_inventory
from tinyrpg.scenes.game import Game as Game


def save_state(file_path: str, states: dict[str, Scene]):
    game_state = {}

    inventory = get_player_inventory()
    game_state["inventory"] = inventory.save_state()

    for key, scene in states.items():
        game_state[key] = scene.save_state()

    with open(file_path, "wb") as fp:
        file_data = io.BytesIO()
        PRPickler(file_data).dump(game_state)
        fp.write(file_data.getvalue())


def load_state(file_path: str, states: dict[str, Scene]):
    if not os.path.exists(file_path):
        return

    with open(file_path, "rb") as fp:
        file_data = io.BytesIO(fp.read())
        game_state = PRUnpickler(file_data).load()

    inventory = get_player_inventory()
    inventory.restore_state(game_state["inventory"])

    for key, scene in states.items():
        scene.restore_state(game_state[key])
