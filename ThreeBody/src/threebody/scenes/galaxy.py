import pyray as pr

from threebody.entities.star import STAR_DISTANCE_SCALE, Star
from threebody.utils.physic import gravity_center, gravity_force
from threebody.utils.vector import vector3_random

# Simulation of N body system with a total mass M equivalent to the sun mass within a diameter D of 1 AU, with a
# timestep T of 10 days.
N = 20  # stars
M = 1.9e18  # Gt
D = 1.5e8  # km
T = 8.64e5  # s

CAMERA_EYE = pr.Vector3(0, 0, -100)
CAMERA_TARGET = pr.Vector3(0, 0, 0)
CAMERA_UP = pr.Vector3(0, 1, 0)


class Context:
    stars: list[Star] = []
    camera: pr.Camera3D = pr.Camera3D()


def init():
    Context.stars = [Star(pr.vector3_scale(vector3_random(), D / 2.0), M / N) for _ in range(N)]
    Context.camera = pr.Camera3D(CAMERA_EYE, CAMERA_TARGET, CAMERA_UP, 45, pr.CameraProjection.CAMERA_PERSPECTIVE)


def release():
    pass


def update(dt: float):
    Context.camera.target = pr.vector3_scale(gravity_center(Context.stars), STAR_DISTANCE_SCALE)  # type: ignore
    pr.update_camera(Context.camera, pr.CameraMode.CAMERA_THIRD_PERSON)

    for i in range(N):
        for j in range(i + 1, N):
            f_i, f_j = gravity_force(Context.stars[i], Context.stars[j])
            Context.stars[i].apply_force(f_i)
            Context.stars[j].apply_force(f_j)

    for star in Context.stars:
        star.update(T * dt)


def draw():
    pr.clear_background(pr.BLACK)

    pr.begin_mode_3d(Context.camera)
    for star in Context.stars:
        star.draw()
    pr.end_mode_3d()

    pr.draw_fps(0, 0)
