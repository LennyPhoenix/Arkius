import math

from pyglet.gl import *
from pyglet import clock
from pyglet import event
from pyglet import graphics
from pyglet import image


class SpriteGroup(graphics.Group):
    """Shared sprite rendering group.

    The group is automatically coalesced with other sprite groups sharing the
    same parent group, texture and blend parameters.
    """

    def __init__(self, texture, blend_src, blend_dest, parent=None):
        """Create a sprite group.

        The group is created internally within `Sprite`; applications usually
        do not need to explicitly create it.

        :Parameters:
            `texture` : `Texture`
                The (top-level) texture containing the sprite image.
            `blend_src` : int
                OpenGL blend source mode; for example,
                ``GL_SRC_ALPHA``.
            `blend_dest` : int
                OpenGL blend destination mode; for example,
                ``GL_ONE_MINUS_SRC_ALPHA``.
            `parent` : `Group`
                Optional parent group.
        """
        super(SpriteGroup, self).__init__(parent)
        self.texture = texture
        self.blend_src = blend_src
        self.blend_dest = blend_dest

    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)
        glPushAttrib(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_BLEND)
        glBlendFunc(self.blend_src, self.blend_dest)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GREATER, 0.01)

    def unset_state(self):
        glPopAttrib()
        glDisable(self.texture.target)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.texture)

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.texture.target == other.texture.target and
                self.texture.id == other.texture.id and
                self.blend_src == other.blend_src and
                self.blend_dest == other.blend_dest)

    def __hash__(self):
        return hash((id(self.parent),
                     self.texture.id, self.texture.target,
                     self.blend_src, self.blend_dest))


