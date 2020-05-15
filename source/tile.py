import random

import pyglet

from . import constants as c
from . import particle
from .basic import Basic


class Tile(Basic):

    def __init__(self, application, room, x, y):
        self.room = room
        self.type = self.room.tilemap[(x, y)]

        if not c.TILES[self.type]["sprite"]["connective"]:
            image = random.choice(
                application.resources[
                    "tiles"
                ][
                    self.room.style
                ][
                    self.type
                ]
            )
        else:
            index = self.room.getImageIndex(x, y)
            image = application.resources[
                "tiles"
            ][
                self.room.style
            ][
                self.type
            ][
                index
            ]

        collider = None
        for n_x in range(-1, 2):
            for n_y in range(-1, 2):
                if (
                    (x+n_x, y+n_y) in self.room.tilemap.keys() and
                    c.TILES[
                        self.room.tilemap[(x+n_x, y+n_y)]
                    ]["collider"] is None
                ):
                    collider = c.TILES[self.type]["collider"]

        super().__init__(
            application,
            x*16, y*16,
            image,
            card_sprite=self.type == c.WALL,
            collider=collider,
            space=self.room.space
        )
        layer = self.application.layers["world"][c.TILES[self.type]["layer"]]
        self.sprite.group = layer
        self.unload()

    def load(self):
        self.loaded = True
        self.sprite.visible = True
        try:
            self.sprite._animate(0)
        except AttributeError:
            pass

        r = random.randint(0, 3)
        if (
            self.type == c.PIT and
            self.room.style == c.VOLCANO and
            r == 0
        ):
            pyglet.clock.schedule_interval_soft(self.emitter, 0.5)
            self.last_bubble = 0
            self.to_wait = random.randint(2, 16)/2

    def unload(self):
        self.loaded = False
        self.sprite.visible = False
        pyglet.clock.unschedule(self.sprite._animate)
        pyglet.clock.unschedule(self.emitter)

    def emitter(self, dt):
        if self.sprite.visible:
            self.last_bubble += dt
            if self.last_bubble >= self.to_wait:
                x = self.position.x+random.randint(2, 6)
                y = self.position.y+random.randint(2, 4)
                particle.AnimationBasedParticle(
                    self.application,
                    x, y,
                    self.application.resources["lava_bubble"]
                )
                self.last_bubble = 0
                self.to_wait = random.randint(4, 16)/2
