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

from Lib.dungeon import Room
from Lib import tilesets


def toString(tileset):
    string = ""
    for y in range(15):
        for x in range(15):
            string += f"{tileset[(x, y)]} "
        string += "\n"
    return string


room = Room(roomType=1, tileset=tilesets.generateRandom())
string = toString(room.groundTiles)

window = Window(caption="Arkius", resizable=True)
tiles = pyglet.text.Label(
    string,
    font_name="Times New Roman",
    font_size=10,
    x=window.width/2,
    y=window.height/2,
    anchor_x="center",
    anchor_y="center",
    multiline=True,
    width=162
)

helptext = pyglet.text.Label(
    "Left click to generate random room, right click to generate boss room.",
    font_name="Times New Roman",
    font_size=20,
    x=window.width/2, y=window.height - 40,
    anchor_x="center",
    anchor_y="center",
    multiline=True,
    width=400
)


@window.event
def on_draw():
    window.clear()
    tiles.draw()
    helptext.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    global tiles, helptext
    if button == 1:
        room = Room(roomType=1, tileset=tilesets.generateRandom())
        string = toString(room.groundTiles)
        tiles = pyglet.text.Label(
            string,
            font_name="Times New Roman",
            font_size=10,
            x=window.width/2,
            y=window.height/2,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=162
        )
    elif button == 4:
        room = Room(roomType=3)
        string = toString(room.groundTiles)
        tiles = pyglet.text.Label(
            string,
            font_name="Times New Roman",
            font_size=10,
            x=window.width/2,
            y=window.height/2,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=162
        )
    window.clear()
    tiles.draw()
    helptext = pyglet.text.Label(
        "Left click to generate random room, right click to generate boss room.",
        font_name="Times New Roman",
        font_size=20,
        x=window.width/2, y=window.height - 40,
        anchor_x="center",
        anchor_y="center",
        multiline=True,
        width=400
    )
    helptext.draw()


pyglet.app.run()
