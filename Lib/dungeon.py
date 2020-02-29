"""Contains class objects for Room."""

from . import tilesets
from . import prefabs
from . import getBitValue

import random
from itertools import product
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
        for x, y in product(range(-1, 16), repeat=2):
            values = {
                (-1, -1): 2,
                (-1, 15): 8,
                (15, -1): 128,
                (15, 15): 32,
                (-1, None): 14,
                (15, None): 224,
                (None, -1): 131,
                (None, 15): 56
            }

            try:
                image_path = f"Images/Tiles/{style}/1/{values[(x, y)]}.png"
            except KeyError:
                try:
                    image_path = f"Images/Tiles/{style}/1/{values[(x, None)]}.png"  # noqa: E501
                except KeyError:
                    try:
                        image_path = f"Images/Tiles/{style}/1/{values[(None, y)]}.png"  # noqa: E501
                    except KeyError:
                        room_tiles = self.ground_tiles
                        tile_id = room_tiles[(x, y)]

                        if tile_id != 0:
                            value = getBitValue(room_tiles, x, y)
                            image_path = f"Images/Tiles/{style}/{tile_id}/{value}.png"  # noqa: E501
                        else:
                            floor_type = random.randint(0, 3)
                            image_path = f"Images/Tiles/{style}/0/{floor_type}.png"  # noqa: E501
                        tile_image = image.load(image_path)
                        tile_image.anchor_x = 0
                        tile_image.anchor_y = 0

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

    def resize(self, window):
        for x, y in product(range(-1, 16), repeat=2):
            self.tiles[(x, y)].update(window)
