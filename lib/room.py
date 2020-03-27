"""Contains class objects for Room."""

import random

from pyglet import image

from . import constants as c
from . import prefabs, tilemaps


class Room:
    """Room class for dungeon."""

    def __init__(self, window, room_type=c.START_ROOM, doors={0: True, 1: True, 2: True, 3: True}, tilemap=None, dimensions=None):  # noqa: E501
        """Initialise the room."""
        self.type = room_type
        self.doors = doors
        self.ground_tiles = {}
        self.tiles = {}
        self.cleared = room_type == c.START_ROOM

        if dimensions is None:
            self.width = c.ROOM_INFO[room_type]["dimensions"][0]
            self.height = c.ROOM_INFO[room_type]["dimensions"][1]
        else:
            self.width, self.height = dimensions[0], dimensions[1]

        self.ground_tiles = tilemaps.create_blank(self.width, self.height)

        self.createSprites(window)

    def createSprites(self, window):
        """Create all the sprites for the room tiles.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        border_type = c.WALL
        style = c.ICE

        door_tiles = {
            0: {
                (-2, self.height+3): border_type,
                (-1, self.height+3): c.FLOOR,
                (0, self.height+3): c.FLOOR,
                (1, self.height+3): c.FLOOR,
                (2, self.height+3): border_type,
                (-2, self.height+2): border_type,
                (-1, self.height+2): c.FLOOR,
                (0, self.height+2): c.FLOOR,
                (1, self.height+2): c.FLOOR,
                (2, self.height+2): border_type,
                (-2, self.height+1): border_type,
                (-1, self.height+1): c.FLOOR,
                (0, self.height+1): c.FLOOR,
                (1, self.height+1): c.FLOOR,
                (2, self.height+1): border_type,
            },
            1: {
                (self.width+1, 2): border_type,
                (self.width+2, 2): border_type,
                (self.width+3, 2): border_type,
                (self.width+1, 1): c.FLOOR,
                (self.width+2, 1): c.FLOOR,
                (self.width+3, 1): c.FLOOR,
                (self.width+1, 0): c.FLOOR,
                (self.width+2, 0): c.FLOOR,
                (self.width+3, 0): c.FLOOR,
                (self.width+1, -1): c.FLOOR,
                (self.width+2, -1): c.FLOOR,
                (self.width+3, -1): c.FLOOR,
                (self.width+1, -2): border_type,
                (self.width+2, -2): border_type,
                (self.width+3, -2): border_type,
            },
            2: {
                (-2, -(self.height+1)): border_type,
                (-1, -(self.height+1)): c.FLOOR,
                (0, -(self.height+1)): c.FLOOR,
                (1, -(self.height+1)): c.FLOOR,
                (2, -(self.height+1)): border_type,
                (-2, -(self.height+2)): border_type,
                (-1, -(self.height+2)): c.FLOOR,
                (0, -(self.height+2)): c.FLOOR,
                (1, -(self.height+2)): c.FLOOR,
                (2, -(self.height+2)): border_type,
                (-2, -(self.height+3)): border_type,
                (-1, -(self.height+3)): c.FLOOR,
                (0, -(self.height+3)): c.FLOOR,
                (1, -(self.height+3)): c.FLOOR,
                (2, -(self.height+3)): border_type,
            },
            3: {
                (-(self.width+3), 2): border_type,
                (-(self.width+2), 2): border_type,
                (-(self.width+1), 2): border_type,
                (-(self.width+3), 1): c.FLOOR,
                (-(self.width+2), 1): c.FLOOR,
                (-(self.width+1), 1): c.FLOOR,
                (-(self.width+3), 0): c.FLOOR,
                (-(self.width+2), 0): c.FLOOR,
                (-(self.width+1), 0): c.FLOOR,
                (-(self.width+3), -1): c.FLOOR,
                (-(self.width+2), -1): c.FLOOR,
                (-(self.width+1), -1): c.FLOOR,
                (-(self.width+3), -2): border_type,
                (-(self.width+2), -2): border_type,
                (-(self.width+1), -2): border_type,
            }
        }

        for x in range(-(self.width+1), self.width+2):
            self.ground_tiles.update({
                (x, self.height+1): border_type,
                (x, -(self.height+1)): border_type
            })
        for y in range(-(self.height+1), self.height+2):
            self.ground_tiles.update({
                (self.width+1, y): border_type,
                (-(self.width+1), y): border_type
            })

        for i in range(4):
            if self.doors[i]:
                self.ground_tiles.update(door_tiles[i])

        for x in range(-(self.width+3), self.width+4):
            for y in range(-(self.height+3), self.height+4):
                if (x, y) in self.ground_tiles.keys():
                    tile_type = self.ground_tiles[(x, y)]
                    if tile_type == c.FLOOR:
                        value = random.randint(0, 9)
                    else:
                        value = self.getBitValue(x, y)
                else:
                    continue

                image_path = f"resources/tilesets/{style}/{tile_type}.png"
                tile_image = image.load(image_path)
                tile_image.anchor_x = 0
                tile_image.anchor_y = 0

                tile_region = tile_image.get_region(
                    *self.getUV(tile_type, value)
                )

                tile = prefabs.Tile(
                    window,
                    x, y,
                    tile_type,
                    tile_region
                )
                self.tiles[(x, y)] = tile

    def update(self, window):
        """Update all tiles.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        for x in range(-(self.width+3), self.width+4):
            for y in range(-(self.height+3), self.height+4):
                if (x, y) in self.tiles.keys():
                    self.tiles[(x, y)].update(window)

    def resize(self, window):
        """Resize all tiles.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        for x in range(-(self.width+3), self.width+4):
            for y in range(-(self.height+3), self.height+4):
                if (x, y) in self.tiles.keys():
                    self.tiles[(x, y)].resize(window)

    def getBitValue(self, x, y):
        """Return the bitmask value for a tile.

        Arguments:
            x {int} -- The x position of the tile.
            y {int} -- The y position of the tile.

        Returns:
            int -- The bitmask value of the tile.
        """
        tilemap = self.ground_tiles
        tileID = tilemap[(x, y)]
        value = 0

        sides = {
            128: False, 1: False,   2: False,
            64: False,              4: False,
            32: False,  16: False,  8: False
        }

        edges = [tileID]

        if (x, y+1) in tilemap.keys() and tilemap[(x, y+1)] not in edges:
            sides.update({128: True, 1: True, 2: True})
        if (x+1, y) in tilemap.keys() and tilemap[(x+1, y)] not in edges:
            sides.update({2: True, 4: True, 8: True})
        if (x, y-1) in tilemap.keys() and tilemap[(x, y-1)] not in edges:
            sides.update({8: True, 16: True, 32: True})
        if (x-1, y) in tilemap.keys() and tilemap[(x-1, y)] not in edges:
            sides.update({32: True, 64: True, 128: True})

        if (x+1, y+1) in tilemap.keys() and tilemap[(x+1, y+1)] not in edges:
            sides[2] = True
        if (x+1, y-1) in tilemap.keys() and tilemap[(x+1, y-1)] not in edges:
            sides[8] = True
        if (x-1, y-1) in tilemap.keys() and tilemap[(x-1, y-1)] not in edges:
            sides[32] = True
        if (x-1, y+1) in tilemap.keys() and tilemap[(x-1, y+1)] not in edges:
            sides[128] = True

        for side in sides.keys():
            if sides[side]:
                value += side

        return value

    def getUV(self, tile_type, tile_value):
        """Find a tile UV position for a tileset.

        Arguments:
            tile_type {int} -- The type of the tile.
            tile_value {int} -- The bitmask value of the tile.

        Returns:
            (int, int) -- The UV position for the tile.
        """
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
