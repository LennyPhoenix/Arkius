"""Contains room configurations."""

GENERATION_OPTIONS = [
    {
        "id": int,
        "overrides": [int, int],
        "seed_amount": int,
        "seed_type": "blob/line",
        "b_spread_amount": int,
        "b_spread_additional": int,
        "b_spread_compound": bool,
        "l_hole_amount": int,
        "l_hole_size_range": (int, int)
    },
]

MAP = {
    "dimensions": (int, int),
    "door_info": {
        0: {"pos": int, "floor": int},
        1: {"pos": int, "floor": int},
        2: {"pos": int, "floor": int},
        3: {"pos": int, "floor": int},
    },
    "matrix": [
        [int, int, int, ],
        [int, int, int, ],
        [int, int, int, ],
    ]
}

CONFIG = {
    "options": GENERATION_OPTIONS,
    "maps": [MAP, MAP]
}
