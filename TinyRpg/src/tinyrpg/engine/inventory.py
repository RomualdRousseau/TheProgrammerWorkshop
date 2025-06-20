from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EquipmentSlot(Enum):
    WEAPON = 0
    NECK = 1
    SHIELD = 2
    NONE = 3


@dataclass
class Item:
    name: str
    slot: int
    texture: str
    damage: int
    armor: int
    description: str


@dataclass
class Inventory:
    equipment: list[Optional[Item]] = field(default_factory=lambda: [None] * 3)
    bag: list[Optional[Item]] = field(default_factory=lambda: [None] * 9)
    coin: int = 0

    def append(self, item_to_put: Item) -> int:
        free_slot = -1
        for slot, item in enumerate(self.bag):
            if item is None:
                free_slot = slot
                break
        if free_slot >= 0:
            self.bag[free_slot] = item_to_put
        return free_slot

    def remove(self, slot: int) -> Optional[Item]:
        item = self.bag[slot]
        self.bag[slot] = None
        return item

    def equip(self, slot: int):
        item = self.bag[slot]
        if item and item.slot != EquipmentSlot.NONE.value:
            self.equipment[item.slot] = item
            self.bag[slot] = None

    def unequip(self, slot: int):
        item = self.equipment[slot]
        if item:
            self.equipment[slot] = None
            self.append(item)
