"""Contains class objects for Room."""

import random

from . import constants as c
from . import prefabs, tilemaps
from .spatial import Space


class Room:
    """Room class for dungeon."""

    def __init__(self, window, room_type=c.START_ROOM, dungeon_style=c.ICE, room_config=None, doors=None):  # noqa: E501
        """Initialise the room.

        Arguments:
            window {Window} -- The application window.

        Keyword Arguments:
            room_type {int} -- The type of room. (default: {c.START_ROOM})
            dungeon_style {int} -- The tileset and style to use.
                                   (default: {c.ICE})
            room_config {dict} -- The room configuration to use.
                                  (default: {None})
            doors {dict} -- The doors that should be open. (default: {None})
        """
        self.window = window
        self.type = room_type
        self.doors = doors
        self.tilemap = {}
        self.tiles = {}
        self.cleared = self.type == c.START_ROOM
        self._visible = False
        self.style = dungeon_style
        self.config = room_config

        self.space = Space(cell_size=4)

        if self.doors is None:
            self.doors = {i: False for i in range(4)}

        self.door_value = 0
        for i in range(4):
            if self.doors[i]:
                self.door_value += 2**i

        if self.config is None:
            self.config = random.choice(
                c.ROOM_INFO[self.type]["configs"][self.style]
            )

        self.map_data = random.choice(self.config["maps"])

        if self.map_data is not None:
            self.map_data = self.map_data.copy()
            self.width = self.map_data["width"]
            self.height = self.map_data["height"]
        else:
            self.width = c.ROOM_INFO[self.type]["default_dimensions"][0]
            self.height = c.ROOM_INFO[self.type]["default_dimensions"][1]

        self.tilemap = tilemaps.create_blank(
            self.width,
            self.height
        )

        if (
            self.map_data is not None and
            self.map_data["matrix"] is not None
        ):
            self.tilemap.update(tilemaps.toMap(self.map_data["matrix"]))
            for i in range(4):
                if type(self.map_data["door_info"][i]["pos"]) is tuple:
                    self.map_data["door_info"][i]["pos"] = random.randint(
                        *self.map_data["door_info"][i]["pos"]
                    )

        self.tilemap = tilemaps.generate(
            self.type,
            self.tilemap,
            self.config["options"],
            self.map_data
        )

        self.tilemap = tilemaps.add_boundaries(
            self.type,
            self.tilemap,
            self.doors,
            self.map_data
        )

        self.createSprites()

    def createSprites(self):
        """Create all the sprites for the room tiles."""

        for x in range(-(self.width+3), self.width+4):
            for y in range(-(self.height+3), self.height+4):
                if (x, y) in self.tilemap.keys():
                    tile_type = self.tilemap[(x, y)]
                    if not c.TILES[tile_type]["sprite"]["connective"]:
                        image = random.choice(self.window.resources["tiles"][
                            self.style
                        ][
                            tile_type
                        ])
                    else:
                        index = self.getImageIndex(x, y)
                        image = self.window.resources["tiles"][
                            self.style
                        ][
                            tile_type
                        ][
                            index
                        ]

                    tile = prefabs.Tile(
                        self.window,
                        x, y,
                        tile_type,
                        image
                    )
                    if c.TILES[tile.type]["collider"] is not None:
                        self.space.insert_body(tile)
                    self.tiles[(x, y)] = tile

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

        connects = c.TILES[tileID]["sprite"]["connects"]

        if (x, y+1) in tilemap.keys() and tilemap[(x, y+1)] not in connects:
            sides.update({128: True, 1: True, 2: True})
        if (x+1, y) in tilemap.keys() and tilemap[(x+1, y)] not in connects:
            sides.update({2: True, 4: True, 8: True})
        if (x, y-1) in tilemap.keys() and tilemap[(x, y-1)] not in connects:
            sides.update({8: True, 16: True, 32: True})
        if (x-1, y) in tilemap.keys() and tilemap[(x-1, y)] not in connects:
            sides.update({32: True, 64: True, 128: True})

        if (
            (x+1, y+1) in tilemap.keys() and
            tilemap[(x+1, y+1)] not in connects
        ):
            sides[2] = True
        if (
            (x+1, y-1) in tilemap.keys() and
            tilemap[(x+1, y-1)] not in connects
        ):
            sides[8] = True
        if (
            (x-1, y-1) in tilemap.keys() and
            tilemap[(x-1, y-1)] not in connects
        ):
            sides[32] = True
        if (
            (x-1, y+1) in tilemap.keys() and
            tilemap[(x-1, y+1)] not in connects
        ):
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

    @property
    def visibility(self):
        """The room's visibility.

        Returns:
            bool -- Is the room marked as visible?
        """
        return self._visible

    @visibility.setter
    def visibility(self, visible):
        """Sets the visibility of each tile.

        Arguments:
            visible {bool} -- The visibility for each tile.
        """
        for pos in self.tiles.keys():
            tile = self.tiles[pos]
            if not tile.loaded and visible:
                tile.load()
            elif tile.loaded and not visible:
                tile.unload()
        self._visible = visible
