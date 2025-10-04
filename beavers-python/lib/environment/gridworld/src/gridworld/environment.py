import numpy as np
import random
from core.agent import Beaver


class Environment:
    def __init__(self, width: int = 128, height: int = 128):
        self.width = width
        self.height = height
        self.agents = []

    def add_agent(self, b: Beaver):
        self.agents.append(b)
        print(f"New agent spawned at [{b.x},{b.y}]")

    def generate_world(self):
        # TODO: This needs to become a actual, complicated world generation built for generating rivers.
        random.seed()
        ground_chance = 0.3
        tree_chance = 0.1
        water_chance = 0.6
        self.world_grid = np.random.choice(
            [0, 1, 1.5],
            size=(self.height, self.width),
            p=[water_chance, ground_chance, tree_chance],
        )
