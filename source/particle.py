import pyglet

from .basic import Basic


class Particle(Basic):
    def __init__(self, application, x, y, image, card_sprite=False):
        super().__init__(application, x, y, image, card_sprite=card_sprite)
        self.sprite.group = self.application.layers["world"]["g_particles"]
        self.application.particles.append(self)

    def destroy(self):
        self.sprite.delete()
        self.application.particles.remove(self)


class TimedParticle(Particle):
    def __init__(self, application, x, y, image, lifetime, update=1/15, card_sprite=False):  # noqa: E501
        super().__init__(application, x, y, image, card_sprite=card_sprite)
        self.lifetime = lifetime
        self.time = 0
        pyglet.clock.schedule_interval_soft(self.update, update)

    def update(self, dt):
        self.time += dt
        if self.time >= self.lifetime:
            self.destroy()
            return False
        return True

    def destroy(self):
        pyglet.clock.unschedule(self.update)
        super().destroy()


class AnimationBasedParticle(Particle):
    def __init__(self, application, x, y, animation, card_sprite=False):
        super().__init__(application, x, y, animation, card_sprite=card_sprite)
        self.sprite.push_handlers(self)

    def on_animation_end(self):
        self.destroy()


class Shadow(TimedParticle):
    def __init__(self, application, x, y, image, lifetime, initial_opacity):
        super().__init__(
            application,
            x, y,
            image,
            lifetime,
            update=1/30,
            card_sprite=True
        )
        self.sprite.group = self.application.layers["world"]["a_particles"]
        self.initial_opacity = initial_opacity
        self.opacity_step = self.initial_opacity/self.lifetime
        self.sprite.opacity = self.initial_opacity

    def update(self, dt):
        if super().update(dt):
            self.sprite.opacity -= self.opacity_step*dt
