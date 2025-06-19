from tinyrpg.utils.bbox import adjust_bbox as adjust_bbox
from tinyrpg.utils.bbox import check_collision_bbox_point as check_collision_bbox_point
from tinyrpg.utils.bbox import check_collision_bbox_ray as check_collision_bbox_ray
from tinyrpg.utils.bbox import get_bbox_center as get_bbox_center
from tinyrpg.utils.bbox import get_bbox_center_2d as get_bbox_center_2d
from tinyrpg.utils.bbox import get_bbox_from_rect as get_bbox_from_rect
from tinyrpg.utils.bbox import resize_bbox as resize_bbox
from tinyrpg.utils.quad_tree import QuadTreeBuilder as QuadTreeBuilder


def clamp(a, b, c):
    return max(a, min(b, c))
