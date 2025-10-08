import torch
import torch.nn as nn
from core.agent import Beaver, Action
import random


class DQNNetwork(nn.Module):
    FIRST_CONV_FEATURE_MAP_COUNT = 32
    SECOND_CONV_FEATURE_MAP_COUNT = 64
    FIRST_FC_NEURON_COUNT = 128

    def __init__(self, observation_shape, n_actions):
        super(DQNNetwork, self).__init__()

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
    def __init__(self, network, x=0, y=0):
        self.beaver = Beaver()
        self.id = self.beaver.id
        self.network = network
        self.done = False

    def select_action(self, observation, epsilon) -> (Action, float):
        q_values = self.network.forward(observation)
        if random.random() < epsilon:
            action = Action.random_action()
        else:
            action = q_values.argmax().item()
        return Action(action), q_values.max()

    def is_done(self) -> bool:
        # TODO: Could we add other 'done' conditions?
        if self.beaver.energy <= 0:
            print("dead beaver")
            return True

        return False
