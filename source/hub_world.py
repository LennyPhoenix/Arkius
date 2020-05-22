import copy

from . import constants as c
from .room import Room
from .ui.map import Map


class HubWorld:
    def __init__(self, application):
        self.application = application
        self.size = 1
        self.map = {}

        for x in range(-1, 2):
            for y in range(-1, 2):
                self.map[(x, y)] = Room(
                    self.application,
                    room_type=0,
                    style=c.HUB,
                    doors={i: True for i in range(4)}
                )

        self.map[(0, 0)].visibility = True
        self.ui_map = Map(self.application, self, discover=True)


class HubRoom:
    pass
