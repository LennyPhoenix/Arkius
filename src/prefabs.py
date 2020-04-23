"""Contains classes for tiles, the player, enemies, etc."""
from math import floor

import pyglet
from pyglet.window import key

from . import constants as c


class Basic:
    """Basic entity."""

    def __init__(
        self,
        window,
        x, y,
        image,
        groups
    ):
        """Initialise with position, dimensions and a sprite.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
            x {float} -- The world X position of the entity.
            y {float} -- The world Y position of the entity.
            image {pyglet.image} -- The image to be used for the sprite.
            groups {dict} -- The Y groups dict to be used.
        """
        self.x = x
        self.y = y
        self.grid_x, self.grid_y = floor(self.x), floor(self.y)
        self.groups = groups

        self.screen_x, self.screen_y = window.worldToScreen(self.x, self.y)
        self.sprite = pyglet.sprite.Sprite(
            image,
            x=self.screen_x, y=self.screen_y,
            batch=window.batch,
            group=self.groups[self.grid_y]
        )
        self.sprite.scale = window.scale_factor

    def draw(self):
        """Manually draw the sprite."""
        self.sprite.draw()

    def update(self, window):
        """Update the sprite and any position variables.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        self.x = round(self.x*16)/16
        self.y = round(self.y*16)/16
        self.grid_x, self.grid_y = floor(self.x), floor(self.y)
        self.sprite.group = self.groups[self.grid_y]

        screen_pos = window.worldToScreen(self.x, self.y, True)
        self.screen_x, self.screen_y = screen_pos[0], screen_pos[1]

        visible = (
            (0-self.sprite.width) < self.screen_x < window.width and
            (0-self.sprite.height) < self.screen_y < window.height
        )

        if visible:
            self.sprite.update(
                x=self.screen_x,
                y=self.screen_y
            )
        if self.sprite.visible != visible:
            self.sprite.visible = visible

    def resize(self, window):
        """Resize the sprite.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
        """
        self.sprite.scale = window.scale_factor


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
            tile_image,
            window.tile_groups
        )
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
            window {pyglet.window.Window} -- The window for the application.
        """
        player_image = window.resources["player"]

        super().__init__(
            window,
            0, 0,
            player_image,
            window.player_groups
        )
        self.ox, self.oy = self.x, self.y

        self.col_x = c.PLAYER_COLLIDER["x"]
        self.col_y = c.PLAYER_COLLIDER["y"]
        self.col_width = c.PLAYER_COLLIDER["width"]
        self.col_height = c.PLAYER_COLLIDER["height"]

        # window.room.space.insert_body(self)

        self.room = (0, 0)

        self.velocity_x = 0
        self.velocity_y = 0
        self.moving = False

    def update(self, window, dt):
        """Update the player.

        Arguments:
            window {pyglet.window.Window} -- The window for the application.
            dt {float} -- Time passed since last update.
        """

        # Position
        self.velocity_x, self.velocity_y = 0, 0
        if window.key_handler[key.W]:
            self.velocity_y += c.PLAYER_SPEED
        if window.key_handler[key.A]:
            self.velocity_x -= c.PLAYER_SPEED
        if window.key_handler[key.S]:
            self.velocity_y -= c.PLAYER_SPEED
        if window.key_handler[key.D]:
            self.velocity_x += c.PLAYER_SPEED

        if (
            (window.key_handler[key.A] or window.key_handler[key.D]) and
            (window.key_handler[key.W] or window.key_handler[key.S])
        ):
            self.velocity_x *= c.DIAGONAL_MULTIPLIER
            self.velocity_y *= c.DIAGONAL_MULTIPLIER

        if window.key_handler[key.LSHIFT]:
            self.velocity_x *= 5
            self.velocity_y *= 5

        self.ox, self.oy = self.x, self.y
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        hits = window.room.space.get_hits(self.aabb)
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

        if self.y < -(window.room.height+3):
            window.room.visibility = False
            self.room = (self.room[0], self.room[1]-1)
            window.room.visibility = True
            self.y = window.room.height+3
            if window.room.map_data is not None:
                self.x = window.room.map_data["door_info"][0]["pos"]
            else:
                self.x = 0

        if self.x < -(window.room.width+3):
            window.room.visibility = False
            self.room = (self.room[0]-1, self.room[1])
            window.room.visibility = True
            self.x = window.room.width+3
            if window.room.map_data is not None:
                self.y = window.room.map_data["door_info"][1]["pos"]
            else:
                self.y = 0

        if self.y > window.room.height+3:
            window.room.visibility = False
            self.room = (self.room[0], self.room[1]+1)
            window.room.visibility = True
            self.y = -(window.room.height+3)
            if window.room.map_data is not None:
                self.x = window.room.map_data["door_info"][2]["pos"]
            else:
                self.x = 0

        if self.x > window.room.width+3:
            window.room.visibility = False
            self.room = (self.room[0]+1, self.room[1])
            window.room.visibility = True
            self.x = -(window.room.width+3)
            if window.room.map_data is not None:
                self.y = window.room.map_data["door_info"][3]["pos"]
            else:
                self.y = 0

        super().update(window)

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
