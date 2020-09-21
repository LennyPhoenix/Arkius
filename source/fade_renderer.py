import jank


class FadeRenderer(jank.renderer.SpriteRenderer):
    duration: float

    start_opacity: int = 255
    end_opacity: int = 0
    timer: float = 0.

    def __init__(
        self,
        image: jank.pyglet.image.AbstractImage,
        x: float, y: float,
        duration: float,
        start_opacity: int = 255,
        end_opacity: int = 0,
        update_frequency: float = 1/30,
        batch: jank.graphics.Batch = None,
        group: jank.graphics.Group = None,
        subpixel: bool = False
    ):
        self.duration = duration
        self.timer = 0.
        self.start_opacity = start_opacity
        self.end_opacity = end_opacity

        super().__init__(image, batch=batch, group=group, subpixel=subpixel)
        self.update((x, y))
        self.opacity = self.start_opacity

        jank.clock.schedule_interval_soft(self.opacity_clock, update_frequency)

    def opacity_clock(self, dt: float):
        self.timer += dt

        time = self.timer / self.duration
        self.opacity = round((self.end_opacity - self.start_opacity)*time)+self.start_opacity

        if self.timer >= self.duration:
            jank.clock.unschedule(self.opacity_clock)
            self.delete()
