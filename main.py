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
from pyglet.window import Window
from pyglet.window import key
from pyglet.text import Label
from pyglet import gl

from Lib.dungeon import Room
from Lib import tilesets
from Lib import prefabs


window = Window(
    caption="Arkius",
    resizable=True,
    fullscreen=True
)
pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = gl.GL_NEAREST
MAIN_BATCH = pyglet.graphics.Batch()

Y_GROUPS = {}
for y in range(-1, 16):
    Y_GROUPS[y] = pyglet.graphics.OrderedGroup(y)

fps_display = pyglet.window.FPSDisplay(window=window)
window.set_minimum_size(1280, 720)

SCALE_FACTOR = window.height/320

room = Room(
    room_type=1,
    tileset=tilesets.fightRoom(),
    window=window,
    batch=MAIN_BATCH,
    groups=Y_GROUPS
)
print(room)

help_text = Label(
    text="Keys: 1 - Fight Room, 2 - Treasure Room, 3 - Boss Room, 4 - Shop Room, 0 - Start Room, F11 - Fullscreen/Windowed",  # noqa: E501
    font_name="Helvetica", font_size=7*SCALE_FACTOR,
    x=10*SCALE_FACTOR, y=window.height-10*SCALE_FACTOR,
    anchor_y="top"
)

player = prefabs.Player(window, SCALE_FACTOR, MAIN_BATCH)


@window.event
def on_key_press(symbol, modifiers):
    global room, MAIN_BATCH
    if symbol == key._0:
        room = Room(
            room_type=0,
            window=window,
            batch=MAIN_BATCH,
            groups=Y_GROUPS
        )
    elif symbol == key._1:
        room = Room(
            room_type=1,
            tileset=tilesets.fightRoom(),
            window=window,
            batch=MAIN_BATCH,
            groups=Y_GROUPS
        )
    elif symbol == key._2:
        room = Room(
            room_type=2,
            window=window,
            batch=MAIN_BATCH,
            groups=Y_GROUPS
        )
    elif symbol == key._3:
        room = Room(
            room_type=3,
            window=window,
            batch=MAIN_BATCH,
            groups=Y_GROUPS
        )
    elif symbol == key._4:
        room = Room(
            room_type=4,
            window=window,
            batch=MAIN_BATCH,
            groups=Y_GROUPS
        )
    elif symbol == key.F11:
        window.set_fullscreen(not window.fullscreen)


def update(dt):
    global room, help_text, player, SCALE_FACTOR, MAIN_BATCH

    window.clear()

    window.push_handlers(player.key_handler)

    player.update(window, SCALE_FACTOR, dt, Y_GROUPS)

    MAIN_BATCH.draw()
    help_text.text = f"Keys: 1 - Fight Room, 2 - Treasure Room, 3 - Boss Room, 4 - Shop Room, 0 - Start Room, F11 - Fullscreen/Windowed  {str(player.x)[:4]}, {str(player.y)[:4]}"  # noqa: E501
    help_text.draw()
    fps_display.draw()


@window.event
def on_resize(width, height):
    global room, SCALE_FACTOR, help_text, player
    SCALE_FACTOR = height/320

    help_text = Label(
        text=f"Keys: 1 - Fight Room, 2 - Treasure Room, 3 - Boss Room, 4 - Shop Room, 0 - Start Room, F11 - Fullscreen/Windowed  {str(player.x)[:4]}, {str(player.y)[:4]}",  # noqa: E501
        font_name="Helvetica", font_size=7*SCALE_FACTOR,
        x=10*SCALE_FACTOR, y=window.height-10*SCALE_FACTOR,
        anchor_y="top"
    )

    room.resize(window, SCALE_FACTOR)
    player.resize(window, SCALE_FACTOR)


pyglet.clock.schedule_interval(update, 1/120)

window.push_handlers(pyglet.window.event.WindowEventLogger())
pyglet.app.run()
