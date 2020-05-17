import pymunk
from pyglet.window import key, mouse

from . import constants as c
from . import particle
from .basic import Basic


class Player(Basic):
    _state = "idle"

    def __init__(self, application):
        self.room = (0, 0)

        anim = application.resources["player"]["idle"]
        super().__init__(
            application,
            0, 0,
            anim,
            card_sprite=True,
            collider=c.PLAYER_COLLIDER,
            collision_type=c.COLLISION_TYPES["player"],
            body_type=pymunk.Body.DYNAMIC,
            space=application.world.map[self.room].space
        )
        self.sprite.group = self.application.layers["world"]["y_ordered"]

        self.dash_vel = pymunk.vec2d.Vec2d(0, 0)
        self.dash_time = 0
        self.dash_length = 0.25
        self.dash_multiplier = 6
        self.dash_cooldown = 0.15
        self.dash_cooldown_timer = 0

        self.last_shadow = 0
        self.shadow_frequency = 1/50

        self.locked = False

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

        if self.locked:
            return super().update(dt)

        if self.state == "dashing":
            if self.last_shadow >= self.shadow_frequency:
                self.last_shadow = 0
                shadow_image = self.sprite.image.frames[
                    self.sprite._frame_index
                ].image
                shadow = particle.Shadow(
                    self.application,
                    self.position.x, self.position.y,
                    shadow_image,
                    0.25,
                    128
                )
                shadow.flip = self.flip
            else:
                self.last_shadow += dt

            self.dash_time += dt
            if self.dash_time >= self.dash_length:
                self.dash_cooldown_timer = 0
                self.dash_time = 0
                self.state = "idle"

            self.apply_force_at_world_point(
                self.dash_vel+pymunk.vec2d.Vec2d(self.vx, self.vy),
                (0, 0)
            )
            self.checkDoors()
            return super().update(dt)

        if (
            (self.vx, self.vy) != (0, 0) and
            self.state == "idle"
        ):
            self.state = "walk"
        elif (
            (self.vx, self.vy) == (0, 0) and
            self.state == "walk"
        ):
            self.state = "idle"

        if (
            controls["dash"] and
            self.dash_cooldown_timer >= self.dash_cooldown
        ):
            if (self.vx, self.vy) != (0, 0):
                self.dash_cooldown_timer = 0
                self.dash_time = 0
                self.dash_vel = pymunk.vec2d.Vec2d(
                    self.vx, self.vy)*self.dash_multiplier
                self.state = "dashing"
        elif (
            not controls["dash"]
        ):
            self.dash_cooldown_timer += dt

        self.apply_force_at_local_point(
            pymunk.vec2d.Vec2d(self.vx, self.vy),
            (0, 0)
        )

        if self.vx < 0:
            self.flip = True
        elif self.vx > 0:
            self.flip = False

        self.checkDoors()
        super().update(dt)

    def checkDoors(self):
        def on_black(door):
            self.state = "idle"
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
            self.locked = False

        # Bottom Door
        if self.position.y <= -(self.application.room.height+3)*16:
            self.locked = True
            self.application.transition.begin(
                on_black=on_black, on_black_args=[2], on_done=on_done
            )

        # Left Door
        if self.position.x <= -(self.application.room.width+3)*16:
            self.locked = True
            self.application.transition.begin(
                on_black=on_black, on_black_args=[3], on_done=on_done
            )

        # Top Door
        if self.position.y >= (self.application.room.height+3)*16:
            self.locked = True
            self.application.transition.begin(
                on_black=on_black, on_black_args=[0], on_done=on_done
            )

        # Right Door
        if self.position.x >= (self.application.room.width+3)*16:
            self.locked = True
            self.application.transition.begin(
                on_black=on_black, on_black_args=[1], on_done=on_done
            )
