from .agent import Beaver, AgentDied
from .action import Action, ActionType


class Reward:
    EXISTENCE_PENALTY = -0.05
    value = 0

    def add(self, other: float):
        self.value += other

    def die(self):
        raise AgentDied

    def existence_penalty(self):
        self.add(self.EXISTENCE_PENALTY)

    def __format__(self, fmt):
        return f"Reward({self.value})"


def calculate_reward(state: Beaver, action: Action):
    reward = Reward()
    import random
    if random.randrange(0, 200, 1) == 1:
        reward.die()
        return

    if state.energy == 0:
        reward.die()
    match action.type:
        case ActionType.Move:
            reward.add(0)
        case ActionType.Eat:
            if state.energy < 40:
                reward.add(1)
        case ActionType.Sleep:
            if state.energy < 20:
                reward.add(1)

    reward.existence_penalty()
    return reward
