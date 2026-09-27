# agent.py: DQN-based episode logic
# ----------------------
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import time, json, random
import os
from collections import deque
from model import DQN, ReplayBuffer, update_target_network
from constants import X_MIN, X_MAX, Y_MIN, Y_MAX, Z_MIN, Z_MAX, MAX_STEPS, ALPHA, GAMMA, ACTIONS, NUM_ACTIONS, BATCH_SIZE, BUFFER_CAPACITY, SCALE_FACTOR
from qt_viz import draw_dqn_q


policy_net = DQN(input_dim=3, output_dim=NUM_ACTIONS)
optimizer = optim.Adam(policy_net.parameters(), lr=ALPHA)
replay_buffer = ReplayBuffer(capacity=BUFFER_CAPACITY)
loss_fn = nn.MSELoss()


if os.path.exists("checkpoints/dqn_full.pt"):
    checkpoint = torch.load("checkpoints/dqn_full.pt")
    policy_net.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    print(f"Loaded model from checkpoints/dqn_full.pt")


def run_episode(agent_host, episode, writer, canvas, epsilon):
    ws = agent_host.getWorldState()
    while ws.is_mission_running and not ws.observations:
        time.sleep(0.1/SCALE_FACTOR)
        ws = agent_host.getWorldState()
    if not ws.is_mission_running:
        return 0

    obs = json.loads(ws.observations[-1].text)
    x_raw, y_raw, z_raw = __extract_coord(obs)
    x, y, z = __clamp_coord(x_raw, y_raw, z_raw)
    prev_x, prev_y, prev_z = x, y, z
    state = __get_state(x, y, z)
    total_reward = 0
    max_z = 0
    new_obs = None
    # stationary_penalty = 0
    
    web_hit_count = 0
    water_hit_count = 0
    hazard_blocks = ["web", "water"]
    
    recently_visited_positions = deque(maxlen=10)  # save 10 recently visited positions
    recently_visited_positions.append((int(x), int(y), int(z)))
    
    for step in range(MAX_STEPS):
        # Select action using ε-greedy
        if random.random() < epsilon:
            action = random.randint(0, NUM_ACTIONS - 1)
        else:
            with torch.no_grad():
                state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
                action = policy_net(state_tensor).argmax().item()

        #action = 3

        cmd, val = ACTIONS[action]
        agent_host.sendCommand("{} {}".format(cmd, val))
        time.sleep(0.3/SCALE_FACTOR)
        agent_host.sendCommand("{} {}".format(cmd, 0))

        ws = agent_host.getWorldState()

        new_x, new_y, new_z = int(x), int(y), int(z)
        if ws.number_of_observations_since_last_state > 0:
            new_obs = json.loads(ws.observations[-1].text)
            new_x_raw, new_y_raw, new_z_raw = __extract_coord(new_obs)
            new_x, new_y, new_z = __clamp_coord(int(new_x_raw), int(new_y_raw), int(new_z_raw))
        new_state = __get_state(new_x, new_y, new_z)

        max_z = max(max_z, new_z)

        # Reward function
        goal_bonus = 150.0 if new_z >= 127 else 0.0

        delta_z = new_z - z
        if delta_z > 0:
            reward = +20.0   # reward for going forward
        elif delta_z < 0:
            reward = -10.0   # penalty for going backward
        else:
            reward = -5.0    # penalty for staying on the same position
        reward += goal_bonus - 1.0   # goal bonus + step cost
        
        pos_tuple = (round(x), round(y), round(z))
        if pos_tuple in recently_visited_positions:
            reward -= 3.0
        recently_visited_positions.append(pos_tuple)
        writer.add_scalar("Penalty for Repeated Position", 1, episode * MAX_STEPS + step)
        
        # if new_obs:
        #     area = new_obs.get("playergrid", [])
        #     if any(block in area for block in hazard_blocks):
        #         if "web" in area:
        #             web_hit_count += 1
        #             hazard_penalty = -10 * web_hit_count
        #             writer.add_scalar("Penalty/Web", web_hit_count, episode * MAX_STEPS + step)
        #         elif "water" in area:
        #             water_hit_count += 1
        #             hazard_penalty = -10 * water_hit_count
        #             writer.add_scalar("Penalty/Water", water_hit_count, episode * MAX_STEPS + step)
                    
        #         reward += hazard_penalty

        #         # revert to previous position
        #         agent_host.sendCommand(f"tpx {int(prev_x) + 0.5}")
        #         agent_host.sendCommand(f"tpy {102}")
        #         agent_host.sendCommand(f"tpz {int(prev_z) - 0.5}")
        
        # Hazardous Penalty
        hazard_penalty = 0.0
        if ws.number_of_observations_since_last_state > 0:
            playergrid = new_obs.get("playergrid", [])
            if any(block in playergrid for block in hazard_blocks):
                # If it's web
                if "web" in playergrid:
                    web_hit_count += 1
                    hazard_penalty -= 10  # first web enter: -10, second web enter -10 ..etc
                # If it's water
                if "water" in playergrid:
                    water_hit_count += 1
                    hazard_penalty -= 10
                # move back to previous coordinates
                agent_host.sendCommand(f"tpx {int(prev_x) + 0.5}")
                agent_host.sendCommand(f"tpy {102}")
                agent_host.sendCommand(f"tpz {int(prev_z) - 0.5}")
        reward += hazard_penalty
                
        # penalty for recently visited positions
        if (new_x, new_y, new_z) in recently_visited_positions:
            reward -= 3.0
        recently_visited_positions.append((new_x, new_y, new_z))
        
        # Reward for reaching the goal
        goal_reached = (new_z >= 127)
        if goal_reached:
            reward += 150.0
            
        total_reward += reward
        max_z = max(max_z, new_z)

        # logging
        writer.add_scalar("Step Reward", reward, episode * MAX_STEPS + step)
        writer.add_scalar("Z Progress", (new_z - Z_MIN) / (Z_MAX - Z_MIN), episode * MAX_STEPS + step)
        
        # Update DQN
        done = (goal_reached or not ws.is_mission_running)
        replay_buffer.push((state, action, reward, new_state, done))
        update_target_network(policy_net, optimizer, replay_buffer, loss_fn, writer, episode, step)
        
        # Prepare for next step (update coordinates)
        state = new_state
        prev_x, prev_y, prev_z = new_x, new_y, new_z
        x, y, z = new_x, new_y, new_z

        # Quit if it reaches goal or mission end
        if done:
            agent_host.sendCommand("quit")
            break

        # if new_z >= 127 or not ws.is_mission_running:
        #     if new_z < 127:
        #         print("Episode {}: Failed to reach goal at Z >= 127".format(episode))
        #         reward -= 10
        #     total_reward += reward
        #     replay_buffer.push((state, action, reward, new_state, new_z >= 127))
        #     agent_host.sendCommand("quit")
        #     break
        # else:
        #     replay_buffer.push((state, action, reward, new_state, new_z >= 127))

    # --------------------------
    # 6. Clear after each episode is done
    # --------------------------
    writer.add_scalar("Episode Reward", total_reward, episode)
    writer.add_scalar("Episode Max Z", max_z, episode)
    writer.add_scalar("Reached Goal?", int(max_z >= 127), episode)

    print(f"[Episode {episode}] Reward={total_reward:.2f} | MaxZ={max_z} | GoalReached={max_z >= 127}")
    if episode % 5 == 0:
        os.makedirs("checkpoints", exist_ok=True)
        torch.save({
            'model_state_dict': policy_net.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
        }, "checkpoints/dqn_full.pt")

    # visualize final status
    draw_dqn_q(policy_net, canvas, highlight_pos=(x, z))

    return total_reward

def __clamp_coord(x, y, z):
    x = max(X_MIN, min(X_MAX, int(x)))
    y = max(Y_MIN, min(Y_MAX, int(y)))
    z = max(Z_MIN, min(Z_MAX, int(z)))
    return x, y, z

def __extract_coord(obs):
    return obs.get('XPos', 0), obs.get('YPos', 0), obs.get('ZPos', 0)

def __get_state(x, y, z):
    return np.array([
        (x - X_MIN) / (X_MAX - X_MIN),
        (y - Y_MIN) / (Y_MAX - Y_MIN),
        (z - Z_MIN) / (Z_MAX - Z_MIN)
    ], dtype=np.float32)
