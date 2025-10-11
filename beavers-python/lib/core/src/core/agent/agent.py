from .action import Action, Move, Eat, Sleep, BuildDam
from core.terrain.tile import Tile

import uuid


class Beaver:
    def __init__(self, x: int = 0, y: int = 0, energy: int = 100):
        self.id = uuid.uuid4()

        self.x: int = x
        self.y: int = y
        self.energy = 100
        self.logs = 0
        self.food = 0
        self.sleep_ticks_remaining = 0

    def move(self, m: Move):
        self.x, self.y = m.direction.apply(self.x, self.y)
        self.energy -= 5

    def eat(self):
        if self.food > 0:
            self.energy += 25

    def build_dam(self, bd: BuildDam, env):
        import core.environment.gridworld as gw
        dam_location_x = self.x
        dam_location_y = self.y
        dam_location_x, dam_location_y = bd.direction.apply(
            dam_location_x, dam_location_y)

        env.grid.raw()[dam_location_x][dam_location_y] = Tile.DAM

    def sleep(self, ticks: int):
        self.sleep_ticks_remaining = ticks

    def do(self, action: Action, env):
        # TODO: Look up if better way to get the Move() instances
        # i think should work without the args but waiting to test
        match action:
            case Move(direction=direction):
                self.move(action)
            case Eat():
                self.eat()
            case Sleep():
                self.sleep(1)
            case BuildDam(direction=direction):
                self.build_dam(action, env)

    def tile_on(self, grid) -> Tile:
        return grid.tile_at(self.x, self.y)
