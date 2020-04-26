"""Contains classes for tiles, the player, enemies, etc."""

from pyglet.window import key

from . import constants as c
from .basic import Basic
from .particle import Shadow


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
        self.sprite.visible = False

        if c.TILES[self.type]["collider"] is not None:
            self.col_x = c.TILES[self.type]["collider"]["x"]
            self.col_y = c.TILES[self.type]["collider"]["y"]
            self.col_width = c.TILES[self.type]["collider"]["width"]
            self.col_height = c.TILES[self.type]["collider"]["height"]

    @property
    def aabb(self):
        if c.TILES[self.type]["collider"] is not None:
            return (
                self.x + self.col_x,
                self.y + self.col_y,
                self.x + self.col_x + self.col_width,
                self.y + self.col_y + self.col_height
            )


class Player(Basic):
    """Player object. Contains basic renderer and controller."""

    def __init__(self, window):
        """Initialise the player class.

        Arguments:
            window {Window} -- The window for the application.
        """
        self._state = "idle"
        player_image = window.resources["player"]

        super().__init__(
            window,
            0, 0,
            player_image,
            True
        )
        layer = self.window.layers["world"]["y_ordered"]
        self.sprite.group = layer
        self.ox, self.oy = self.x, self.y

        self.last_shadow = 0
        self.shadow_frequency = 1/25

        self.col_x = c.PLAYER_COLLIDER["x"]
        self.col_y = c.PLAYER_COLLIDER["y"]
        self.col_width = c.PLAYER_COLLIDER["width"]
        self.col_height = c.PLAYER_COLLIDER["height"]

        # window.room.space.insert_body(self)

        self.room = (0, 0)

        self.velocity_x = 0
        self.velocity_y = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state in c.PLAYER_STATES[self.state]:
            self._state = state

    def update(self, dt):
        """Update the player.

        Arguments:
            dt {float} -- Time passed since last update.
        """

        # Position
        self.velocity_x, self.velocity_y = 0, 0
        if self.state != "locked":
            if self.window.key_handler[key.W]:
                self.velocity_y += c.PLAYER_SPEED
            if self.window.key_handler[key.A]:
                self.velocity_x -= c.PLAYER_SPEED
            if self.window.key_handler[key.S]:
                self.velocity_y -= c.PLAYER_SPEED
            if self.window.key_handler[key.D]:
                self.velocity_x += c.PLAYER_SPEED

            if (
                (
                    self.window.key_handler[key.A] or
                    self.window.key_handler[key.D]
                ) and
                (
                    self.window.key_handler[key.W] or
                    self.window.key_handler[key.S]
                )
            ):
                self.velocity_x *= c.DIAGONAL_MULTIPLIER
                self.velocity_y *= c.DIAGONAL_MULTIPLIER

            if self.window.key_handler[key.LSHIFT]:
                self.velocity_x *= 5
                self.velocity_y *= 5
                self.last_shadow += dt
                if self.last_shadow >= self.shadow_frequency:
                    Shadow(
                        self.window,
                        self.x, self.y,
                        self.sprite.image,
                        0.25,
                        128
                    )
                    self.last_shadow = 0

        self.ox, self.oy = self.x, self.y
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        hits = self.window.room.space.get_hits(self.aabb)
        for body in hits:
            if (
                self.aabb[1] <= body.aabb[3] and
                self.old_aabb[1] >= body.aabb[3]
            ):
                self.y = body.aabb[3] - self.col_y

            elif (
                self.aabb[3] >= body.aabb[1] and
                self.old_aabb[3] <= body.aabb[1]
            ):
                self.y = body.aabb[1] - self.col_y - self.col_height

            if (
                self.aabb[2] >= body.aabb[0] and
                self.old_aabb[2] <= body.aabb[0]
            ):
                self.x = body.aabb[0] - self.col_x - self.col_width

            elif (
                self.aabb[0] <= body.aabb[2] and
                self.old_aabb[0] >= body.aabb[2]
            ):
                self.x = body.aabb[2] - self.col_x

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
            self.x + self.col_x,
            self.y + self.col_y,
            self.x + self.col_x + self.col_width,
            self.y + self.col_y + self.col_height
        )

    @property
    def old_aabb(self):
        return (
            self.ox + self.col_x,
            self.oy + self.col_y,
            self.ox + self.col_x + self.col_width,
            self.oy + self.col_y + self.col_height
        )
