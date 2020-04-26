"""
Copyright (C) 2020,  DoAltPlusF4.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pyglet
from pyglet import gl
from pyglet.window import key, mouse

from src import constants as c
from src import prefabs
from src.camera import Camera
from src.dungeon import Dungeon

pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = gl.GL_NEAREST


class Window(pyglet.window.Window):
    """Custom Window class.

    Arguments:
        pyglet {window.Window} -- Pyglet's window class.

    Returns:
        Window -- Custom window class.
    """

    def __init__(self, *args, **kwargs):
        """Initialise the window class."""
        super().__init__(*args, **kwargs)
        self.set_minimum_size(*c.MIN_SIZE)

        self.key_handler = key.KeyStateHandler()
        self.fps_display = pyglet.window.FPSDisplay(window=self)
        self.zoom = 1

        self.world_camera = Camera(0, 0, 1000)
        self.world_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()

        self.createLayers()
        self.loadResources()

        self.dungeon = Dungeon(
            self,
            c.VOLCANO
        )

        self.player = prefabs.Player(self)

        self.positionCamera()
        self.push_handlers(self.key_handler)

    def createLayers(self):
        """Create all layers."""
        self.layers = {}

        self.layers["world_master"] = pyglet.graphics.OrderedGroup(0)
        world = {}
        world["ground"] = pyglet.graphics.OrderedGroup(
            0, parent=self.layers["world_master"]
        )
        world["y_ordered"] = {}
        for i in range(-50, 51):
            world["y_ordered"][i] = pyglet.graphics.OrderedGroup(
                51-i, parent=self.layers["world_master"]
            )
        self.layers["world"] = world

        self.layers["ui_master"] = pyglet.graphics.OrderedGroup(1)
        ui = {}
        ui["map_window"] = pyglet.graphics.OrderedGroup(
            0, self.layers["ui_master"]
        )
        ui["map_rooms"] = pyglet.graphics.OrderedGroup(
            1, self.layers["ui_master"]
        )
        ui["map_icons"] = pyglet.graphics.OrderedGroup(
            2, self.layers["ui_master"]
        )
        self.layers["ui"] = ui

    def loadResources(self):
        """Preload all resources."""
        self.resources = {}

        tiles = {}
        for style in c.STYLES:
            tiles[style] = {}
            for tile in c.TILES.keys():
                image = pyglet.resource.image(
                    f"resources/tilesets/{style}/{tile}.png"
                )

                if c.TILES[tile]["sprite"]["connective"]:
                    image_grid = pyglet.image.ImageGrid(
                        image,
                        c.TILESET_DIMENSIONS[1],
                        c.TILESET_DIMENSIONS[0],
                        item_width=c.TILES[tile]["sprite"]["width"],
                        item_height=c.TILES[tile]["sprite"]["height"]
                    )
                else:
                    image_grid = pyglet.image.ImageGrid(
                        image,
                        image.height // c.TILES[tile]["sprite"]["height"],
                        image.width // c.TILES[tile]["sprite"]["width"],
                        item_width=c.TILES[tile]["sprite"]["width"],
                        item_height=c.TILES[tile]["sprite"]["height"]
                    )
                tiles[style][tile] = pyglet.image.TextureGrid(image_grid)
                # if image.width > c.TILESET_DIMENSIONS[0] * 16:
                #     frames = image.
        self.resources["tiles"] = tiles

        self.resources["player"] = pyglet.resource.image(
            "resources/sprites/player.png"
        )

        ui = {}
        ui["map"] = {}
        ui["map"]["window"] = pyglet.resource.image(
            "resources/ui/map_window.png"
        )
        image = pyglet.resource.image(
            "resources/ui/map_rooms.png"
        )
        image_grid = pyglet.image.ImageGrid(
            image,
            4, 16
        )
        ui["map"]["rooms"] = pyglet.image.TextureGrid(image_grid)
        image = pyglet.resource.image(
            "resources/ui/map_icons.png"
        )
        image_grid = pyglet.image.ImageGrid(
            image,
            1, 5
        )
        ui["map"]["icons"] = pyglet.image.TextureGrid(image_grid)
        self.resources["ui"] = ui

        debug = {}
        debug["collider"] = pyglet.resource.image(
            "resources/collider.png"
        )
        self.resources["debug"] = debug

    def on_draw(self):
        """Redraw the window."""
        self.clear()
        with self.world_camera:
            self.world_batch.draw()
        self.ui_batch.draw()
        self.fps_display.draw()

    def update(self, dt):
        """Update all sprites.

        Arguments:
            dt {float} -- Time passed since last update.
        """

        rezoom = False
        if self.key_handler[key.EQUAL]:
            self.zoom += 2 * dt
            rezoom = True
        elif self.key_handler[key.MINUS]:
            self.zoom -= 2 * dt
            rezoom = True
        if rezoom:
            self.zoom = max(c.MIN_ZOOM, min(c.MAX_ZOOM, self.zoom))
            zoom = (
                (min(self.width, self.height) / c.MIN_SIZE[1]) *
                self.zoom
            )
            if zoom >= 1:
                self.world_camera.zoom = round(zoom)
            else:
                self.world_camera.zoom = round(zoom*4)/4

        self.positionCamera()

        self.player.update(dt)

    def on_key_press(self, symbol, modifiers):
        """Fullscreen the window or create a new room.

        Arguments:
            symbol {int} -- The key symbol pressed.
            modifiers {int} -- Bitwise combination of the key modifiers active.
        """
        if symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)

        return super().on_key_press(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            world_x, world_y = self.screenToWorld(x, y)
            self.player.x, self.player.y = world_x-0.5, world_y

    def on_resize(self, width, height):
        """Resize the room.

        Arguments:
            width {int} -- The new window width.
            height {int} -- The new window height.
        """
        zoom = (
            (min(self.width, self.height) / c.MIN_SIZE[1]) *
            self.zoom
        )
        if zoom >= 1:
            self.world_camera.zoom = round(zoom)
        else:
            self.world_camera.zoom = round(zoom*4)/4

        return super().on_resize(width, height)

    def worldToScreen(self, x, y):
        """Convert a world position to a screen position.

        Arguments:
            x {float} -- The world x position.
            y {float} -- The world y position.

        Returns:
            (int, int) -- The screen position of the object.
        """
        screen_x = (x*16) - 8
        screen_y = (y*16) - 8

        return (screen_x, screen_y)

    def screenToWorld(self, x, y):
        """Convert a screen position to a world position.

        Arguments:
            x {int} -- The screen X position.
            y {int} -- The screen Y position.
        """
        world_x = (
            (x+self.world_camera.offset_x*self.world_camera.zoom) /
            self.world_camera.zoom
        )
        world_y = (
            (y+self.world_camera.offset_y*self.world_camera.zoom) /
            self.world_camera.zoom
        )

        world_x = world_x/16+0.5
        world_y = world_y/16+0.5

        return world_x, world_y

    def positionCamera(self):
        """Sets the position of the world_camera."""
        self.world_camera.position = (
            round((-self.width/self.world_camera.zoom//2) -
                  (
                (self.player.x) * -8 *
                self.room.width/25
            )),
            round((-self.height/self.world_camera.zoom//2) -
                  (
                (self.player.y) * -8 *
                self.room.height/15
            ))
        )

    @property
    def room(self):
        """Gets the room occupied by the player.

        Returns:
            Room -- The active room.
        """
        room_map = self.dungeon.map
        return room_map[self.player.room]


if __name__ == "__main__":
    window = Window(
        caption="Arkius",
        resizable=True,
        fullscreen=True,
        vsync=True
    )
    pyglet.clock.schedule_interval(window.update, c.UPDATE_SPEED)
    window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()
