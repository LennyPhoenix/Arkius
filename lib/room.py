"""Contains class objects for Room."""

import random

from . import constants as c
from . import prefabs, tilemaps
from .spatial import Space


class Room:
    """Room class for dungeon."""

    def __init__(self, window, room_type=c.START_ROOM, doors={0: True, 1: True, 2: True, 3: True}, dimensions=None):  # noqa: E501
        """Initialise the room."""
        self.type = room_type
        self.doors = doors
        self.tilemap = {}
        self.tiles = {}
        self.cleared = self.type == c.START_ROOM

        self.space = Space(cell_size=4)

        if dimensions is None:
            self.width = c.ROOM_INFO[self.type]["dimensions"][0]
            self.height = c.ROOM_INFO[self.type]["dimensions"][1]
        else:
            self.width, self.height = dimensions[0], dimensions[1]

        self.tilemap = tilemaps.create_blank(
            self.width,
            self.height
        )
        if c.ROOM_INFO[self.type]["base"] is not None:
            tilemap = random.choice(c.ROOM_INFO[self.type]["base"])
            self.tilemap.update(tilemaps.toMap(tilemap))

        self.tilemap = tilemaps.generate(
            self.width, self.height,
            self.tilemap,
            self.type
        )

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
            self.tilemap.update({
                (x, self.height+1): border_type,
                (x, -(self.height+1)): border_type
            })
        for y in range(-(self.height+1), self.height+2):
            self.tilemap.update({
                (self.width+1, y): border_type,
                (-(self.width+1), y): border_type
            })

        for i in range(4):
            if self.doors[i]:
                self.tilemap.update(door_tiles[i])

        for x in range(-(self.width+3), self.width+4):
            for y in range(-(self.height+3), self.height+4):
                if (x, y) in self.tilemap.keys():
                    tile_type = self.tilemap[(x, y)]
                    if not c.TILES[tile_type]["sprite"]["connective"]:
                        image = random.choice(window.resources["tiles"][
                            style
                        ][
                            tile_type
                        ])
                    else:
                        index = self.getImageIndex(x, y)
                        image = window.resources["tiles"][
                            style
                        ][
                            tile_type
                        ][
                            index
                        ]

                    tile = prefabs.Tile(
                        window,
                        x, y,
                        tile_type,
                        image
                    )
                    if c.TILES[tile.type]["collider"] is not None:
                        self.space.insert_body(tile)
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

    def getImageIndex(self, x, y):
        """Return the image index for a tile.

        Arguments:
            x {int} -- The x position of the tile.
            y {int} -- The y position of the tile.

        Returns:
            int -- The image index of the tile.
        """
        tilemap = self.tilemap
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

        index_dict = {
            34: 2, 136: 3, 226: 4, 184: 5, 58: 6, 142: 7, 138: 8, 162: 9,
            251: 10, 187: 11, 191: 12, 255: 13, 139: 14, 46: 15, 232: 16,
            163: 17, 42: 18, 168: 19, 248: 20, 56: 21, 62: 22, 254: 23,
            250: 24, 186: 25, 190: 26, 2: 27, 130: 28, 128: 29, 224: 30, 0: 31,
            14: 32, 238: 33, 234: 34, 174: 36, 10: 37, 170: 38, 160: 39,
            227: 40, 131: 41, 143: 42, 239: 43, 235: 44, 171: 45, 175: 46,
            8: 47, 40: 48, 32: 49
        }

        return index_dict[value]
