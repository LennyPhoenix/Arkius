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
from Lib import prefabs, tilesets
from Lib.dungeon import Room
from pyglet import gl
from pyglet.text import Label
from pyglet.window import key


class Window(pyglet.window.Window):
    """
    Custom window class for application.
    Derived from pyglet.window.Window.
    """

    def __init__(self, *args, **kwargs):
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

    def on_key_press(self, symbol, modifiers):
        global room

        room_keys = {
            key._0: 0,
            key._1: 1,
            key._2: 2,
            key._3: 3,
            key._4: 4,
        }

        if symbol in room_keys.keys():
            room = Room(
                room_type=room_keys[symbol],
                tileset=tilesets.fightRoom(),
                window=self
            )
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)
        elif symbol == key.ESCAPE:
            self.close()

    def scaleFactor(self):
        """Returns the scale factor of the window."""
        scale_factor = self.height / 320
        return scale_factor


window = Window(
    caption="Arkius",
    resizable=True,
    fullscreen=True
)
pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = gl.GL_NEAREST

room = Room(
    room_type=1,
    tileset=tilesets.fightRoom(),
    window=window
)
print(room)

player = prefabs.Player(window)
help_text = None


def update(dt):
    global room, player
    scale_factor = window.scaleFactor()

    window.clear()

    window.push_handlers(player.key_handler)

    player.update(window, dt)

    window.BATCH.draw()
    help_text = Label(
        text=f"Keys: 1 - Fight Room, 2 - Treasure Room, 3 - Boss Room, 4 - Shop Room, 0 - Start Room, F11 - Fullscreen/Windowed  {str(player.x)[:4]}, {str(player.y)[:4]}",  # noqa: E501
        font_name="Helvetica", font_size=6.5*scale_factor,
        x=10*scale_factor, y=window.height-10*scale_factor,
        multiline=True,
        width=window.width-10*scale_factor,
        anchor_y="top"
    )
    help_text.draw()
    window.fps_display.draw()


@window.event
def on_resize(width, height):
    global room, player
    room.resize(window)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/120)
    window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()
