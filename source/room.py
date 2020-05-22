import random

import pymunk

from . import constants as c
from . import tilemaps
from .tile import Tile


class Room:

    def __init__(
        self,
        application,
        room_type=c.START_ROOM,
        style=None, room_config=None, doors=None
    ):
        self.application = application
        self.type = room_type
        self.doors = doors
        self.base = {}
        self.tilemap = {}
        self.tiles = {}
        self.cleared = self.type == c.START_ROOM
        self._visible = False
        self.style = style
        self.config = room_config

        self.space = pymunk.Space(threaded=True)
        self.space.damping = 0

        if self.style is None:
            self.style = self.application.world.style

        if self.doors is None:
            self.doors = {i: False for i in range(4)}

        self.door_value = 0
        for i in range(4):
            if self.doors[i]:
                self.door_value += 2**i

        if self.config is None:
            self.config = random.choice(
                c.ROOM_INFO[self.type]["configs"][self.style]
            )

        self.map_data = random.choice(self.config["maps"])

        if self.map_data is not None:
            self.map_data = self.map_data.copy()
            self.width = self.map_data["width"]
            self.height = self.map_data["height"]
        else:
            self.width = c.ROOM_INFO[self.type]["default_dimensions"][0]
            self.height = c.ROOM_INFO[self.type]["default_dimensions"][1]

        self.border_colliders = {
            "top": pymunk.Segment(
                self.space.static_body,
                (
                    -(self.width+2.5)*c.TILE_SIZE,
                    (self.height+3.5)*c.TILE_SIZE
                ),
                (
                    (self.width+3.5)*c.TILE_SIZE,
                    (self.height+3.5)*c.TILE_SIZE
                ),
                1
            ),
            "right": pymunk.Segment(
                self.space.static_body,
                (
                    (self.width+3.5)*c.TILE_SIZE,
                    -(self.height+2.5)*c.TILE_SIZE
                ),
                (
                    (self.width+3.5)*c.TILE_SIZE,
                    (self.height+3.5)*c.TILE_SIZE
                ),
                1
            ),
            "bottom": pymunk.Segment(
                self.space.static_body,
                (
                    -(self.width+2.5)*c.TILE_SIZE,
                    -(self.height+2.5)*c.TILE_SIZE
                ),
                (
                    (self.width+3.5)*c.TILE_SIZE,
                    -(self.height+2.5)*c.TILE_SIZE
                ),
                1
            ),
            "left": pymunk.Segment(
                self.space.static_body,
                (
                    -(self.width+2.5)*c.TILE_SIZE,
                    -(self.height+2.5)*c.TILE_SIZE
                ),
                (
                    -(self.width+2.5)*c.TILE_SIZE,
                    (self.height+3.5)*c.TILE_SIZE
                ),
                1
            )
        }
        self.border_colliders[
            "top"
        ].collision_type = c.COLLISION_TYPES["room_border"]
        self.border_colliders[
            "right"
        ].collision_type = c.COLLISION_TYPES["room_border"]
        self.border_colliders[
            "bottom"
        ].collision_type = c.COLLISION_TYPES["room_border"]
        self.border_colliders[
            "left"
        ].collision_type = c.COLLISION_TYPES["room_border"]
        self.space.add(self.border_colliders["top"])
        self.space.add(self.border_colliders["right"])
        self.space.add(self.border_colliders["bottom"])
        self.space.add(self.border_colliders["left"])

        def begin(arbiter, space, data):
            shapes = arbiter.shapes
            player = shapes[0].body
            border = shapes[1]

            ids = {
                self.border_colliders["top"]: 0,
                self.border_colliders["right"]: 1,
                self.border_colliders["bottom"]: 2,
                self.border_colliders["left"]: 3
            }
            player.triggerDoor(ids[border])

            return True

        h = self.space.add_collision_handler(
            c.COLLISION_TYPES["player"], c.COLLISION_TYPES["room_border"]
        )
        h.begin = begin

        self.base = tilemaps.create_blank(
            self.width,
            self.height
        )

        if (
            self.map_data is not None and
            self.map_data["matrix"] is not None
        ):
            self.base.update(tilemaps.toMap(self.map_data["matrix"]))
            for i in range(4):
                if type(self.map_data["door_info"][i]["pos"]) is tuple:
                    self.map_data["door_info"][i]["pos"] = random.randint(
                        *self.map_data["door_info"][i]["pos"]
                    )

        active_doors = [key for key, value in self.doors.items() if value]
        possible = False
        while not possible:
            self.tilemap = self.base.copy()
            self.tilemap = tilemaps.generate(
                self.type,
                self.tilemap,
                self.config["options"],
                self.map_data
            )
            self.tilemap = tilemaps.add_boundaries(
                self.type,
                self.tilemap,
                self.doors,
                self.map_data
            )

            if len(active_doors) > 0:
                starting_door = random.choice(active_doors)
                door_p = {}
                for i in range(4):
                    if self.map_data is not None:
                        if i == 0:
                            door_p[i] = (
                                self.map_data["door_info"][i]["pos"],
                                self.height
                            )
                        elif i == 1:
                            door_p[i] = (
                                self.width,
                                self.map_data["door_info"][i]["pos"]
                            )
                        elif i == 2:
                            door_p[i] = (
                                self.map_data["door_info"][i]["pos"],
                                -self.height
                            )
                        elif i == 3:
                            door_p[i] = (
                                -self.width,
                                self.map_data["door_info"][i]["pos"]
                            )
                    else:
                        if i == 0:
                            door_p[i] = (
                                0,
                                self.height
                            )
                        elif i == 1:
                            door_p[i] = (
                                self.width,
                                0
                            )
                        elif i == 2:
                            door_p[i] = (
                                0,
                                -self.height
                            )
                        elif i == 3:
                            door_p[i] = (
                                -self.width,
                                0
                            )

                neighbours = [
                    (0, 1),
                    (1, 0),
                    (0, -1),
                    (-1, 0)
                ]
                self.reached = [door_p[starting_door]]
                reachable = []
                for x, y in neighbours:
                    n_x = x+door_p[starting_door][0]
                    n_y = y+door_p[starting_door][1]
                    if (
                        (n_x, n_y) in self.tilemap.keys() and
                        (n_x, n_y) not in reachable and
                        (n_x, n_y) not in self.reached and
                        c.TILES[self.tilemap[
                            (n_x, n_y)
                        ]]["collider"] is None
                    ):
                        reachable.append((n_x, n_y))

                while len(reachable) > 0:
                    pos = random.choice(reachable)
                    self.reached.append(pos)
                    reachable.remove(pos)

                    for x, y in neighbours:
                        n_x = x+pos[0]
                        n_y = y+pos[1]
                        if (
                            (n_x, n_y) in self.tilemap.keys() and
                            (n_x, n_y) not in reachable and
                            (n_x, n_y) not in self.reached and
                            c.TILES[self.tilemap[
                                (n_x, n_y)
                            ]]["collider"] is None
                        ):
                            reachable.append((n_x, n_y))

                possible = True
                for x, y in door_p.values():
                    if (x, y) not in self.reached:
                        possible = False
            else:
                possible = True

    def createSprites(self):
        for x in range(-(self.width+3), self.width+4):
            for y in range(-(self.height+3), self.height+4):
                if (x, y) in self.tilemap.keys():
                    tile = Tile(
                        self.application,
                        self,
                        x, y
                    )
                    self.tiles[(x, y)] = tile

    def getImageIndex(self, x, y):
        tilemap = self.tilemap
        tileID = tilemap[(x, y)]
        value = 0

        sides = {
            128: False, 1: False,   2: False,
            64: False,              4: False,
            32: False,  16: False,  8: False
        }

        connects = c.TILES[tileID]["sprite"]["connects"]

        if (x, y+1) in tilemap.keys() and tilemap[(x, y+1)] not in connects:
            sides.update({128: True, 1: True, 2: True})
        if (x+1, y) in tilemap.keys() and tilemap[(x+1, y)] not in connects:
            sides.update({2: True, 4: True, 8: True})
        if (x, y-1) in tilemap.keys() and tilemap[(x, y-1)] not in connects:
            sides.update({8: True, 16: True, 32: True})
        if (x-1, y) in tilemap.keys() and tilemap[(x-1, y)] not in connects:
            sides.update({32: True, 64: True, 128: True})

        if (
            (x+1, y+1) in tilemap.keys() and
            tilemap[(x+1, y+1)] not in connects
        ):
            sides[2] = True
        if (
            (x+1, y-1) in tilemap.keys() and
            tilemap[(x+1, y-1)] not in connects
        ):
            sides[8] = True
        if (
            (x-1, y-1) in tilemap.keys() and
            tilemap[(x-1, y-1)] not in connects
        ):
            sides[32] = True
        if (
            (x-1, y+1) in tilemap.keys() and
            tilemap[(x-1, y+1)] not in connects
        ):
            sides[128] = True

        for side in sides.keys():
            if sides[side]:
                value += side

        index_dict = {
            34: 2, 136: 3, 226: 4, 184: 5, 58: 6, 142: 7, 138: 8, 162: 9,
            251: 10, 187: 11, 191: 12, 255: 13, 139: 14, 46: 15, 232: 16,
            163: 17, 42: 18, 168: 19, 248: 20, 56: 21, 62: 22, 254: 23,
            250: 24, 186: 25, 190: 26, 2: 27, 130: 28, 128: 29, 224: 30, 0: 31,
            14: 32, 238: 33, 234: 34, 174: 36, 10: 37, 170: 38, 160: 39,
            227: 40, 131: 41, 143: 42, 239: 43, 235: 44, 171: 45, 175: 46,
            8: 47, 40: 48, 32: 49
        }

        return index_dict[value]

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
            tile = self.tiles[pos]
            tile.sprite.delete()
        self.tiles = None
