import random
import numpy as np
import torch
from dataclasses import dataclass
from typing import List
from core.agent.action import BeaverStepInfo, Action
from collections import deque


@dataclass
class Experience:
    # TODO: get the actual type of the states, which are just observations
    state: any
    action: Action
    next_state: any
    reward: float
    done: bool
    info: BeaverStepInfo


@dataclass
class ReplaySample:
    states: np.ndarray
    next_states: np.ndarray
    actions: List[Action]
    rewards: List[float]
    dones: List[bool]


class ReplayBuffer:
    def __init__(self, limit=0xFFFF):
        self._list = deque()
        self.limit = limit

    def add(self, e: Experience):
        if self.len() >= self.limit:
            old_len = self.len()
            self._list.popleft()

        self._list.append(e)

    def len(self) -> int:
        return len(self._list)

    def sample(self, batch_sz: int) -> ReplaySample:
        if batch_sz > len(self._list):
            batch_sz = len(self._list)

        candidates = random.sample(self._list, min(batch_sz, self.len()))

        # Need to convert each element in an experience
        # so its ready to be used
        states = torch.cat([s.state for s in candidates])
        next_states = torch.cat([s.next_state for s in candidates])
        assert states.shape == next_states.shape

        actions = torch.tensor([int(s.action) for s in candidates])
        rewards = torch.tensor([s.reward for s in candidates])
        dones = torch.tensor([s.done for s in candidates])
        return ReplaySample(states, next_states, actions,
                            rewards, dones)
