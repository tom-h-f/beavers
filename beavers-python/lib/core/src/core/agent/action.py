from dataclasses import dataclass


@dataclass
class MoveQuantity:
    dx: int
    dy: int


@dataclass
class ActionType:
    Move = 0
    Eat = 1
    Sleep = 2


@dataclass
class Action:
    type: ActionType
    quantity: int

    def __init__(self, type, quantity=1):
        self.type = type
        self.quantity = quantity
