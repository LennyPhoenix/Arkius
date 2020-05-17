import pymunk
from pyglet.window import key, mouse

from . import constants as c
from . import particle
from .basic import Basic


class Player(Basic):
    _state = "idle_right"

    def __init__(self, application):
        self.room = (0, 0)

        anim = application.resources["player"]["idle_right"]
        super().__init__(
            application,
            0, 0,
            anim,
            card_sprite=True,
            collider=c.PLAYER_COLLIDER,
            body_type=pymunk.Body.DYNAMIC,
            space=application.world.map[self.room].space
        )
        self.sprite.group = self.application.layers["world"]["y_ordered"]

        self.dash_vel = pymunk.vec2d.Vec2d(0, 0)
        self.dash_time = 0
        self.dash_length = 0.25
        self.dash_multiplier = 6
        self.dash_cooldown = 0.15

        self.last_shadow = 0
        self.shadow_frequency = 1/50

        self.vx, self.vy = 0, 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state != self.state:
            if state in self.application.resources["player"].keys():
                anim = self.application.resources["player"][state]
                self.sprite.image = anim
            elif state == "locked":
                if self._state == "walk_right":
                    self.state = "idle_right"
                elif self._state == "walk_left":
                    self.state = "idle_left"
            self._state = state

    def update(self, dt):
        controls = {
            "up": (
                self.application.key_handler[key.W] or
                self.application.key_handler[key.UP]
            ),
            "down": (
                self.application.key_handler[key.S] or
                self.application.key_handler[key.DOWN]
            ),
            "left": (
                self.application.key_handler[key.A] or
                self.application.key_handler[key.LEFT]
            ),
            "right": (
                self.application.key_handler[key.D] or
                self.application.key_handler[key.RIGHT]
            ),
            "dash": (
                self.application.mouse_handler[mouse.RIGHT]
            )
        }

        # Position
        self.vx, self.vy = 0, 0
        if controls["up"]:
            self.vy += c.PLAYER_SPEED
        if controls["down"]:
            self.vy -= c.PLAYER_SPEED
        if controls["left"]:
            self.vx -= c.PLAYER_SPEED
        if controls["right"]:
            self.vx += c.PLAYER_SPEED

        if (
            self.vx != 0 and
            self.vy != 0
        ):
            self.vx /= 2**0.5
            self.vy /= 2**0.5

        if self.state == "locked":
            return super().update(dt)

        if self.state == "dashing":
            if self.last_shadow >= self.shadow_frequency:
                shadow_image = self.sprite.image.frames[
                    self.sprite._frame_index
                ].image
                particle.Shadow(
                    self.application,
                    self.position.x, self.position.y,
                    shadow_image,
                    0.25,
                    128
                )
                self.last_shadow = 0
            else:
                self.last_shadow += dt

            self.dash_time += dt
            if self.dash_time >= self.dash_length:
                self.dash_time = 0
                if self.dash_vel.x > 0:
                    self.state = "idle_right"
                elif self.dash_vel.x < 0:
                    self.state = "idle_left"
                else:
                    self.state = "idle_right"

            self.apply_force_at_world_point(
                self.dash_vel+pymunk.vec2d.Vec2d(self.vx, self.vy),
                (0, 0)
            )
            self.checkDoors()
            return super().update(dt)

        if (
            controls["up"] ^
            controls["down"]
        ):
            if self.state == "idle_left":
                self.state = "walk_left"
            elif self.state == "idle_right":
                self.state = "walk_right"

        if (
            controls["left"] ^
            controls["right"]
        ):
            if controls["left"] and self.state != "walk_left":
                self.state = "walk_left"
            if controls["right"] and self.state != "walk_right":
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
            controls["dash"] and
            self.dash_time >= self.dash_cooldown
        ):
            if (self.vx, self.vy) != (0, 0):
                self.dash_time = 0
                self.dash_vel = pymunk.vec2d.Vec2d(
                    self.vx, self.vy)*self.dash_multiplier
                self.state = "dashing"
        elif (
            not controls["dash"]
        ):
            self.dash_time += dt

        self.apply_force_at_local_point(
            pymunk.vec2d.Vec2d(self.vx, self.vy),
            (0, 0)
        )
        self.checkDoors()
        super().update(dt)

    def checkDoors(self):
        def on_black(door):
            while len(self.application.particles) > 0:
                self.application.particles[0].destroy()
            self.application.room.visibility = False
            self.application.room.space.remove(self, self.collider)
            if door == 0:  # Top
                self.application.room.visibility = False
                if self.application.room.map_data is not None:
                    offset = (
                        self.position.x -
                        self.application.room.map_data[
                            "door_info"
                        ][0]["pos"]*16
                    )
                else:
                    offset = self.position.x
                self.room = (
                    self.room[0], self.room[1]+1
                )
                self.application.room.visibility = True
                if self.application.room.map_data is not None:
                    self.position = (
                        offset +
                        self.application.room.map_data[
                            "door_info"
                        ][2]["pos"]*16,
                        -(self.application.room.height+2.5)*16
                    )
                else:
                    self.position = (
                        0 + offset,
                        -(self.application.room.height+2.5)*16
                    )
            elif door == 1:  # Right
                if self.application.room.map_data is not None:
                    offset = (
                        self.position.y -
                        self.application.room.map_data[
                            "door_info"
                        ][1]["pos"]*16
                    )
                else:
                    offset = self.position.y
                self.room = (
                    self.room[0]+1, self.room[1]
                )
                self.application.room.visibility = True
                if self.application.room.map_data is not None:
                    self.position = (
                        -(self.application.room.width+2.5)*16,
                        (
                            offset +
                            self.application.room.map_data[
                                "door_info"
                            ][3]["pos"]*16
                        )
                    )
                else:
                    self.position = (
                        -(self.application.room.width+2.5)*16,
                        offset + 0
                    )
            elif door == 3:  # Left
                self.application.room.visibility = False
                if self.application.room.map_data is not None:
                    offset = (
                        self.position.y -
                        self.application.room.map_data[
                            "door_info"
                        ][3]["pos"]*16
                    )
                else:
                    offset = self.position.y
                self.room = (
                    self.room[0]-1, self.room[1]
                )
                self.application.room.visibility = True
                self.position.x = (self.application.room.width+3)*16

                if self.application.room.map_data is not None:
                    self.position = (
                        (self.application.room.width+2.5)*16,
                        (
                            offset +
                            self.application.room.map_data[
                                "door_info"
                            ][1]["pos"]*16
                        )
                    )
                else:
                    self.position = (
                        (self.application.room.width+2.5)*16,
                        offset + 0
                    )
            elif door == 2:  # Bottom
                self.application.room.visibility = False
                if self.application.room.map_data is not None:
                    offset = (
                        self.position.x -
                        self.application.room.map_data[
                            "door_info"
                        ][2]["pos"]*16
                    )
                else:
                    offset = self.position.x
                self.room = (
                    self.room[0], self.room[1]-1
                )
                self.application.room.visibility = True
                if self.application.room.map_data is not None:
                    self.position = (
                        offset +
                        self.application.room.map_data[
                            "door_info"
                        ][0]["pos"]*16,
                        (self.application.room.height+2.5)*16
                    )
                else:
                    self.position = (
                        0 + offset,
                        (self.application.room.height+2.5)*16
                    )
            self.application.room.space.add(self, self.collider)
            self.application.world.ui_map.discover(self.room)
            self.door = None

        def on_done():
            self.state = self.pre_locked

        # Bottom Door
        if self.position.y <= -(self.application.room.height+3)*16:
            self.pre_locked = str(self.state)
            self.state = "locked"
            self.application.transition.begin(
                on_black=on_black, on_black_args=[2], on_done=on_done
            )

        # Left Door
        if self.position.x <= -(self.application.room.width+3)*16:
            self.pre_locked = str(self.state)
            self.state = "locked"
            self.application.transition.begin(
                on_black=on_black, on_black_args=[3], on_done=on_done
            )

        # Top Door
        if self.position.y >= (self.application.room.height+3)*16:
            self.pre_locked = str(self.state)
            self.state = "locked"
            self.application.transition.begin(
                on_black=on_black, on_black_args=[0], on_done=on_done
            )

        # Right Door
        if self.position.x >= (self.application.room.width+3)*16:
            self.pre_locked = str(self.state)
            self.state = "locked"
            self.application.transition.begin(
                on_black=on_black, on_black_args=[1], on_done=on_done
            )
