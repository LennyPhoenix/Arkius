import random

import pyglet
import pymunk
from pyglet.window import key

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

        self.last_shadow = 0
        self.shadow_frequency = 1/25

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
                self.application.key_handler[key.LSHIFT]
            )
        }

        # Position
        vx, vy = 0, 0
        if self.state != "locked":
            if controls["up"]:
                vy += c.PLAYER_SPEED
            if controls["down"]:
                vy -= c.PLAYER_SPEED
            if controls["left"]:
                vx -= c.PLAYER_SPEED
            if controls["right"]:
                vx += c.PLAYER_SPEED

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
                (
                    controls["left"] or
                    controls["right"]
                ) and
                (
                    controls["up"] or
                    controls["down"]
                )
            ):
                vx /= 2**0.5
                vy /= 2**0.5

            if controls["dash"]:
                vx *= 5
                vy *= 5
                self.last_shadow += dt
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

        self.apply_force_at_local_point((vx, vy), (0, 0))
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
                        -(self.application.room.height+3)*16
                    )
                else:
                    self.position = (
                        0 + offset,
                        -(self.application.room.height+3)*16
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
                        -(self.application.room.width+3)*16,
                        (
                            offset +
                            self.application.room.map_data[
                                "door_info"
                            ][3]["pos"]*16
                        )
                    )
                else:
                    self.position = (
                        -(self.application.room.width+3)*16,
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
                        (self.application.room.width+3)*16,
                        (
                            offset +
                            self.application.room.map_data[
                                "door_info"
                            ][1]["pos"]*16
                        )
                    )
                else:
                    self.position = (
                        (self.application.room.width+3)*16,
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
                        (self.application.room.height+3)*16
                    )
                else:
                    self.position = (
                        0 + offset,
                        (self.application.room.height+3)*16
                    )
            self.application.room.space.add(self, self.collider)
            self.application.world.ui_map.discover(self.room)
            self.door = None

        def on_done():
            self.state = self.pre_locked

        if self.state != "locked":
            # Bottom Door
            if self.position.y < -(self.application.room.height+3)*16:
                self.pre_locked = str(self.state)
                self.state = "locked"
                self.application.transition.begin(
                    on_black=on_black, on_black_args=[2], on_done=on_done
                )

            # Left Door
            if self.position.x < -(self.application.room.width+3)*16:
                self.pre_locked = str(self.state)
                self.state = "locked"
                self.application.transition.begin(
                    on_black=on_black, on_black_args=[3], on_done=on_done
                )

            # Top Door
            if self.position.y > (self.application.room.height+3)*16:
                self.pre_locked = str(self.state)
                self.state = "locked"
                self.application.transition.begin(
                    on_black=on_black, on_black_args=[0], on_done=on_done
                )

            # Right Door
            if self.position.x > (self.application.room.width+3)*16:
                self.pre_locked = str(self.state)
                self.state = "locked"
                self.application.transition.begin(
                    on_black=on_black, on_black_args=[1], on_done=on_done
                )
