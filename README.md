# Torchbearer.AI – Deep Reinforcement Learning for Minecraft Pathfinding

Torchbearer.AI is a deep reinforcement learning project that trains an AI agent to navigate hazardous cave environments in Minecraft using Microsoft Project Malmo.

The goal of the project is to teach an agent to reach a destination as quickly and safely as possible while avoiding obstacles such as lava, cobwebs, and other environmental hazards.

## Key Features

- Deep Q-Network (DQN) based reinforcement learning
- Minecraft environment powered by Microsoft Project Malmo
- Custom reward function designed to encourage fast and safe navigation
- Epsilon-greedy exploration with decay
- Experience replay for improved training stability
- TensorBoard-based training visualization
- Custom Q-value visualization for monitoring agent behavior

## Approach

The project initially used tabular Q-learning as a baseline. As the state space grew, memory and generalization limitations became apparent, so the model was scaled to a Deep Q-Network (DQN).

The final neural network uses:

- 2 hidden layers
- 64 neurons per hidden layer
- ReLU activation
- Replay buffer for experience sampling
- Epsilon-greedy exploration with decay
- Target network for improved stability

## Reward Design

The reward function was designed to prioritize efficient navigation by rewarding goal completion while penalizing unnecessary movement, repeated states, and hazardous contacts.

```text
reward = 150 * goal - 3 * visited - 10 * hazard - steps

## Demo

**Demo Video:** [Watch Torchbearer.AI in Action](https://drive.google.com/file/d/1qTq0qIfpmk97zcE8I8SJ14hVvYT1IQMF/view?usp=sharing)

