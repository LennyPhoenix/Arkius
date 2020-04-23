"""Contains tilemap generator and premade tilemaps for rooms."""

import random

from . import constants as c


def toMap(matrix):
    """Convert a matrix to a tilemap dict.

    Arguments:
        matrix {list} -- The tile matrix to convert.

    Returns:
        dict -- The converted tilemap dict.
    """
    height = len(matrix)//2
    width = len(matrix[0])//2
    tilemap = {}
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] != c.FLOOR:
                tilemap[(-width+x, height-y)] = matrix[y][x]
    return tilemap


def add_boundaries(room_map, width, height, doors_enabled, map_data):  # noqa: E501
    """Applies boundaries and doors.

    Arguments:
        room_map {dict} -- The dictionary tilemap to modify.
        width {int} -- The room's width.
        height {int} -- The room's height.
        doors_enabled {dict} -- A dict of all enabled doors.
        map_data {dict} -- The data about the map.

    Returns:
        dict -- The modified tilemap.
    """

    if map_data is not None:
        border_type = map_data["border_type"]
    else:
        border_type = c.WALL

    door_f = {}
    door_p = {}
    for i in range(4):
        if map_data is not None:
            door_f[i] = map_data["door_info"][i]["floor"]
            door_p[i] = map_data["door_info"][i]["pos"]
        else:
            door_f[i] = c.FLOOR
            door_p[i] = 0

    door_tiles = {
        0: {
            (door_p[0]-2, height+3): border_type,
            (door_p[0]-1, height+3): door_f[0],
            (door_p[0], height+3): door_f[0],
            (door_p[0]+1, height+3): door_f[0],
            (door_p[0]+2, height+3): border_type,

            (door_p[0]-2, height+2): border_type,
            (door_p[0]-1, height+2): door_f[0],
            (door_p[0], height+2): door_f[0],
            (door_p[0]+1, height+2): door_f[0],
            (door_p[0]+2, height+2): border_type,

            (door_p[0]-2, height+1): border_type,
            (door_p[0]-1, height+1): door_f[0],
            (door_p[0], height+1): door_f[0],
            (door_p[0]+1, height+1): door_f[0],
            (door_p[0]+2, height+1): border_type,
        },
        1: {
            (width+1, door_p[1]+2): border_type,
            (width+2, door_p[1]+2): border_type,
            (width+3, door_p[1]+2): border_type,
            (width+1, door_p[1]+1): door_f[1],
            (width+2, door_p[1]+1): door_f[1],
            (width+3, door_p[1]+1): door_f[1],
            (width+1, door_p[1]): door_f[1],
            (width+2, door_p[1]): door_f[1],
            (width+3, door_p[1]): door_f[1],
            (width+1, door_p[1]-1): door_f[1],
            (width+2, door_p[1]-1): door_f[1],
            (width+3, door_p[1]-1): door_f[1],
            (width+1, door_p[1]-2): border_type,
            (width+2, door_p[1]-2): border_type,
            (width+3, door_p[1]-2): border_type,
        },
        2: {
            (door_p[2]-2, -(height+1)): border_type,
            (door_p[2]-1, -(height+1)): door_f[2],
            (door_p[2], -(height+1)): door_f[2],
            (door_p[2]+1, -(height+1)): door_f[2],
            (door_p[2]+2, -(height+1)): border_type,
            (door_p[2]-2, -(height+2)): border_type,
            (door_p[2]-1, -(height+2)): door_f[2],
            (door_p[2], -(height+2)): door_f[2],
            (door_p[2]+1, -(height+2)): door_f[2],
            (door_p[2]+2, -(height+2)): border_type,
            (door_p[2]-2, -(height+3)): border_type,
            (door_p[2]-1, -(height+3)): door_f[2],
            (door_p[2], -(height+3)): door_f[2],
            (door_p[2]+1, -(height+3)): door_f[2],
            (door_p[2]+2, -(height+3)): border_type,
        },
        3: {
            (-(width+3), door_p[3]+2): border_type,
            (-(width+2), door_p[3]+2): border_type,
            (-(width+1), door_p[3]+2): border_type,
            (-(width+3), door_p[3]+1): door_f[3],
            (-(width+2), door_p[3]+1): door_f[3],
            (-(width+1), door_p[3]+1): door_f[3],
            (-(width+3), door_p[3]): door_f[3],
            (-(width+2), door_p[3]): door_f[3],
            (-(width+1), door_p[3]): door_f[3],
            (-(width+3), door_p[3]-1): door_f[3],
            (-(width+2), door_p[3]-1): door_f[3],
            (-(width+1), door_p[3]-1): door_f[3],
            (-(width+3), door_p[3]-2): border_type,
            (-(width+2), door_p[3]-2): border_type,
            (-(width+1), door_p[3]-2): border_type,
        }
    }

    for x in range(-(width+1), width+2):
        room_map.update({
            (x, height+1): border_type,
            (x, -(height+1)): border_type
        })
    for y in range(-(height+1), height+2):
        room_map.update({
            (width+1, y): border_type,
            (-(width+1), y): border_type
        })

    for i in range(4):
        if doors_enabled[i]:
            room_map.update(door_tiles[i])

    return room_map


def create_blank(width=7, height=7, tile_type=c.FLOOR):
    """Creates a coordinate based dictionary with the specified width and height.

    Keyword Arguments:
        width {int} -- The room's width. (default: {7})
        height {int} -- The room's height. (default: {7})
        type {int} -- The tile type that should be used. (default: {c.FLOOR})

    Returns:
        dict -- The empty map.
    """
    map = {}
    for x in range(-width, width+1):
        for y in range(-height, height+1):
            map[(x, y)] = tile_type
    return map