class CardSprite(event.EventDispatcher):
    """Instance of an on-screen image.

    See the module documentation for usage.
    """

    _batch = None
    _animation = None
    _rotation = 0
    _opacity = 255
    _rgb = (255, 255, 255)
    _scale = 1.0
    _scale_x = 1.0
    _scale_y = 1.0
    _visible = True
    _vertex_list = None

    def __init__(self,
                 img, x=0, y=0,
                 blend_src=GL_SRC_ALPHA,
                 blend_dest=GL_ONE_MINUS_SRC_ALPHA,
                 batch=None,
                 group=None,
                 usage='dynamic',
                 subpixel=False,
                 tilt=1):
        """Create a sprite.

        :Parameters:
            `img` : `AbstractImage` or `Animation`
                Image or animation to display.
            `x` : int
                X coordinate of the sprite.
            `y` : int
                Y coordinate of the sprite.
            `blend_src` : int
                OpenGL blend source mode.  The default is suitable for
                compositing sprites drawn from back-to-front.
            `blend_dest` : int
                OpenGL blend destination mode.  The default is suitable for
                compositing sprites drawn from back-to-front.
            `batch` : `Batch`
                Optional batch to add the sprite to.
            `group` : `Group`
                Optional parent group of the sprite.
            `usage` : str
                Vertex buffer object usage hint, one of ``"none"``,
                ``"stream"``, ``"dynamic"`` (default) or ``"static"``.  Applies
                only to vertex data.
            `subpixel` : bool
                Allow floating-point coordinates for the sprite. By default,
                coordinates are restricted to integer values.
        """
        if batch is not None:
            self._batch = batch

        self._x = x
        self._y = y

        if isinstance(img, image.Animation):
            self._animation = img
            self._frame_index = 0
            self._texture = img.frames[0].image.get_texture()
            self._next_dt = img.frames[0].duration
            if self._next_dt:
                clock.schedule_once(self._animate, self._next_dt)
        else:
            self._texture = img.get_texture()

        self._group = SpriteGroup(self._texture, blend_src, blend_dest, group)
        self._usage = usage
        self._subpixel = subpixel
        self._tilt = tilt
        self._create_vertex_list()

    def __del__(self):
        try:
            if self._vertex_list is not None:
                self._vertex_list.delete()
        except:
            pass

    def delete(self):
        """Force immediate removal of the sprite from video memory.

        This is often necessary when using batches, as the Python garbage
        collector will not necessarily call the finalizer as soon as the
        sprite is garbage.
        """
        if self._animation:
            clock.unschedule(self._animate)
        self._vertex_list.delete()
        self._vertex_list = None
        self._texture = None

        # Easy way to break circular reference, speeds up GC
        self._group = None

    def _animate(self, dt):
        self._frame_index += 1
        if self._frame_index >= len(self._animation.frames):
            self._frame_index = 0
            self.dispatch_event('on_animation_end')
            if self._vertex_list is None:
                return  # Deleted in event handler.

        frame = self._animation.frames[self._frame_index]
        self._set_texture(frame.image.get_texture())

        if frame.duration is not None:
            duration = frame.duration - (self._next_dt - dt)
            duration = min(max(0, duration), frame.duration)
            clock.schedule_once(self._animate, duration)
            self._next_dt = duration
        else:
            self.dispatch_event('on_animation_end')

    @property
    def batch(self):
        """Graphics batch.

        The sprite can be migrated from one batch to another, or removed from
        its batch (for individual drawing).  Note that this can be an expensive
        operation.

        :type: `Batch`
        """
        return self._batch

    @batch.setter
    def batch(self, batch):
        if self._batch == batch:
            return

        if batch is not None and self._batch is not None:
            self._batch.migrate(self._vertex_list,
                                GL_QUADS, self._group, batch)
            self._batch = batch
        else:
            self._vertex_list.delete()
            self._batch = batch
            self._create_vertex_list()

    @property
    def group(self):
        """Parent graphics group.

        The sprite can change its rendering group, however this can be an
        expensive operation.

        :type: `Group`
        """
        return self._group.parent

    @group.setter
    def group(self, group):
        if self._group.parent == group:
            return
        self._group = SpriteGroup(self._texture,
                                  self._group.blend_src,
                                  self._group.blend_dest,
                                  group)
        if self._batch is not None:
            self._batch.migrate(self._vertex_list, GL_QUADS, self._group,
                                self._batch)

    @property
    def image(self):
        """Image or animation to display.

        :type: `AbstractImage` or `Animation`
        """
        if self._animation:
            return self._animation
        return self._texture

    @image.setter
    def image(self, img):
        if self._animation is not None:
            clock.unschedule(self._animate)
            self._animation = None

        if isinstance(img, image.Animation):
            self._animation = img
            self._frame_index = 0
            self._set_texture(img.frames[0].image.get_texture())
            self._next_dt = img.frames[0].duration
            if self._next_dt:
                clock.schedule_once(self._animate, self._next_dt)
        else:
            self._set_texture(img.get_texture())
        self._update_position()

    def _set_texture(self, texture):
        if texture.id is not self._texture.id:
            self._group = SpriteGroup(texture,
                                      self._group.blend_src,
                                      self._group.blend_dest,
                                      self._group.parent)
            if self._batch is None:
                self._vertex_list.tex_coords[:] = texture.tex_coords
            else:
                self._vertex_list.delete()
                self._texture = texture
                self._create_vertex_list()
        else:
            self._vertex_list.tex_coords[:] = texture.tex_coords
        self._texture = texture

    def _create_vertex_list(self):
        if self._subpixel:
            vertex_format = 'v3f/%s' % self._usage
        else:
            vertex_format = 'v3i/%s' % self._usage
        if self._batch is None:
            self._vertex_list = graphics.vertex_list(4, vertex_format,
                                                     'c4B', ('t3f', self._texture.tex_coords))
        else:
            self._vertex_list = self._batch.add(4, GL_QUADS, self._group,
                                                vertex_format, 'c4B', ('t3f', self._texture.tex_coords))
        self._update_position()
        self._update_color()

    def _update_position(self):
        img = self._texture
        scale = self._scale
        scale_x = self._scale_x
        scale_y = self._scale_y
        top_z = self._tilt
        if not self._visible:
            vertices = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif self._rotation:
            x1 = -img.anchor_x * scale
            y1 = -img.anchor_y * scale
            x2 = x1 + img.width * scale
            y2 = y1 + img.height * scale
            x = self._x
            y = self._y
            r = -math.radians(self._rotation)
            cr = math.cos(r)
            sr = math.sin(r)
            ax = x1 * cr - y1 * sr + x
            ay = x1 * sr + y1 * cr + y
            bx = x2 * cr - y1 * sr + x
            by = x2 * sr + y1 * cr + y
            cx = x2 * cr - y2 * sr + x
            cy = x2 * sr + y2 * cr + y
            dx = x1 * cr - y2 * sr + x
            dy = x1 * sr + y2 * cr + y
            vertices = [ax, ay, 0, bx, by, 0, cx, cy, top_z, dx, dy, top_z]
        elif scale != 1.0 or scale_x != 1.0 or scale_y != 1.0:
            x1 = self._x - img.anchor_x * scale * scale_x
            y1 = self._y - img.anchor_y * scale * scale_y
            x2 = x1 + img.width * scale * scale_x
            y2 = y1 + img.height * scale * scale_y
            vertices = [x1, y1, 0, x2, y1, 0, x2, y2, top_z, x1, y2, top_z]
        else:
            x1 = self._x - img.anchor_x
            y1 = self._y - img.anchor_y
            x2 = x1 + img.width
            y2 = y1 + img.height
            vertices = [x1, y1, 0, x2, y1, 0, x2, y2, top_z, x1, y2, top_z]
        if not self._subpixel:
            vertices = list(map(int, vertices))
        self._vertex_list.vertices[:] = vertices

    def _update_color(self):
        r, g, b = self._rgb
        self._vertex_list.colors[:] = [r, g, b, int(self._opacity)] * 4

    @property
    def image_aabb(self):
        img = self._texture
        l = self._x - img.anchor_x
        b = self._y - img.anchor_y
        r = l + img.width
        t = b + img.height
        return l, b, r, t

    @property
    def polygon(self):
        v = self._vertex_list.vertices
        # vertices = [ax, ay, z, bx, by, z, cx, cy, z, dx, dy, z]
        return v[0], v[1], v[3], v[4], v[6], v[7], v[9], v[10]

    @property
    def corners(self):
        v = self._vertex_list.vertices
        return (v[0], v[1]), (v[3], v[4]), (v[6], v[7]), (v[9], v[10])

    @property
    def position(self):
        """The (x, y) coordinates of the sprite, as a tuple.

        :Parameters:
            `x` : int
                X coordinate of the sprite.
            `y` : int
                Y coordinate of the sprite.
        """
        return self._x, self._y

    @position.setter
    def position(self, pos):
        self._x, self._y = pos
        self._update_position()

    @property
    def x(self):
        """X coordinate of the sprite.

        :type: int
        """
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self._update_position()

    @property
    def y(self):
        """Y coordinate of the sprite.

        :type: int
        """
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self._update_position()

    @property
    def rotation(self):
        """Clockwise rotation of the sprite, in degrees.

        The sprite image will be rotated about its image's (anchor_x, anchor_y)
        position.

        :type: float
        """
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation
        self._update_position()

    @property
    def scale(self):
        """Scaling factor.

        A scaling factor of 1 (the default) has no effect.  A scale of 2 will
        draw the sprite at twice the native size of its image.

        :type: float
        """
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
        self._update_position()

    @property
    def scale_x(self):
        return self._scale_x

    @scale_x.setter
    def scale_x(self, scale_x):
        self._scale_x = scale_x
        self._update_position()

    @property
    def scale_y(self):
        return self._scale_y

    @scale_y.setter
    def scale_y(self, scale_y):
        self._scale_y = scale_y
        self._update_position()

    def update(self, x=None, y=None, rotation=None, scale=None):
        """Change simultaneously the position, rotation and scale.

        The reason for this extra method is performance only. If
        the sprite changes two or the three components position,
        rotation and scale at the same time, there will be a benefit
        from calling this method, rather than using its position 
        setter followed by its rotation setter for instance.

        :Parameters:
            `x` : int
                X coordinate of the sprite.
            `y` : int
                Y coordinate of the sprite.
            `rotation` : float
                Clockwise rotation of the sprite, in degrees.
            `scale` : float
                Scaling factor.
        """
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        if rotation is not None:
            self._rotation = rotation
        if scale is not None:
            self._scale = scale
        self._update_position()

    @property
    def width(self):
        """Scaled width of the sprite.

        Read-only.  Invariant under rotation.

        :type: int
        """
        if self._subpixel:
            return self._texture.width * self._scale
        else:
            return int(self._texture.width * self._scale)

    @property
    def height(self):
        """Scaled height of the sprite.

        Read-only.  Invariant under rotation.

        :type: int
        """
        if self._subpixel:
            return self._texture.height * self._scale
        else:
            return int(self._texture.height * self._scale)

    @property
    def opacity(self):
        """Blend opacity.

        This property sets the alpha component of the colour of the sprite's
        vertices.  With the default blend mode (see the constructor), this
        allows the sprite to be drawn with fractional opacity, blending with the
        background.

        An opacity of 255 (the default) has no effect.  An opacity of 128 will
        make the sprite appear translucent.

        :type: int
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        self._opacity = opacity
        self._update_color()

    @property
    def color(self):
        """Blend color.

        This property sets the color of the sprite's vertices. This allows the
        sprite to be drawn with a color tint.

        The color is specified as an RGB tuple of integers '(red, green, blue)'.
        Each color component must be in the range 0 (dark) to 255 (saturated).

        :type: (int, int, int)
        """
        return self._rgb

    @color.setter
    def color(self, rgb):
        self._rgb = list(map(int, rgb))
        self._update_color()

    @property
    def visible(self):
        """True if the sprite will be drawn.

        :type: bool
        """
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible = visible
        self._update_position()

    def draw(self):
        """Draw the sprite at its current position.

        See the module documentation for hints on drawing multiple sprites
        efficiently.
        """
        self._group.set_state_recursive()
        self._vertex_list.draw(GL_QUADS)
        self._group.unset_state_recursive()


CardSprite.register_event_type('on_animation_end')
