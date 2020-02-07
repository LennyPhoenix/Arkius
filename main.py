"""Very basic room renderer."""
import Lib
from Lib import tilesets
from Lib import dungeon

tileset = tilesets.cornerPits()

print()

string = ""
for y in range(7):
    for x in range(7):
        string += f'{tileset[(x, y)]} '
    string += "\n"

print(string)
