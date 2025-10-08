import numpy as np


class Observer:
    def __init__(self, world_grid: np.ndarray, all_agents):
        self.world_grid = world_grid
        self.all_agents = all_agents

    def get_terrain_layer(self) -> np.ndarray:
        return self.world_grid

    def get_agent_layer(self) -> np.ndarray:
        a = np.zeros_like(self.world_grid)
        for agent in self.all_agents:
            a[agent.beaver.x][agent.beaver.y] = 1.0
        return a

    # TODO: implement resources
    def get_resource_layer(self) -> np.ndarray:
        return np.zeros_like(self.world_grid)
