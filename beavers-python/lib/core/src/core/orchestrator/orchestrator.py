import render

import core.environment.gridworld.observation as gw_obs

from core.dqn import DQNBeaver, DQNNetwork
from core.agent import Action
from core.environment import EnvironmentType
from core.runner import Runner

from .config import OrchestratorConfig


class Orchestrator:
    agents = []

    def __init__(self, config: OrchestratorConfig):
        self.config = config
        self.graphics = render.PygameRenderer(config.size, config.size)

        self.network = DQNNetwork(
            self.observation_shape(), Action.how_many())
        self.target_network = DQNNetwork(
            self.observation_shape(), Action.how_many())

        for _ in range(self.config.number_of_agents):
            self.agents.append(DQNBeaver(self.network))

        self.runner = Runner(
            config, self.agents, self.network, self.target_network)

    def train(self):
        self.runner.run(self.agents)

    def observation_shape(self):
        match self.config.env_type:
            case EnvironmentType.GridWorld:
                return (gw_obs.N_OBSERVATION_DIMENSIONS,
                        self.config.size, self.config.size)
