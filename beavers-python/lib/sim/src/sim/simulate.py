from gridworld import Environment
import render
from core.agent import Beaver
import random
import math


class Simulator():
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.env = Environment(self.grid_width, self.grid_height)
        for i in range(0, 100):
            self.env.add_agent(Beaver(
                math.floor(
                    self.grid_width / random.randrange(1, 5, 1)),
                math.floor(self.grid_height / random.randrange(1, 5, 1))
            ))
        random.seed()

    def run(self, running):
        self.env.generate_world()
        gpu = render.PygameRenderer(self.grid_width, self.grid_height)

        while running:
            self.env.step()
            running = gpu.render(self.env)
