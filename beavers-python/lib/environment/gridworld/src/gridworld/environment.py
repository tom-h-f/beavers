import numpy as np
import random
from core.agent import Beaver
from core.terrain.tile import Tile


class Environment:
    def __init__(self, width: int = 128, height: int = 128):
        self.width = width
        self.height = height
        self.agents = []

    def add_agent(self, b: Beaver):
        self.agents.append(b)
        print(f"New agent spawned at [{b.x},{b.y}]")

    def agent_move_is_valid(self, b: Beaver, dx: int, dy: int):
        proposed_x = int(b.x) + dx
        proposed_y = int(b.y) + dy
        if proposed_x < 0 or proposed_y < 0:
            return False
        if proposed_x > self.width or proposed_y > self.height:
            return False

        return self.world_grid[proposed_x][proposed_y] == Tile.GROUND

    def step(self):
        for b in self.agents:
            if b.sleep_ticks_remaining > 0:
                b.sleep_ticks_remaining -= 1
                continue
            decision = random.randrange(0, 3, 1)
            match decision:
                case 0:
                    dx = random.randrange(-1, 2, 1)
                    dy = random.randrange(-1, 2, 1)
                    print(f"moving [{dx}, {dy}], now at [{b.x}, {b.y}]")
                    if (self.agent_move_is_valid(b, dx, dy)):
                        b.move(dx, dy)
                        print(f"moved [{dx}, {dy}], now at [{b.x}, {b.y}]")

                case 1:
                    print("eating")
                    b.eat()
                case 2:
                    print("sleeping")
                    b.sleep(random.randrange(0, 5, 1))

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
