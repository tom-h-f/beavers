from dataclasses import dataclass
from enum import Enum


@dataclass
class MoveQuantity:
    dx: int
    dy: int


class Actions(Enum):
    RIGHT: 0
    UP_RIGHT: 1
    UP: 2
    UP_LEFT: 3
    LEFT: 4
    DOWN_LEFT: 5
    DOWN: 6
    DOWN_RIGHT: 7
    STAY_STILL: 8
    EAT: 9
    SLEEP: 10


@dataclass
class ActionType:
    Move = 0
    Eat = 1
    Sleep = 2


# TODO refactor this to work with the gym `Actions` enum defined above
@dataclass
class Action:
    type: ActionType
    quantity: int

    def __init__(self, type, quantity=1):
        self.type = type
        self.quantity = quantity
