import numpy as np
import math
import random
from core.agent import Action
from core.agent import Beaver
from core.terrain.tile import Tile


def agent_move_is_valid(env, b: Beaver, action: Action):
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
    if proposed_x >= env.width or proposed_y >= env.height:
        return False

    tile_is_ground = env.world_grid[proposed_x][proposed_y] == Tile.GROUND
    return tile_is_ground


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


def _generate_river(env_width, env_height, world_grid):
    # Start from left edge
    start_y = random.randint(0, env_height - 1)
    x, y = 0, start_y
    target_y = start_y
    river_length = 0

    while x < env_width - 1:
        base_width = math.floor(env_height / 8)
        # Vary width with sine wave
        variation = int(2 * np.sin(river_length * 0.1))
        width = max(base_width, base_width + variation)

        # Fill the river width around the current y
        half_width = width // 2
        for dy in range(-half_width, half_width + 1):
            ny = y + dy
            if 0 <= ny < env_height:
                world_grid[ny, x] = Tile.WATER

        # Smoothly adjust target_y for better flow
        if random.random() < 0.3:  # 30% chance to adjust target
            target_y += random.choice([-1, 0, 1])  # Small changes
            target_y = max(0, min(env_height - 1, target_y))

        # Move towards target_y gradually
        if y < target_y and y < env_height - 1:
            y += 1
        elif y > target_y and y > 0:
            y -= 1
        else:
            x += 1  # Continue right if at target

        river_length += 1

        # Prevent infinite loops
        if x >= env_width - 1:
            break
