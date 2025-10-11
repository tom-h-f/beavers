import random
import numpy as np
import torch
from dataclasses import dataclass
from typing import List
from core.agent.action import BeaverStepInfo, Action, action_to_int
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
    def __init__(self, batch_size):
        self._list = deque()
        self.batch_size = batch_size

    def add(self, e: Experience):
        if self.len() >= 100_000:
            self._list.popleft()

        self._list.append(e)

    def len(self) -> int:
        return len(self._list)

    def sample(self) -> ReplaySample:
        if self.batch_size > len(self._list):
            self.batch_size = len(self._list)

        candidates = random.sample(
            self._list, min(self.batch_size, self.len()))

        # Need to convert each element in an experience
        # so its ready to be used
        states = torch.cat([s.state for s in candidates])
        next_states = torch.cat([s.next_state for s in candidates])
        assert states.shape == next_states.shape

        actions = torch.tensor([action_to_int(s.action) for s in candidates])
        rewards = torch.tensor([s.reward for s in candidates])
        dones = torch.tensor([s.done for s in candidates])
        return ReplaySample(states, next_states, actions,
                            rewards, dones)
