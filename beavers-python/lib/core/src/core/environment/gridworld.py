import numpy as np
import torch
from .gridworld_helpers import generate_world, agent_move_is_valid
from core.agent import Action
from core.agent.exceptions import AgentMoveNotValid
from core.agent.reward import calculate_reward
from core.agent.dqn import DQNBeaver
from .observation import Observer
from core.agent.experience import Experience, BeaverStepInfo


class Environment:
    def __init__(self, width: int = 128, height: int = 128, agent_cnt=1):
        self.width = width
        self.height = height
        self.world_grid = generate_world(width, height)

    def reset(self):
        self.world_grid = generate_world(self.width, self.height)

    def step(
        self, all_agents, agent: DQNBeaver, action: Action, device="mps"
    ) -> Experience:
        if action.is_move():
            if not agent_move_is_valid(self, agent.beaver, action):
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
        o = Observer(self.world_grid, all_agents)
        terrain = o.get_terrain_layer()
        agents = o.get_agent_layer()
        resources = o.get_resource_layer()
        # Stacks the arrays into our 3D observation -> [channels, height, width]
        # Resulting shape will be (3, self.height, self.width)
        stacked = np.stack([terrain, agents, resources])
        # TODO: use `.to` at the end here using `device` param
        # currently we get a MPSFLoat Error, requires investigation
        return torch.from_numpy(stacked).float().unsqueeze(0)
