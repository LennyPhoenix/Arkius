import copy

from . import constants as c
from .room import Room
from .ui.map import Map

MAP_LAYOUT = {
    (0, 0): {
        "map": [
        ]
    }
}


class HubWorld:
    def __init__(self, application):
        self.application = application
        self.size = 1
        self.map = {

        }

        self.map[(0, 0)].visibility = True
        self.ui_map = Map(self.application, self, discover=True)


class HubRoom:
    _visible = False

    def __init__(self, application, tilemap, objects):
        self.application = application
        self.tilemap = copy.deepcopy(tilemap)
        self.tiles = {}
        self.style = c.HUB

    @property
    def visibility(self):
        return self._visible

    @visibility.setter
    def visibility(self, visible):

        if self.visibility == visible:
            return

        for pos in self.tiles.keys():
            tile = self.tiles[pos]
            if not tile.loaded and visible:
                tile.load()
            elif tile.loaded and not visible:
                tile.unload()
        self._visible = visible

    def delete(self):
        for pos in self.tiles.keys():
            self.tiles[pos].sprite.delete()
        del self.tiles
