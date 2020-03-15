"""Contains class objects for Room."""

import random
from itertools import product

from pyglet import image
from pyglet.sprite import Sprite

from . import prefabs, tilesets


class Room:
    """Room class for dungeon."""

    def __init__(self, window, room_type=0, doors={0: True, 1: True, 2: True, 3: True}, tileset=tilesets.basic()):  # noqa: E501
        """Initialise the Room class."""
        self.type = room_type
        self.doors = doors
        self.ground_tiles = {}
        self.tiles = {}
        self.cleared = room_type == 0

        border_image = image.load("resources/border.png")
        border_image.anchor_x = border_image.width // 2
        border_image.anchor_y = border_image.height // 2

        border_x, border_y = window.worldToScreen(7.5, 7.5)
        self.border = Sprite(
            border_image,
            x=border_x, y=border_y,
            batch=window.BATCH,
            group=window.UI_LAYERS[0]
        )
        self.border.scale = window.scaleFactor()

        types = {
            0: tilesets.startRoom(),
            1: tileset,
            2: tilesets.treasureRoom(),
            3: tilesets.bossRoom(),
            4: tilesets.basic()
        }

        self.ground_tiles = types[room_type]

        self.createSprites(window)

    def __str__(self):
        string = ""
        for y in range(15):
            for x in range(15):
                y = 14 - y
                string += f"{self.ground_tiles[(x, y)]} "
            string += "\n"
        return string

    def createSprites(self, window):
        """Creates all the tile sprites."""
        style = 0
        room_tiles = self.ground_tiles
        borders = {
            (-1, -1): 2,
            (-1, 15): 8,
            (15, -1): 128,
            (15, 15): 32,
            (-1, None): 14,
            (15, None): 224,
            (None, -1): 131,
            (None, 15): 56
        }
        doors = self.doors
        if doors[0]:
            door_tiles = {
                (5, 17): 14, (6, 17): 0, (7, 17): 0, (8, 17): 0, (9, 17): 224,
                (5, 16): 14, (6, 16): 0, (7, 16): 0, (8, 16): 0, (9, 16): 224,
                (5, 15): 62, (6, 15): 0, (7, 15): 0, (8, 15): 0, (9, 15): 248,
            }
            borders.update(door_tiles)
        if doors[1]:
            door_tiles = {
                (15, 9): 248, (16, 9): 56, (17, 9): 56,
                (15, 8): 0, (16, 8): 0, (17, 8): 0,
                (15, 7): 0, (16, 7): 0, (17, 7): 0,
                (15, 6): 0, (16, 6): 0, (17, 6): 0,
                (15, 5): 227, (16, 5): 131, (17, 5): 131,
            }
            borders.update(door_tiles)
        if doors[2]:
            door_tiles = {
                (5, -1): 143, (6, -1): 0, (7, -1): 0, (8, -1): 0, (9, -1): 227,
                (5, -2): 14, (6, -2): 0, (7, -2): 0, (8, -2): 0, (9, -2): 224,
                (5, -3): 14, (6, -3): 0, (7, -3): 0, (8, -3): 0, (9, -3): 224,
            }
            borders.update(door_tiles)
        if doors[3]:
            door_tiles = {
                (-3, 9): 56, (-2, 9): 56, (-1, 9): 62,
                (-3, 8): 0, (-2, 8): 0, (-1, 8): 0,
                (-3, 7): 0, (-2, 7): 0, (-1, 7): 0,
                (-3, 6): 0, (-2, 6): 0, (-1, 6): 0,
                (-3, 5): 131, (-2, 5): 131, (-1, 5): 143,
            }
            borders.update(door_tiles)

        for x, y in product(range(-3, 18), repeat=2):
            if (x, y) in borders.keys() and borders[(x, y)] > 0:
                value = borders[(x, y)]
                tile_type = 1
            elif (x, y) in borders.keys() and borders[(x, y)] == 0:
                value = random.randint(0, 9)
                tile_type = 0
            elif (x, None) in borders.keys() and -1 <= y and y <= 15:
                value = borders[(x, None)]
                tile_type = 1
            elif (None, y) in borders.keys() and -1 <= x and x <= 15:
                value = borders[(None, y)]
                tile_type = 1
            elif (x, y) in room_tiles.keys():
                tile_type = room_tiles[(x, y)]
                if tile_type == 0:
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
        border_x, border_y = window.worldToScreen(7.5, 7.5, True)
        self.border.update(
            x=border_x,
            y=border_y
        )
        for x, y in product(range(-3, 18), repeat=2):
            if (x, y) in self.tiles.keys():
                self.tiles[(x, y)].update(window)

    def resize(self, window):
        border_x, border_y = window.worldToScreen(7.5, 7.5, True)
        self.border.update(
            x=border_x,
            y=border_y
        )
        self.border.scale = window.scaleFactor()
        for x, y in product(range(-3, 18), repeat=2):
            if (x, y) in self.tiles.keys():
                self.tiles[(x, y)].resize(window)

    def getBitValue(self, x, y):
        """Returns the bitmasking value of a tile."""
        tileset = self.ground_tiles
        tileID = tileset[(x, y)]
        value = 0

        sides = {
            128: False, 1: False,   2: False,
            64: False,              4: False,
            32: False,  16: False,  8: False
        }

        edges = [tileID]

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

    def getUV(self, tile_type, tile_value):
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


class Dungeon:
    """Dungeon class, contains rooms."""

    def __init__(self, window):
        self.rooms = {}
        self.style = 0

        self.rooms[(0, 0)] = Room(window)
