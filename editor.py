import json

from src import constants as c

import pyglet


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.world_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()

    def loadResources(self):
        """Preload all resources."""
        self.resources = {}

        tiles = {}
        for style in c.STYLES:
            tiles[style] = {}
            for tile in c.TILES.keys():
                tile_width = c.TILES[tile]["sprite"]["width"]
                tile_height = c.TILES[tile]["sprite"]["height"]
                image = pyglet.resource.image(
                    f"resources/tilesets/{style}/{tile}.png"
                )
                try:
                    data_path = f"resources/tilesets/{style}/{tile}.json"
                    with open(data_path, "r") as f:
                        data = json.load(f)

                    sprite_sheet = pyglet.image.ImageGrid(
                        image,
                        len(data["animations"]),
                        data["max_length"],
                        item_width=data["frame"][0],
                        item_height=data["frame"][1]
                    )

                    if c.TILES[tile]["sprite"]["connective"]:
                        frame_grids = []
                        for frame in range(sprite_sheet.__len__()):
                            frame_grids.append(
                                pyglet.image.ImageGrid(
                                    sprite_sheet[frame],
                                    c.TILESET_DIMENSIONS[1],
                                    c.TILESET_DIMENSIONS[0],
                                    item_width=tile_width,
                                    item_height=tile_height
                                )
                            )

                        image_grid = {}
                        for index in range(frame_grids[0].__len__()):
                            tile_frames = []
                            for i in range(data["animations"][0]["length"]):
                                tile_frames.append(
                                    frame_grids[i][index]
                                )
                            frame_length = data["animations"][0]["frame_length"]  # noqa: E501
                            image_grid[index] = pyglet.image.Animation.from_image_sequence(  # noqa: E501
                                tile_frames,
                                frame_length,
                                loop=data["animations"][0]["loop"]
                            )
                    else:
                        frame_grids = []
                        for frame in range(sprite_sheet.__len__()):
                            frame_grids.append(
                                pyglet.image.ImageGrid(
                                    sprite_sheet[frame],
                                    image.height // tile_height,
                                    image.width // tile_width,
                                    item_width=tile_width,
                                    item_height=tile_height
                                )
                            )

                        image_grid = []
                        for index in range(frame_grids[0].__len__()):
                            tile_frames = []
                            for i in range(data["animations"][0]["length"]):
                                tile_frames.append(
                                    frame_grids[i][index]
                                )
                            frame_length = data["animations"][0]["frame_length"]  # noqa: E501
                            image_grid.append(
                                pyglet.image.Animation.from_image_sequence(
                                    tile_frames,
                                    frame_length,
                                    loop=data["animations"][0]["loop"]
                                )
                            )

                except FileNotFoundError:
                    if c.TILES[tile]["sprite"]["connective"]:
                        image_grid = pyglet.image.ImageGrid(
                            image,
                            c.TILESET_DIMENSIONS[1],
                            c.TILESET_DIMENSIONS[0],
                            item_width=c.TILES[tile]["sprite"]["width"],
                            item_height=c.TILES[tile]["sprite"]["height"]
                        )
                    else:
                        image_grid = pyglet.image.ImageGrid(
                            image,
                            image.height // c.TILES[tile]["sprite"]["height"],
                            image.width // c.TILES[tile]["sprite"]["width"],
                            item_width=c.TILES[tile]["sprite"]["width"],
                            item_height=c.TILES[tile]["sprite"]["height"]
                        )

                tiles[style][tile] = image_grid
        self.resources["tiles"] = tiles


if __name__ == "__main__":
    window = Window(
        caption="Arkius Tilemap Editor",
        resizable=True,
        fullscreen=True,
        vsync=True
    )
    pyglet.app.run()
