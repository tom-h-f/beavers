from dataclasses import dataclass
from core.agent.action import BeaverStepInfo
from collections import deque
from typing import List
import random


@dataclass
class Experience:
    next_state: float
    reward: float
    done: bool
    info: BeaverStepInfo


class ReplayBuffer:
    def __init__(self):
        self._list = deque()

    def add(self, e: Experience):
        self._list.append(e)

    def sample(self, batch_sz: int) -> List[Experience]:
        return random.sample(self._list, batch_sz)
