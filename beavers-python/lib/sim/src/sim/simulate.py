from gridworld import Environment
import render
from core.agent import Beaver
import random


class Simulator():
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.env = Environment(self.grid_width, self.grid_height)
        self.env.add_agent(Beaver(self.grid_width / 2, self.grid_height / 2))
        random.seed()

    def run(self):
        self.env.generate_world()
        gpu = render.PygameRenderer(self.grid_width, self.grid_height)

        while True:
            self.env.step()
            gpu.render(self.env)
