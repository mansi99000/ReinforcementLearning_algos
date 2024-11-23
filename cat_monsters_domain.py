# need to play around with the values of step size. 

import numpy as np
from collections import defaultdict

# Cat-vs-Monster domain
grid_size = 5  # 5x5 grid
reward_food = 10
reward_monster = -8
reward_default = -0.05
states = [(r, c) for r in range(grid_size) for c in range(grid_size)]
actions = ["AU", "AD", "AL", "AR"]

forbidden_positions = [(3, 2), (2, 2), (2, 1), (2, 3)]
monster_positions = [(0, 3), (4, 1)]
food_position = (4, 4)
valid_states = [state for state in states if state not in forbidden_positions and state is not food_position]


def get_possible_next_states(state, action):
    row, col = state    
    next_states = defaultdict(list)

    # Define intended move based on action
    if action == "AU":  # Up
        intended = (row - 1, col) if row > 0 else (row, col)
        right = (row, col + 1) if col < grid_size - 1 else (row, col)
        left = (row, col - 1) if col > 0 else (row, col)
    elif action == "AD":  # Down
        intended = (row + 1, col) if row < grid_size - 1 else (row, col)
        right = (row, col - 1) if col > 0 else (row, col)
        left = (row, col + 1) if col < grid_size - 1 else (row, col)
    elif action == "AL":  # Left
        intended = (row, col - 1) if col > 0 else (row, col)
        right = (row - 1, col) if row > 0 else (row, col)
        left = (row + 1, col) if row < grid_size - 1 else (row, col)
    elif action == "AR":  # Right
        intended = (row, col + 1) if col < grid_size - 1 else (row, col)
        right = (row + 1, col) if row < grid_size - 1 else (row, col)
        left = (row - 1, col) if row > 0 else (row, col)

    if intended in forbidden_positions:
        intended = (row, col)
    if right in forbidden_positions:
        right = (row, col)
    if left in forbidden_positions:
        left = (row, col)

    next_states[intended].append(0.7)
    next_states[right].append(0.12)
    next_states[left].append(0.12)
    # Add the probability of staying in place
    next_states[(row, col)].append(0.06)

    states, probabilities = zip(*next_states.items())
    probabilities = [sum(p) for p in probabilities]
    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]
    state_indices = list(range(len(states)))
    sampled_index = np.random.choice(state_indices, p=probabilities)
    sampled_state = states[sampled_index]
    return sampled_state

def get_reward(next_state):
    if next_state == food_position:
        return reward_food
    elif next_state in monster_positions:
        return reward_monster
    else:
        return reward_default






