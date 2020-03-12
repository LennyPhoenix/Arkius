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
        sides.update({128: True, 1: True, 2: True})
    if x != 14 and tileset[(x+1, y)] not in edges:
        sides.update({2: True, 4: True, 8: True})
    if y != 0 and tileset[(x, y-1)] not in edges:
        sides.update({8: True, 16: True, 32: True})
    if x != 0 and tileset[(x-1, y)] not in edges:
        sides.update({32: True, 64: True, 128: True})

    if y != 14 and x != 14 and tileset[(x+1, y+1)] not in edges:
        sides[2] = True
    if x != 14 and y != 0 and tileset[(x+1, y-1)] not in edges:
        sides[8] = True
    if y != 0 and x != 0 and tileset[(x-1, y-1)] not in edges:
        sides[32] = True
    if x != 0 and y != 14 and tileset[(x-1, y+1)] not in edges:
        sides[128] = True

    for side in sides.keys():
        if sides[side]:
            value += side

    return value


def getUV(tile_type, tile_value):
    """Returns the tile's UV from its type and value."""
    if tile_type == 0:
        values_dict = {
            0: (0, 0), 1: (16, 0), 2: (32, 0), 3: (48, 0), 4: (64, 0),
            5: (0, 16), 6: (16, 16), 7: (32, 16), 8: (48, 16), 9: (64, 16)
        }
    else:
        values_dict = {
            34: (32, 0), 136: (48, 0), 226: (64, 0), 184: (80, 0),
            58: (96, 0), 142: (112, 0), 138: (128, 0), 162: (144, 0),

            251: (0, 16), 187: (16, 16), 191: (32, 16), 255: (48, 16),
            139: (64, 16), 46: (80, 16), 232: (96, 16), 163: (112, 16),
            42: (128, 16), 168: (144, 16),

            248: (0, 32), 56: (16, 32), 62: (32, 32), 254: (48, 32),
            250: (64, 32), 186: (80, 32), 190: (96, 32), 2: (112, 32),
            130: (128, 32), 128: (144, 32),

            224: (0, 48), 0: (16, 48), 14: (32, 48), 238: (48, 48),
            234: (64, 48), 174: (96, 48), 10: (112, 48), 170: (128, 48),
            160: (144, 48),

            227: (0, 64), 131: (16, 64), 143: (32, 64), 239: (48, 64),
            235: (64, 64), 171: (80, 64), 175: (96, 64), 8: (112, 64),
            40: (128, 64), 32: (144, 64)
        }

    x, y = values_dict[tile_value]

    if tile_type == 1:
        tile_height = 32
        y *= 2
    else:
        tile_height = 16

    return (x, y, 16, tile_height)
