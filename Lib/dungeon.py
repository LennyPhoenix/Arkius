"""Contains class objects for Room."""

from . import tilesets


class Room(object):
    """
    Room class for dungeon.

    Args:
        Type: (int)
        Selects the room type. Versions include:
        0 = Start
        1 = Fight
        2 = Treasure
        3 = Boss
        4 = Shop
        Defaults to Start.

        Pos: (Tuple (X, Y))
        The room's position in the dungeon.
        Defaults to (0, 0).

        Doors: (Dict {DoorID: True/False})
        The open doors of the room.
        Defaults to the top door only.

        Tileset: (Dict {(X, Y): TileValue})
        The tiles that make up the room's ground.
    """

    def __init__(self, room_type=0, pos=(0, 0), doors={0: False, 1: False, 2: False, 3: False}, tileset=tilesets.basic()):  # noqa: E501
        """Initialise the Room class."""
        self.type = room_type
        self.pos = pos
        self.doors = doors
        self.ground_tiles = {}

        if self.type == 0:
            self.ground_tiles = tilesets.startRoom()
        elif self.type == 1:
            self.ground_tiles = tileset
        elif self.type == 2:
            self.ground_tiles = tilesets.treasureRoom()
        elif self.type == 3:
            self.ground_tiles = tilesets.bossRoom()
        elif self.type == 4:
            self.ground_tiles = tilesets.basic()

    def __str__(self):
        string = ""
        for y in range(15):
            for x in range(15):
                y = 14 - y
                string += f"{self.ground_tiles[(x, y)]} "
            string += "\n"
        return string
