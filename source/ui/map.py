
import pyglet

from .. import constants as c


class Map:
    def __init__(self, application, world, discover=False):
        self.application = application
        self.world = world
        map_image = self.application.resources["ui"]["map"]["window"]
        map_layer = self.application.layers["ui"]["map_window"]
        self.map_window = pyglet.sprite.Sprite(
            map_image,
            0, 0,
            batch=self.application.ui_batch,
            group=map_layer
        )
        self.map_window.opacity = 200

        room_max = 0
        for pos in self.world.map.keys():
            for i in range(2):
                if abs(pos[i]) > room_max:
                    room_max = abs(pos[i])

        self.map_rooms = {}
        for pos, room in self.world.map.items():
            if discover:
                image = self.application.resources["ui"]["map"]["rooms"][(
                    1, room.door_value
                )]
            else:
                image = self.application.resources["ui"]["map"]["rooms"][(
                    3, room.door_value
                )]
            icon = self.application.resources["ui"]["map"]["icons"][room.type]
            self.map_rooms[pos] = {}
            self.map_rooms[pos]["sprite"] = pyglet.sprite.Sprite(
                image,
                0, 0,
                batch=self.application.ui_batch,
                group=self.application.layers["ui"]["map_rooms"]
            )
            self.map_rooms[pos]["icon"] = pyglet.sprite.Sprite(
                icon,
                0, 0,
                batch=self.application.ui_batch,
                group=self.application.layers["ui"]["map_icons"]
            )
            self.map_rooms[pos]["icon"].visible = discover
            self.map_rooms[pos]["visited"] = discover
            self.map_rooms[pos]["room"] = room

        self.update_position()
        self.discover((0, 0))
        self.application.pushHandler(self)

    def update_position(self):
        scale = min(
            self.application.window.width,
            self.application.window.height
        ) / c.MIN_SIZE[1]

        self.map_window.scale = scale
        self.map_window.update(
            x=(
                self.application.window.width -
                self.map_window.width
            ),
            y=(
                self.application.window.height -
                self.map_window.height
            )
        )

        for pos in self.map_rooms.keys():
            self.map_rooms[pos]["sprite"].scale = (
                scale / (self.world.size / c.DEFAULT_WORLD_SIZE)
            )
            self.map_rooms[pos]["sprite"].update(
                x=(
                    self.map_window.x +
                    self.map_window.width//2 -
                    self.map_rooms[pos]["sprite"].width//2 +
                    pos[0]*12 *
                    scale/(self.world.size/c.DEFAULT_WORLD_SIZE)
                ),
                y=(
                    self.map_window.y +
                    self.map_window.height//2 -
                    self.map_rooms[pos]["sprite"].height//2 +
                    pos[1]*12 *
                    scale/(self.world.size/c.DEFAULT_WORLD_SIZE)
                )
            )
            self.map_rooms[pos]["icon"].scale = (
                scale / (self.world.size / c.DEFAULT_WORLD_SIZE)
            )
            self.map_rooms[pos]["icon"].update(
                x=(
                    self.map_window.x +
                    self.map_window.width//2 -
                    self.map_rooms[pos]["icon"].width//2 +
                    pos[0]*12 *
                    scale/(self.world.size/c.DEFAULT_WORLD_SIZE)
                ),
                y=(
                    self.map_window.y +
                    self.map_window.height//2 -
                    self.map_rooms[pos]["icon"].height//2 +
                    pos[1]*12 *
                    scale/(self.world.size/c.DEFAULT_WORLD_SIZE)
                )
            )

    def discover(self, pos):
        neighbours = {
            (1, 0): 1,
            (-1, 0): 3,
            (0, -1): 2,
            (0, 1): 0
        }
        image = self.application.resources["ui"]["map"]["rooms"][(
            0, self.map_rooms[pos]["room"].door_value
        )]
        self.map_rooms[pos]["sprite"].image = image
        self.map_rooms[pos]["visited"] = True
        self.map_rooms[pos]["icon"].visible = True

        for (x, y), door in neighbours.items():
            n_x, n_y = x+pos[0], y+pos[1]
            if (
                (n_x, n_y) in self.map_rooms.keys() and
                self.world.map[pos].doors[door]
            ):
                if self.map_rooms[(n_x, n_y)]["visited"]:
                    image = self.application.resources["ui"]["map"]["rooms"][(
                        1, self.map_rooms[(n_x, n_y)]["room"].door_value
                    )]
                else:
                    image = self.application.resources["ui"]["map"]["rooms"][(
                        2, self.map_rooms[(n_x, n_y)]["room"].door_value
                    )]
                self.map_rooms[(
                    n_x, n_y
                )]["sprite"].image = image
                self.map_rooms[(n_x, n_y)]["icon"].visible = True

    def on_resize(self, width, height):
        self.update_position()

    def delete(self):
        self.map_window.delete()
        for pos in self.map_rooms.keys():
            self.map_rooms[pos]["icon"].delete()
            self.map_rooms[pos]["sprite"].delete()
        del self.map_rooms
