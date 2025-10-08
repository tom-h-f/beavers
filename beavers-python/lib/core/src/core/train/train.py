from core.dqn import DQNNetwork, DQNBeaver
from core.agent.experience import ReplayBuffer
import torch
import torch.nn as nn
import math


class Trainer:
    # how much we value future rewards vs immediate
    # higher is longer-term thinking
    gamma = 0.7  # aka 'discount factor'
    learning_rate = 0.01  # TODO look up proper values for this and gamma

    def __init__(self,  network: DQNNetwork, target_network: DQNNetwork, replay_buffer: ReplayBuffer):
        self.network = network
        self.target_network = target_network
        self.replay_buffer = replay_buffer
        self.optimiser = torch.optim.SGD(
            self.network.parameters(), self.learning_rate
        )
        self.losses = []

    def train_step(self, a: DQNBeaver):
        sample = self.replay_buffer.sample()
        q_values = self.network(sample.states)
        # shape: [batch_sz, n_actions]
        # i need to index for whatever batch i was using,
        # and the action we used. Effectively:
        # q_values[n][a]

        # We add the 1st(n_actions) dimension here
        # The list/tensor that is `sample.actions` indexes to get us to the correct batch
        # then value inside indexes to get the q-value
        # for the selected aciton
        action_tensor = torch.unsqueeze(sample.actions, 1)
        computed_q = torch.gather(q_values, 1, action_tensor).squeeze(1)

        with torch.no_grad():
            q_values = self.target_network.forward(sample.next_states)
            selected_q = q_values.max(1).values

            target_q = sample.rewards + self.gamma * \
                selected_q * (sample.dones.float())

        loss = self.loss(computed_q, target_q)
        self.losses.append(loss.item())
        print(f"loss={loss}", end="\r")
        self.optimiser.zero_grad()

        # TODO: look up how this backward function works, what does it actually do
        loss.backward()
        self.optimiser.step()

    def loss(self, current, target) -> float:
        loss_fn = nn.L1Loss()
        return loss_fn(current, target)
