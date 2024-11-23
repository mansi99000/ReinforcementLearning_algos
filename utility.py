# need to play around with the values of step size. 

import numpy as np
from collections import defaultdict
from cat_monsters_domain import get_possible_next_states, valid_states, forbidden_positions, food_position, states, get_reward

optimal_value = {
    (0, 0): 2.6638, (0, 1): 2.9969, (0, 2): 2.8117, (0, 3): 3.6671, (0, 4): 4.8497,
    (1, 0): 2.9713, (1, 1): 3.5101, (1, 2): 4.0819,   (1, 3): 4.8497, (1, 4): 7.1648,
    (2, 0): 2.5936, (2, 1): None,   (2, 2): None,   (2, 3): None,   (2, 4): 8.4687,
    (3, 0): 2.0992, (3, 1): 1.0849, (3, 2): None,   (3, 3): 8.6097, (3, 4): 9.5269,
    (4, 0): 1.0849, (4, 1): 4.9465, (4, 2): 8.4687, (4, 3): 9.5269, (4, 4): 0.0000,
}
# optimal_value

def max_norm(v_1, v_2):
    diff = max(np.abs(v_1[s] - v_2[s]) for s in valid_states)
    if diff < 0.2:
        return True
    return False

def sample_initial_state():
    """Sample uniformly from non-forbidden, non-terminal states."""
    valid_states = [s for s in states if s not in forbidden_positions and s != food_position]
    return valid_states[np.random.choice(len(valid_states))]

def initialize_optimal_policy():
    policy = {
        (0, 0): "AR", (0, 1): "AD", (0, 2): "AL", (0, 3): "AD", (0, 4): "AD",
        (1, 0): "AR", (1, 1): "AR", (1, 2): "AR", (1, 3): "AR", (1, 4): "AD",
        (2, 0): "AU", (2, 1): None,   (2, 2): None,   (2, 3): None,   (2, 4): "AD",
        (3, 0): "AU", (3, 1): "AL", (3, 2): None,   (3, 3): "AR", (3, 4): "AD",
        (4, 0): "AU", (4, 1): "AR", (4, 2): "AR", (4, 3): "AR", (4, 4): None  # Terminal state (G)
    }
    return policy

def generate_episode(policy, start_state):
    """Generate an episode following the given policy."""
    state = start_state
    episode = []
    t = 0
    while state != food_position:
        if(t > 100):
            break
        action = policy[state]
        next_state = get_possible_next_states(state, action)  
        reward = get_reward(next_state)
        episode.append((state, action, reward, next_state))
        state = next_state
        t+=1
    return episode

def print_value_function_grid(value_function, grid_size=5):
    print("Estimated Value Function Grid:")
    for row in range(grid_size):
        row_values = []
        for col in range(grid_size):
            value = value_function.get((row, col), 0)  # Default to 0 if not in the dictionary
            row_values.append(f"{value:8.4f}")  # Format the value to 2 decimal places
        print(" ".join(row_values))  # Join and print the row values

