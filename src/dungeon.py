"""Contains dungeon class."""
import random

from . import constants as c
from .room import Room
from .ui.map import Map


class Dungeon:
    """Dungeon class, contains room map."""

    def __init__(self, window, style, config=None):
        """Define the style and dungeon configuration.

        Arguments:
            window {Window} -- The window for the application.
            style {int} -- The tileset/style of the dungeon.

        Keyword Arguments:
            config {dict} -- The dungeon config to use for room
                             numbering. (default: {None})
        """
        self.window = window
        self.style = style
        self.map = {}
        self.config = config

        if self.config is None:
            self.config = c.DUNGEON_BASE
        self.size = self.config["size"]

        self.generateRooms()
        self.map[(0, 0)].visibility = True
        self.ui_map = Map(self.window, self)

    def generateRooms(self):
        """Place and create each room."""
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
        config = self.config.copy()
        while len(config["rooms"]) > 0:
            room_type = random.choice(list(config["rooms"].keys()))
            pos = random.choice(list(gen_map.keys()))
            x, y = random.choice(list(neighbours.keys()))
            n_x, n_y = pos[0] + x, pos[1] + y
            doors = neighbours[(x, y)]

            if (
                room_type in c.ROOM_INFO[
                    gen_map[pos]["type"]
                ]["dont_connect"]
            ):
                continue

            if not (
                -self.size <= n_x <= self.size and
                -self.size <= n_y <= self.size
            ):
                continue

            if (n_x, n_y) not in gen_map.keys():
                gen_map[pos]["doors"][doors[0]] = True
                gen_map[(n_x, n_y)] = {
                    "type": room_type,
                    "doors": {i: (i == doors[1]) for i in range(4)}
                }
                config["rooms"][room_type] -= 1
                if config["rooms"][room_type] <= 0:
                    del config["rooms"][room_type]

        planted = 0
        while planted < self.config["connections"]:
            pos = random.choice(list(gen_map.keys()))
            x, y = random.choice(list(neighbours.keys()))
            n_x, n_y = pos[0] + x, pos[1] + y
            doors = neighbours[(x, y)]

            if (n_x, n_y) in gen_map.keys():
                if (
                    gen_map[pos]["type"] in c.ROOM_INFO[
                        gen_map[(n_x, n_y)]["type"]
                    ]["dont_connect"] or
                    gen_map[(n_x, n_y)]["type"] in c.ROOM_INFO[
                        gen_map[pos]["type"]
                    ]["dont_connect"]
                ):
                    continue

                gen_map[pos]["doors"][doors[0]] = True
                gen_map[(n_x, n_y)]["doors"][doors[1]] = True
                planted += 1

        for pos, data in gen_map.items():
            self.map[pos] = Room(
                self.window,
                room_type=data["type"],
                style=self.style,
                doors=data["doors"]
            )
