"""Contains class objects for Room."""

from . import tilesets


class Room(object):
    """Room class for dungeon."""

    def __init__(self, roomType=0, pos=(0, 0), doors={0: True, 1: False, 2: False, 3: False}, tileset=tilesets.basic()):  # noqa: E501
        """
        Initialise the Room class.

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
        """
        self.type = roomType
        self.pos = pos
        self.doors = doors
        self.groundTiles = {}

        if self.type == 0:
            self.groundTiles = tilesets.startRoom()
        elif self.type == 1:
            self.groundTiles = tileset
        elif self.type == 2:
            self.groundTiles = tilesets.treasureRoom()
        elif self.type == 3:
            self.groundTiles = tilesets.bossRoom()
        elif self.type == 4:
            self.groundTiles = tilesets.basic()
