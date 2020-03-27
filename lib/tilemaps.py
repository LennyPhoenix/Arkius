"""Contains tilemap generator and premade tilemaps for rooms."""


def create_blank(width=7, height=7, type=0):
    """Creates a coordinate based dictionary with the specified width and height.

    Keyword Arguments:
        width {int} -- The room's width. (default: {7})
        height {int} -- The room's height. (default: {7})
        type {int} -- The tile type that should be used. (default: {0})

    Returns:
        dict -- The empty map.
    """
    map = {}
    for x in range(-width, width+1):
        for y in range(-height, height+1):
            map[(x, y)] = type
    return map
