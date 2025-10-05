import random
from .action import Action, ActionType, MoveQuantity


class Beaver:
    def __init__(self, x: int = 0, y: int = 0, energy: int = 100):
        self.x: int = x
        self.y: int = y
        self.energy = 100
        self.inventory = {"logs": 0}
        self.sleep_ticks_remaining = 0

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
        self.energy -= dx+dy

    def eat(self):
        if self.inventory["logs"] > 0:
            self.inventory["logs"] -= 1
            self.energy += 10

    def sleep(self, ticks: int):
        self.sleep_ticks_remaining = ticks

    def do(self, action: Action):
        match action.type:
            case ActionType.Move:
                dx = action.quantity.dx
                dy = action.quantity.dy
                self.move(dx, dy)

            case ActionType.Eat:
                self.eat()
            case ActionType.Sleep:
                self.sleep(action.quantity)

    def get_action(self, env):
        # TODO: Obviously this should not be a random, should be policy
        decision = random.randrange(0, 3, 1)
        # TODO: Remove the randoms from the ranges below
        match decision:
            case 0:
                return Action(ActionType.Move, MoveQuantity(random.randrange(-1, 2, 1), random.randrange(-1, 2, 1)))
            case 1:
                return Action(ActionType.Eat, 1)
            case 2:
                return Action(ActionType.Sleep, random.randrange(0, 3, 1))


class AgentDied(Exception):
    """Raised when agent dies """
    pass
