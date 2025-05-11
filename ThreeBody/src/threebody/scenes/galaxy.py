import sys

import pyray as pr

from threebody.entities.star import STAR_DISTANCE_SCALE, Star
from threebody.utils.light import LIGHT_POINT, Light, create_light, delete_light, update_light_values
from threebody.utils.physic import gravity_center, gravity_force
from threebody.utils.vector import vector3_random

# Simulation of N body system with a total mass M equivalent to the sun mass within a diameter D of 1 AU, with a
# timestep T of 10 days.
N = 3  # stars
M = 1.9e18  # Gt
D = 1.5e8  # km
T = 8.64e5  # s

CAMERA_EYE = pr.Vector3(0, 0, 100)
CAMERA_TARGET = pr.Vector3(0, 0, 0)
CAMERA_UP = pr.Vector3(0, 1, 0)

AMBIENT_COLOR = pr.Vector4(0.1, 0.1, 0.1, 1.0)

LIGHT_POSITION = pr.Vector3(0, 0, 0)
LIGHT_TARGET = pr.Vector3(0, 0, 0)


class Context:
    stars: list[Star] = []
    camera: pr.Camera3D = pr.Camera3D()
    shader: pr.Shader
    light: Light


def init():
    num_stars = N
    if len(sys.argv) > 1:
        num_stars = int(sys.argv[1])

    Context.stars = [Star(pr.vector3_scale(vector3_random(), D / 2.0), M / num_stars) for _ in range(num_stars)]
    Context.camera = pr.Camera3D(CAMERA_EYE, CAMERA_TARGET, CAMERA_UP, 45, pr.CameraProjection.CAMERA_PERSPECTIVE)

    Context.shader = pr.load_shader("data/shaders/lighting.vs", "data/shaders/lighting.fs")
    Context.shader.locs[pr.ShaderLocationIndex.SHADER_LOC_VECTOR_VIEW] = pr.get_shader_location(
        Context.shader, "viewPos"
    )
    pr.set_shader_value(
        Context.shader,
        pr.get_shader_location(Context.shader, "ambient"),
        AMBIENT_COLOR,
        pr.ShaderUniformDataType.SHADER_UNIFORM_VEC4,
    )

    Context.light = create_light(LIGHT_POINT, LIGHT_POSITION, LIGHT_TARGET, pr.WHITE, Context.shader)


def release():
    delete_light(Context.light)
    pr.unload_shader(Context.shader)


def update(dt: float):
    num_stars = len(Context.stars)
    for i in range(num_stars):
        for j in range(i + 1, num_stars):
            f_i, f_j = gravity_force(Context.stars[i], Context.stars[j])
            Context.stars[i].apply_force(f_i)
            Context.stars[j].apply_force(f_j)

    for star in Context.stars:
        star.update(T * dt)


def draw():
    Context.camera.target = pr.vector3_scale(gravity_center(Context.stars), STAR_DISTANCE_SCALE)  # type: ignore
    pr.update_camera(Context.camera, pr.CameraMode.CAMERA_THIRD_PERSON)
    pr.set_shader_value(
        Context.shader,
        Context.shader.locs[pr.ShaderLocationIndex.SHADER_LOC_VECTOR_VIEW],
        Context.camera.position,
        pr.ShaderUniformDataType.SHADER_UNIFORM_VEC3,
    )
    Context.light.position = Context.camera.target
    update_light_values(Context.light)

    pr.clear_background(pr.BLACK)

    pr.begin_mode_3d(Context.camera)
    pr.begin_shader_mode(Context.shader)
    for star in Context.stars:
        star.draw()
    pr.end_shader_mode()
    # pr.draw_sphere(Context.camera.target, 1, pr.YELLOW)
    # pr.draw_sphere(LIGHT_POSITION, 1, pr.WHITE)
    pr.end_mode_3d()

    pr.draw_fps(0, 0)
