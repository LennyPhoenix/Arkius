"""
This is a secondary application for Arkius that allows the
modification and creation of tilemaps.
"""

import random

import pyglet
from pyglet import gl
from pyglet.window import key

from lib import constants as c
from lib import prefabs, tilemaps

pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = gl.GL_NEAREST

TILE_MATRIX = None


class Window(pyglet.window.Window):
    """Custom window class for application.

    Arguments:
        pyglet {window.Window} -- The pyglet window to be derived from.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.batch = pyglet.graphics.Batch()
        self.scale_divisor = c.DEFAULT_SCALE_DIVISOR

        self.room_style = c.ICE

        self.tile_groups = {}
        for y in range(-50, 51):
            self.tile_groups[y] = pyglet.graphics.OrderedGroup(50-y*2)

        self.images = {}
        for style in c.STYLES:
            self.images[style] = {}
            for tile_type in c.TILE_TYPES:
                self.images[style][tile_type] = pyglet.image.load(
                    f"resources/tilesets/{style}/{tile_type}.png"
                )

        if TILE_MATRIX is None:
            self.room_width = c.DEFAULT_ROOM_SIZE
            self.room_height = c.DEFAULT_ROOM_SIZE
            self.tilemap = tilemaps.create_blank(
                self.room_width+1,
                self.room_height+1
            )
        else:
            self.room_height = len(TILE_MATRIX)//2
            self.room_width = len(TILE_MATRIX[0])//2
            self.tilemap = tilemaps.create_blank(
                self.room_width+1,
                self.room_height+1
            )
            self.tilemap.update(tilemaps.toMap(TILE_MATRIX))

        self.tiles = {}
        self.generate_tiles()

        scale_factor = self.scaleFactor()
        self.dimensions_label = pyglet.text.Label(
            f"Width: {self.room_width}  Height: {self.room_height}",
            font_size=10*scale_factor,
            x=10*scale_factor,
            y=10*scale_factor
        )

    def generate_tiles(self):
        for pos, tile in self.tiles.items():
            tile.sprite.delete()
        self.tiles = {}
        for x in range(-self.room_width, self.room_width+1):
            for y in range(-self.room_height, self.room_height+1):
                tile_type = self.tilemap[(x, y)]
                if tile_type == c.FLOOR:
                    value = random.randint(0, 9)
                else:
                    value = self.getBitValue(x, y)
                UV = self.getUV(self.tilemap[(x, y)], value)
                image = self.images[self.room_style][tile_type]
                image_region = image.get_region(*UV)
                self.tiles[(x, y)] = prefabs.Tile(
                    self,
                    x, y,
                    tile_type,
                    image_region
                )

    def on_key_press(self, symbol, modifiers):
        """Fullscreen the window.

        Arguments:
            symbol {int} -- The key symbol pressed.
            modifiers {int} -- Bitwise combination of the key modifiers active.
        """
        super().on_key_press(symbol, modifiers)

        if symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)
        elif symbol == key.EQUAL:
            self.scale_divisor -= 20
            self.on_resize(self.width, self.height)
        elif symbol == key.MINUS:
            self.scale_divisor += 20
            self.on_resize(self.width, self.height)

        resize_keys = {
            key.LEFT: (-1, 0),
            key.RIGHT: (1, 0),
            key.DOWN: (0, -1),
            key.UP: (0, 1)
        }

        if symbol in resize_keys.keys():
            self.room_width += resize_keys[symbol][0]
            self.room_height += resize_keys[symbol][1]
            tilemap = tilemaps.create_blank(
                self.room_width+1,
                self.room_height+1
            )
            tilemap.update(self.tilemap)
            self.tilemap = tilemap
            for pos, tile in self.tilemap.items():
                if not (
                    -self.room_width <= pos[0] <= self.room_width and
                    -self.room_height <= pos[1] <= self.room_height
                ):
                    self.tilemap[pos] = 0
            self.generate_tiles()
            self.dimensions_label.text = f"Width: {self.room_width}  Height: {self.room_height}"

        if symbol == key.ENTER:
            output = "[\n"
            for y in range(-self.room_height, self.room_height+1):
                output += "    ["
                for x in range(-self.room_width, self.room_width+1):
                    output += f"{self.tilemap[(x, -y)]}, "
                output += "],\n"
            output += "]"
            print(output)

    def on_resize(self, width, height):
        """Resize the tiles.

        Arguments:
            width {int} -- The new window width.
            height {int} -- The new window height.
        """
        super().on_resize(width, height)

        for pos, tile in self.tiles.items():
            tile.resize(self)

    def update(self, dt):
        """Redraw the tiles and update positions etc.

        Arguments:
            dt {float} -- Time passed since last update.
        """
        for pos, tile in self.tiles.items():
            tile.resize

        self.clear()
        self.batch.draw()
        self.dimensions_label.draw()

    def worldToScreen(self, x, y, parallax=False):
        """Convert a world position to a screen position.

        Arguments:
            x {float} -- The world x position.
            y {float} -- The world y position.

        Returns:
            (int, int) -- The screen position of the object.
        """
        scale_factor = self.scaleFactor()

        screen_x = (x-0.5) * 16 * scale_factor
        screen_x += self.width/2

        screen_y = (y-0.5) * 16 * scale_factor
        screen_y += self.height/2

        return (screen_x, screen_y)

    def scaleFactor(self):
        """Return the scale factor of the window.

        Returns:
            float -- The window's scale factor.
        """
        scale_factor = self.height / self.scale_divisor
        return scale_factor

    def getBitValue(self, x, y):
        """Return the bitmask value for a tile.

        Arguments:
            x {int} -- The x position of the tile.
            y {int} -- The y position of the tile.

        Returns:
            int -- The bitmask value of the tile.
        """
        tilemap = self.tilemap
        tileID = tilemap[(x, y)]
        value = 0

        sides = {
            128: False, 1: False,   2: False,
            64: False,              4: False,
            32: False,  16: False,  8: False
        }

        edges = [tileID]

        if (x, y+1) in tilemap.keys() and tilemap[(x, y+1)] not in edges:
            sides.update({128: True, 1: True, 2: True})
        if (x+1, y) in tilemap.keys() and tilemap[(x+1, y)] not in edges:
            sides.update({2: True, 4: True, 8: True})
        if (x, y-1) in tilemap.keys() and tilemap[(x, y-1)] not in edges:
            sides.update({8: True, 16: True, 32: True})
        if (x-1, y) in tilemap.keys() and tilemap[(x-1, y)] not in edges:
            sides.update({32: True, 64: True, 128: True})

        if (x+1, y+1) in tilemap.keys() and tilemap[(x+1, y+1)] not in edges:
            sides[2] = True
        if (x+1, y-1) in tilemap.keys() and tilemap[(x+1, y-1)] not in edges:
            sides[8] = True
        if (x-1, y-1) in tilemap.keys() and tilemap[(x-1, y-1)] not in edges:
            sides[32] = True
        if (x-1, y+1) in tilemap.keys() and tilemap[(x-1, y+1)] not in edges:
            sides[128] = True

        for side in sides.keys():
            if sides[side]:
                value += side

        return value

    def getUV(self, tile_type, tile_value):
        """Find a tile UV position for a tileset.

        Arguments:
            tile_type {int} -- The type of the tile.
            tile_value {int} -- The bitmask value of the tile.

        Returns:
            (int, int) -- The UV position for the tile.
        """
        if tile_type == c.FLOOR:
            values_dict = {
                0: (0, 0), 1: (16, 0), 2: (32, 0), 3: (48, 0), 4: (64, 0),
                5: (0, 16), 6: (16, 16), 7: (32, 16), 8: (48, 16), 9: (64, 16)
            }
        else:
            values_dict = {
                34: (32, 0), 136: (48, 0), 226: (64, 0), 184: (80, 0),
                58: (96, 0), 142: (112, 0), 138: (128, 0), 162: (144, 0),

                251: (0, 16), 187: (16, 16), 191: (32, 16), 255: (48, 16),
                139: (64, 16), 46: (80, 16), 232: (96, 16), 163: (112, 16),
                42: (128, 16), 168: (144, 16),

                248: (0, 32), 56: (16, 32), 62: (32, 32), 254: (48, 32),
                250: (64, 32), 186: (80, 32), 190: (96, 32), 2: (112, 32),
                130: (128, 32), 128: (144, 32),

                224: (0, 48), 0: (16, 48), 14: (32, 48), 238: (48, 48),
                234: (64, 48), 174: (96, 48), 10: (112, 48), 170: (128, 48),
                160: (144, 48),

                227: (0, 64), 131: (16, 64), 143: (32, 64), 239: (48, 64),
                235: (64, 64), 171: (80, 64), 175: (96, 64), 8: (112, 64),
                40: (128, 64), 32: (144, 64)
            }

        x, y = values_dict[tile_value]

        if tile_type == c.WALL:
            tile_height = 32
            y *= 2
        else:
            tile_height = 16

        return (x, y, 16, tile_height)


if __name__ == "__main__":
    window = Window(
        caption="Arkius Tilemapper",
        resizable=True,
        fullscreen=True,
        vsync=True
    )
    pyglet.clock.schedule_interval(window.update, c.UPDATE_SPEED)
    window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()
