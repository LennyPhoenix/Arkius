import random

import pyglet
from pyglet.window import key

from . import constants as c
from .basic import Basic
from . import particle


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

        super().__init__(
            application,
            x, y,
            image,
            card_sprite=self.type == c.WALL,
            collider=c.TILES[self.type]["collider"],
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
                x = self.x+random.randint(2, 6)/16
                y = self.y+random.randint(2, 4)/16
                particle.AnimationBasedParticle(
                    self.application,
                    x,
                    y,
                    self.application.resources["lava_bubble"]
                )
                self.last_bubble = 0
                self.to_wait = random.randint(4, 16)/2


class Player(Basic):
    def __init__(self, application):
        self._state = "idle_right"
        anim = application.resources["player"]["idle_right"]
        super().__init__(
            application,
            0, 0,
            anim,
            card_sprite=True,
            collider=c.PLAYER_COLLIDER,
            static=False
        )
        self.sprite.group = self.application.layers["world"]["y_ordered"]

        self.room = (0, 0)

        self.last_shadow = 0
        self.shadow_frequency = 1/25

        self.cx = c.PLAYER_COLLIDER["x"]
        self.cy = c.PLAYER_COLLIDER["y"]
        self.cw = c.PLAYER_COLLIDER["width"]
        self.ch = c.PLAYER_COLLIDER["height"]

        self.vx = 0
        self.vy = 0

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
        self.vx, self.vy = 0, 0
        if self.state != "locked":
            if controls["up"]:
                self.vy += c.PLAYER_SPEED
            if controls["down"]:
                self.vy -= c.PLAYER_SPEED
            if controls["left"]:
                self.vx -= c.PLAYER_SPEED
            if controls["right"]:
                self.vx += c.PLAYER_SPEED

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

            if (
                self.vx == 0 and
                self.vy == 0
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
                        self.application,
                        self.x, self.y,
                        shadow_image,
                        0.25,
                        128
                    )
                    self.last_shadow = 0

        self.move(dt)
        self.checkDoors()
        super().update()

    def checkDoors(self):
        def on_black(door):
            while len(self.application.particles) > 0:
                self.application.particles[0].destroy()
            self.application.room.visibility = False
            if door == 0:
                self.application.room.visibility = False
                if self.application.room.map_data is not None:
                    offset = (
                        self.x -
                        self.application.room.map_data["door_info"][0]["pos"]
                    )
                else:
                    offset = self.x
                self.room = (
                    self.room[0], self.room[1]+1
                )
                self.application.room.visibility = True
                self.y = -(self.application.room.height+3)
                if self.application.room.map_data is not None:
                    self.x = (
                        offset +
                        self.application.room.map_data["door_info"][2]["pos"]
                    )
                else:
                    self.x = 0 + offset
            elif door == 1:
                if self.application.room.map_data is not None:
                    offset = (
                        self.y -
                        self.application.room.map_data["door_info"][1]["pos"]
                    )
                else:
                    offset = self.y
                self.room = (
                    self.room[0]+1, self.room[1]
                )
                self.application.room.visibility = True
                self.x = -(self.application.room.width+3)
                if self.application.room.map_data is not None:
                    self.y = (
                        offset +
                        self.application.room.map_data["door_info"][3]["pos"]
                    )
                else:
                    self.y = 0 + offset
            elif door == 3:
                self.application.room.visibility = False
                if self.application.room.map_data is not None:
                    offset = (
                        self.y -
                        self.application.room.map_data["door_info"][3]["pos"]
                    )
                else:
                    offset = self.y
                self.room = (
                    self.room[0]-1, self.room[1]
                )
                self.application.room.visibility = True
                self.x = self.application.room.width+3
                if self.application.room.map_data is not None:
                    self.y = (
                        offset +
                        self.application.room.map_data["door_info"][1]["pos"]
                    )
                else:
                    self.y = 0 + offset
            elif door == 2:
                self.application.room.visibility = False
                if self.application.room.map_data is not None:
                    offset = (
                        self.x -
                        self.application.room.map_data["door_info"][2]["pos"]
                    )
                else:
                    offset = self.x
                self.room = (
                    self.room[0], self.room[1]-1
                )
                self.application.room.visibility = True
                self.y = self.application.room.height+3
                if self.application.room.map_data is not None:
                    self.x = (
                        offset +
                        self.application.room.map_data["door_info"][0]["pos"]
                    )
                else:
                    self.x = 0 + offset
            self.application.world.ui_map.discover(self.room)
            self.door = None

        def on_done():
            self.state = self.pre_locked

        if self.state != "locked":
            # Bottom Door
            if self.y < -(self.application.room.height+3):
                self.pre_locked = str(self.state)
                self.state = "locked"
                self.application.transition.begin(
                    on_black=on_black, on_black_args=[2], on_done=on_done
                )

            # Left Door
            if self.x < -(self.application.room.width+3):
                self.pre_locked = str(self.state)
                self.state = "locked"
                self.application.transition.begin(
                    on_black=on_black, on_black_args=[3], on_done=on_done
                )

            # Top Door
            if self.y > self.application.room.height+3:
                self.pre_locked = str(self.state)
                self.state = "locked"
                self.application.transition.begin(
                    on_black=on_black, on_black_args=[0], on_done=on_done
                )

            # Right Door
            if self.x > self.application.room.width+3:
                self.pre_locked = str(self.state)
                self.state = "locked"
                self.application.transition.begin(
                    on_black=on_black, on_black_args=[1], on_done=on_done
                )
