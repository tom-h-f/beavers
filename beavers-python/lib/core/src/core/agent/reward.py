from core.agent import Beaver
from core.agent.exceptions import AgentIsDead
from .action import Action


def calculate_reward(state: Beaver, action: Action) -> float:
    existence_penalty = -0.05
    reward = 0.0

    match action:
        case Action.MoveRight:
            reward += 1
        case Action.MoveUp:
            reward += 1
        case Action.MoveLeft:
            reward += 1
        case Action.MoveDown:
            reward += 1
        case Action.Eat:
            # TODO: this reward and the eat itself should check for the log in inventory, massive penalty when attempting
            # to eat when we dont have a log to eat.
            if state.energy < 40:
                reward += 50
            elif state.energy > 75:
                reward -= 50
        case Action.Sleep:
            return 0xFFFFFFF
            if state.energy < 20:
                reward += 50
            elif state.energy > 60:
                reward -= 50

    reward += existence_penalty
    return reward
