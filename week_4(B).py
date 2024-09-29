import numpy as np
import scipy.io
import random
import math

# Load the scrambled puzzle
data = scipy.io.loadmat('scrambled_lena.mat')
scrambled_puzzle = data['scrambled_lena']

# Define the energy function
def energy(state):
    # Calculate the energy based on the number of misplaced pieces
    correct_puzzle = np.arange(state.size).reshape(state.shape)
    return np.sum(state != correct_puzzle)

# Define the neighbor function
def get_neighbor(state):
    neighbor = state.copy()
    i, j = random.sample(range(state.size), 2)
    neighbor.flat[i], neighbor.flat[j] = neighbor.flat[j], neighbor.flat[i]
    return neighbor

# Simulated annealing algorithm
def simulated_annealing(initial_state, initial_temp, cooling_rate, max_iter):
    current_state = initial_state
    current_energy = energy(current_state)
    temperature = initial_temp

    for iteration in range(max_iter):
        if temperature <= 0:
            break

        neighbor = get_neighbor(current_state)
        neighbor_energy = energy(neighbor)

        if neighbor_energy < current_energy or random.uniform(0, 1) < math.exp((current_energy - neighbor_energy) / temperature):
            current_state = neighbor
            current_energy = neighbor_energy

        temperature *= cooling_rate

    return current_state

# Initial parameters
initial_state = scrambled_puzzle
initial_temp = 1000
cooling_rate = 0.99
max_iter = 10000

# Solve the puzzle
solved_puzzle = simulated_annealing(initial_state, initial_temp, cooling_rate, max_iter)
print("Solved Puzzle:")
print(solved_puzzle)