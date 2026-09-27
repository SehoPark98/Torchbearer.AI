import torch
import torch.nn as nn
import numpy as np
from collections import deque
from constants import BATCH_SIZE, GAMMA, MAX_STEPS
import random


def update_target_network(policy_net, optimizer, replay_buffer, loss_fn, writer, episode, step):
    if len(replay_buffer) >= BATCH_SIZE:
        transitions = replay_buffer.sample(BATCH_SIZE)
        states, actions, rewards, next_states, dones = zip(*transitions)

        states = torch.tensor(np.array(states), dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1)
        q_values = policy_net(states).gather(1, actions)

        with torch.no_grad():
            max_next_q = policy_net(next_states).max(1)[0].unsqueeze(1)
            target_q = rewards + GAMMA * max_next_q * (1 - dones)

        loss = loss_fn(q_values, target_q)
        optimizer.zero_grad()
        loss.backward()
        writer.add_scalar("Training Loss", loss.item(), episode * MAX_STEPS + step)
        writer.add_scalar("Q Max", q_values.max().item(), episode * MAX_STEPS + step)
        writer.add_scalar("TD Target", target_q.mean().item(), episode * MAX_STEPS + step)
        optimizer.step()


class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        return self.net(x)


    
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, transition):
        self.buffer.append(transition)

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)
