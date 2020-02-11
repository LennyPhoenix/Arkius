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
from pyglet import image
from pyglet import gl

from Lib.dungeon import Room
from Lib import tilesets


def getValue(tileset, x, y):
    """Returns the bitmasking value of a tile."""
    tileID = tileset[(x, y)]
    value = 255
    sides = {
        128: False, 1: False,   2: False,
        64: False,              4: False,
        32: False,  16: False,  8: False
    }

    if y != 14 and tileset[(x, y+1)] != tileID:
        sides[128] = True
        sides[1] = True
        sides[2] = True
    if y != 14 and x != 14 and tileset[(x+1, y+1)] != tileID:
        sides[2] = True
    if x != 14 and tileset[(x+1, y)] != tileID:
        sides[2] = True
        sides[4] = True
        sides[8] = True
    if x != 14 and y != 0 and tileset[(x+1, y-1)] != tileID:
        sides[8] = True
    if y != 0 and tileset[(x, y-1)] != tileID:
        sides[8] = True
        sides[16] = True
        sides[32] = True
    if y != 0 and x != 0 and tileset[(x-1, y-1)] != tileID:
        sides[32] = True
    if x != 0 and tileset[(x-1, y)] != tileID:
        sides[32] = True
        sides[64] = True
        sides[128] = True
    if x != 0 and y != 14 and tileset[(x-1, y+1)] != tileID:
        sides[128] = True

    for side in sides.keys():
        if sides[side]:
            value -= side

    return value


room = Room(roomType=1, tileset=tilesets.generateRandom())
print(room)

print("\n\n\n")

window = Window(caption="Arkius", resizable=True, fullscreen=True)
scalefactor = window.height/320
tileBatch = pyglet.graphics.Batch()
pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = gl.GL_NEAREST


def makeTile(image, batch, x, y, scalefactor):
    tile = pyglet.sprite.Sprite(
        image,
        batch=batch,
        x=(x*16*scalefactor)+(2.5*16*scalefactor) +
        (window.width/2)-(20*16*scalefactor/2),
        y=(y*16*scalefactor)+(2.5*16*scalefactor) +
        (window.height/2)-(20*16*scalefactor/2),
        usage="static"
    )
    tile.scale = scalefactor
    return tile


def drawTiles(dt=None):
    global room, scalefactor
    tiles = {}

    for x in range(15):
        for y in range(15):
            roomTiles = room.groundTiles
            tileID = roomTiles[(x, y)]

            if tileID != 0:
                value = getValue(roomTiles, x, y)
                tileImage = image.load(f"Images/Tiles/1-{tileID}/{value}.png")
            else:
                tileImage = image.load(f"Images/Tiles/1-0.png")
            tileImage.anchor_x = 0
            tileImage.anchor_y = 0
            tile = makeTile(tileImage, tileBatch, x, y, scalefactor)
            tiles[(x, y)] = tile

    # Render room borders.
    for x in range(15):
        y = -1
        tileImage = image.load(f"Images/Tiles/1-1/124.png")
        tileImage.anchor_x = 0
        tileImage.anchor_y = 0
        tile = makeTile(tileImage, tileBatch, x, y, scalefactor)
        tiles[(x, y)] = tile
    for x in range(15):
        y = 15
        tileImage = image.load(f"Images/Tiles/1-1/199.png")
        tileImage.anchor_x = 0
        tileImage.anchor_y = 0
        tile = makeTile(tileImage, tileBatch, x, y, scalefactor)
        tiles[(x, y)] = tile
    for y in range(15):
        x = -1
        tileImage = image.load(f"Images/Tiles/1-1/241.png")
        tileImage.anchor_x = 0
        tileImage.anchor_y = 0
        tile = makeTile(tileImage, tileBatch, x, y, scalefactor)
        tiles[(x, y)] = tile
    for y in range(15):
        x = 15
        tileImage = image.load(f"Images/Tiles/1-1/31.png")
        tileImage.anchor_x = 0
        tileImage.anchor_y = 0
        tile = makeTile(tileImage, tileBatch, x, y, scalefactor)
        tiles[(x, y)] = tile

    window.clear()
    tileBatch.draw()


@window.event
def on_show():
    global room, scalefactor
    scalefactor = window.height/320
    drawTiles()


@window.event
def on_key_press(symbol, modifiers):
    global room, scalefactor
    if symbol == key._0:
        room = Room(roomType=0, tileset=tilesets.generateRandom())
    if symbol == key._1:
        room = Room(roomType=1, tileset=tilesets.generateRandom())
    elif symbol == key._2:
        room = Room(roomType=2, tileset=tilesets.generateRandom())
    elif symbol == key._3:
        room = Room(roomType=3, tileset=tilesets.generateRandom())
    elif symbol == key._4:
        room = Room(roomType=4, tileset=tilesets.generateRandom())
    drawTiles()


@window.event
def on_resize(width, height):
    global scalefactor, room
    scalefactor = window.height/320
    pyglet.clock.schedule_once(drawTiles, 0.1)


@window.event
def on_draw():
    pass


pyglet.app.run()
