"""Contains classes for tiles, the player, enemies, etc."""

import pyglet
from pyglet import image
from pyglet.window import key


class Tile():
    """
    Prefab for a tile.
    Contains a sprite renderer and a collision box.
    """

    def __init__(self, window, tile_group, batch, x, y, tile_image):
        scale_factor = window.height/320
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(
            tile_image,
            group=tile_group,
            batch=batch,
            x=(self.x*16*scale_factor)+(2.5*16*scale_factor) +
            (window.width/2)-(20*16*scale_factor/2),
            y=(self.y*16*scale_factor)+(2.5*16*scale_factor) +
            (window.height/2)-(20*16*scale_factor/2),
            usage="static"
        )
        self.sprite.scale = scale_factor

    def resize(self, window, scale_factor):
        self.sprite.update(
            x=(self.x*16*scale_factor)+(2.5*16*scale_factor) +
            (window.width/2)-(20*16*scale_factor/2),
            y=(self.y*16*scale_factor)+(2.5*16*scale_factor) +
            (window.height/2)-(20*16*scale_factor/2)
        )
        self.sprite.scale = scale_factor


class Player():
    """
    Prefab for the player.
    Contains a sprite renderer and a collision box.
    """

    def __init__(self, window, scale_factor, batch):
        self.x = 7.0
        self.y = 7.0

        self.velocity_x = 0
        self.velocity_y = 0

        self.key_handler = key.KeyStateHandler()

        player_image = image.load("./Images/Sprites/Player.png")
        player_image.anchor_x = 7
        player_image.anchor_y = 0

        self.sprite = pyglet.sprite.Sprite(
            player_image,
            batch=batch,
            x=(self.x*16*scale_factor)+(2.5*16*scale_factor) +
            (window.width/2)-(20*16*scale_factor/2),
            y=(self.y*16*scale_factor)+(2.5*16*scale_factor) +
            (window.height/2)-(20*16*scale_factor/2),
            usage="dynamic"
        )

    def resize(self, window, scale_factor):
        self.sprite.update(
            x=(self.x*16*scale_factor)+(2.5*16*scale_factor) +
            (window.width/2)-(20*16*scale_factor/2),
            y=(self.y*16*scale_factor)+(2.5*16*scale_factor) +
            (window.height/2)-(20*16*scale_factor/2)
        )
        self.sprite.scale = scale_factor

    def update(self, window, scale_factor, dt, groups):
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
            self.velocity_x *= 0.75
            self.velocity_y *= 0.75

        self.x += self.velocity_x * dt * 60
        self.y += self.velocity_y * dt * 60

        self.sprite.update(
            x=(self.x*16*scale_factor)+(2.5*16*scale_factor) +
            (window.width/2)-(20*16*scale_factor/2),
            y=(self.y*16*scale_factor)+(2.5*16*scale_factor) +
            (window.height/2)-(20*16*scale_factor/2)
        )
        self.sprite.group = groups[14-round(self.y-0.5)]
