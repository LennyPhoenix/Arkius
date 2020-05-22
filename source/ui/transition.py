import pyglet


class Transition:
    _visible = False
    _state = "empty"

    def __init__(self, application):
        self.application = application

        self.on_black = None
        self.on_black_args = None
        self.on_done = None
        self.on_done_args = None

        self.states = self.application.resources["ui"]["transition"]
        self.sprite = pyglet.sprite.Sprite(
            self.states[self.state],
            0, 0,
            batch=self.application.ui_batch,
            group=self.application.layers["ui"]["transition"]
        )
        self.update_position()

        self.application.pushHandler(self)
        self.sprite.push_handlers(self)

    def begin(
        self,
        on_black=None, on_black_args=[],
        on_done=None, on_done_args=[]
    ):
        self.state = "fade_out"

        self.on_black = on_black
        self.on_black_args = on_black_args

        self.on_done = on_done
        self.on_done_args = on_done_args

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        self.sprite.image = self.states[state]
        if state == "empty":
            self.sprite.visible = False
        if state == "fade_out":
            self.sprite.visible = True

    def update_position(self):
        self.sprite.scale = max(
            self.application.window.width /
            (self.sprite.width/self.sprite.scale),
            self.application.window.height /
            (self.sprite.height/self.sprite.scale)
        )

    def on_animation_end(self):
        if self.state == "fade_out":
            self.state = "black"
        elif self.state == "black":
            if self.on_black is not None:
                self.on_black(*self.on_black_args)
            del self.on_black, self.on_black_args
            self.state = "fade_in"
        elif self.state == "fade_in":
            if self.on_done is not None:
                self.on_done(*self.on_done_args)
            del self.on_done, self.on_done_args
            self.state = "empty"

    def on_resize(self, width, height):
        self.update_position()
