"""Small pure math helpers shared by the physics layer."""


def clamp(value: float, low: float, high: float) -> float:
    """Constrain a value to the inclusive [low, high] range."""
    return max(low, min(value, high))
