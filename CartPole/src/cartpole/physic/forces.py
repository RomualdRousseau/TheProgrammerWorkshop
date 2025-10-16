import pyray as pr

from cartpole.physic.rigid_body import RigidBody

G = 9.81


def gravity_force(body: RigidBody) -> pr.Vector2:
    return pr.Vector2(0, body.mass * G)


def friction_force(body: RigidBody, coef: float) -> pr.Vector2:
    return pr.vector2_scale(body.vel, -coef)


def spring_force(body: RigidBody, point: pr.Vector2, length: float, coef: float) -> pr.Vector2:
    v = pr.vector2_subtract(body.pos, point)
    return pr.vector2_scale(pr.vector2_normalize(v), coef * (length - pr.vector2_length(v)))


def motor_force(power: float) -> pr.Vector2:
    motor = pr.Vector2(0, 0)
    if pr.is_key_down(pr.KeyboardKey.KEY_A):
        motor = pr.Vector2(power, 0)
    if pr.is_key_down(pr.KeyboardKey.KEY_D):
        motor = pr.Vector2(-power, 0)
    return motor


def edge_force(body: RigidBody, point: pr.Vector2, radius: float, coef: float) -> pr.Vector2:
    v = pr.vector2_subtract(body.pos, point)
    d = pr.vector2_length(v)
    if d < radius:
        v = pr.vector2_scale(pr.vector2_normalize(v), radius - d)
        body.pos = pr.vector2_add(body.pos, v)
        body.vel = pr.vector2_zero()
        return pr.vector2_scale(v, coef)
    else:
        return pr.vector2_zero()
