import json

import jank

import source


class Application(jank.Application):
    PHYSICS_STEPS = 10

    def __init__(self):
        config = source.Config()
        super().__init__(config=config, debug_mode=False, show_fps=True)
        self.load_resources()

        self.wall = jank.Entity(
            position=(100, 0),
            body_type=jank.Entity.STATIC,
            collider=jank.colliders.Rect(
                width=16,
                height=16,
                friction=0.5
            )
        )
        self.wall.renderer = jank.renderer.RectRenderer(16, 16, batch=jank.get_app().world_batch)
        self.wall_label = jank.renderer.TextRenderer(
            "1 Tile ↓", font_size=8,
            batch=self.world_batch
        )
        self.wall_label.update(position=self.wall.position)
        self.wall_label.offset = (-16, 20)
        self.wall.space = self.physics_space

        self.player = source.Player(jank.Vec2d(0, 0))
        self.camera.zoom = 2

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
