import random

from . import constants as c
from .room import Room


class Dungeon:
    def __init__(self, window, style, config=None):
        self.style = style
        self.map = {}
        self.config = config

        if self.config is None:
            self.config = c.DUNGEON_BASE

        self.generateRooms(window)

    def generateRooms(self, window):
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
        for room_type in c.ROOM_INFO.keys():
            if room_type == c.START_ROOM:
                continue
            planted = 0
            while planted < self.config["rooms"][room_type]:
                pos = random.choice(list(gen_map.keys()))
                x, y = random.choice(list(neighbours.keys()))
                n_x, n_y = pos[0] + x, pos[1] + y
                doors = neighbours[(x, y)]

                gen_map[pos]["doors"][doors[0]] = True

                if (n_x, n_y) not in gen_map.keys():
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