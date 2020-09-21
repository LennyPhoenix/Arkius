import typing as t

import jank

from .fade_renderer import FadeRenderer


class Player(jank.Entity, jank.StateMachine):
    SPEED: float = 96.

    DASH_SPEED_MULTIPLIER: float = 4.
    DASH_COOLDOWN: float = .15
    DASH_DURATION: float = .20
    DASH_SHADOW_FREQUENCY: float = .05
    DASH_SHADOW_DURATION: float = .1
    DASH_SHADOW_START_OPACITY: int = 128
    DASH_SHADOW_END_OPACITY: int = 0

    controls: t.Dict[str, bool] = {
        "up": False,
        "down": False,
        "left": False,
        "right": False,
    }

    dash_cooldown_timer: float = 0.
    dash_duration_timer: float = 0.
    dash_shadow_timer: float = 0.

    def __init__(self, position: jank.Vec2d):
        self.shadows = []

        jank.get_app().push_handlers(self)

        space: jank.physics.Space = jank.get_app().physics_space

        super().__init__(
            position=position,
            mass=5,
            collider=jank.colliders.Segment(
                a=(-3, 1),
                b=(3, 1),
                radius=4,
                friction=0
            )
        )
        self.friction_constraint = jank.physics.PivotJoint(
            space.static_body,
            self.body,
            (0, 0), (0, 0)
        )

        self.space = space

        self.state_sprites: dict = jank.get_app().resources["player"]

        self.renderer = jank.renderer.SpriteRenderer(
            self.state_sprites["idle"],
            batch=jank.get_app().world_batch,
            group=jank.get_app().world_layers["y_ordered"]
        )
        self.renderer.offset = (0, 9)

        self.state = "idle"

    def set_space(self, space: jank.physics.Space):
        super().set_space(space)

    def on_state_change(self, state: str, previous_state: str):
        if state in self.state_sprites.keys():
            self.renderer.image = self.state_sprites[state]

    def on_key_press(self, button: int, *args):

        # Flip Renderer
        if button == jank.key.A:
            self.renderer.flip_x = True
        if button == jank.key.D:
            self.renderer.flip_x = False

        # Trigger Dash
        if button == jank.key.SPACE and self.dash_cooldown_timer <= 0 and self.state != "dash":
            self.state = "dash"

            # TODO Calculate velocity.

            self.dash_duration_timer = self.DASH_DURATION
            self.dash_shadow_timer = 0.

    def on_update(self, dt: float):
        keys = jank.get_app().key_handler
        self.controls = {
            "up": (keys[jank.key.W] or keys[jank.key.UP]),
            "down": (keys[jank.key.S] or keys[jank.key.DOWN]),
            "left": (keys[jank.key.A] or keys[jank.key.LEFT]),
            "right": (keys[jank.key.D] or keys[jank.key.RIGHT]),
        }

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= dt
            if self.dash_cooldown_timer <= 0:
                self.dash_cooldown_timer = 0.

        if self.state == "dash":
            self.dash_duration_timer -= dt
            self.dash_shadow_timer -= dt
            if self.dash_duration_timer <= 0:
                self.state = "walk"
                self.dash_duration_timer = 0.
                self.dash_cooldown_timer = self.DASH_COOLDOWN
            if self.dash_shadow_timer <= 0:
                self.dash_shadow_timer = self.DASH_SHADOW_FREQUENCY
                fi = self.renderer.sprite._frame_index
                frame = self.renderer.image.frames[fi].image
                shadow = FadeRenderer(
                    frame,
                    *self.position,
                    self.DASH_SHADOW_DURATION,
                    self.DASH_SHADOW_START_OPACITY,
                    self.DASH_SHADOW_END_OPACITY,
                    batch=jank.get_app().world_batch,
                    group=jank.get_app().world_layers["g_particles"]
                )
                shadow.offset = (0, 9)
                shadow.flip_x = self.renderer.flip_x
                self.shadows.append(shadow)

    def get_velocity(self, speed=SPEED):
        vel = jank.Vec2d.zero()

        if self.controls["up"]:
            vel.y += speed
        if self.controls["down"]:
            vel.y -= speed
        if self.controls["left"]:
            vel.x -= speed
        if self.controls["right"]:
            vel.x += speed

        if self.state != "dash":
            if vel.length != 0:
                self.state = "walk"
            else:
                self.state = "idle"

        if (
            (self.controls["up"] ^ self.controls["down"])
            and (self.controls["left"] ^ self.controls["right"])
        ):
            vel /= 2**.5

        return vel

    def velocity_func(self, body, gravity, damping, dt):
        vel = self.get_velocity()
        body.velocity = vel + gravity
