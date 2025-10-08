from enum import IntEnum

# No. of pixels per tile
TILE_SIZE_PX = 8


class Tile(IntEnum):
    WATER = 0
    GROUND = 1
    TREE = 2
