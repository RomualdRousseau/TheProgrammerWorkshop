import pyray as pr

from threebody.entities.entity import Entity

G = 6.67e-8  # km3 Gt−1 s−2
SOFT = 1e7


def centrifuge_force_on_axis_y(e: Entity, w: float) -> pr.Vector3:
    u = pr.Vector3(0, w, 0)
    v = pr.vector3_normalize(pr.Vector3(e.pos.x, 0, e.pos.z))
    return pr.vector3_scale(pr.vector3_cross_product(u, v), e.mass)


def gravity_center(entities: list[Entity]) -> pr.Vector3:
    sum = pr.vector3_zero()
    for entity in entities:
        sum = pr.vector3_add(sum, entity.pos)
    return pr.vector3_scale(sum, 1.0 / len(entities))


def gravity_force(e1: Entity, e2: Entity) -> tuple[pr.Vector3, pr.Vector3]:
    v = pr.vector3_subtract(e1.pos, e2.pos)
    d = pr.vector3_length(v)
    n = pr.vector3_normalize(v)
    f = pr.vector3_scale(n, -G * e1.mass * e2.mass / (d**2 + SOFT**2))
    return f, pr.vector3_scale(f, -1)
