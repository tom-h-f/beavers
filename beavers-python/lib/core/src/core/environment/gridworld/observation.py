import numpy as np

N_OBSERVATION_DIMENSIONS = 3


class Observer:
    def __init__(self, grid: np.ndarray, all_agents):
        self.grid = grid
        self.all_agents = all_agents

    def get_terrain_layer(self) -> np.ndarray:
        return self.grid

    def get_agent_layer(self) -> np.ndarray:
        a = np.zeros_like(self.grid)
        for agent in self.all_agents:
            a[agent.beaver.x][agent.beaver.y] = 1.0
        return a

    # TODO: implement resources
    def get_resource_layer(self) -> np.ndarray:
        return np.zeros_like(self.grid)
