from . import room_configurations as conf

# Window
MIN_SIZE = (568, 320)
UPDATE_SPEED = 1/144
MIN_ZOOM = 0.25
MAX_ZOOM = 2
PARALLAX_X = 70
PARALLAX_Y = 15
DEFAULT_WORLD_SIZE = 3

WORLD_LAYERS = [
    "ground",
    "g_deco",
    "g_particles",
    "y_ordered",
    "a_particles"
]
UI_LAYERS = [
    "transition",
    "map_window",
    "map_rooms",
    "map_icons",
]

# Player
PLAYER_SPEED = 3200
PLAYER_COLLIDER = {
    "type": "circle",
    "radius": 7,
    "offset": (8, 5)
}

# Collider Types
COLLISION_TYPES = {
    "player": 1,
    "tile": 2,
    "enemy": 3,
    "room_border": 4,
    "projectile": 5
}

# Styles
TILESET_DIMENSIONS = (10, 5)
HUB = 0
ICE = 1
VOLCANO = 2
FOREST = 3
STYLES = [HUB, ICE, VOLCANO]

# Tile Types
TILE_SIZE = 16
VOID = -1
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
            "type": "rect",
            "x": 0,
            "y": 0,
            "width": 16,
            "height": 16,
            "radius": 0
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
            "type": "rect",
            "x": 2,
            "y": 2,
            "width": 12,
            "height": 12,
            "radius": 0
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
            "connects": [PAVEMENT]
        },
        "collider": None,
        "layer": "ground"
    }
}

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
            HUB: [conf.C_START],
            ICE: [conf.C_START],
            VOLCANO: [conf.C_START]
        }
    },
    FIGHT_ROOM: {
        "default_dimensions": (7, 7),
        "dont_connect": [],
        "configs": {
            HUB: [
                conf.C_FIGHT_LARGE,
                conf.C_FIGHT_SEMI_RANDOM,
                conf.C_FIGHT_RANDOM
            ],
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
            HUB: [conf.C_TREASURE],
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
            HUB: [conf.C_BOSS_CENTRED],
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
            HUB: [conf.C_EMPTY],
            ICE: [conf.C_EMPTY],
            VOLCANO: [conf.C_EMPTY]
        }
    }
}

# Dungeon Configs
DUNGEON_BASE = {
    "size": 3,
    "rooms": {
        FIGHT_ROOM: 30,
        TREASURE_ROOM: 8,
        BOSS_ROOM: 3,
        SHOP_ROOM: 1
    },
    "connections": 30
}

DUNGEON_BIG = {
    "size": 5,
    "rooms": {
        FIGHT_ROOM: 60,
        TREASURE_ROOM: 20,
        BOSS_ROOM: 5,
        SHOP_ROOM: 3
    },
    "connections": 30
}
