"""Contains constants used for the game."""

from . import room_configurations as conf

# Window
MIN_SIZE = (568, 320)
UPDATE_SPEED = 1/144
MIN_ZOOM = 0.25
MAX_ZOOM = 2
PARALLAX_X = 70
PARALLAX_Y = 15
DEFAULT_DUNGEON_SIZE = 3

# Player
PLAYER_SPEED = 4
DIAGONAL_MULTIPLIER = 0.7
PLAYER_COLLIDER = {
    "x": 1/16,
    "y": 2/16,
    "width": 14/16,
    "height": 10/16
}

# Styles
TILESET_DIMENSIONS = (10, 5)
ICE = 0
VOLCANO = 1
FOREST = 2
STYLES = [ICE, VOLCANO]

# Tile Types
FLOOR = 0
WALL = 1
PIT = 2
SECONDARY_FLOOR = 3
PAVEMENT = 4
TILES = {
    FLOOR: {
        "sprite": {
            "width": 16,
            "height": 16,
            "connective": False,
            "connects": []
        },
        "collider": None,
        "layer": "ground"
    },
    WALL: {
        "sprite": {
            "width": 16,
            "height": 25,
            "connective": True,
            "connects": [WALL]
        },
        "collider": {
            "x": 0,
            "y": 0,
            "width": 1,
            "height": 1
        },
        "layer": "y_ordered"
    },
    PIT: {
        "sprite": {
            "width": 16,
            "height": 16,
            "connective": True,
            "connects": [PIT]
        },
        "collider": {
            "x": 2/16,
            "y": 3/16,
            "width": 11/16,
            "height": 11/16
        },
        "layer": "ground"
    },
    SECONDARY_FLOOR: {
        "sprite": {
            "width": 16,
            "height": 16,
            "connective": True,
            "connects": [SECONDARY_FLOOR]
        },
        "collider": None,
        "layer": "ground"
    },
    PAVEMENT: {
        "sprite": {
            "width": 16,
            "height": 16,
            "connective": True,
            "connects": [WALL, PAVEMENT]
        },
        "collider": None,
        "layer": "ground"
    }
}

# Tilemaps
DEFAULT_ROOM_SIZE = 7
DEFAULT_MAP_SETTINGS = [
    {
        "id": SECONDARY_FLOOR,
        "overrides": [FLOOR],
        "seed_amount": 3,
        "seed_type": "blob",
        "b_spread_amount": 20,
        "b_spread_additional": 20,
        "b_spread_compound": False
    },
    {
        "id": PIT,
        "overrides": [FLOOR, SECONDARY_FLOOR],
        "seed_amount": 1,
        "seed_type": "blob",
        "b_spread_amount": 50,
        "b_spread_additional": 50,
        "b_spread_compound": True
    },
    {
        "id": WALL,
        "overrides": [FLOOR, PIT, SECONDARY_FLOOR],
        "seed_amount": 2,
        "seed_type": "line",
        "l_hole_amount": 3,
        "l_hole_size_range": (2, 4)
    },
]

# Room Types
START_ROOM = 0
FIGHT_ROOM = 1
TREASURE_ROOM = 2
BOSS_ROOM = 3
SHOP_ROOM = 4
ROOM_INFO = {
    START_ROOM: {
        "default_dimensions": (6, 6),
        "dont_connect": [
            BOSS_ROOM,
            START_ROOM,
            TREASURE_ROOM,
            SHOP_ROOM
        ],
        "configs": {
            ICE: [conf.C_START],
            VOLCANO: [conf.C_START]
        }
    },
    FIGHT_ROOM: {
        "default_dimensions": (7, 7),
        "dont_connect": [],
        "configs": {
            ICE: [
                conf.C_FIGHT_LARGE,
                conf.C_FIGHT_SEMI_RANDOM,
                conf.C_FIGHT_SEMI_RANDOM,
                conf.C_FIGHT_RANDOM
            ],
            VOLCANO: [
                conf.C_FIGHT_LARGE,
                conf.C_FIGHT_SEMI_RANDOM,
                conf.C_FIGHT_RANDOM
            ]
        }
    },
    TREASURE_ROOM: {
        "default_dimensions": (6, 5),
        "dont_connect": [
            TREASURE_ROOM,
            SHOP_ROOM,
            BOSS_ROOM
        ],
        "configs": {
            ICE: [conf.C_TREASURE],
            VOLCANO: [conf.C_TREASURE]
        }
    },
    BOSS_ROOM: {
        "default_dimensions": (9, 9),
        "dont_connect": [
            START_ROOM,
            FIGHT_ROOM,
            BOSS_ROOM,
            TREASURE_ROOM,
            SHOP_ROOM
        ],
        "configs": {
            ICE: [conf.C_BOSS_CENTRED],
            VOLCANO: [conf.C_BOSS_CENTRED]
        }
    },
    SHOP_ROOM: {
        "default_dimensions": (10, 7),
        "dont_connect": [
            START_ROOM,
            FIGHT_ROOM,
            TREASURE_ROOM,
            SHOP_ROOM
        ],
        "configs": {
            ICE: [conf.C_EMPTY],
            VOLCANO: [conf.C_EMPTY]
        }
    }
}

# Dungeon Configs
DUNGEON_BASE = {
    "size": 5,
    "rooms": {
        FIGHT_ROOM: 60,
        TREASURE_ROOM: 20,
        BOSS_ROOM: 5,
        SHOP_ROOM: 3
    },
    "connections": 30
}
