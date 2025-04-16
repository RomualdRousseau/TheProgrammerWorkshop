import pyray as pr

TRAIL_RADIUS_SCALE = 0.5
TRAIL_ALPHA = 0.5


class Sphere:
    def __init__(self, trail_size: int) -> None:
        self.trail_size = trail_size
        self.trail: list[pr.Vector3] = []

    def draw(self, pos: pr.Vector3, radius: float, color: pr.Color) -> None:
        if len(self.trail) > self.trail_size:
            self.trail.pop(0)
        self.trail.append(pos)

        for pos in self.trail:
            pr.draw_point_3d(pos, pr.color_alpha(color, TRAIL_ALPHA))

        pr.draw_sphere(self.trail[-1], radius, color)
