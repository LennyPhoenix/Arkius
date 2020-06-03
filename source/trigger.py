import pymunk
import random


class Trigger:
    def __init__(
        self, application,
        func, collider,
        space, solid=False,
        filter=None,
        args=()
    ):
        self.application = application
        while True:
            id = random.randint(1000, 100000)
            if id not in self.application.trigger_ids:
                self.application.trigger_ids.append(id)
                self.id = id
                break

        self.space = space
        self.solid = solid
        self.filter = filter

        self.func = func
        self.args = args

        if collider["type"] == "rect":
            self.collider = pymunk.Poly(
                body=self.space.static_body,
                vertices=[
                    (
                        collider["x"],
                        collider["y"]
                    ),
                    (
                        collider["x"]+collider["width"],
                        collider["y"]
                    ),
                    (
                        collider["x"]+collider["width"],
                        collider["y"]+collider["height"]
                    ),
                    (
                        collider["x"],
                        collider["y"]+collider["height"]
                    )
                ],
                radius=collider["radius"]
            )
        elif collider["type"] == "circle":
            self.collider = pymunk.Circle(
                body=self.space.static_body,
                radius=collider["radius"],
                offset=collider["offset"]
            )
        elif collider["type"] == "poly":
            self.collider = pymunk.Poly(
                body=self.space.static_body,
                vertices=collider["vertices"],
                radius=collider["radius"]
            )
        self.space.add(self.collider)

        if self.filter is None:
            self.handler = self.space.add_wildcard_collision_handler(self.id)
        else:
            self.handler = self.space.add_collision_handler(
                self.id,
                self.filter
            )
        self.handler.begin = self.begin

    def begin(self, arbiter, space, data):
        self.func(*self.args)
        return self.solid

    def delete(self):
        self.space.remove(self.collider)
        self.application.trigger_ids.remove(self.id)
