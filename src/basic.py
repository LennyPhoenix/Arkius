"""Contains Basic class."""

import pyglet

from .cardsprite import CardSprite


class Basic:
    """Basic entity."""

    def __init__(self, window, x, y, image, card_sprite=False, collider=None, space=None, static=True):  # noqa: E501
        """Initalise with position, collider (if necessary) and sprite.

        Arguments:
            window {Window} -- The application window.
            x {float} -- The X position.
            y {float} -- The Y position.
            image {pyglet.AbstractImage} -- The image/animation to use.

        Keyword Arguments:
            card_sprite {bool} -- Use the custom card sprite class?
                                  (default: {False})
            collider {dict} -- The collider to use. (default: {None})
            space {Space} -- The space to use. (default: {None})
            static {bool} -- If the object is static. (default: {True})
        """
        self.window = window
        self.x = x
        self.y = y

        self.static = static
        self.vx, self.vy = 0, 0
        self.collider = collider
        if self.collider is not None:
            self.cx = self.collider["x"]
            self.cy = self.collider["y"]
            self.cw = self.collider["width"]
            self.ch = self.collider["height"]

            self.space = space
            if self.space is not None:
                self.space.add(self)

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
        self.sx, self.sy = self.window.worldToScreen(self.x, self.y)

        self.sprite.update(
            x=self.sx,
            y=self.sy
        )

    @property
    def aabb(self):
        if self.collider is not None:
            return (
                self.x + self.cx,
                self.y + self.cy,
                self.x + self.cx + self.cw,
                self.y + self.cy + self.ch
            )

    def sweptAABB(self, other):
        if self.vx > 0:
            x_inv_entry = other.aabb[0] - self.aabb[2]
            x_inv_exit = other.aabb[2] - self.aabb[0]
        else:
            x_inv_entry = other.aabb[2] - self.aabb[0]
            x_inv_exit = self.aabb[0] - self.aabb[2]

        if self.vy > 0:
            y_inv_entry = other.aabb[1] - self.aabb[3]
            y_inv_exit = other.aabb[3] - self.aabb[1]
        else:
            y_inv_entry = other.aabb[3] - self.aabb[1]
            y_inv_exit = other.aabb[1] - self.aabb[3]

        if self.vx == 0:
            x_entry = float("-inf")
            x_exit = float("inf")
        else:
            x_entry = x_inv_entry / self.vx
            x_exit = x_inv_exit / self.vx

        if self.vy == 0:
            y_entry = float("-inf")
            y_exit = float("inf")
        else:
            y_entry = y_inv_entry / self.vy
            y_exit = y_inv_exit / self.vy

        entry_time = max(x_entry, y_entry)
        exit_time = min(x_exit, y_exit)

        if (
            entry_time > exit_time or
            x_entry < 0 and y_entry < 0 or
            x_entry > 1 or
            y_entry > 1
        ):
            normal_x = 0
            normal_y = 0
            return 1, normal_x, normal_y
        else:
            if x_entry > y_entry:
                if x_inv_entry < 0:
                    normal_x = 1
                    normal_y = 0
                else:
                    normal_x = -1
                    normal_y = 0
            else:
                if y_inv_entry < 0:
                    normal_x = 0
                    normal_y = 1
                else:
                    normal_x = 0
                    normal_y = -1

            return entry_time, normal_x, normal_y

    @property
    def broad_phase_box(self):
        return (
            self.aabb[0] if self.vx >= 0 else self.aabb[0] + self.vx,
            self.aabb[1] if self.vy >= 0 else self.aabb[1] + self.vy,
            self.aabb[2] + self.vx if self.vx >= 0 else self.aabb[2],
            self.aabb[3] + self.vy if self.vy >= 0 else self.aabb[3]
        )

    def broadCheck(self, body):
        return (
            self.broad_phase_box[2] > body.aabb[0] and
            self.broad_phase_box[0] < body.aabb[2] and
            self.broad_phase_box[3] > body.aabb[1] and
            self.broad_phase_box[1] < body.aabb[3]
        )

    def collideWith(self, vx, vy):
        tvx, tvy = self.vx, self.vy
        self.vx, self.vy = vx, vy

        collision_time = 1
        for body in [
            body for body in self.window.room.space
            if (
                body != self and
                self.x-4 < body.x < self.x+4 and
                self.y-4 < body.y < self.y+4
            )
        ]:
            if self.broadCheck(body):
                c_time, n_x, n_y = self.sweptAABB(body)
                if c_time < collision_time:
                    collision_time = c_time

        self.x += self.vx*collision_time
        self.y += self.vy*collision_time
        self.vx, self.vy = tvx, tvy
        return collision_time

    def move(self, dt):
        self.vx *= dt
        self.vy *= dt

        if self.collideWith(self.vx, self.vy) < 1:
            if self.collideWith(self.vx, 0) < 1:
                self.collideWith(0, self.vy)
