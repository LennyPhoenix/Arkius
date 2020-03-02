"""Contains some frequently used functions."""


def getBitValue(tileset, x, y):
    """Returns the bitmasking value of a tile."""
    tileID = tileset[(x, y)]
    value = 0

    sides = {
        128: False, 1: False,   2: False,
        64: False,              4: False,
        32: False,  16: False,  8: False
    }

    edges = [tileID]
    if tileID == 2:
        edges.append(1)

    if y != 14 and tileset[(x, y+1)] not in edges:
        sides[128] = True
        sides[1] = True
        sides[2] = True
    if y != 14 and x != 14 and tileset[(x+1, y+1)] not in edges:
        sides[2] = True
    if x != 14 and tileset[(x+1, y)] not in edges:
        sides[2] = True
        sides[4] = True
        sides[8] = True
    if x != 14 and y != 0 and tileset[(x+1, y-1)] not in edges:
        sides[8] = True
    if y != 0 and tileset[(x, y-1)] not in edges:
        sides[8] = True
        sides[16] = True
        sides[32] = True
    if y != 0 and x != 0 and tileset[(x-1, y-1)] not in edges:
        sides[32] = True
    if x != 0 and tileset[(x-1, y)] not in edges:
        sides[32] = True
        sides[64] = True
        sides[128] = True
    if x != 0 and y != 14 and tileset[(x-1, y+1)] not in edges:
        sides[128] = True

    for side in sides.keys():
        if sides[side]:
            value += side

    return value


def worldToScreen(x, y, window):
    """Converts a world postion to the screen position."""
    scale_factor = window.scaleFactor()

    screen_x = (x + 2.5) * 16 * scale_factor  # With buffer
    screen_x += window.width/2 - 20*16*scale_factor/2  # Center

    screen_y = (y + 2.5) * 16 * scale_factor  # With buffer
    screen_y += window.height/2 - 20*16*scale_factor/2  # Center

    return (screen_x, screen_y)
