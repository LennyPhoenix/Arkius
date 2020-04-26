from math import floor

import pyglet

from .cardsprite import CardSprite


# class AnimationPlayer(pyglet.sprite.Sprite):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._paused = False

#     def pause_animation(self):
#         if self._paused or self._animation is None:
#             return
#         pyglet.clock.unschedule(self._animate)
#         self._paused = True

#     def resume_animation(self):
#         if not self._paused or self._animation is None:
#             return
#         frame = self._animation.frames[self._frame_index]
#         self._texture = frame.image.get_texture()
#         self._next_dt = frame.duration
#         if self._next_dt:
#             pyglet.clock.schedule_once(self._animate, self._next_dt)
#         self._paused = False

#     @property
#     def paused(self):
#         return self._paused

#     @paused.setter
#     def paused(self, pause):
#         if pause:
#             self.pause_animation()
#         else:
#             self.resume_animation()

#     @property
#     def frame_index(self):
#         return self._frame_index

#     @frame_index.setter
#     def frame_index(self, index):
#         # Bound to available number of frames
#         self._frame_index = max(0, min(index, len(self._animation.frames)-1))

#     def on_animation_end(self):
#         print("Animation Ended!")
#         # Do some predefined action


class Basic:
    """Basic entity."""

    def __init__(self, window, x, y, image, card_sprite=False):
        """Initialise with position, dimensions and a sprite.

        Arguments:
            window {Window} -- The window for the application.
            x {float} -- The world X position of the entity.
            y {float} -- The world Y position of the entity.
            image {pyglet.image} -- The image to be used for the sprite.
            card_sprite {bool} -- Whether or not to use the "CardSprite".
        """
        self.window = window
        self.x = x
        self.y = y
        self.grid_x, self.grid_y = floor(self.x), floor(self.y)

        self.screen_x, self.screen_y = window.worldToScreen(self.x, self.y)
        if card_sprite:
            self.sprite = CardSprite(
                image,
                x=self.screen_x, y=self.screen_y,
                batch=self.window.world_batch,
                subpixel=True
            )
        else:
            self.sprite = pyglet.sprite.Sprite(
                image,
                x=self.screen_x, y=self.screen_y,
                batch=self.window.world_batch,
                subpixel=True
            )

    def update(self):
        """Update the sprite and any position variables."""
        self.x = round(self.x*16)/16
        self.y = round(self.y*16)/16
        self.grid_x, self.grid_y = floor(self.x), floor(self.y)

        screen_pos = self.window.worldToScreen(self.x, self.y)
        self.screen_x, self.screen_y = screen_pos[0], screen_pos[1]

        self.sprite.update(
            x=self.screen_x,
            y=self.screen_y
        )
