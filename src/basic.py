"""Contains Basic class."""

import pyglet

from .cardsprite import CardSprite


class Basic:
    """Basic entity."""

    def __init__(self, window, x, y, image, card_sprite=False):
        """Initialise with position, dimensions and a sprite.

        Arguments:
            window {Window} -- The window for the application.
            x {float} -- The world X position of the entity.
            y {float} -- The world Y position of the entity.
            image {pyglet.image} -- The image to be used for the sprite.
            card_sprite {bool} -- Whether or not to use the "CardSprite".
        """
        self.window = window
        self.x = x
        self.y = y

        self.sx, self.sy = window.worldToScreen(self.x, self.y)
        if card_sprite:
            self.sprite = CardSprite(
                image,
                x=self.sx, y=self.sy,
                batch=self.window.world_batch,
                subpixel=True
            )
        else:
            self.sprite = pyglet.sprite.Sprite(
                image,
                x=self.sx, y=self.sy,
                batch=self.window.world_batch,
                subpixel=True
            )

    def update(self):
        """Update the sprite and any position variables."""
        self.x = round(self.x*16)/16
        self.y = round(self.y*16)/16

        self.sx, self.sy = self.window.worldToScreen(self.x, self.y)

        self.sprite.update(
            x=self.sx,
            y=self.sy
        )
