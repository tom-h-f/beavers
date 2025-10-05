from .agent import Beaver
from .action import Action, ActionType


class Reward:
    EXISTENCE_PENALTY = -0.05
    alive = True
    value = 0

    def add(self, other: float):
        self.value += other

    def die(self):
        self.alive = False

    def existence_penalty(self):
        self.add(self.EXISTENCE_PENALTY)

    def __format__(self, fmt):
        alive_str = "Alive" if self.alive else "Dead"
        return f"Reward({self.value}, {alive_str})"


def calculate_reward(state: Beaver, action: Action):
    reward = Reward()

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
