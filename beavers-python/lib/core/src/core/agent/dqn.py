import torch
import torch.nn as nn
import torch.nn.functional as F
from core.agent import Beaver, Action
from .experience import ReplayBuffer, Experience
import random


class DQN(nn.Module):
    FIRST_CONV_FEATURE_MAP_COUNT = 32
    SECOND_CONV_FEATURE_MAP_COUNT = 64
    FIRST_FC_NEURON_COUNT = 128

    def __init__(self, observation_shape, n_actions):
        super(DQN, self).__init__()

        n_channels = observation_shape[0]
        self.conv1 = nn.Conv2d(
            n_channels, self.FIRST_CONV_FEATURE_MAP_COUNT, kernel_size=3, padding=1
        )
        self.conv2 = nn.Conv2d(
            self.FIRST_CONV_FEATURE_MAP_COUNT,
            self.SECOND_CONV_FEATURE_MAP_COUNT,
            kernel_size=3,
            padding=1,
        )
        flattened_size = (
            self.SECOND_CONV_FEATURE_MAP_COUNT
            * observation_shape[1]
            * observation_shape[1]
        )
        self.fc1 = nn.Linear(flattened_size, self.FIRST_FC_NEURON_COUNT)
        self.fc2 = nn.Linear(self.FIRST_FC_NEURON_COUNT, n_actions)

    def forward(self, x):
        # x comes in as [batch_sz, 32, height, width]

        x = self.conv1(x)  # x shape: [batch_sz, 32, height, width]
        x = torch.relu(x)

        x = self.conv2(x)  # x shape: [batch_sz, 64, height, width]
        x = torch.relu(x)

        # Flatten spatial dimensions and keep batch dimension
        # x.size(0) = batch_sz
        # -1 tells pytorch to calculate this dimension automatically
        x = x.view(x.size(0), -1)  # x shape: [batch_sz, 64*height*width]
        # Fully Connected Layers
        x = self.fc1(x)
        x = torch.relu(x)

        x = self.fc2(x)
        return x


class DQNBeaver:
    epsilon = 1.0
    epsilon_min = 0.01
    epsilon_decay = 0.998

    # how much we value future rewards vs immediate
    # higher is longer-term thinking
    gamma = 0.7  # aka 'discount factor'

    learning_rate = 0.001

    def __init__(self, observation_shape, n_actions, spawn_x=0, spawn_y=0):
        self.n_actions = n_actions
        self.q_network = DQN(observation_shape, self.n_actions)
        self.target_network = DQN(observation_shape, self.n_actions)
        self.beaver = Beaver()
        self.id = self.beaver.id
        self.update_target_network()
        self.replay_buffer = ReplayBuffer()
        self.optimiser = torch.optim.SGD(
            self.q_network.parameters(), self.learning_rate
        )
        # TODO: this really should be somewhere else...
        self.done = False

    def select_action(self, observation, epsilon) -> (Action, float):
        q_values = self.q_network.forward(observation)
        if random.random() < epsilon:
            action = Action.random_action()
        else:
            action = q_values.argmax().item()
        return Action(action), q_values.max()

    def is_done(self) -> bool:
        # TODO: Could we add other 'done' conditions?
        if self.beaver.energy <= 0 or self.epsilon <= self.epsilon_min:
            return True

        return False

    def train_step(self, state: Experience, current_q: float, nth_step: int):
        with torch.no_grad():
            q_vals = self.target_network.forward(state.next_state)

            # We are using .max() here because we don't actually care *what* action
            # is the next one, we just care if we can get a high q-value.
            target_q = state.reward + self.gamma * q_vals.max()

        loss = self.get_loss(current_q, target_q)
        print(f"loss={loss.item():32} - epsilon={self.epsilon:32}", end="\r")

        self.optimiser.zero_grad()
        loss.backward()
        self.optimiser.step()

        # TODO: Add -> Every 100 cycles or so, copy the network to target network, transferring the weights
        # TODO: handle done flag, when episode complete do something with the gamma * max_next_q part?

        self.decay_epsilon()

    def get_loss(self, current, target) -> float:
        loss_fn = nn.L1Loss()
        return loss_fn(current, target)

    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
