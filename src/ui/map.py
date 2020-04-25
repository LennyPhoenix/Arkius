"""The ui map for a dungeon."""

import pyglet


class Map:
    def __init__(self, window, dungeon):
        """Initialise the map with all rooms/

        Arguments:
            window {Window} -- The application window.
            dungeon {Dungeon} -- The dungeon for the map.
        """
        self.window = window
        self.dungeon = dungeon
        map_image = self.window.resources["ui"]["map"]["window"]
        map_layer = self.window.layers["ui_layers"]["map_window"]
        scale_factor = self.window.scale_factor*1.5
        self.map_window = pyglet.sprite.Sprite(
            map_image,
            x=(
                self.window.width -
                map_image.width *
                scale_factor
            ),
            y=(
                self.window.height -
                map_image.height *
                scale_factor
            ),
            batch=self.window.ui_batch,
            group=map_layer
        )
        self.map_window.scale = scale_factor
        self.map_window.opacity = 200

        room_max = 0
        for pos in self.dungeon.map.keys():
            for i in range(2):
                if abs(pos[i]) > room_max:
                    room_max = abs(pos[i])

        self.map_rooms = {}
        for pos, room in self.dungeon.map.items():
            image = self.window.resources["ui"]["map"]["rooms"][(
                3, room.door_value
            )]
            icon = self.window.resources["ui"]["map"]["icons"][room.type]
            self.map_rooms[pos] = {}
            self.map_rooms[pos]["sprite"] = pyglet.sprite.Sprite(
                image,
                x=(
                    self.map_window.x +
                    self.map_window.width//2 -
                    image.width//2*scale_factor +
                    pos[0]*12*scale_factor
                ),
                y=(
                    self.map_window.y +
                    self.map_window.height//2 -
                    image.height//2*scale_factor +
                    pos[1]*12*scale_factor
                ),
                batch=self.window.ui_batch,
                group=self.window.layers["ui_layers"]["map_rooms"]
            )
            self.map_rooms[pos]["sprite"].scale = scale_factor
            self.map_rooms[pos]["icon"] = pyglet.sprite.Sprite(
                icon,
                x=(
                    self.map_window.x +
                    self.map_window.width//2 -
                    icon.width//2*scale_factor +
                    pos[0]*12*scale_factor
                ),
                y=(
                    self.map_window.y +
                    self.map_window.height//2 -
                    icon.height//2*scale_factor +
                    pos[1]*12*scale_factor
                ),
                batch=self.window.ui_batch,
                group=self.window.layers["ui_layers"]["map_icons"]
            )
            self.map_rooms[pos]["icon"].scale = scale_factor
            self.map_rooms[pos]["icon"].visible = False
            self.map_rooms[pos]["visited"] = False
            self.map_rooms[pos]["room"] = room

        self.discover((0, 0))

    def discover(self, pos):
        """Discover rooms on the map.

        Arguments:
            pos {tuple} -- The x and y position to discover.
        """
        neighbours = {
            (1, 0): 1,
            (-1, 0): 3,
            (0, -1): 2,
            (0, 1): 0
        }
        image = self.window.resources["ui"]["map"]["rooms"][(
            0, self.map_rooms[pos]["room"].door_value
        )]
        self.map_rooms[pos]["sprite"].image = image
        self.map_rooms[pos]["visited"] = True
        self.map_rooms[pos]["icon"].visible = True

        for (x, y), door in neighbours.items():
            n_x, n_y = x+pos[0], y+pos[1]
            if (
                (n_x, n_y) in self.map_rooms.keys() and
                self.dungeon.map[pos].doors[door]
            ):
                if self.map_rooms[(n_x, n_y)]["visited"]:
                    image = self.window.resources["ui"]["map"]["rooms"][(
                        1, self.map_rooms[(n_x, n_y)]["room"].door_value
                    )]
                else:
                    image = self.window.resources["ui"]["map"]["rooms"][(
                        2, self.map_rooms[(n_x, n_y)]["room"].door_value
                    )]
                self.map_rooms[(
                    n_x, n_y
                )]["sprite"].image = image
                self.map_rooms[(n_x, n_y)]["icon"].visible = True

    def resize(self):
        """Resize the map."""
        scale_factor = self.window.scale_factor
        self.map_window.scale = scale_factor
        self.map_window.update(
            x=(
                self.window.width -
                self.map_window.width
            ),
            y=(
                self.window.height -
                self.map_window.height
            )
        )
        for pos, room in self.dungeon.map.items():
            self.map_rooms[pos]["sprite"].update(
                x=(
                    self.map_window.x +
                    self.map_window.width//2 -
                    self.map_rooms[pos]["sprite"].width//2 +
                    pos[0]*12*scale_factor
                ),
                y=(
                    self.map_window.y +
                    self.map_window.height//2 -
                    self.map_rooms[pos]["sprite"].height//2 +
                    pos[1]*12*scale_factor
                )
            )
            self.map_rooms[pos]["sprite"].scale = scale_factor
            self.map_rooms[pos]["icon"].update(
                x=(
                    self.map_window.x +
                    self.map_window.width//2 -
                    self.map_rooms[pos]["icon"].width//2 +
                    pos[0]*12*scale_factor
                ),
                y=(
                    self.map_window.y +
                    self.map_window.height//2 -
                    self.map_rooms[pos]["icon"].height//2 +
                    pos[1]*12*scale_factor
                )
            )
            self.map_rooms[pos]["icon"].scale = scale_factor
