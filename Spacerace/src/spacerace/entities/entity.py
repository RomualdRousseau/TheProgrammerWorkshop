from typing import Protocol

import pyray as pr


class Entity(Protocol):
    def get_collision_box(self) -> tuple[float, float, float, float]: ...

    def update(self, dt: float): ...

    def draw(self): ...

    def collide(self): ...


def check_collisions(entities: list[Entity]):
    for i in range(len(entities) - 1):
        entity1 = entities[i]
        for j in range(i + 1, len(entities)):
            entity2 = entities[j]
            if pr.check_collision_recs(entity1.get_collision_box(), entity2.get_collision_box()):
                entity1.collide()
                entity2.collide()
