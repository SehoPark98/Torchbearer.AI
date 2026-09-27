# constants.py: defines constants used
import numpy as np

# Map Bounds (based on walls and blocks)
X_MIN, X_MAX = 101, 107
Z_MIN, Z_MAX = 100, 130
Y_MIN, Y_MAX = 100, 106

# Useful Coordinates
X_MID = (X_MIN + X_MAX) // 2         # Center X coordinate = 102
Y_FLOOR = 100                        # Floor level from first cuboid
X_LEFT_WALL = X_MIN                 # Left wall at x = 100
X_RIGHT_WALL = X_MAX                # Right wall at x = 105

# Dimensions
X_WIDTH  = X_MAX - X_MIN + 1        # 6 blocks wide
Z_HEIGHT = Z_MAX - Z_MIN + 1

TURNS = (
    [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12] +
    [-12, -12, -11, -12, -11, -10, -11, -12, -12, -11, -10, -11, -12] +
    [-12, -11, -10, -9, -8, -7, -6, -7, -8, -9, -10, -11, -12] +
    [-12, -11, -10, -9, -8, -7, -6, -7, -8, -9, -10, -11, -12] +
    [-12, -11, -10, -9, -8, -7, -6, -7, -8, -9, -10, -11, -12] +
    [-12, -11, -10, -9, -8, -7, -6, -7, -8, -9, -10, -11, -12] +
    [-11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0] +
    [0, 0, 0, 0, 0, 0, 0]
)

# Hyperparameters
ALPHA   = 0.001  # Learning rate
GAMMA   = 0.9  # Discount factor
#EPSILON = 0.2 # Exploration probability
EPSILON_START = 1.0
EPSILON_END = 0.05
EPSILON_DECAY = 0.995

# Agent Control
ACTIONS = [("movesouth", 1), ("movewest", 1), ("moveeast", 1)]
NUM_ACTIONS = len(ACTIONS)
MAX_STEPS = 500

# Q-learning and Runtime Control
Q_TABLE = np.zeros((X_WIDTH * Z_HEIGHT, NUM_ACTIONS))  # (3000, 4)
EPISODES = 20000
RUNTIME = 50
SCALE_FACTOR = 1
MS_PER_TICK = int(50 / SCALE_FACTOR)


#DQN and NN
BATCH_SIZE = 64
BUFFER_CAPACITY = 10000