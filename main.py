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

        self.batch = pyglet.graphics.Batch()
        self.key_handler = key.KeyStateHandler()
        self.fps_display = pyglet.window.FPSDisplay(window=self)
        self.scale_divisor = c.DEFAULT_SCALE_DIVISOR

        self.enable_debugging = True

        self.createLayers()
        self.loadResources()

        self.dungeon = Dungeon(
            self,
            c.VOLCANO
        )

        self.player = prefabs.Player(self)
        self.push_handlers(self.key_handler)

    def createLayers(self):
        """Create all layers."""
        self.layers = {}
        self.layers["room"] = pyglet.graphics.OrderedGroup(1)
        room_layers = {}
        room_layers["ground"] = pyglet.graphics.OrderedGroup(
            1, parent=self.layers["room"]
        )
        room_layers["y_ordered"] = {}
        for i in range(-50, 51):
            room_layers["y_ordered"][i] = pyglet.graphics.OrderedGroup(
                51-i, parent=self.layers["room"]
            )
        self.layers["room_layers"] = room_layers

        self.layers["ui"] = pyglet.graphics.OrderedGroup(2)
        ui_layers = {}
        ui_layers["map_window"] = pyglet.graphics.OrderedGroup(
            1, parent=self.layers["ui"]
        )
        ui_layers["map_rooms"] = pyglet.graphics.OrderedGroup(
            2, parent=self.layers["ui"]
        )
        ui_layers["map_icons"] = pyglet.graphics.OrderedGroup(
            3, parent=self.layers["ui"]
        )
        self.layers["ui_layers"] = ui_layers

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
        self.batch.draw()
        self.fps_display.draw()

    def update(self, dt):
        """Update all sprites.

        Arguments:
            dt {float} -- Time passed since last update.
        """

        if self.key_handler[key.EQUAL]:
            self.scale_divisor -= 100 * dt
            for pos in self.dungeon.map.keys():
                self.dungeon.map[pos].resize(self)
            self.player.resize(self)
        elif self.key_handler[key.MINUS]:
            self.scale_divisor += 100 * dt
            for pos in self.dungeon.map.keys():
                self.dungeon.map[pos].resize(self)
            self.player.resize(self)

        self.player.update(self, dt)
        self.room.update(self)

    def on_key_press(self, symbol, modifiers):
        """Fullscreen the window or create a new room.

        Arguments:
            symbol {int} -- The key symbol pressed.
            modifiers {int} -- Bitwise combination of the key modifiers active.
        """
        super().on_key_press(symbol, modifiers)

        if symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.MIDDLE:
            world_x, world_y = self.screenToWorld(
                x, y,
                parallax=True
            )
            self.player.x, self.player.y = world_x-0.5, world_y
        return super().on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width, height):
        """Resize the room.

        Arguments:
            width {int} -- The new window width.
            height {int} -- The new window height.
        """
        super().on_resize(width, height)
        for pos in self.dungeon.map.keys():
            self.dungeon.map[pos].resize(self)
        self.dungeon.ui_map.resize(self)
        self.player.resize(self)

    def worldToScreen(self, x, y, parallax=False):
        """Convert a world position to a screen position.

        Arguments:
            x {float} -- The world x position.
            y {float} -- The world y position.

        Returns:
            (int, int) -- The screen position of the object.
        """
        scale_factor = self.scale_factor

        screen_x = (x) * 16 * scale_factor
        screen_x += self.width/2
        screen_x -= 8 * scale_factor

        screen_y = (y) * 16 * scale_factor
        screen_y += self.height/2
        screen_y -= 8 * scale_factor

        if parallax is True:
            screen_x += (
                (self.player.x) * -16 * scale_factor
            )
            screen_y += (
                (self.player.y) * -16 * scale_factor
            )

        return (screen_x, screen_y)

    def screenToWorld(self, x, y, parallax=False):
        """Convert a world position to a screen position.

        Arguments:
            x {float} -- The screen x position.
            y {float} -- The screen y position.

        Returns:
            (int, int) -- The world position of the object.
        """
        scale_factor = self.scale_factor

        world_x, world_y = 0, 0

        if parallax is True:
            world_x += (
                (self.player.x) * 16 * scale_factor
            )
            world_y += (
                (self.player.y) * 16 * scale_factor
            )

        world_x += (x+0.5) - self.width / 2
        world_x += 8 * scale_factor
        world_x /= 16 * scale_factor

        world_y += (y+0.5) - self.height / 2
        world_y += 8 * scale_factor
        world_y /= 16 * scale_factor

        return (world_x, world_y)

    @property
    def room(self):
        """Gets the room occupied by the player.

        Returns:
            Room -- The active room.
        """
        room_map = self.dungeon.map
        return room_map[self.player.room]

    @property
    def scale_factor(self):
        """Return the scale factor of the window.

        Returns:
            float -- The window's scale factor.
        """
        scale_factor = self.height / self.scale_divisor
        return scale_factor


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
