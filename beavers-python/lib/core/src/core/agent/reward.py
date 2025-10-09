from core.agent import Beaver
from .action import Action


def calculate_reward(state: Beaver, action: Action, env) -> (float, bool):
    existence_penalty = -0.05
    reward = 0.0
    INVALID_ACTION = -1

    if not action.is_valid(state, env.grid):
        return INVALID_ACTION, False

    match action:
        case Action.MoveRight:
            reward += 0.025
        case Action.MoveUp:
            reward += 0.025
        case Action.MoveLeft:
            reward += 0.025
        case Action.MoveDown:
            reward += 0.025
        case Action.Eat:
            # TODO: this reward and the eat itself should check for the log in inventory, massive penalty when attempting
            # to eat when we dont have a log to eat.
            if state.energy < 40:
                reward += 0.75
            elif state.energy > 75:
                reward -= 0.5
        case Action.Sleep:
            if state.energy < 20:
                reward += 0.75
            elif state.energy > 60:
                reward -= 0.5

    reward += existence_penalty
    return reward, True
