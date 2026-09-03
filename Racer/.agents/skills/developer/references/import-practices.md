# Pythonic Import Practices

Adhere to these rules for clean and consistent namespaces:

## 1. Absolute Imports Only
Never use relative imports (`from . import ...`). Always use the full package path.
```python
# GOOD
from my_game.game.state import GameState

# BAD
from .state import GameState
```

## 2. No Wildcard Imports
Never use `from module import *`. Explicitly import the names you need.
```python
# GOOD
from pyray import Vector2, init_window

# BAD
from pyray import *
```

## 3. Alias Pyray
Always import `pyray` as `pr` to keep drawing calls concise and identifiable.
```python
import pyray as pr

def main():
    pr.init_window(800, 450, "My Game")
    # ...
    pr.begin_drawing()
    # ...
    pr.end_drawing()
```

## 4. Group Imports
Order your imports:
1. Standard library
2. Third-party (e.g., `pyray`)
3. Local module imports
