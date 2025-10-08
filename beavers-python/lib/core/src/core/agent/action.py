from dataclasses import dataclass
from enum import IntEnum
import random


@dataclass
class MoveQuantity:
    dx: int
    dy: int


class Action(IntEnum):
    MoveRight = 0
    MoveUp = 1
    MoveLeft = 2
    MoveDown = 3
    Eat = 4
    Sleep = 5

    def is_move(self) -> bool:
        return int(self) < Action.Eat

    def random_action():
        return Action(random.randrange(0, 6))

    def to_type_str(self) -> str:
        if self.is_move():
            return "move"
        match self:
            case Action.Eat:
                return "eat"
            case Action.Sleep:
                return "sleep"
            case _:
                raise ValueError("Invalid Action")

    def how_many():
        return len(Action)

    def is_valid(self, b, grid):
        if self.is_move() and not grid.agent_move_is_valid(b, self):
            return False

        return True


@dataclass
class BeaverStepInfo:
    success: True
    action_type: str
