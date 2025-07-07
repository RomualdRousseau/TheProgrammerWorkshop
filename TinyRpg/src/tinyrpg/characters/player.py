import pyray as pr

from tinyrpg.characters.rules import Rules
from tinyrpg.constants import INPUT_ATTACK
from tinyrpg.engine import (
    CHARACTER_NO_RESET_MASK,
    CHARACTER_SIZE,
    Animation,
    AnimationFlag,
    Character,
    CharacterAction,
    CharacterStats,
    EquipmentType,
    get_player_inventory,
    is_action_down,
)

HERO_ANIMATIONS = lambda: {
    "Idle": Animation(pr.Vector2(0, 0), CHARACTER_SIZE, 6, 3),
    "WalkUp": Animation(pr.Vector2(0, 5), CHARACTER_SIZE, 6, 5),
    "WalkDown": Animation(pr.Vector2(0, 3), CHARACTER_SIZE, 6, 5),
    "WalkLeft": Animation(pr.Vector2(0, 4), CHARACTER_SIZE, 6, 5, AnimationFlag.MIRROR_X),
    "WalkRight": Animation(pr.Vector2(0, 4), CHARACTER_SIZE, 6, 5),
    "AttackUp": Animation(pr.Vector2(0, 8), CHARACTER_SIZE, 4, 5),
    "AttackDown": Animation(pr.Vector2(0, 6), CHARACTER_SIZE, 4, 5),
    "AttackLeft": Animation(pr.Vector2(0, 7), CHARACTER_SIZE, 4, 5, AnimationFlag.MIRROR_X),
    "AttackRight": Animation(pr.Vector2(0, 7), CHARACTER_SIZE, 4, 5),
    "Die": Animation(pr.Vector2(0, 9), CHARACTER_SIZE, 4, 5, AnimationFlag.NONE, False),
}

HERO_STATS = lambda: CharacterStats(
    speed=20,  # pixel * s-1
    attack_speed=0.5,  # s
    damage=1,
    armor=0,
    hp=5,
)


class Player(Character):
    def __init__(self, name: str, pos: pr.Vector2, boundary: pr.BoundingBox):
        super().__init__("player", name, pos, HERO_STATS(), HERO_ANIMATIONS(), boundary, Rules())
        self.inventory = get_player_inventory()

    def handle_ai(self) -> None:
        assert self.inventory is not None, "Inventory must exist"

        super().handle_ai()

        if is_action_down("UP"):
            self.dir.y = -1
            self.speed = self.stats.speed
            self.actions = (self.actions & CHARACTER_NO_RESET_MASK) | CharacterAction.WALKING
        elif is_action_down("DOWN"):
            self.dir.y = 1
            self.speed = self.stats.speed
            self.actions = (self.actions & CHARACTER_NO_RESET_MASK) | CharacterAction.WALKING
        if is_action_down("LEFT"):
            self.dir.x = -1
            self.speed = self.stats.speed
            self.actions = (self.actions & CHARACTER_NO_RESET_MASK) | CharacterAction.WALKING
        elif is_action_down("RIGHT"):
            self.dir.x = 1
            self.speed = self.stats.speed
            self.actions = (self.actions & CHARACTER_NO_RESET_MASK) | CharacterAction.WALKING
        if is_action_down(INPUT_ATTACK) and self.inventory.is_equiped_with(EquipmentType.WEAPON):
            self.speed = 0
            self.actions = (self.actions & CHARACTER_NO_RESET_MASK) | CharacterAction.ATTACKING

    def reload_resources(self):
        super().reload_resources()
        self.inventory = get_player_inventory()
