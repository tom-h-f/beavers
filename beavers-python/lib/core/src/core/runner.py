from typing import List
import matplotlib.pyplot as plt
import math
import time

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
    epsilon = 1.0
    epsilon_min = 0.01
    epsilon_decay = 0.990

    def __init__(self, config: OrchestratorConfig, agents, network, target_network, graphics=None):
        self.max_steps = config.max_steps
        print("Max Steps: ", self.max_steps)

        self.init_environment(config)
        self.replay_buffer = ReplayBuffer(config.batch_size)

        self.trainer = Trainer(network, target_network, self.replay_buffer)
        self.number_of_episodes = config.number_of_episodes
        self.agents = agents
        self.graphics = graphics
        self.reset_agents()

        self.total_actions = 0
        self.invalid_actions = 0

    def init_environment(self, config: OrchestratorConfig):
        match config.env_type:
            case EnvironmentType.GridWorld:
                self.env = gridworld.Environment(config.size)
            case _:
                raise ValueError("Invalid Environment")

    def reset_agents(self):
        # TODO: also reset their state like energy+inventory etc?
        for a in self.agents:
            a.beaver.x, a.beaver.y = self.env.grid.get_random_spawn_pos()
            a.beaver.energy = 100

        # Reset action counters for new episode
        self.total_actions = 0
        self.invalid_actions = 0

    def run(self, agents: List[DQNBeaver]):
        episode_losses = []
        for i in range(self.number_of_episodes):
            start = time.perf_counter()
            print(f"\nRunning episode {i} - e={self.epsilon}")
            self.env.reset()
            self.reset_agents()
            step_count = 0
            episode_loss = []
            while not self.is_episode_done(step_count):
                for a in [x for x in agents if not x.done]:
                    exp = self.agent_step(a)
                    if self.graphics is not None:
                        self.graphics.render(self, exp.action, a)
                    self.replay_buffer.add(exp)
                    if step_count % 16 == 0:
                        self.trainer.train_step(a)
                        if self.trainer.losses:
                            episode_loss.append(self.trainer.losses[-1])

                step_count += 1
                if step_count % 32 == 0:
                    self.trainer.update_target_network()

            episode_losses.append(sum(episode_loss) /
                                  len(episode_loss) if episode_loss else 0)
            print("Final Loss:   ", sum(episode_loss) / len(episode_loss))
            print(f"Episode took: {time.perf_counter() - start:.6f}s")

            if self.total_actions > 0:
                invalid_percentage = (
                    self.invalid_actions / self.total_actions) * 100
                print(f"Invalid Actions: {
                      self.invalid_actions}/{self.total_actions} ({invalid_percentage:.2f}%)")
            else:
                print("No actions attempted in this episode.")

            self.decay_epsilon()
        self.plot_losses(episode_losses)

    def agent_step(self, a: DQNBeaver) -> Experience:
        observation = self.observe(a)

        action, q = a.select_action(observation, self.epsilon)

        reward, valid = calculate_reward(
            a.beaver, self.agents, action, self.env)

        # ANSI codes
        RED = "\033[31m"
        RESET = "\033[0m"

        prefix = "" if valid else RED
        suffix = "" if valid else RESET

        # print(f"{prefix}action={action.str():10}\treward={
        #      reward}\tepsilon={self.epsilon}{suffix}")
        self.total_actions += 1

        if valid:
            a.beaver.do(action, self.env)
            next_state = self.observe(a)
        else:
            self.invalid_actions += 1
            # print(f"[{str(a.id)[:2]}] INVALID ACTION [{a.beaver.x}, { a.beaver.y}]: {action.name} ")
            next_state = observation
            return Experience(observation, action, next_state, reward,
                              True, BeaverStepInfo(True, action.str()))

        return Experience(observation, action, next_state, reward,
                          a.is_done(), BeaverStepInfo(True, action.str()))

    def observe(self, a: DQNBeaver):
        return self.env.get_observation(self.alive_agents(), a)

    def decay_epsilon(self) -> None:
        self.epsilon = max(self.epsilon * self.epsilon_decay,
                           self.epsilon_min)

    def is_episode_done(self, step_count: int) -> bool:
        return step_count >= self.max_steps

    def alive_agents(self) -> List[DQNBeaver]:
        return [x for x in self.agents if not x.done]

    def plot_losses(self, episode_losses):
        plt.figure(figsize=(10, 5))
        plt.plot(range(len(episode_losses)), episode_losses)
        plt.xlabel('Episode')
        plt.ylabel('Average Loss')
        plt.title('Loss over Episodes')
        plt.savefig("loss.png")
