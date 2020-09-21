import typing as t

import jank


class Config(jank.Config):
    def __init__(self):
        super().__init__()
        self.antialiasing: int = 16
        self.bilinear_filtering: bool = False
        self.vsync: bool = False
        self.default_size: t.Tuple[int, int] = (1400, 800)
        self.minimum_size: t.Tuple[int, int] = (568, 320)
        self.world_layers: t.List[str] = [
            # "ground",
            # "g_deco",
            "g_particles",
            "y_ordered",
            # "a_particles",
        ]
        # self.ui_layers: t.List[str] = [
        #     "transition",
        #     "map_window",
        #     "map_rooms",
        #     "map_icons",
        # ]
