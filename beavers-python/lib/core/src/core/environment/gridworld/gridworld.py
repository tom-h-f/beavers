import numpy as np
import torch
from core.agent import Action
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
        terrain = o.get_terrain_layer()
        agents = o.get_agent_layer()
        resources = o.get_resource_layer()

        # Stacks the arrays into our 3D observation -> [channels, size, size]
        # Resulting shape will be (3, self.size, self.size)
        stacked = np.stack([terrain, agents, resources])

        return torch.from_numpy(stacked).float().unsqueeze(0)
