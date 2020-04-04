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
from pyglet.window import key

from lib import constants as c
from lib import prefabs
from lib.room import Room

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
        self.fps_display = pyglet.window.FPSDisplay(window=self)
        self.scale_divisor = c.DEFAULT_SCALE_DIVISOR

        self.enable_debugging = True

        self.loadResources()

        self.tile_groups = {}
        self.player_groups = {}
        for y in range(-50, 51):
            self.tile_groups[y] = pyglet.graphics.OrderedGroup(50-y*2)
            self.player_groups[y] = pyglet.graphics.OrderedGroup(50-y*2+1)

        self.ui_layers = {}
        for z in range(5):
            self.ui_layers[z] = pyglet.graphics.OrderedGroup(z+100)

        self.room = Room(
            window=self
        )

        self.player = prefabs.Player(self)

    def loadResources(self):
        self.resources = {}

        tiles = {}
        for style in c.STYLES:
            tiles[style] = {}
            for tile in c.TILE_TYPES:
                path = f"resources/tilesets/{style}/{tile}.png"
                tiles[style][tile] = pyglet.image.load(path)
        self.resources["tiles"] = tiles

        path = f"resources/sprites/player.png"
        self.resources["player"] = pyglet.image.load(path)

        debug = {}
        path = "resources/collider.png"
        debug["collider"] = pyglet.image.load(path)
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

        self.push_handlers(self.player.key_handler)

        self.player.update(self, dt)
        self.room.update(self)

    def on_key_press(self, symbol, modifiers):
        """Fullscreen the window or create a new room.

        Arguments:
            symbol {int} -- The key symbol pressed.
            modifiers {int} -- Bitwise combination of the key modifiers active.
        """
        super().on_key_press(symbol, modifiers)
        room_keys = {
            key._0: 0,
            key._1: 1,
            key._2: 2,
            key._3: 3,
            key._4: 4,
        }

        if symbol in room_keys.keys():
            self.room = Room(
                room_type=room_keys[symbol],
                window=self
            )
            self.player.moving = True
            self.player.x, self.player.y = 0, 0
            self.room.update(self)
        elif symbol == key.EQUAL:
            self.scale_divisor -= 5
            self.room.resize(self)
            self.player.resize(self)
        elif symbol == key.MINUS:
            self.scale_divisor += 5
            self.room.resize(self)
            self.player.resize(self)
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)

    def on_resize(self, width, height):
        """Resize the room.

        Arguments:
            width {int} -- The new window width.
            height {int} -- The new window height.
        """
        super().on_resize(width, height)
        self.room.resize(self)
        self.player.resize(self)

    def worldToScreen(self, x, y, parallax=False):
        """Convert a world position to a screen position.

        Arguments:
            x {float} -- The world x position.
            y {float} -- The world y position.

        Keyword Arguments:
            parallax {bool} -- Render with parallax. (default: {False})

        Returns:
            (int, int) -- The screen position of the object.
        """
        scale_factor = self.scale_factor

        screen_x = (x) * 16 * scale_factor
        screen_x += self.width/2

        screen_y = (y) * 16 * scale_factor
        screen_y += self.height/2

        if parallax is True:
            room = self.room
            screen_x += (
                (self.player.x) * -8 * scale_factor *
                (room.width / c.DEFAULT_ROOM_SIZE) /
                (self.scale_divisor / c.DEFAULT_SCALE_DIVISOR)
            )
            screen_y += (
                (self.player.y) * -8 * scale_factor *
                (room.height / c.DEFAULT_ROOM_SIZE) /
                (self.scale_divisor / c.DEFAULT_SCALE_DIVISOR)
            )

        return (screen_x, screen_y)

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
