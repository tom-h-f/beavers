import random
import numpy as np
import render
import core.environment.gridworld as enviroment
from core.agent.dqn import DQNBeaver
from core.agent.exceptions import AgentMoveNotValid
from core.terrain.tile import Tile


class Trainer:
    n_actions = 7
    decay = 0.001

    def __init__(self, count, render_enabled=False, n_episodes=100, device="mps"):
        self.width = 32
        self.device = device
        self.height = 32
        self.observation_shape = (3, self.height, self.width)
        self.render_enabled = render_enabled
        self.env = enviroment.Environment(
            self.width, self.height, agent_cnt=count)
        self.agents = []
        self.n_episodes = n_episodes
        if render_enabled:
            self.gpu = render.PygameRenderer(self.width, self.height)

        for _ in range(0, 3):
            x, y = self.env.grid.get_random_pos_of_tile_type(Tile.GROUND)
            print(f"X = {x} Y = {y}")
            self.agents.append(
                DQNBeaver(self.observation_shape, self.n_actions, x, y))

    def training_loop(self):
        epsilon = 1
        print(f"{len(self.agents)} agents present")
        print(f"Running {self.n_episodes} episodes...")
        for episode in range(self.n_episodes):
            print(f"Episode {episode}:")
            # FIXME: THIS SHOULD BE THE ENV.RESET METHOD BUT IT DOES NOT WORKYY :(
            self.env = enviroment.Environment(
                self.width, self.height, agent_cnt=len(self.agents)
            )
            # FIXME: THIS SHOULD ALSO BE IN THE RESET
            for a in self.agents:
                a.done = False
            if self.render_enabled and episode == self.n_episodes - 1:
                self.gpu.render(self)

            # TODO: move the render and the env reset, to its own shit, like ur supposed to
            episode_done = False
            while not episode_done:
                random.seed()
                # currently they all die at the same time, likely due to starting on the same spot
                # and the fact the network doesnt actually change at all.
                # TODO: We can look into 'personality'
                # via changing some of the parameters like the discount_factor etc
                alive_agent_count = len([x for x in self.agents if not x.done])
                if alive_agent_count == 0:
                    episode_done = True

                for a in [x for x in self.agents if not x.done]:
                    obs = self.env.get_observation(
                        self.agents, a, device=self.device)
                    action, q_value = a.select_action(obs, epsilon)
                    # print(f"{a.id}=>{action.name:10}")

                    try:
                        exp = self.env.step(self.agents, a, action)
                        if self.render_enabled and episode == self.n_episodes - 1:
                            self.gpu.render(self)
                    except AgentMoveNotValid:
                        continue
                    except Exception as e:
                        raise e

                    a.replay_buffer.add(exp)

                    a.train_step(exp, q_value, 0)

                    if exp.done:
                        print(f"!!!BEAVER DEATH!!! [{a.id}] energy={
                              a.beaver.energy}")
                        a.done = True
            if self.render_enabled:
                import time

                time.sleep(5)

    def get_beaver_list(self):
        return [x.beaver for x in self.agents]