def generate(width, height, room_map, tile_options, map_data):
    """Randomly modify given tilemap with the options specified.

    Arguments:
        width {int} -- The width of the tilemap's room.
        height {int} -- The height of the tilemap's room.
        room_map {dict} -- The dictionary tilemap to randomise.
        tile_options {list} -- The tiles that should be randomised and their
                               options.

    Returns:
        dict -- The randomised tilemap dict.
    """

    pre_generation = room_map.copy()

    def blob(options):
        seeded = 0
        possible_seeds = [
            pos for pos in room_map.keys() if
            room_map[pos] in options["overrides"]
        ]
        while seeded < options["seed_amount"] and len(possible_seeds) > 0:
            seed = random.choice(possible_seeds)
            room_map[seed] = options["id"]
            neighbours = [
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1)
            ]
            possible = []
            spread = 0
            additional_chance = random.random() * 100

            for x, y in neighbours:
                n_x, n_y = seed[0]+x, seed[1]+y
                if (
                    (n_x, n_y) in room_map.keys() and
                    room_map[(n_x, n_y)] in options["overrides"]
                ):
                    possible.append((n_x, n_y))

            while (
                (
                    spread < options["b_spread_amount"] or
                    additional_chance < options["b_spread_additional"]
                ) and
                len(possible) > 0
            ):
                next_pos = random.choice(possible)
                room_map[next_pos] = options["id"]

                while next_pos in possible:
                    possible.remove(next_pos)

                for x, y in neighbours:
                    n_x, n_y = next_pos[0]+x, next_pos[1]+y
                    if (
                        (n_x, n_y) in room_map.keys() and
                        room_map[(n_x, n_y)] in options["overrides"] and
                        (
                            (n_x, n_y) not in possible or
                            options["b_spread_compound"]
                        )
                    ):
                        possible.append((n_x, n_y))

                spread += 1
                additional_chance = random.random() * 100

            possible_seeds = [
                pos for pos in room_map.keys() if
                room_map[pos] in options["overrides"]
            ]
            seeded += 1

    def line(options):
        seeded = 0
        tries = 0

        walls = {
            True: [],
            False: []
        }

        while (
            seeded < options["seed_amount"] and
            tries < 50
        ):
            old_map = room_map.copy()

            horizontal = random.choice([True, False])
            if horizontal:
                l_pos = random.randint(-(height-2), (height-2))
                line = [
                    (x, l_pos) for x in range(-width, width+1) if
                    room_map[(x, l_pos)] in options["overrides"]
                ]
            else:
                l_pos = random.randint(-(width-2), (width-2))
                line = [
                    (l_pos, y) for y in range(-height, height+1) if
                    room_map[(l_pos, y)] in options["overrides"]
                ]

            too_close = False
            for previous in walls[horizontal]:
                if previous-3 < l_pos < previous+3:
                    too_close = True

            angle_doors = {
                True: [1, 3],
                False: [0, 2]
            }
            for door_id in angle_doors[horizontal]:
                if map_data is not None:
                    d_pos = map_data["door_info"][door_id]["pos"]
                else:
                    d_pos = 0
                if d_pos-3 < l_pos < d_pos+3:
                    too_close = True

            if not too_close:
                for x, y in line:
                    room_map[(x, y)] = options["id"]
                    walls[horizontal].append(l_pos)

                for i in range(options["l_hole_amount"]):
                    hole_possible = []
                    hole_size = random.randint(*options["l_hole_size_range"])
                    if horizontal:
                        hole_pos = random.randint(-width, width)
                        room_map[
                            (hole_pos, l_pos)
                        ] = old_map[(hole_pos, l_pos)]
                        neighbours = [
                            (1, 0),
                            (-1, 0)
                        ]
                    else:
                        hole_pos = random.randint(-height, height)
                        room_map[
                            (l_pos, hole_pos)
                        ] = old_map[(l_pos, hole_pos)]
                        neighbours = [
                            (0, 1),
                            (0, -1)
                        ]

                    for x, y in neighbours:
                        if horizontal:
                            n_x, n_y = hole_pos + x, l_pos + y
                        else:
                            n_x, n_y = l_pos + x, hole_pos + y
                        if (
                            (n_x, n_y) in room_map.keys() and
                            (n_x, n_y) not in hole_possible
                        ):
                            hole_possible.append((n_x, n_y))

                    hole = 1
                    while hole < hole_size:
                        next_pos = random.choice(hole_possible)
                        room_map[next_pos] = old_map[next_pos]
                        hole_possible.remove(next_pos)

                        for x, y in neighbours:
                            n_x, n_y = next_pos[0] + x, next_pos[1] + y
                            if (
                                (n_x, n_y) in room_map.keys() and
                                (n_x, n_y) not in hole_possible
                            ):
                                hole_possible.append((n_x, n_y))

                        hole += 1
                seeded += 1
                tries = 0
            else:
                tries += 1

    generators = {
        "blob": blob,
        "line": line
    }

    for options in tile_options:
        if options["seed_type"] in generators.keys():
            generators[options["seed_type"]](options)
    angle_doors = {
        1: (True, 1),
        3: (True, -1),
        0: (False, 1),
        2: (False, -1)
    }
    for i in range(4):
        if map_data is not None:
            d_pos = map_data["door_info"][i]["pos"]
        else:
            d_pos = 0
        for offset in range(-1, 2):
            if angle_doors[i][0]:
                pos = (width*angle_doors[i][1], d_pos+offset)
            else:
                pos = (d_pos+offset, height*angle_doors[i][1])
            if c.TILES[room_map[pos]]["collider"] is not None:
                room_map[pos] = pre_generation[pos]

    return room_map
