"""Transition UI element."""

import pyglet


class Transition:
    """Moves between the different transition animations."""

    def __init__(self, window):
        self.window = window
        self._visible = False
        self._state = "fade_in"

        self.player = None
        self.door = None

        self.states = self.window.resources["ui"]["transition"]
        self.sprite = pyglet.sprite.Sprite(
            self.states[self.state],
            0, 0,
            batch=self.window.ui_batch,
            group=self.window.layers["ui"]["transition"]
        )
        self.update_position()

        self.window.push_handlers(self)
        self.sprite.push_handlers(self)

    def begin(self, player, door):
        if self.state == "empty":
            self.state = "fade_out"
            self.player = player
            self.player.state = "locked"
            self.door = door

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
            self.window.width/(self.sprite.width/self.sprite.scale),
            self.window.height/(self.sprite.height/self.sprite.scale)
        )

    def on_animation_end(self):
        if self.state == "fade_out":
            self.state = "black"
        elif self.state == "black":
            while len(self.window.particles) > 0:
                self.window.particles[0].destroy()
            self.window.room.visibility = False
            if self.player is not None:
                if self.door == 0:
                    self.window.room.visibility = False
                    if self.window.room.map_data is not None:
                        offset = (
                            self.player.x -
                            self.window.room.map_data["door_info"][0]["pos"]
                        )
                    else:
                        offset = self.player.x
                    self.player.room = (
                        self.player.room[0], self.player.room[1]+1)
                    self.window.room.visibility = True
                    self.player.y = -(self.window.room.height+3)
                    if self.window.room.map_data is not None:
                        self.player.x = (
                            offset +
                            self.window.room.map_data["door_info"][2]["pos"]
                        )
                    else:
                        self.player.x = 0 + offset
                elif self.door == 1:
                    if self.window.room.map_data is not None:
                        offset = (
                            self.player.y -
                            self.window.room.map_data["door_info"][1]["pos"]
                        )
                    else:
                        offset = self.player.y
                    self.player.room = (
                        self.player.room[0]+1, self.player.room[1])
                    self.window.room.visibility = True
                    self.player.x = -(self.window.room.width+3)
                    if self.window.room.map_data is not None:
                        self.player.y = (
                            offset +
                            self.window.room.map_data["door_info"][3]["pos"]
                        )
                    else:
                        self.player.y = 0 + offset
                elif self.door == 3:
                    self.window.room.visibility = False
                    if self.window.room.map_data is not None:
                        offset = (
                            self.player.y -
                            self.window.room.map_data["door_info"][3]["pos"]
                        )
                    else:
                        offset = self.player.y
                    self.player.room = (
                        self.player.room[0]-1, self.player.room[1])
                    self.window.room.visibility = True
                    self.player.x = self.window.room.width+3
                    if self.window.room.map_data is not None:
                        self.player.y = (
                            offset +
                            self.window.room.map_data["door_info"][1]["pos"]
                        )
                    else:
                        self.player.y = 0 + offset
                elif self.door == 2:
                    self.window.room.visibility = False
                    if self.window.room.map_data is not None:
                        offset = (
                            self.player.x -
                            self.window.room.map_data["door_info"][2]["pos"]
                        )
                    else:
                        offset = self.player.x
                    self.player.room = (
                        self.player.room[0], self.player.room[1]-1)
                    self.window.room.visibility = True
                    self.player.y = self.window.room.height+3
                    if self.window.room.map_data is not None:
                        self.player.x = (
                            offset +
                            self.window.room.map_data["door_info"][0]["pos"]
                        )
                    else:
                        self.player.x = 0 + offset
                self.window.dungeon.ui_map.discover(self.player.room)
                self.door = None
            self.state = "fade_in"
        elif self.state == "fade_in":
            if self.player is not None:
                self.player.state = "idle"
                self.player = None
            self.state = "empty"

    def on_resize(self, width, height):
        """Update the position and scale of everything."""
        self.update_position()
