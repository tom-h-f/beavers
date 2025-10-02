import numpy as np
import random


class Environment:
    def __init__(self, width: int = 128, height: int = 128):
        self.width = width
        self.height = width

    def generate_world(self):
        # TODO: This needs to become a actual, complicated world generation built for generating rivers.
        # Also, we will need to randomly add trees, maybe in another array (this probs just has to be a seperate `terrain` class tbh)
        random.seed()
        ground_chance = 0.3
        water_chance = 0.7
        self.world_grid = np.random.choice(
            [0, 1], size=(self.height, self.width), p=[ground_chance, water_chance]
        )
        print(f"Water Tile Count: {(self.world_grid == 1).sum()}")
        print(f"Ground Tile Count: {(self.world_grid == 0).sum()}")
