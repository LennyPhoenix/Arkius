import jank


class Player(jank.Entity, jank.StateMachine):
    _state = "idle"

    def __init__(self, position: jank.Vec2d):
        jank.get_app().push_handlers(self)

        super().__init__(
            position=position,
            mass=5,
            collider=jank.shapes.Segment(
                a=(-3, 0),
                b=(3, 0),
                radius=4,
                friction=1
            )
        )
        self.space: jank.physics.Space = jank.get_app().physics_space

        self.state_sprites: dict = jank.get_app().resources["player"]

        self.sprite_offset = (0, 8)
        self.sprite = jank.Sprite(
            self.state_sprites["idle"],
            0, 0,
            batch=jank.get_app().world_batch,
            group=jank.get_app().world_layers["y_ordered"]
        )

    def on_state_change(self, state, previous_state):
        if state in self.state_sprites.keys():
            self.sprite.image = self.state_sprites[state]

    def on_key_press(self, button, *args):
        if button == jank.key.ENTER:
            state_changer = {
                "idle": "walk",
                "walk": "idle"
            }
            self.state = state_changer[self.state]
