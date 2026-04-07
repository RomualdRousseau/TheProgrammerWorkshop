# Functional Game Patterns for Raylib

## State Management
Prefer simple `match` statements or a dictionary of functions over complex state machine classes.

```python
def update_menu(state):
    if pr.is_key_pressed(pr.KEY_ENTER):
        return "game"
    return "menu"

# ... and so on ...
```

## Physics Integration
When implementing movement or force application, avoid branching where possible. For normalization, add an `EPSILON` to the denominator to prevent division by zero without an `if` statement.

```python
# GOOD: Branchless normalization
dist = (dx**2 + dy**2)**0.5
direction_x = dx / (dist + EPSILON)
direction_y = dy / (dist + EPSILON)

# AVOID: Branching logic for normalization
if dist > EPSILON:
    direction_x = dx / dist
```

## Object Pooling
Use pre-allocated lists with "active" flags. Use modular functions to manage the pool state.

```python
def get_from_pool(pool):
    for obj in pool:
        if not obj.active:
            obj.active = True
            return obj
    return None
```
