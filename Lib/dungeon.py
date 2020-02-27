"""Contains class objects for Room."""

from . import tilesets
from . import prefabs
from . import getBitValue

import random
from pyglet import image


class Room():
    """Room class for dungeon."""

    def __init__(self, window, batch, groups, room_type=0, pos=(0, 0), doors={0: False, 1: False, 2: False, 3: False}, tileset=tilesets.basic()):  # noqa: E501
        """Initialise the Room class."""
        self.type = room_type
        self.pos = pos
        self.doors = doors
        self.ground_tiles = {}
        self.tiles = {}
        self.cleared = room_type == 0

        types = {
            0: tilesets.startRoom(),
            1: tileset,
            2: tilesets.treasureRoom(),
            3: tilesets.bossRoom(),
            4: tilesets.basic()
        }

        self.ground_tiles = types[room_type]

        self.createSprites(window, batch, groups)

    def __str__(self):
        string = ""
        for y in range(15):
            for x in range(15):
                y = 14 - y
                string += f"{self.ground_tiles[(x, y)]} "
            string += "\n"
        return string

    def createSprites(self, window, batch, groups):
        """Creates all the tile sprites."""
        style = 0
        for x in range(15):
            for y in range(15):
                room_tiles = self.ground_tiles
                tile_id = room_tiles[(x, y)]

                if tile_id != 0:
                    value = getBitValue(room_tiles, x, y)
                    image_path = f"Images/Tiles/{style}/{tile_id}/{value}.png"
                else:
                    floor_type = random.randint(0, 3)
                    image_path = f"Images/Tiles/{style}/0/{floor_type}.png"
                tile_image = image.load(image_path)
                tile_image.anchor_x = 0
                tile_image.anchor_y = 0

                tile = prefabs.Tile(
                    window=window,
                    tile_group=groups[14-y],
                    batch=batch,
                    x=x, y=y,
                    tile_image=tile_image
                )
                self.tiles[(x, y)] = tile

        for x in range(-1, 16):
            for y in range(-1, 16):

                value = None
                values = {
                    (-1, -1): 2,
                    (-1, 15): 8,
                    (15, -1): 128,
                    (15, 15): 32
                }

                if x == -1:
                    value = 14
                elif x == 15:
                    value = 224
                elif y == -1:
                    value = 131
                elif y == 15:
                    value = 56

                if (x, y) in values.keys():
                    value = values[(x, y)]

                if value is not None:
                    image_path = f"Images/Tiles/{style}/1/{value}.png"
                    tile_image = image.load(image_path)
                    tile_image.anchor_x = 0
                    tile_image.anchor_y = 0

                    tile = prefabs.Tile(
                        window=window,
                        tile_group=groups[14-y],
                        batch=batch,
                        x=x, y=y,
                        tile_image=tile_image
                    )
                    self.tiles[(x, y)] = tile

    def resize(self, window, scale_factor):
        for x in range(-1, 16):
            for y in range(-1, 16):
                self.tiles[(x, y)].resize(window, scale_factor)
