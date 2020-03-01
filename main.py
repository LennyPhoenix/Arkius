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
from Lib import prefabs, scaleFactor, tilesets
from Lib.dungeon import Room
from pyglet import gl
from pyglet.text import Label
from pyglet.window import Window, key

window = Window(
    caption="Arkius",
    resizable=True,
    fullscreen=True
)
pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = gl.GL_NEAREST
MAIN_BATCH = pyglet.graphics.Batch()

TILE_Y_GROUPS = {}
for y in range(-3, 19):
    TILE_Y_GROUPS[y] = pyglet.graphics.OrderedGroup(20-2*y)

PLAYER_Y_GROUPS = {}
for y in range(-3, 19):
    PLAYER_Y_GROUPS[y] = pyglet.graphics.OrderedGroup(20-2*y+1)

fps_display = pyglet.window.FPSDisplay(window=window)
window.set_minimum_size(768, 480)

SCALE_FACTOR = scaleFactor(window)

room = Room(
    room_type=1,
    tileset=tilesets.fightRoom(),
    window=window,
    batch=MAIN_BATCH,
    groups=TILE_Y_GROUPS
)
print(room)

player = prefabs.Player(window, MAIN_BATCH)
help_text = None


@window.event
def on_key_press(symbol, modifiers):
    global room, MAIN_BATCH

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
            window=window,
            batch=MAIN_BATCH,
            groups=TILE_Y_GROUPS
        )
    elif symbol == key.F11:
        window.set_fullscreen(not window.fullscreen)


def update(dt):
    global room, help_text, player, SCALE_FACTOR, MAIN_BATCH

    window.clear()

    window.push_handlers(player.key_handler)

    player.update(window, dt, PLAYER_Y_GROUPS)

    MAIN_BATCH.draw()
    help_text.text = f"Keys: 1 - Fight Room, 2 - Treasure Room, 3 - Boss Room, 4 - Shop Room, 0 - Start Room, F11 - Fullscreen/Windowed  {str(player.x)[:4]}, {str(player.y)[:4]}"  # noqa: E501
    help_text.draw()
    fps_display.draw()


@window.event
def on_resize(width, height):
    global room, SCALE_FACTOR, help_text, player
    SCALE_FACTOR = scaleFactor(window)

    help_text = Label(
        text=f"Keys: 1 - Fight Room, 2 - Treasure Room, 3 - Boss Room, 4 - Shop Room, 0 - Start Room, F11 - Fullscreen/Windowed  {str(player.x)[:4]}, {str(player.y)[:4]}",  # noqa: E501
        font_name="Helvetica", font_size=6.5*SCALE_FACTOR,
        x=10*SCALE_FACTOR, y=window.height-10*SCALE_FACTOR,
        multiline=True,
        width=window.width-10*SCALE_FACTOR,
        anchor_y="top"
    )

    room.resize(window)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/120)
    window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()
