from .basic import Basic

import pyglet


class Particle(Basic):
    def __init__(self, window, x, y, image, lifetime, card_sprite=False):
        super().__init__(window, x, y, image, card_sprite)
        self.sprite.group = self.window.layers["world"]["particles"]
        self.lifetime = lifetime
        self.time = 0
        pyglet.clock.schedule_interval(self.update, 1/15)
        self.window.particles.append(self)

    def update(self, dt):
        self.time += dt
        if self.time >= self.lifetime:
            self.sprite.delete()
            pyglet.clock.unschedule(self.update)
            self.window.particles.remove(self)
            return False
        super().update()
        return True


class Shadow(Particle):
    def __init__(self, window, x, y, image, lifetime, initial_opacity):
        super().__init__(window, x, y, image, lifetime)
        self.sprite.group = self.window.layers["world"]["y_ordered"]
        self.initial_opacity = initial_opacity
        self.opacity_step = self.initial_opacity/self.lifetime
        self.sprite.opacity = self.initial_opacity

    def update(self, dt):
        if super().update(dt):
            self.sprite.opacity -= self.opacity_step*dt
