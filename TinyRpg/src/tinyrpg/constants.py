APP_NAME = "Tutorial5 - TinyRpg"

WINDOW_WIDTH = 1024  # px
WINDOW_HEIGHT = 1024  # px
FRAME_RATE = 60  # fps

DEBUG_ENABLED = True

CAMERA_SPEED = 5  # px.s-1

WORLD_WIDTH = 256  # px
WORLD_HEIGHT = 256  # px
WORLD_LAYER_COUNT = 3
WORLD_BACKGROUND_LAYER = 0
WORLD_FOREGROUND_LAYER = 1
WORLD_DEBUG_LAYER = 2

ENTITY_MASS_DEFAULT = 1.0  # kg
ENTITY_DENSITY_DEFAULT = 8  # px.kg-1

CHARACTER_TRIGGER_NEAR_DEFAULT = 16
CHARACTER_TRIGGER_FAR_DEFAULT = 64
CHARACTER_FREE_TIMER = 60  # s

INPUT_TAKE_SCREENSHOT = "START"
INPUT_ATTACK = "SQUARE"
INPUT_OPEN_INVENTORY = "TRIANGLE"
INPUT_INVENTORY_NEXT = "RIGHT"
INPUT_INVENTORY_PREVIOUS = "LEFT"
INPUT_INVENTORY_CLOSE = "CIRCLE"
INPUT_INVENTORY_EQUIP = "CROSS"
INPUT_INVENTORY_UNEQUIP = "CROSS"
INPUT_INVENTORY_DROP = "TRIANGLE"
INPUT_MESSAGE_NEXT = "CROSS"

MAX_AVOID_FORCE = 2000  # N

EPSILON = 1e-6

DIR4 = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]

DIR8 = [
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
]

ITEM_DATABASE = [
    ("Sword", 0, "sword", 1, 0, "+1 Damage"),
    ("Shield", 2, "shield", 0, 1, "+1 Armor"),
    ("Necklace", 1, "gem", 1, 1, "Magic\n+1 Damage\n+1 Armor"),
    ("Potion", 3, "potion", 0, 0, "Restore 5 HP"),
]

MESSAGE_GRACE = """Hello Romuald! How are you?
Help me to find my treasure?
I give you a sword and a shield.
I love you ...
"""

MESSAGE_PLAYER = """Hello Grace, I a good and you!
Yes, sure. Thank you!
I love you too ...
"""
