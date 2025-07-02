import io
import os
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Optional

from tinyrpg.engine.base.database import get_database
from tinyrpg.engine.utils.pickle import DBPickler, DBUnpickler


class EquipmentType(Enum):
    WEAPON = 0
    CLOTHE = 1
    SHIELD = 2
    CONSUMABLE = 3


@dataclass
class Item:
    name: str
    slot: int
    texture: str
    damage: int
    armor: int
    cost: int
    description: str


class Inventory:
    def __init__(self):
        self.equipment: list[Optional[Item]] = [None] * 3
        self.bag: list[Optional[Item]] = [None] * 9
        self.coin: int = 0

    def is_equiped_with(self, type: EquipmentType) -> bool:
        slot = type.value
        return self.equipment[slot] is not None

    def get_equipment(self, type: EquipmentType) -> Optional[Item]:
        slot = type.value
        return self.equipment[slot]

    def index(self, item: Item) -> int:
        return item in self.bag

    def append(self, item_to_append: Item) -> int:
        free_slot = -1
        for slot, item in enumerate(self.bag):
            if item is None:
                free_slot = slot
                break
        if free_slot >= 0:
            self.bag[free_slot] = item_to_append
        return free_slot

    def drop(self, slot: int) -> Optional[Item]:
        item_to_drop = self.bag[slot]
        self.bag[slot] = None
        return item_to_drop

    def equip(self, slot: int) -> Optional[Item]:
        item_to_equip = self.bag[slot]
        if item_to_equip and item_to_equip.slot != EquipmentType.CONSUMABLE.value:
            self.equipment[item_to_equip.slot] = item_to_equip
            self.bag[slot] = None
        return item_to_equip

    def unequip(self, slot: int) -> Optional[Item]:
        item_to_unequip = self.equipment[slot]
        if item_to_unequip:
            self.equipment[slot] = None
            self.append(item_to_unequip)
        return item_to_unequip

    def save(self, character_name: str):
        file_data = io.BytesIO()
        DBPickler(file_data).dump(self)
        with open(f"saved/inventory_{character_name}.pkl", "wb") as fp:
            fp.write(file_data.getvalue())


@cache
def get_player_inventory(player_name: str) -> Inventory:
    path = f"saved/inventory_{player_name}.pkl"
    if not os.path.exists(path):
        inventory = Inventory()
    else:
        with open(path, "rb") as fp:
            file_data = io.BytesIO(fp.read())
        inventory = DBUnpickler(file_data).load()
    return inventory


@cache
def get_inventory_item(name: str) -> Item:
    return Item(*get_database().select_dict("items")[name])
