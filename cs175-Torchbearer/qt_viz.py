import tkinter as tk
import numpy as np
from constants import X_MIN, X_MAX, Y_MIN, Y_MAX, Z_MIN, Z_MAX
import torch


def init_canvas():
    world_x = X_MAX - X_MIN + 1
    world_z = Z_MAX - Z_MIN + 1
    scale = 20  # pixels per grid square
    canvas_root = tk.Tk()
    canvas_root.title("DQN Q-Values")
    canvas = tk.Canvas(canvas_root, width=world_x * scale, height=world_z * scale, bg="black")
    canvas.grid()
    canvas_root.update()
    return canvas_root, canvas


def get_state(x, y, z):
    return torch.tensor([
        (x - X_MIN) / (X_MAX - X_MIN),
        (y - Y_MIN) / (Y_MAX - Y_MIN),
        (z - Z_MIN) / (Z_MAX - Z_MIN)
    ], dtype=torch.float32).unsqueeze(0)

def draw_dqn_q(policy_net, canvas, scale=20, highlight_pos=None):
    canvas.delete("all")
    action_radius = 0.08

    action_offsets = {
        0: (0.5, 0.1),  # movesouth
        1: (0.15, 0.5),  # movewest
        2: (0.85, 0.5),  # moveeast
    }

    world_x = X_MAX - X_MIN + 1

    for x in range(X_MIN, X_MAX + 1):
        for z in range(Z_MIN, Z_MAX + 1):
            state = get_state(x, Y_MIN, z)
            with torch.no_grad():
                q_vals = policy_net(state).squeeze().numpy()

            # Normalize per cell
            q_min = np.min(q_vals)
            q_max = np.max(q_vals)
            if q_max - q_min < 1e-6:
                q_max = q_min + 1e-6

            for a, q in enumerate(q_vals):
                norm_q = (q - q_min) / (q_max - q_min)
                color = int(255 * norm_q)
                color_str = '#%02x%02x%02x' % (255 - color, color, 0)

                offset = action_offsets.get(a, (0.5, 0.5))
                cx = (world_x - 1 - (x - X_MIN) + offset[0]) * scale
                cy = (z - Z_MIN + offset[1]) * scale
                r = action_radius * scale
                canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color_str, outline=color_str)

            canvas.create_rectangle(
                (world_x - 1 - (x - X_MIN)) * scale,
                (Z_MAX - z) * scale,
                (world_x - (x - X_MIN)) * scale,
                (Z_MAX - z + 1) * scale,
                outline="#444"
            )

    if highlight_pos:
        x, z = highlight_pos
        cx = (world_x - 1 - (x - X_MIN) + 0.5) * scale
        cy = (Z_MAX - z + 0.5) * scale
        r = 0.2 * scale
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="white", fill="white")

    canvas.update()