"""Contains dungeon class."""
import random

from . import constants as c
from .room import Room


class Dungeon:
    """Dungeon class, contains room map."""

    def __init__(self, window, style, config=None):
        """Define the style and dungeon configuration.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
            style {int} -- The tileset/style of the dungeon.

        Keyword Arguments:
            config {dict} -- The dungeon config to use for room
                             numbering. (default: {None})
        """
        self.style = style
        self.map = {}
        self.config = config

        if self.config is None:
            self.config = c.DUNGEON_BASE

        self.generateRooms(window)

    def generateRooms(self, window):
        """Place and create each room.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        gen_map = {}
        neighbours = {
            (1, 0): (1, 3),
            (-1, 0): (3, 1),
            (0, -1): (2, 0),
            (0, 1): (0, 2)
        }
        gen_map[(0, 0)] = {
            "type": c.START_ROOM,
            "doors": {i: False for i in range(4)}
        }
        for room_type in self.config["rooms"].keys():
            planted = 0
            while planted < self.config["rooms"][room_type]:
                pos = random.choice(list(gen_map.keys()))
                x, y = random.choice(list(neighbours.keys()))
                n_x, n_y = pos[0] + x, pos[1] + y
                doors = neighbours[(x, y)]

                if (
                    (
                        gen_map[(pos)]["type"] == c.START_ROOM or
                        gen_map[(pos)]["type"] == c.BOSS_ROOM
                    ) and
                    (
                        room_type == c.START_ROOM or
                        room_type == c.BOSS_ROOM
                    )
                ):
                    continue

                if (
                    gen_map[(pos)]["type"] == c.TREASURE_ROOM and
                    room_type == c.TREASURE_ROOM
                ):
                    continue

                if not (
                    -3 <= n_x <= 3 and
                    -3 <= n_y <= 3
                ):
                    continue

                if (n_x, n_y) not in gen_map.keys():
                    gen_map[pos]["doors"][doors[0]] = True
                    gen_map[(n_x, n_y)] = {
                        "type": room_type,
                        "doors": {i: (i == doors[1]) for i in range(4)}
                    }
                    planted += 1

        planted = 0
        while planted < self.config["connections"]:
            pos = random.choice(list(gen_map.keys()))
            x, y = random.choice(list(neighbours.keys()))
            n_x, n_y = pos[0] + x, pos[1] + y
            doors = neighbours[(x, y)]

            if (n_x, n_y) in gen_map.keys():

                if (
                    (
                        gen_map[(pos)]["type"] == c.START_ROOM or
                        gen_map[(pos)]["type"] == c.BOSS_ROOM
                    ) and
                    (
                        gen_map[(n_x, n_y)]["type"] == c.START_ROOM and
                        gen_map[(n_x, n_y)]["type"] == c.BOSS_ROOM
                    )
                ):
                    continue

                if (
                    gen_map[(pos)]["type"] == c.TREASURE_ROOM and
                    gen_map[(n_x, n_y)]["type"] == c.TREASURE_ROOM
                ):
                    continue

                gen_map[pos]["doors"][doors[0]] = True
                gen_map[(n_x, n_y)]["doors"][doors[1]] = True
                planted += 1

        for pos, data in gen_map.items():
            self.map[pos] = Room(
                window,
                room_type=data["type"],
                dungeon_style=self.style,
                doors=data["doors"]
            )
