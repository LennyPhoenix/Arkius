"""Contains classes for tiles, the player, enemies, etc."""
from math import floor

import pyglet
from pyglet import image
from pyglet.window import key

from . import constants as c


class Basic:
    def __init__(self, window, x, y, width, height, image, groups):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.grid_x, self.grid_y = floor(self.x), floor(self.y)
        self.groups = groups

        self.screen_x, self.screen_y = window.worldToScreen(self.x, self.y)
        self.sprite = pyglet.sprite.Sprite(
            image,
            x=self.screen_x, y=self.screen_y,
            batch=window.batch,
            group=self.groups[self.grid_y]
        )
        self.sprite.scale = window.scaleFactor()

    def draw(self):
        self.sprite.draw()

    def update(self, window):
        self.grid_x, self.grid_y = floor(self.x), floor(self.y)
        self.sprite.group = self.groups[self.grid_y]
        screen_pos = window.worldToScreen(self.x, self.y, True)
        self.screen_x, self.screen_y = screen_pos[0], screen_pos[1]

        self.sprite.update(
            x=self.screen_x,
            y=self.screen_y
        )

    def resize(self, window):
        self.sprite.scale = window.scaleFactor()


class Tile(Basic):
    """Tile object. Contains basic sprite renderer."""

    def __init__(self, window, x, y, tile_type, tile_image):
        """Initialise the Tile class.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
            x {float} -- The x position of the tile.
            y {float} -- The y position of the tile.
            tile_type {int} -- The tile's type.
            tile_image {pyglet.image} -- The image for the tile.
        """
        self.type = tile_type

        super().__init__(
            window,
            x, y,
            1, 1,
            tile_image,
            window.tile_groups
        )


class Player(Basic):
    """Player object. Contains basic renderer and controller."""

    def __init__(self, window):
        """Initialise the player class.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        player_image = image.load("resources/sprites/player.png")
        player_image.anchor_x = player_image.width // 2
        player_image.anchor_y = 0

        super().__init__(
            window,
            0.5, 0.5,
            0.9, 0.5,
            player_image,
            window.player_groups
        )

        self.room = (0, 0)

        self.velocity_x = 0
        self.velocity_y = 0
        self.moving = False

        self.key_handler = key.KeyStateHandler()

    def update(self, window, dt):
        """Update the player.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
            dt {float} -- Time passed since last update.
        """

        # Position
        self.velocity_x, self.velocity_y = 0, 0
        if self.key_handler[key.W]:
            self.velocity_y += c.PLAYER_SPEED
        if self.key_handler[key.A]:
            self.velocity_x -= c.PLAYER_SPEED
        if self.key_handler[key.S]:
            self.velocity_y -= c.PLAYER_SPEED
        if self.key_handler[key.D]:
            self.velocity_x += c.PLAYER_SPEED

        if (
            (self.key_handler[key.A] or self.key_handler[key.D]) and
            (self.key_handler[key.W] or self.key_handler[key.S])
        ):
            self.velocity_x *= c.DIAGONAL_MULTIPLIER
            self.velocity_y *= c.DIAGONAL_MULTIPLIER

        if self.key_handler[key.LSHIFT]:
            self.velocity_x *= 5
            self.velocity_y *= 5

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        if (self.x <= -(window.room.width+3) or
                self.x >= window.room.width+4 or
                self.y <= -(window.room.height+3) or
                self.y >= window.room.height+4):
            self.x, self.y = 0, 0

        super().update(window)
