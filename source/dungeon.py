import copy
import random

from . import constants as c
from .room import Room
from .ui.map import Map


class Dungeon:

    def __init__(self, application, style, config=None):
        self.application = application
        self.style = style
        self.map = {}

        if config is None:
            config = c.DUNGEON_BASE
        self.config = copy.deepcopy(config)
        self.size = self.config["size"]

        self.generateMap()
        self.generateRooms()
        self.generateTiles()
        self.map[(0, 0)].visibility = True
        self.ui_map = Map(self.application, self)

    def generateMap(self):
        self.gen_map = {}
        neighbours = {
            (1, 0): (1, 3),
            (-1, 0): (3, 1),
            (0, -1): (2, 0),
            (0, 1): (0, 2)
        }
        self.gen_map[(0, 0)] = {
            "type": c.START_ROOM,
            "doors": {i: False for i in range(4)}
        }

        config = copy.deepcopy(self.config)
        while len(config["rooms"]) > 0:
            room_type = random.choice(list(config["rooms"].keys()))
            pos = random.choice(list(self.gen_map.keys()))
            x, y = random.choice(list(neighbours.keys()))
            n_x, n_y = pos[0] + x, pos[1] + y
            doors = neighbours[(x, y)]

            if (
                room_type in c.ROOM_INFO[
                    self.gen_map[pos]["type"]
                ]["dont_connect"]
            ):
                continue

            if not (
                -self.size <= n_x <= self.size and
                -self.size <= n_y <= self.size
            ):
                continue

            if (n_x, n_y) not in self.gen_map.keys():
                self.gen_map[pos]["doors"][doors[0]] = True
                self.gen_map[(n_x, n_y)] = {
                    "type": room_type,
                    "doors": {i: (i == doors[1]) for i in range(4)}
                }
                config["rooms"][room_type] -= 1
                if config["rooms"][room_type] <= 0:
                    del config["rooms"][room_type]

        planted = 0
        while planted < self.config["connections"]:
            pos = random.choice(list(self.gen_map.keys()))
            x, y = random.choice(list(neighbours.keys()))
            n_x, n_y = pos[0] + x, pos[1] + y
            doors = neighbours[(x, y)]

            if (n_x, n_y) in self.gen_map.keys():
                if (
                    self.gen_map[pos]["type"] in c.ROOM_INFO[
                        self.gen_map[(n_x, n_y)]["type"]
                    ]["dont_connect"] or
                    self.gen_map[(n_x, n_y)]["type"] in c.ROOM_INFO[
                        self.gen_map[pos]["type"]
                    ]["dont_connect"]
                ):
                    continue

                self.gen_map[pos]["doors"][doors[0]] = True
                self.gen_map[(n_x, n_y)]["doors"][doors[1]] = True
                planted += 1

    def generateRooms(self):
        for pos, data in self.gen_map.items():
            self.map[pos] = Room(
                self.application,
                room_type=data["type"],
                style=self.style,
                doors=data["doors"]
            )

    def generateTiles(self):
        for pos, room in self.map.items():
            self.map[pos].createSprites()

    def delete(self):
        for pos in self.map.keys():
            room = self.map[pos]
            room.delete()
        self.ui_map.delete()
        del self.map
        del self.ui_map
