from typing import List
import matplotlib.pyplot as plt

import core.environment.gridworld as gridworld

from core.dqn import DQNBeaver
from core.train import Trainer
from .environment.env_types import EnvironmentType
from core.terrain.tile import Tile
from core.orchestrator.config import OrchestratorConfig
from core.agent.reward import calculate_reward
from core.agent.experience import Experience, ReplayBuffer
from core.agent.action import BeaverStepInfo


class Runner:
    epsilon = 0.6
    epsilon_min = 0.001
    epsilon_decay = 0.990

    def __init__(self, config: OrchestratorConfig, agents, network, target_network):
        self.torch_device = config.torch_device
        self.max_steps = config.batch_size * config.batch_size
        print("Max Steps: ", self.max_steps)

        self.init_environment(config)
        self.replay_buffer = ReplayBuffer(config.batch_size)

        self.trainer = Trainer(network, target_network, self.replay_buffer)
        self.number_of_episodes = config.number_of_episodes
        self.agents = agents
        self.reset_agents()

    def init_environment(self, config: OrchestratorConfig):
        match config.env_type:
            case EnvironmentType.GridWorld:
                self.env = gridworld.Environment(config.size)
            case _:
                raise ValueError("Invalid Environment")

    def reset_agents(self):
        # TODO: also reset their state like energy+inventory etc?
        for a in self.agents:
            a.beaver.x, a.beaver.y = self.env.grid.get_random_tile_of_type(
                Tile.GROUND)
            a.beaver.energy = 100

    def run(self, agents: List[DQNBeaver]):
        episode_losses = []
        for i in range(self.number_of_episodes):
            print(f"\nRunning episode {i} - e={self.epsilon}")
            self.reset_agents()
            step_count = 0
            episode_loss = []
            while not self.is_episode_done(step_count):
                for a in [x for x in agents if not x.done]:
                    exp = self.agent_step(a)
                    self.replay_buffer.add(exp)
                    self.trainer.train_step(a)
                    if self.trainer.losses:
                        episode_loss.append(self.trainer.losses[-1])

                step_count += 1
            episode_losses.append(sum(episode_loss) /
                                  len(episode_loss) if episode_loss else 0)
            print(episode_losses)
            self.decay_epsilon()
        self.plot_losses(episode_losses)

    def agent_step(self, a: DQNBeaver) -> Experience:
        observation = self.observe(a)

        action, q = a.select_action(observation, self.epsilon)

        reward, valid = calculate_reward(a.beaver, action, self.env)
        # print(f"action{action.name:10}\treward={reward}\tepsilon={self.epsilon}")
        if valid:
            a.beaver.do(action)
            next_state = self.observe(a)
        else:
            next_state = observation
        return Experience(observation, action, next_state, reward,
                          a.is_done(), BeaverStepInfo(True, action.to_type_str()))

    def observe(self, a: DQNBeaver):
        return self.env.get_observation(self.alive_agents(), a,
                                        self.torch_device)

    def decay_epsilon(self) -> None:
        self.epsilon = max(self.epsilon * self.epsilon_decay,
                           self.epsilon_min)

    def is_episode_done(self, step_count: int) -> bool:
        return any(agent.is_done() for agent in self.agents) or step_count >= self.max_steps

    def alive_agents(self) -> List[DQNBeaver]:
        return [x for x in self.agents if not x.done]

    def plot_losses(self, episode_losses):
        plt.figure(figsize=(10, 5))
        plt.plot(range(len(episode_losses)), episode_losses)
        plt.xlabel('Episode')
        plt.ylabel('Average Loss')
        plt.title('Loss over Episodes')
        plt.savefig("loss.png")
