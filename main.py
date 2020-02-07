"""
Copyright (C) 2020    Contributers of Arkius.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

from Lib.dungeon import Room

room = Room(roomType=3)
tileset = room.groundTiles


string = ""
for y in range(7):
    for x in range(7):
        string += f"{tileset[(x, y)]} "
    string += "\n"

print(string)
