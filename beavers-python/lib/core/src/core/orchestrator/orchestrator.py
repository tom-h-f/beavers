import torch

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

        torch.set_default_device(config.torch_device)
        if config.render_enabled:
            if config.renderer_type == "pygame":
                import render
                self.graphics = render.PygameRenderer(
                    config.size, config.size)
            elif config.renderer_type == "tui":
                from render.tui import TerminalRenderer
                self.graphics = TerminalRenderer(
                    config.size, config.size)
            else:
                raise ValueError(f"Unknown renderer type: {
                                 config.renderer_type}")
        else:
            self.graphics = None

        self.network = DQNNetwork(
            self.observation_shape(), Action.how_many())
        self.target_network = DQNNetwork(
            self.observation_shape(), Action.how_many())

        if self.config.model_path is not None:
            state_dict = torch.load(self.config.model_path)
            self.network.load_state_dict(state_dict)
            self.target_network.load_state_dict(state_dict)

        for _ in range(self.config.number_of_agents):
            self.agents.append(DQNBeaver(self.network))
        assert (len(self.agents) == self.config.number_of_agents)

        self.runner = Runner(
            config, self.agents, self.network, self.target_network)

    def train(self):
        self.runner.run(self.agents)
        torch.save(self.network.state_dict(), "./model.torch")

    def observation_shape(self):
        match self.config.env_type:
            case EnvironmentType.GridWorld:
                return (gw_obs.N_OBSERVATION_DIMENSIONS,
                        3, 3)
