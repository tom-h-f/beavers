import numpy as np
import random
from core.agent import Beaver
from core.agent import Action, ActionType
from core.agent import calculate_reward
from core.terrain.tile import Tile


class Environment:
    def __init__(self, width: int = 128, height: int = 128):
        self.width = width
        self.height = height
        self.agents = []

    def add_agent(self, b: Beaver):
        self.agents.append(b)
        print(f"New agent spawned at [{b.x},{b.y}]")

    def agent_move_is_valid(self, b: Beaver, action: Action):
        proposed_x = int(b.x) + action.quantity.dx
        proposed_y = int(b.y) + action.quantity.dy
        if proposed_x < 0 or proposed_y < 0:
            return False
        if proposed_x >= self.width or proposed_y >= self.height:
            return False

        return self.world_grid[proposed_x][proposed_y] == Tile.GROUND

    def step(self):
        for b in self.agents:
            if b.sleep_ticks_remaining > 0:
                b.sleep_ticks_remaining -= 1
                continue
            act = b.get_action(self)
            # TODO should the fact it is not valid be passed
            # to the reward function? idk
            reward = calculate_reward(b, act)
            if (act.type == ActionType.Move
                    and not self.agent_move_is_valid(b, act)):
                continue

            print(f"reward: {reward:02}\tenergy: {b.energy:02}")
            b.do(act)

    def generate_world(self):
        # TODO: This needs to become a actual, complicated world generation built for generating rivers.
        random.seed()
        ground_chance = 0.5
        tree_chance = 0.1
        water_chance = 0.4
        self.world_grid = np.random.choice(
            [0, 1, 1.5],
            size=(self.height, self.width),
            p=[water_chance, ground_chance, tree_chance],
        )
