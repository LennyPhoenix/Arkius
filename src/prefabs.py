"""Contains classes for tiles, the player, enemies, etc."""

import random

import pyglet
from pyglet.window import key

from . import constants as c
from .basic import Basic
from . import particle


class Tile(Basic):
    """Tile object. Contains basic sprite renderer."""

    def __init__(self, window, x, y, tile_type, tile_image):
        """Initialise the Tile class.

        Arguments:
            window {Window} -- The window for the application.
            x {float} -- The x position of the tile.
            y {float} -- The y position of the tile.
            tile_type {int} -- The tile's type.
            tile_image {pyglet.image} -- The image for the tile.
        """
        self.type = tile_type

        super().__init__(
            window,
            x, y,
            tile_image,
            self.type == c.WALL
        )
        layer = self.window.layers["world"][c.TILES[self.type]["layer"]]
        self.sprite.group = layer
        self.unload()

        if c.TILES[self.type]["collider"] is not None:
            self.cx = c.TILES[self.type]["collider"]["x"]
            self.cy = c.TILES[self.type]["collider"]["y"]
            self.cw = c.TILES[self.type]["collider"]["width"]
            self.ch = c.TILES[self.type]["collider"]["height"]

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
            self.window.dungeon_style == c.VOLCANO and
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
                x = self.x+random.randint(2, 6)/16
                y = self.y+random.randint(2, 4)/16
                particle.AnimationBasedParticle(
                    self.window,
                    x,
                    y,
                    self.window.resources["lava_bubble"]
                )
                self.last_bubble = 0
                self.to_wait = random.randint(4, 16)/2

    @property
    def aabb(self):
        if c.TILES[self.type]["collider"] is not None:
            return (
                self.x + self.cx,
                self.y + self.cy,
                self.x + self.cx + self.cw,
                self.y + self.cy + self.ch
            )


class Player(Basic):
    """Player object. Contains basic renderer and controller."""

    def __init__(self, window):
        """Initialise the player class.

        Arguments:
            window {Window} -- The window for the application.
        """
        self._state = "idle_right"
        anim = window.resources["player"]["idle_right"]
        super().__init__(
            window,
            0, 0,
            anim,
            card_sprite=True
        )
        self.sprite.group = self.window.layers["world"]["y_ordered"]
        self.ox, self.oy = self.x, self.y

        self.last_shadow = 0
        self.shadow_frequency = 1/25

        self.cx = c.PLAYER_COLLIDER["x"]
        self.cy = c.PLAYER_COLLIDER["y"]
        self.cw = c.PLAYER_COLLIDER["width"]
        self.ch = c.PLAYER_COLLIDER["height"]

        # window.room.space.insert_body(self)

        self.room = (0, 0)

        self.vx = 0
        self.vy = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state != self.state:
            if state in self.window.resources["player"].keys():
                anim = self.window.resources["player"][state]
                self.sprite.image = anim
            elif state == "locked":
                if self._state == "walk_right":
                    self.state = "idle_right"
                elif self._state == "walk_left":
                    self.state = "idle_left"
            self._state = state

    def update(self, dt):
        """Update the player.

        Arguments:
            dt {float} -- Time passed since last update.
        """

        controls = {
            "up": (
                self.window.key_handler[key.W] or
                self.window.key_handler[key.UP]
            ),
            "down": (
                self.window.key_handler[key.S] or
                self.window.key_handler[key.DOWN]
            ),
            "left": (
                self.window.key_handler[key.A] or
                self.window.key_handler[key.LEFT]
            ),
            "right": (
                self.window.key_handler[key.D] or
                self.window.key_handler[key.RIGHT]
            ),
            "dash": (
                self.window.key_handler[key.LSHIFT]
            )
        }

        # Position
        self.vx, self.vy = 0, 0
        if self.state != "locked":
            if controls["up"]:
                self.vy += c.PLAYER_SPEED
            if controls["down"]:
                self.vy -= c.PLAYER_SPEED

            if (
                controls["up"] or
                controls["down"]
            ):
                if self.state == "idle_left":
                    self.state = "walk_left"
                elif self.state == "idle_right":
                    self.state = "walk_right"

            if controls["left"]:
                self.vx -= c.PLAYER_SPEED
                self.state = "walk_left"
            if controls["right"]:
                self.vx += c.PLAYER_SPEED
                self.state = "walk_right"

            if not (
                controls["up"] or
                controls["down"] or
                controls["left"] or
                controls["right"]
            ):
                if self.state == "walk_left":
                    self.state = "idle_left"
                elif self.state == "walk_right":
                    self.state = "idle_right"

            if (
                (
                    controls["left"] or
                    controls["right"]
                ) and
                (
                    controls["up"] or
                    controls["down"]
                )
            ):
                self.vx /= 2**0.5
                self.vy /= 2**0.5

            if controls["dash"]:
                self.vx *= 5
                self.vy *= 5
                self.last_shadow += dt
                if self.last_shadow >= self.shadow_frequency:
                    shadow_image = self.sprite.image.frames[
                        self.sprite._frame_index
                    ].image
                    particle.Shadow(
                        self.window,
                        self.x, self.y,
                        shadow_image,
                        0.25,
                        128
                    )
                    self.last_shadow = 0

        self.ox, self.oy = self.x, self.y
        self.x += self.vx * dt
        self.y += self.vy * dt

        hits = self.window.room.space.get_hits(self.aabb)
        for body in hits:
            if (
                self.aabb[1] <= body.aabb[3] and
                self.old_aabb[1] >= body.aabb[3]
            ):
                self.y = body.aabb[3] - self.cy

            elif (
                self.aabb[3] >= body.aabb[1] and
                self.old_aabb[3] <= body.aabb[1]
            ):
                self.y = body.aabb[1] - self.cy - self.ch

            if (
                self.aabb[2] >= body.aabb[0] and
                self.old_aabb[2] <= body.aabb[0]
            ):
                self.x = body.aabb[0] - self.cx - self.cw

            elif (
                self.aabb[0] <= body.aabb[2] and
                self.old_aabb[0] >= body.aabb[2]
            ):
                self.x = body.aabb[2] - self.cx

        self.checkDoors()

        super().update()

    def checkDoors(self):
        """Check if the player is exiting through a door."""
        # Bottom Door
        if self.y < -(self.window.room.height+3):
            self.window.dungeon.transition.begin(self, 2)

        # Left Door
        if self.x < -(self.window.room.width+3):
            self.window.dungeon.transition.begin(self, 3)

        # Top Door
        if self.y > self.window.room.height+3:
            self.window.dungeon.transition.begin(self, 0)

        # Right Door
        if self.x > self.window.room.width+3:
            self.window.dungeon.transition.begin(self, 1)

    @property
    def aabb(self):
        return (
            self.x + self.cx,
            self.y + self.cy,
            self.x + self.cx + self.cw,
            self.y + self.cy + self.ch
        )

    @property
    def old_aabb(self):
        return (
            self.ox + self.cx,
            self.oy + self.cy,
            self.ox + self.cx + self.ch,
            self.oy + self.cy + self.ch
        )
