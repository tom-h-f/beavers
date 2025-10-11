from core.agent import Beaver
from .action import Action, Move, Sleep, Eat, BuildDam
from core.terrain.tile import Tile
from typing import List
from core.dqn import DQNBeaver


def calculate_reward(state: Beaver, all_agents: List[DQNBeaver], action: Action, env) -> (float, bool):
    existence_penalty = -0.05
    reward = 0.0
    INVALID_ACTION = -1

    if not action.is_valid(state, all_agents, env.grid):
        return INVALID_ACTION, False

    # TODO: print out the relevant states esp when we hit one of the conditionals for eating,sleeping and building dams
    match action:
        case Move(direction=direction):
            reward += 0.1
        case Eat():
            # TODO: this reward and the eat itself should check for the log in inventory, massive penalty when attempting
            # to eat when we dont have a log to eat. That should just be an invalid action actually.
            if state.energy < 20:
                reward += 0.7
            elif state.energy < 40:
                reward += 0.3
        case Sleep():
            if state.energy < 10:
                reward += 0.7
            elif state.energy < 20:
                reward += 0.3
        case BuildDam(direction=direction):
            # TODO: Check for log in inventory
            reward += 0.40
            if state.tile_on(env.grid) == Tile.DAM:
                reward += 0.2

    reward += existence_penalty
    return reward, True
