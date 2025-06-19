from dataclasses import dataclass, field
from functools import cache
from typing import Optional


@dataclass
class Item:
    name: str
    hand: str
    damage: int
    armor: int


@dataclass
class Inventory:
    right_hand: Optional[Item] = None
    left_hand: Optional[Item] = None
    bag: list[Item] = field(default_factory=list)


@cache
def get_inventory() -> Inventory:
    return Inventory()
