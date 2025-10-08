from .action import Action
import uuid


class Beaver:
    def __init__(self, x: int = 0, y: int = 0, energy: int = 100):
        self.id = uuid.uuid4()

        self.x: int = x
        self.y: int = y
        self.energy = 100
        self.inventory = {"logs": 0}
        self.sleep_ticks_remaining = 0

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
        self.energy -= (dx + dy) * 4

    def eat(self):
        if self.inventory["logs"] > 0:
            self.inventory["logs"] -= 1
            self.energy += 5

    def sleep(self, ticks: int):
        self.sleep_ticks_remaining = ticks

    def do(self, action: Action):
        match action:
            case Action.MoveRight:
                self.move(1, 0)
            case Action.MoveUp:
                self.move(0, 1)
            case Action.MoveLeft:
                self.move(-1, 0)
            case Action.MoveDown:
                self.move(0, -1)
            case Action.Eat:
                self.eat()
            case Action.Sleep:
                self.sleep(1)
