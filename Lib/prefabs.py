"""Contains classes for tiles, the player, enemies, etc."""

import pyglet
from pyglet import image
from pyglet.window import key


class Tile:
    """
    Prefab for a tile.
    Contains a sprite renderer and a collision box.
    """

    def __init__(self, window, x, y, type, tile_image):
        self.type = type

        self.x = x
        self.y = y

        self.screen_x, self.screen_y = window.worldToScreen(self.x, self.y)

        self.sprite = pyglet.sprite.Sprite(
            tile_image,
            group=window.TILE_Y_GROUPS[y],
            batch=window.BATCH,
            x=self.screen_x,
            y=self.screen_y,
            usage="static"
        )
        self.sprite.scale = window.scaleFactor()

    def resize(self, window):
        screen_pos = window.worldToScreen(self.x, self.y, True)
        self.screen_x, self.screen_y = screen_pos[0], screen_pos[1]

        self.sprite.update(
            x=self.screen_x,
            y=self.screen_y
        )
        self.sprite.scale = window.scaleFactor()

    def update(self, window):
        screen_pos = window.worldToScreen(self.x, self.y, True)
        self.screen_x, self.screen_y = screen_pos[0], screen_pos[1]

        self.sprite.update(
            x=self.screen_x,
            y=self.screen_y
        )


class Player:
    """
    Prefab for the player.
    Contains a sprite renderer and a collision box.
    """

    def __init__(self, window):
        self.room = (0, 0)

        self.x = 7.0
        self.y = 7.0

        self.tile_x = round(self.x-0.5)
        self.tile_y = round(self.y-0.5)

        self.velocity_x = 0
        self.velocity_y = 0
        self.moving = False

        self.key_handler = key.KeyStateHandler()

        player_image = image.load("./Images/Sprites/Player.png")
        player_image.anchor_x = 7
        player_image.anchor_y = 0

        self.screen_x, self.screen_y = window.worldToScreen(self.x, self.y)

        self.sprite = pyglet.sprite.Sprite(
            player_image,
            batch=window.BATCH,
            x=self.screen_x,
            y=self.screen_y,
            usage="dynamic"
        )
        self.sprite.scale = window.scaleFactor()

    def update(self, window, tiles, dt):
        self.tile_x = round(self.x-0.5)
        self.tile_y = round(self.y-0.5)

        # Position
        self.velocity_x, self.velocity_y = 0, 0
        if self.key_handler[key.W]:
            self.velocity_y += 0.1
        if self.key_handler[key.A]:
            self.velocity_x -= 0.1
        if self.key_handler[key.S]:
            self.velocity_y -= 0.1
        if self.key_handler[key.D]:
            self.velocity_x += 0.1

        if (
            (self.key_handler[key.A] or self.key_handler[key.D]) and
            (self.key_handler[key.W] or self.key_handler[key.S])
        ):
            self.velocity_x *= 0.7
            self.velocity_y *= 0.7

        self.x += self.velocity_x * dt * 60
        self.y += self.velocity_y * dt * 60

        if self.velocity_x != 0 or self.velocity_y != 0:
            self.moving = True
        else:
            self.moving = False

        if self.x <= -3 or self.x >= 18 or self.y <= -3 or self.y >= 18:
            self.x, self.y = 7.5, 7.5

        screen_pos = window.worldToScreen(self.x, self.y, True)
        self.screen_x, self.screen_y = screen_pos[0], screen_pos[1]

        # Sprite
        scale_factor = window.scaleFactor()

        self.sprite.update(
            x=self.screen_x,
            y=self.screen_y
        )
        self.sprite.scale = scale_factor

        if self.sprite.group != window.PLAYER_Y_GROUPS[self.tile_y]:
            self.sprite.group = window.PLAYER_Y_GROUPS[self.tile_y]
