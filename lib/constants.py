"""Contains constants used for the game."""

# Window
MIN_SIZE = (568, 320)
UPDATE_SPEED = 1/120

# Tilemaps
DEFAULT_ROOM_SIZE = 7

# Room Types
START_ROOM = 0
FIGHT_ROOM = 1
TREASURE_ROOM = 2
BOSS_ROOM = 3
SHOP_ROOM = 4
ROOM_INFO = {
    0: {
        "dimensions": (6, 6)
    },
    1: {
        "dimensions": (7, 7)
    },
    2: {
        "dimensions": (6, 5)
    },
    3: {
        "dimensions": (8, 8)
    },
    4: {
        "dimensions": (10, 7)
    }
}

# Tile Types
FLOOR = 0
WALL = 1
PIT = 2
SECONDARY_FLOOR = 3

# Styles
ICE = 0

# Player
PLAYER_SPEED = 4
DIAGONAL_MULTIPLIER = 0.7
