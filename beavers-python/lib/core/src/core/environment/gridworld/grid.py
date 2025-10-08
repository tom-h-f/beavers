import random
import math
import numpy as np

from core.agent import Beaver, Action
from core.terrain.tile import Tile


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._grid = generate_world(width, height)

    def raw(self):
        return self._grid

    def reset(self):
        # TODO: Check this does actually change it
        self._grid = generate_world(self.width, self.height)

    def agent_move_is_valid(self, b: Beaver, action: Action):
        assert action.is_move()
        proposed_x = b.x
        proposed_y = b.y
        match action:
            case Action.MoveRight:
                proposed_x += 1
            case Action.MoveUp:
                proposed_y += 1
            case Action.MoveLeft:
                proposed_x -= 1
            case Action.MoveDown:
                proposed_y -= 1

        if proposed_x < 0 or proposed_y < 0:
            return False
        if proposed_x >= self.width or proposed_y >= self.height:
            return False

        return self.tile_at(proposed_x, proposed_y) == Tile.GROUND

    def tile_at(self, x: int, y: int) -> Tile:
        return Tile(self._grid[x][y])

    def get_random_tile_of_type(self, tile_type: Tile) -> (int, int):
        """
        Gets a position of a tile in the grid matching the given `tile_type`
        """
        ground_y, ground_x = np.where(self._grid == tile_type)

        idx = np.random.choice(len(ground_x))
        return ground_x[idx], ground_y[idx]


def generate_world(width, height):
    # Generate a world with river-like structures
    random.seed()
    world_grid = np.full((height, width), Tile.GROUND, dtype=float)

    # Generate rivers
    num_rivers = random.randint(1, 3)  # 1 to 3 rivers
    for _ in range(num_rivers):
        _generate_river(width, height, world_grid)

    # Add trees randomly on ground tiles
    tree_positions = np.random.rand(height, width) < 0.05
    world_grid[tree_positions & (world_grid == Tile.GROUND)] = Tile.TREE
    return world_grid


def _generate_river(env_width, size, world_grid):
    # Start from left edge
    start_y = random.randint(0, size - 1)
    x, y = 0, start_y
    target_y = start_y
    river_length = 0

    while x < env_width - 1:
        base_width = math.floor(size / 8)
        # Vary width with sine wave
        variation = int(2 * np.sin(river_length * 0.1))
        width = max(base_width, base_width + variation)

        # Fill the river width around the current y
        half_width = width // 2
        for dy in range(-half_width, half_width + 1):
            ny = y + dy
            if 0 <= ny < size:
                world_grid[ny, x] = Tile.WATER

        # Smoothly adjust target_y for better flow
        if random.random() < 0.3:  # 30% chance to adjust target
            target_y += random.choice([-1, 0, 1])  # Small changes
            target_y = max(0, min(size - 1, target_y))

        # Move towards target_y gradually
        if y < target_y and y < size - 1:
            y += 1
        elif y > target_y and y > 0:
            y -= 1
        else:
            x += 1  # Continue right if at target

        river_length += 1

        # Prevent infinite loops
        if x >= env_width - 1:
            break
