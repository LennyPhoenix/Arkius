"""Contains classes for tiles, the player, enemies, etc."""

import pyglet
from pyglet import image
from pyglet.window import key

from . import constants as c


class Tile:
    """Tile object. Contains basic sprite renderer."""

    def __init__(self, window, x, y, type, tile_image):
        """Initialise the Tile class.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
            x {float} -- The x position of the tile.
            y {float} -- The y position of the tile.
            type {int} -- The tile's type.
            tile_image {pyglet.image} -- The image for the tile.
        """
        self.type = type

        self.x = x
        self.y = y

        self.screen_x, self.screen_y = window.worldToScreen(self.x, self.y)

        self.sprite = pyglet.sprite.Sprite(
            tile_image,
            group=window.tile_groups[y],
            batch=window.batch,
            x=self.screen_x,
            y=self.screen_y,
            usage="static"
        )
        self.sprite.scale = window.scaleFactor()

    def resize(self, window):
        """Resize the tile.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        screen_pos = window.worldToScreen(self.x, self.y, True)
        self.screen_x, self.screen_y = screen_pos[0], screen_pos[1]

        self.sprite.update(
            x=self.screen_x,
            y=self.screen_y
        )
        self.sprite.scale = window.scaleFactor()

    def update(self, window):
        """Update the position of the tile.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        screen_pos = window.worldToScreen(self.x, self.y, True)
        self.screen_x, self.screen_y = screen_pos[0], screen_pos[1]

        self.sprite.update(
            x=self.screen_x,
            y=self.screen_y
        )


class Player:
    """Player object. Contains basic renderer and controller."""

    def __init__(self, window):
        """Initialise the player class.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        self.room = (0, 0)

        self.x = 0.5
        self.y = 0.5

        self.tile_x = round(self.x-0.5)
        self.tile_y = round(self.y-0.5)

        self.velocity_x = 0
        self.velocity_y = 0
        self.moving = False

        self.key_handler = key.KeyStateHandler()

        player_image = image.load("resources/sprites/player.png")
        player_image.anchor_x = player_image.width // 2
        player_image.anchor_y = 0

        self.screen_x, self.screen_y = window.worldToScreen(self.x, self.y)

        self.sprite = pyglet.sprite.Sprite(
            player_image,
            group=window.player_groups[self.tile_y],
            batch=window.batch,
            x=self.screen_x,
            y=self.screen_y,
            usage="dynamic"
        )
        self.sprite.scale = window.scaleFactor()

    def update(self, window, dt):
        """Update the player.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
            dt {float} -- Time passed since last update.
        """
        self.tile_x = round(self.x-0.5)
        self.tile_y = round(self.y-0.5)

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

        if self.velocity_x != 0 or self.velocity_y != 0:
            self.moving = True
        else:
            self.moving = False

        if (self.x <= -(window.room.width+3) or
                self.x >= window.room.width+4 or
                self.y <= -(window.room.height+3) or
                self.y >= window.room.height+4):
            self.x, self.y = 0, 0

        screen_pos = window.worldToScreen(self.x, self.y, True)
        self.screen_x, self.screen_y = screen_pos[0], screen_pos[1]

        # Sprite
        scale_factor = window.scaleFactor()

        self.sprite.update(
            x=self.screen_x,
            y=self.screen_y
        )

        if self.sprite.scale != scale_factor:
            self.sprite.scale = scale_factor

        if self.sprite.group != window.player_groups[self.tile_y]:
            self.sprite.group = window.player_groups[self.tile_y]
