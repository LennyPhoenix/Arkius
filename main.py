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
from pyglet.text import Label
from pyglet.window import key

from Lib import prefabs, tilesets
from Lib.dungeon import Room

pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = gl.GL_NEAREST


class Window(pyglet.window.Window):
    """
    Custom window class for application.
    Derived from pyglet.window.Window.
    """

    def __init__(self, *args, **kwargs):
        """Creates the dungeon and player etc."""
        super().__init__(*args, **kwargs)
        self.set_minimum_size(768, 480)

        self.BATCH = pyglet.graphics.Batch()
        self.fps_display = pyglet.window.FPSDisplay(window=self)

        self.TILE_Y_GROUPS = {}
        for y in range(-3, 19):
            self.TILE_Y_GROUPS[y] = pyglet.graphics.OrderedGroup(20-2*y)

        self.PLAYER_Y_GROUPS = {}
        for y in range(-3, 19):
            self.PLAYER_Y_GROUPS[y] = pyglet.graphics.OrderedGroup(20-2*y+1)

        self.UI_LAYERS = {}
        for y in range(5):
            self.UI_LAYERS[y] = pyglet.graphics.OrderedGroup(y+100)

        self.room = Room(
            room_type=1,
            tileset=tilesets.fightRoom(),
            window=self
        )
        print(self.room)

        self.player = prefabs.Player(self)

    def on_key_press(self, symbol, modifiers):
        """Run on every key press."""
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
                tileset=tilesets.fightRoom(),
                window=self
            )
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)

    def on_resize(self, width, height):
        """Run on every window resize."""
        super().on_resize(width, height)
        self.room.resize(self)

    def update(self, dt):
        """Run 120 times per second."""
        scale_factor = self.scaleFactor()

        self.clear()

        self.push_handlers(self.player.key_handler)

        self.player.update(self, dt)

        self.BATCH.draw()
        help_text = Label(
            text=f"Keys: 1 - Fight Room, 2 - Treasure Room, 3 - Boss Room, 4 - Shop Room, 0 - Start Room, F11 - Fullscreen/Windowed  {str(self.player.tile_x)[:4]}, {str(self.player.tile_y)[:4]}",  # noqa: E501
            font_name="Helvetica", font_size=6.5*scale_factor,
            x=10*scale_factor, y=self.height-10*scale_factor,
            multiline=True,
            width=self.width-10*scale_factor,
            anchor_y="top"
        )
        help_text.draw()
        self.fps_display.draw()

    def scaleFactor(self):
        """Returns the scale factor of the window."""
        scale_factor = self.height / 320
        return scale_factor


if __name__ == "__main__":
    window = Window(
        caption="Arkius",
        resizable=True,
        fullscreen=True,
        vsync=True
    )
    pyglet.clock.schedule_interval(window.update, 1/120)
    window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()
