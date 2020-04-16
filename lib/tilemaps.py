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


def generate(width, height, room_map, room_type, tile_options=None):
    """Randomly modify given tilemap with the options specified.

    Arguments:
        width {int} -- The width of the tilemap's room.
        height {int} -- The height of the tilemap's room.
        room_map {dict} -- The dictionary tilemap to randomise.
        room_type {int} -- The type of room.

    Keyword Arguments:
        tile_options {dict} -- The tiles that should be randomised and their
                               options. (default: {None})

    Returns:
        dict -- The randomised tilemap dict.
    """

    if tile_options is None:
        tile_options = c.ROOM_INFO[room_type]["generation_options"]

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
                possible.remove(next_pos)

                for x, y in neighbours:
                    n_x, n_y = next_pos[0]+x, next_pos[1]+y
                    if (
                        (n_x, n_y) in room_map.keys() and
                        room_map[(n_x, n_y)] in options["overrides"] and
                        (n_x, n_y) not in possible
                    ):
                        possible.append((n_x, n_y))

                spread += 1
                additional_chance = random.random() * 100

            possible_seeds = [
                pos for pos in room_map.keys() if
                room_map[pos] in options["overrides"]
            ]
            seeded += 1


    generators = {
        "blob": blob,
        "line": line
    }

    for options in tile_options:
        if options["seed_type"] in generators.keys():
            generators[options["seed_type"]](options)

    return room_map
