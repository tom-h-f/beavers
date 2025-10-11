from dataclasses import dataclass
from typing import final
from enum import IntEnum
import random

from core.terrain.tile import Tile

NUMBER_OF_ACTIONS = 10


class Direction(IntEnum):
    right = 0
    up = 1
    left = 2
    down = 3

    def apply(self, x, y) -> tuple[int, int]:
        match self:
            case Direction.right:
                y += 1
            case Direction.left:
                y -= 1
            case Direction.up:
                x -= 1
            case Direction.down:
                x += 1
        return x, y


class Action():

    def is_move(self) -> bool:
        match self:
            case Move(direction=direction):
                return True
            case _:
                return False

    def random_action():
        return action_from_int(random.randrange(0, NUMBER_OF_ACTIONS))

    def how_many():
        return NUMBER_OF_ACTIONS

    def is_valid(self, b, all_agents, grid):
        match self:
            case Move() | BuildDam():
                proposed_x = b.x
                proposed_y = b.y
                proposed_x, proposed_y = self.direction.apply(
                    proposed_x, proposed_y)

                if proposed_x < 0 or proposed_y < 0:
                    return False
                if proposed_x >= grid.width or proposed_y >= grid.height:
                    return False

                match self:
                    case Move():
                        tile_types = [Tile.GROUND, Tile.DAM]
                    case BuildDam():
                        tile_types = [Tile.WATER]

                tile = grid.tile_at(proposed_x, proposed_y)
                if not tile in tile_types:
                    return False
            case Eat():
                return b.energy < 40
            case Sleep():
                return b.energy < 20

        return True


@final
class Eat(Action):
    def str(self): return "eat"
    pass


@final
class Sleep(Action):
    def str(self): return "sleep"
    pass


@dataclass
class Move(Action):
    def str(self): return f"move:{self.direction.name}"

    def __init__(self, direction: Direction):
        self.direction = direction


@dataclass
class BuildDam(Action):
    def str(self): return f"build_dam:{self.direction.name}"

    def __init__(self, direction: Direction):
        self.direction = direction


@dataclass
class BeaverStepInfo:
    success: bool
    action_type: str


def action_from_int(action_int: int) -> Action:
    """Convert network output (int) to Action object"""
    match action_int:
        case 0:
            return Move(Direction.right)
        case 1:
            return Move(Direction.up)
        case 2:
            return Move(Direction.left)
        case 3:
            return Move(Direction.down)
        case 4:
            return Eat()
        case 5:
            return Sleep()
        case 6:
            return BuildDam(Direction.right)
        case 7:
            return BuildDam(Direction.up)
        case 8:
            return BuildDam(Direction.left)
        case 9:
            return BuildDam(Direction.down)
        case _:
            raise ValueError(f"Invalid action int: {action_int}")


def action_to_int(action: Action) -> int:
    """Convert Action object to int (for storing in replay buffer)"""
    match action:
        case Move():
            match action.direction:
                case Direction.right:
                    return 0
                case Direction.up:
                    return 1
                case Direction.left:
                    return 2
                case Direction.down:
                    return 3
        case Eat():
            return 4
        case Sleep():
            return 5
        case BuildDam():
            match action.direction:
                case Direction.right:
                    return 6
                case Direction.up:
                    return 7
                case Direction.left:
                    return 8
                case Direction.down:
                    return 9
        case _:
            raise ValueError(f"Unknown action: {action}")
