"""
This is a secondary application for Arkius that allows the
modification and creation of tilemaps.

Controls:
 • Arrow Keys: Change room size.
 • "+" and "-": Change zoom level.
 • Left Click: Place tile.
 • Right Click: Cycle tile type.
 • Enter: Print tilemap to console.

"""

import random
from math import floor

import pyglet
from pyglet import gl
from pyglet.window import key
from pyglet.window import mouse

from src import constants as c
from src import prefabs, tilemaps

pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = gl.GL_NEAREST

# Options:
ROOM_STYLE = c.VOLCANO
TILE_MATRIX = None


class Window(pyglet.window.Window):
    """Custom window class for application.

    Arguments:
        pyglet {window.Window} -- The pyglet window to be derived from.
    """

    def __init__(self, *args, **kwargs):
        """Initialise the editor."""
        super().__init__(*args, **kwargs)

        self.batch = pyglet.graphics.Batch()
        self.key_handler = key.KeyStateHandler()
        self.scale_divisor = c.DEFAULT_SCALE_DIVISOR

        self.room_style = ROOM_STYLE
        self.brush = c.WALL
        self.enable_debugging = False

        self.tile_groups = {}
        for y in range(-100, 101):
            self.tile_groups[y] = pyglet.graphics.OrderedGroup(100-y*2)

        self.tile_images = {}
        for style in c.STYLES:
            self.tile_images[style] = {}
            for tile in c.TILES.keys():
                path = f"resources/tilesets/{style}/{tile}.png"
                image = pyglet.image.load(path)
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
                self.tile_images[style][tile] = image_grid

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

        scale_factor = self.scale_factor
        self.dimensions_label = pyglet.text.Label(
            f"Width: {self.room_width}  Height: {self.room_height}",
            font_size=10*scale_factor,
            x=10*scale_factor,
            y=10*scale_factor
        )
        self.brush_label = pyglet.text.Label(
            f"Current Brush ID: {self.brush}",
            font_size=10*scale_factor,
            x=10*scale_factor,
            y=self.height - 20*scale_factor
        )

        self.cursor_green = pyglet.image.load("resources/selection_green.png")
        self.cursor_red = pyglet.image.load("resources/selection_red.png")
        cursor_x, cursor_y = self.worldToScreen(0, 0)
        self.cursor = pyglet.sprite.Sprite(
            self.cursor_green,
            x=cursor_x,
            y=cursor_y,
            group=self.tile_groups[-100],
            batch=self.batch
        )
        self.cursor.scale = scale_factor

    def generate_tiles(self):
        """Generate all tile sprites."""
        for pos, tile in self.tiles.items():
            tile.sprite.delete()
        self.tiles = {}
        for x in range(-self.room_width, self.room_width+1):
            for y in range(-self.room_height, self.room_height+1):
                tile_type = self.tilemap[(x, y)]
                if not c.TILES[tile_type]["sprite"]["connective"]:
                    image = random.choice(self.tile_images[
                        self.room_style
                    ][
                        tile_type
                    ])
                else:
                    index = self.getImageIndex(x, y)
                    image = self.tile_images[
                        self.room_style
                    ][
                        tile_type
                    ][
                        index
                    ]
                self.tiles[(x, y)] = prefabs.Tile(
                    self,
                    x, y,
                    tile_type,
                    image
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
            text = f"Width: {self.room_width}  Height: {self.room_height}"
            self.dimensions_label.text = text

        if symbol == key.ENTER:
            output = "MAP = {\n"
            output += f"    \"width\": {self.room_width},\n"
            output += f"    \"height\": {self.room_height},\n"
            output += "    \"border_type\": 1,\n"
            output += "    \"door_info\": {\n"
            output += "        0: {\"pos\": 0, \"floor\": 0},\n"
            output += "        1: {\"pos\": 0, \"floor\": 0},\n"
            output += "        2: {\"pos\": 0, \"floor\": 0},\n"
            output += "        3: {\"pos\": 0, \"floor\": 0},\n"
            output += "    },\n"
            output += "    \"matrix\": [\n"

            for y in range(-self.room_height, self.room_height+1):
                output += "        ["
                for x in range(-self.room_width, self.room_width+1):
                    output += f"{self.tilemap[(x, -y)]}, "
                output += "],\n"

            output += "    ]\n"
            output += "}\n"
            with open("map.txt", "w+") as f:
                f.write(output)
            print(output)

    def on_mouse_motion(self, x, y, dx, dy):
        """Move the cursor sprite.

        Arguments:
            x {int} -- The mouse X position.
            y {int} -- The mouse Y position.
            dx {int} -- The X position relative to the last position.
            dy {int} -- The Y position relative to the last position.
        """
        world_x, world_y = self.screenToWorld(x, y)
        tile_x = floor(world_x)
        tile_y = floor(world_y)
        cursor_x, cursor_y = self.worldToScreen(tile_x, tile_y)
        self.cursor.update(
            x=cursor_x,
            y=cursor_y
        )
        if (tile_x, tile_y) in self.tiles.keys():
            self.cursor.image = self.cursor_green
        else:
            self.cursor.image = self.cursor_red
        return super().on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        """Paint or change the brush.

        Arguments:
            x {int} -- The mouse X position.
            y {int} -- The mouse Y position.
            button {int} -- The mouse button pushed.
            modifiers {int} -- Bitwise combination of any keyboard
                               modifiers currently active.
        """
        if button == mouse.LEFT:
            world_x, world_y = self.screenToWorld(x, y)
            tile_x = floor(world_x)
            tile_y = floor(world_y)

            if (
                -self.room_width <= tile_x <= self.room_width and
                -self.room_height <= tile_y <= self.room_height
            ):
                self.tilemap[(tile_x, tile_y)] = self.brush

                to_refresh = [
                    (tile_x, tile_y),
                    (tile_x+1, tile_y),
                    (tile_x-1, tile_y),
                    (tile_x, tile_y+1),
                    (tile_x, tile_y-1),
                    (tile_x+1, tile_y+1),
                    (tile_x-1, tile_y-1),
                    (tile_x+1, tile_y-1),
                    (tile_x-1, tile_y+1),
                ]
                for tile_x, tile_y in to_refresh:
                    if (tile_x, tile_y) in self.tiles:
                        tile_type = self.tilemap[(tile_x, tile_y)]
                        if tile_type == 0:
                            index = random.randint(0, 9)
                        else:
                            index = self.getImageIndex(tile_x, tile_y)
                        image = self.tile_images[
                            self.room_style
                        ][
                            tile_type
                        ][
                            index
                        ]
                        self.tiles[(tile_x, tile_y)].sprite.image = image

        if button == mouse.RIGHT:
            self.brush += 1
            if self.brush > len(c.TILES)-1:
                self.brush = 0
            self.brush_label.text = f"Current Brush ID: {self.brush}"

        return super().on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width, height):
        """Resize the tiles.

        Arguments:
            width {int} -- The new window width.
            height {int} -- The new window height.
        """
        super().on_resize(width, height)

        for pos, tile in self.tiles.items():
            tile.resize(self)

        scale_factor = self.scale_factor
        self.dimensions_label.x = 10 * scale_factor
        self.dimensions_label.y = 10 * scale_factor
        self.dimensions_label.font_size = 10 * scale_factor
        self.brush_label.x = 10 * scale_factor
        self.brush_label.y = self.height - 20 * scale_factor
        self.brush_label.font_size = 10 * scale_factor
        self.cursor.scale = scale_factor

    def update(self, dt):
        """Redraw the tiles and update positions etc.

        Arguments:
            dt {float} -- Time passed since last update.
        """
        self.push_handlers(self.key_handler)

        if self.key_handler[key.EQUAL]:
            self.scale_divisor -= 100 * dt
            self.on_resize(self.width, self.height)
        elif self.key_handler[key.MINUS]:
            self.scale_divisor += 100 * dt
            self.on_resize(self.width, self.height)

        for pos, tile in self.tiles.items():
            tile.update(self)

        self.clear()
        self.batch.draw()
        self.dimensions_label.draw()
        self.brush_label.draw()
        self.draw_mouse_cursor()

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

        world_x = (x+0.5) - self.width / 2
        world_x += 8 * scale_factor
        world_x /= 16 * scale_factor

        world_y = (y+0.5) - self.height / 2
        world_y += 8 * scale_factor
        world_y /= 16 * scale_factor

        return (world_x, world_y)

    @property
    def scale_factor(self):
        """Return the scale factor of the window.

        Returns:
            float -- The window's scale factor.
        """
        scale_factor = self.height / self.scale_divisor
        return scale_factor

    def getImageIndex(self, x, y):
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

        connects = c.TILES[tileID]["sprite"]["connects"]

        if (x, y+1) in tilemap.keys() and tilemap[(x, y+1)] not in connects:
            sides.update({128: True, 1: True, 2: True})
        if (x+1, y) in tilemap.keys() and tilemap[(x+1, y)] not in connects:
            sides.update({2: True, 4: True, 8: True})
        if (x, y-1) in tilemap.keys() and tilemap[(x, y-1)] not in connects:
            sides.update({8: True, 16: True, 32: True})
        if (x-1, y) in tilemap.keys() and tilemap[(x-1, y)] not in connects:
            sides.update({32: True, 64: True, 128: True})

        if (
            (x+1, y+1) in tilemap.keys() and
            tilemap[(x+1, y+1)] not in connects
        ):
            sides[2] = True
        if (
            (x+1, y-1) in tilemap.keys() and
            tilemap[(x+1, y-1)] not in connects
        ):
            sides[8] = True
        if (
            (x-1, y-1) in tilemap.keys() and
            tilemap[(x-1, y-1)] not in connects
        ):
            sides[32] = True
        if (
            (x-1, y+1) in tilemap.keys() and
            tilemap[(x-1, y+1)] not in connects
        ):
            sides[128] = True

        for side in sides.keys():
            if sides[side]:
                value += side

        index_dict = {
            34: 2, 136: 3, 226: 4, 184: 5, 58: 6, 142: 7, 138: 8, 162: 9,
            251: 10, 187: 11, 191: 12, 255: 13, 139: 14, 46: 15, 232: 16,
            163: 17, 42: 18, 168: 19, 248: 20, 56: 21, 62: 22, 254: 23,
            250: 24, 186: 25, 190: 26, 2: 27, 130: 28, 128: 29, 224: 30, 0: 31,
            14: 32, 238: 33, 234: 34, 174: 36, 10: 37, 170: 38, 160: 39,
            227: 40, 131: 41, 143: 42, 239: 43, 235: 44, 171: 45, 175: 46,
            8: 47, 40: 48, 32: 49
        }

        return index_dict[value]


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
