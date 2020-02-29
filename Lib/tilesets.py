"""
Contains premade tilesets for rooms.

Tilesets should be dictionaries in the format {(X, Y): TileValue}

Tile values:
0 = Empty (Plain floor)
1 = Wall
2 = Pit
"""

import random


def toSet(tilearray):
    """Convert a tilearray to a full dictionary."""
    tileset = {}
    for y in range(15):
        for x in range(15):
            tileset[(x, y)] = tilearray[y][x]

    return tileset


def basic():
    """Full floor."""
    tilearray = {
        14: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        13: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        12: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        11: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        10: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        9:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        8:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        7:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        6:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        5:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        4:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        3:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        2:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        1:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        0:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }

    tileset = toSet(tilearray)
    return tileset


def startRoom():
    """Bevelled corners and pit ring. Bridge at North side."""
    tilearray = {
        14: [1, 1, 1, 2, 2, 2, 0, 0, 0, 2, 2, 2, 1, 1, 1],
        13: [1, 1, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 1, 1],
        12: [1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1],
        11: [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
        10: [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
        9:  [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
        8:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        7:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        6:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        5:  [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
        4:  [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
        3:  [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
        2:  [1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1],
        1:  [1, 1, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 1, 1],
        0:  [1, 1, 1, 2, 2, 2, 0, 0, 0, 2, 2, 2, 1, 1, 1],
    }

    tileset = toSet(tilearray)
    return tileset


def treasureRoom():
    """Island in centre. Bridges on either side."""
    tilearray = {
        14: [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        13: [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        12: [1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 1],
        11: [0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0],
        10: [0, 0, 0, 2, 2, 1, 0, 0, 0, 1, 2, 2, 0, 0, 0],
        9:  [0, 0, 2, 2, 1, 1, 0, 0, 0, 1, 1, 2, 2, 0, 0],
        8:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        7:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        6:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        5:  [0, 0, 2, 2, 1, 1, 0, 0, 0, 1, 1, 2, 2, 0, 0],
        4:  [0, 0, 0, 2, 2, 1, 0, 0, 0, 1, 2, 2, 0, 0, 0],
        3:  [0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0],
        2:  [1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 1],
        1:  [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        0:  [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    }

    tileset = toSet(tilearray)
    return tileset


def fightRoom():
    """Wall seeds and pits."""
    tilearray = {
        14: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        13: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        12: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        11: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        10: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        9:  [0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0],
        8:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        7:  [0, 0, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 0, 0],
        6:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        5:  [0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0],
        4:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        3:  [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        2:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        1:  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        0:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }

    tileset = toSet(tilearray)
    randomTileset = generateRandom(wallChance=0, pitChance=0, tileset=tileset)
    return randomTileset


def bossRoom():
    """8 walls. 5 pits."""
    tilearray = {
        14: [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        13: [1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
        12: [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        11: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        10: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        9:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        8:  [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        7:  [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
        6:  [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        5:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        4:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        3:  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        2:  [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
        1:  [1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
        0:  [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    }

    tileset = toSet(tilearray)
    randomTileset = generateRandom(wallChance=0, pitChance=0, tileset=tileset)
    return randomTileset


def generateRandom(tileset, wallChance=7, pitChance=5, wallSize=15, pitSize=35):  # noqa: E501
    """Generate a random tileset."""

    originalWallChance = wallChance
    originalPitChance = pitChance
    nearDoor = [
        (6, 0), (7, 0), (8, 0),
        (6, 14), (7, 14), (8, 14),
        (0, 6), (0, 7), (0, 8),
        (14, 6), (14, 7), (14, 8)
    ]

    for y in range(15):
        for x in range(15):
            if x != 0 and tileset[(x-1, y)] == 1:
                wallChance += wallSize
            if x != 14 and tileset[(x+1, y)] == 1:
                wallChance += wallSize
            if y != 0 and tileset[(x, y-1)] == 1:
                wallChance += wallSize
            if y != 14 and tileset[(x, y+1)] == 1:
                wallChance += wallSize

            if (x, y) in nearDoor:
                wallChance = wallChance / 5

            if random.random() * 100 < wallChance:
                tileset[(x, y)] = 1

            wallChance = originalWallChance

            if x != 14 and tileset[(x+1, y)] == 2:
                pitChance += pitSize
            if x != 0 and tileset[(x-1, y)] == 2:
                pitChance += pitSize
            if y != 14 and tileset[(x, y+1)] == 2:
                pitChance += pitSize
            if y != 0 and tileset[(x, y-1)] == 2:
                pitChance += pitSize

            if x == 0 or x == 14 or y == 0 or y == 14:
                pitChance = pitChance / 2

            if (x, y) in nearDoor:
                pitChance = pitChance / 4

            if random.random() * 100 < pitChance:
                tileset[(x, y)] = 2

            pitChance = originalPitChance
    return tileset
