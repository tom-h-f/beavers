import numpy as np
import torch
from core.agent.action import Action
from .observation import Observer
from core.agent.experience import BeaverStepInfo
from .grid import Grid


class Environment:
    def __init__(self, size):
        self.size = size
        self.grid = Grid(size, size)

    def reset(self):
        self.grid.reset()

    def get_info(self, action: Action) -> BeaverStepInfo:
        b = BeaverStepInfo(True, action.to_type_str())
        return b

    def get_observation(self, all_agents, agent):
        o = Observer(self.grid.raw(), all_agents)
        terrain = o.get_terrain_layer(agent)
        agents = o.get_agent_layer(agent)
        resources = o.get_resource_layer(agent)

        # State layers (also 3x3, but uniform values)
        energy_layer = np.full((3, 3), agent.beaver.energy / 100.0)
        logs_layer = np.full((3, 3), agent.beaver.logs / 50.0)
        food_layer = np.full((3, 3), agent.beaver.food / 20.0)

        # Stacks the arrays into our 3D observation -> [channels, size, size]
        # Resulting shape will be (3, self.size, self.size)
        stacked = np.stack([terrain, agents, resources,
                           energy_layer, logs_layer, food_layer])

        return torch.from_numpy(stacked).float().unsqueeze(0)
