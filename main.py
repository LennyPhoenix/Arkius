import json

import jank

import source


class Application(jank.Application):
    PHYSICS_STEPS = 10

    def __init__(self):
        config = source.Config()
        super().__init__(config=config, debug_mode=True, show_fps=True)
        self.load_resources()

        self.wall = jank.Entity(
            position=(100, 0),
            body_type=jank.Entity.STATIC,
            collider=jank.shapes.Rect(
                width=16,
                height=64,
                friction=1
            )
        )
        self.wall.space = self.physics_space

        self.wall_dynamic = jank.Entity(
            position=(-100, 0),
            collider=jank.shapes.Rect(
                width=16,
                height=64,
                friction=1
            )
        )
        self.wall_dynamic.space = self.physics_space

        self.player = source.Player(jank.Vec2d(0, 0))
        self.camera.zoom = 5

    def load_resources(self):
        self.resources = {}

        player_sheet = jank.resource.image("resources/sprites/player.png")
        player_data_file = jank.resource.file("resources/sprites/player.json", "r")
        player_data = json.load(player_data_file)

        self.resources["player"] = jank.load_animation_sheet(player_sheet, player_data)

    def on_fixed_update(self, dt):
        for _ in range(self.PHYSICS_STEPS):
            self.physics_space.step(1/120 / self.PHYSICS_STEPS)

    def on_key_press(self, button, *args):
        if button == jank.key.GRAVE:
            self.debug_mode = not self.debug_mode


if __name__ == "__main__":
    application = Application()
    application.run()
