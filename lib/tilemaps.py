"""Contains tilemap generator and premade tilemaps for rooms."""

import random

from . import constants as c


def toMap(matrix):
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
    if tile_options is None:
        tile_options = c.ROOM_INFO[room_type]["generation_options"]

    return room_map
