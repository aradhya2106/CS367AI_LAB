import numpy as np

class Node:
    def __init__(self, parent, state, cost):
        self.parent = parent
        self.state = state
        self.cost = cost

    def __hash__(self):
        return hash(tuple(self.state))  # Use tuple as state representation for hashing

    def __str__(self):
        return ''.join(self.state)  # Concatenate state for string representation

    def __eq__(self, other):
        return self.state == other.state  # Directly compare states
    
    def __ne__(self, other):
        return self.state != other.state  # Direct inequality comparison

class PriorityQueue():
    def __init__(self):
        self.queue = []

    def push(self, node):
        self.queue.append(node)

    def pop(self):
        # Find the node with the least cost and pop it from the queue
        min_cost = min(self.queue, key=lambda node: node.cost)
        self.queue.remove(min_cost)
        return min_cost

    def is_empty(self):
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)

class Environment():
    def __init__(self, number_rabbits):
        self.actions = [1, 2, 3, 4]
        self.start_state = ['L'] * number_rabbits + ['_'] + ['R'] * number_rabbits
        self.goal_state = ['R'] * number_rabbits + ['_'] + ['L'] * number_rabbits
        self.number_rabbits = number_rabbits

    def get_start_state(self):
        return self.start_state

    def get_next_states(self, state):
        space = state.index('_')
        new_states = []

        # Move right (L -> R)
        if space != len(state) - 1 and state[space + 1] == 'R':
            new_state = state[:]
            new_state[space], new_state[space + 1] = new_state[space + 1], new_state[space]
            new_states.append(new_state)

        # Move left (R -> L)
        if space != 0 and state[space - 1] == 'L':
            new_state = state[:]
            new_state[space], new_state[space - 1] = new_state[space - 1], new_state[space]
            new_states.append(new_state)

        # Hop over 1 position left
        if space - 2 >= 0 and state[space - 2] == 'L':
            new_state = state[:]
            new_state[space], new_state[space - 2] = new_state[space - 2], new_state[space]
            new_states.append(new_state)

        # Hop over 1 position right
        if space + 2 <= len(state) - 1 and state[space + 2] == 'R':
            new_state = state[:]
            new_state[space], new_state[space + 2] = new_state[space + 2], new_state[space]
            new_states.append(new_state)

        return new_states

    def reached_goal(self, state):
        return state == self.goal_state

# Initialize the environment and priority queue
env = Environment(number_rabbits=4)
explored = dict()
frontier = PriorityQueue()

init_state = env.get_start_state()
init_node = Node(parent=None, state=init_state, cost=0)
frontier.push(init_node)
goal_node = None

# Best-first search loop
while not frontier.is_empty():
    curr_node = frontier.pop()

    if curr_node in explored:
        continue

    explored[curr_node] = curr_node  # Mark node as explored

    if env.reached_goal(curr_node.state):
        goal_node = curr_node
        break

    next_states = env.get_next_states(curr_node.state)

    for state in next_states:
        node = Node(parent=curr_node, state=state, cost=curr_node.cost + 1)
        frontier.push(node)

# Backtrack from goal to start to get the solution path
node = goal_node
path = []
while node is not None:
    path.append(node)
    node = node.parent

# Print solution path
step = 1
for node in path[::-1]:
    print(f"Step: {step}")
    print(node)
    print()
    step += 1

# Step:  1
# ['L', 'L', 'L', 'L', '_', 'R', 'R', 'R', 'R']

# Step:  2
# ['L', 'L', 'L', 'L', 'R', '_', 'R', 'R', 'R']

# Step:  3
# ['L', 'L', 'L', '_', 'R', 'L', 'R', 'R', 'R']

# Step:  4
# ['L', 'L', '_', 'L', 'R', 'L', 'R', 'R', 'R']

# Step:  5
# ['L', 'L', 'R', 'L', '_', 'L', 'R', 'R', 'R']

# Step:  6
# ['L', 'L', 'R', 'L', 'R', 'L', '_', 'R', 'R']

# Step:  7
# ['L', 'L', 'R', 'L', 'R', 'L', 'R', '_', 'R']

# Step:  8
# ['L', 'L', 'R', 'L', 'R', '_', 'R', 'L', 'R']

# Step:  9
# ['L', 'L', 'R', '_', 'R', 'L', 'R', 'L', 'R']

# Step:  10
# ['L', '_', 'R', 'L', 'R', 'L', 'R', 'L', 'R']

# Step:  11
# ['_', 'L', 'R', 'L', 'R', 'L', 'R', 'L', 'R']

# Step:  12
# ['R', 'L', '_', 'L', 'R', 'L', 'R', 'L', 'R']

# Step:  13
# ['R', 'L', 'R', 'L', '_', 'L', 'R', 'L', 'R']

# Step:  14
# ['R', 'L', 'R', 'L', 'R', 'L', '_', 'L', 'R']

# Step:  15
# ['R', 'L', 'R', 'L', 'R', 'L', 'R', 'L', '_']

# Step:  16
# ['R', 'L', 'R', 'L', 'R', 'L', 'R', '_', 'L']

# Step:  17
# ['R', 'L', 'R', 'L', 'R', '_', 'R', 'L', 'L']

# Step:  18
# ['R', 'L', 'R', '_', 'R', 'L', 'R', 'L', 'L']

# Step:  19
# ['R', '_', 'R', 'L', 'R', 'L', 'R', 'L', 'L']

# Step:  20
# ['R', 'R', '_', 'L', 'R', 'L', 'R', 'L', 'L']

# Step:  21
# ['R', 'R', 'R', 'L', '_', 'L', 'R', 'L', 'L']

# Step:  22
# ['R', 'R', 'R', 'L', 'R', 'L', '_', 'L', 'L']

# Step:  23
# ['R', 'R', 'R', 'L', 'R', '_', 'L', 'L', 'L']

# Step:  24
# ['R', 'R', 'R', '_', 'R', 'L', 'L', 'L', 'L']

# Step:  25
# ['R', 'R', 'R', 'R', '_', 'L', 'L', 'L', 'L']
