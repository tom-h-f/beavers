import numpy as np
import torch
from core.agent import Action
from core.agent.exceptions import AgentMoveNotValid
from core.agent.reward import calculate_reward
from core.dqn import DQNBeaver
from .observation import Observer
from core.agent.experience import Experience, BeaverStepInfo
from .grid import Grid


class Environment:
    def __init__(self, size):
        self.size = size
        self.grid = Grid(size, size)

    def reset(self):
        self.grid.reset()

    def step(
        self, all_agents, agent: DQNBeaver, action: Action, device="mps"
    ) -> Experience:
        if action.is_move():
            if not self.grid.agent_move_is_valid(agent.beaver, action):
                raise AgentMoveNotValid

        agent.beaver.do(action)
        next_state = self.get_observation(all_agents, agent, device)
        reward = calculate_reward(agent.beaver, action)
        # print(f"\raction={action.name} reward={reward}")
        done = agent.is_done()

        info = self.get_info(action)
        return Experience(next_state, reward, done, info)

    def get_info(self, action: Action) -> BeaverStepInfo:
        b = BeaverStepInfo(True, action.to_type_str())
        return b

    def get_observation(self, all_agents, agent, device):
        o = Observer(self.grid.raw(), all_agents)
        terrain = o.get_terrain_layer()
        agents = o.get_agent_layer()
        resources = o.get_resource_layer()

        # Stacks the arrays into our 3D observation -> [channels, size, size]
        # Resulting shape will be (3, self.size, self.size)
        stacked = np.stack([terrain, agents, resources])

        # TODO: use `.to` at the end here using `device` param
        # currently we get a MPSFLoat Error, requires investigation
        return torch.from_numpy(stacked).float().unsqueeze(0)
