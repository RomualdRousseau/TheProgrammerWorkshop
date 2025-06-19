import pyray as pr

from tinyrpg.constants import CAMERA_SPEED, WINDOW_HEIGHT, WINDOW_WIDTH, WORLD_HEIGHT, WORLD_WIDTH
from tinyrpg.engine.entity import Entity
from tinyrpg.utils import resize_bbox

CAMERA_BOUNDARY_RESIZE = pr.Vector2(-WORLD_WIDTH // 2, -WORLD_HEIGHT // 2)  # pixels


class FixedCamera:
    def __init__(self):
        self.camera = pr.Camera2D((0, 0), (0, 0), 0, WINDOW_WIDTH // WORLD_WIDTH)


class FollowCamera:
    def __init__(self, boundary):
        self.camera = pr.Camera2D((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), (0, 0), 0, WINDOW_WIDTH // WORLD_WIDTH)
        self.target = pr.vector2_zero()
        self.boundary = resize_bbox(boundary, CAMERA_BOUNDARY_RESIZE)

    def set_boundary(self, boundary: pr.BoundingBox):
        self.boundary = resize_bbox(boundary, CAMERA_BOUNDARY_RESIZE)

    def set_follower(self, follower: Entity):
        self.follower = follower

    def update(self, dt: float):
        self.target = pr.vector2_clamp(
            self.follower.pos,
            pr.Vector2(self.boundary.min.x, self.boundary.min.y),
            pr.Vector2(self.boundary.max.x, self.boundary.max.y),
        )

        target_ab = pr.vector2_subtract(self.target, self.camera.target)
        if pr.vector2_length_sqr(target_ab) < 1.0:
            self.camera.target = self.target
        else:
            self.camera.target = pr.vector2_add(self.camera.target, pr.vector2_scale(target_ab, CAMERA_SPEED * dt))
