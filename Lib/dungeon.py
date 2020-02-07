"""Contains class objects for Room."""


class Room(object):
    """Room class for dungeon."""

    def __init__(self, roomType=0, pos=(0, 0), doors={0: True, 1: False, 2: False, 3: False}):  # noqa: E501
        """Initialise the Room class.

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
          The rooms position in the dungeon.
          Defaults to (0, 0).

          Doors: (Dict {DoorID: True/False})
          The open doors of the room.
          Defaults to the top door only.


        """
        self.type = roomType
        self.pos = pos
        self.doors = doors
        self.groundTiles = {  # TODO

        }
        self.obstacleTiles = {  # TODO
            (0, 0): 0, (1, 0): 0, (2, 0): 0, (3, 0): 0, (4, 0): 0, (5, 0): 0, (6, 0): 0,  # noqa: E501
            (0, 1): 0, (1, 1): 0, (2, 1): 1, (3, 1): 1, (4, 1): 1, (5, 1): 1, (6, 1): 0,  # noqa: E501
            (0, 2): 0, (1, 2): 0, (2, 2): 2, (3, 2): 1, (4, 2): 1, (5, 2): 1, (6, 2): 0,  # noqa: E501
            (0, 3): 0, (1, 3): 0, (2, 3): 1, (3, 3): 1, (4, 3): 1, (5, 3): 1, (6, 3): 0,  # noqa: E501
            (0, 4): 0, (1, 4): 0, (2, 4): 1, (3, 4): 1, (4, 4): 1, (5, 4): 1, (6, 4): 0,  # noqa: E501
            (0, 5): 0, (1, 5): 0, (2, 5): 1, (3, 5): 1, (4, 5): 1, (5, 5): 1, (6, 5): 0,  # noqa: E501
            (0, 6): 0, (1, 6): 0, (2, 6): 1, (3, 6): 1, (4, 6): 1, (5, 6): 1, (6, 6): 0  # noqa: E501
        }
