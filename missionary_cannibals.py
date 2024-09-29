import numpy as np

class Node:
    def __init__(self, parent, state, cost):
        self.parent = parent
        self.state = state
        self.cost = cost

    def __hash__(self):
        x = self.state.flatten()
        x = [str(i) for i in x]
        return hash(''.join(x))

    def __str__(self):
        return str(self.state)

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

    def __ne__(self, other):
        return not np.array_equal(self.state, other.state)

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, node):
        self.queue.append(node)

    def pop(self):
        next_state = None
        state_cost = float('inf')
        index = -1

        for i in range(len(self.queue)):
            if self.queue[i].cost < state_cost:
                state_cost = self.queue[i].cost
                index = i

        return self.queue.pop(index)

    def is_empty(self):
        return len(self.queue) == 0

    def __str__(self):
        l = []
        for i in self.queue:
            l.append(i.state)

        return str(l)

    def __len__(self):
        return len(self.queue)

class Environment:
    def __init__(self, start_state=None, goal_state=None):
        self.actions = [1, 2, 3, 4, 5]  # 1 - M, 2 - C, 3 - MM, 4 - CC, 5 - CM 
        self.start_state = start_state
        self.goal_state = goal_state

    def get_start_state(self):
        return self.start_state

    def get_next_states(self, state):
        shore = 0
        if state[1][2] == 1:
            shore = 1

        new_states = []
        not_shore = 1 - shore  # opposite shore

        # Action 1: Move 1 missionary
        if state[shore][0] - 1 >= 0 and (state[shore][0] - 1 == 0 or state[shore][0] - 1 >= state[shore][1]):
            new_state = state.copy()
            new_state[shore][0] -= 1
            new_state[shore][2] = 0
            new_state[not_shore][0] += 1
            new_state[not_shore][2] = 1
            new_states.append(new_state)

        # Action 2: Move 1 cannibal
        if state[shore][1] - 1 >= 0 and (state[not_shore][1] + 1 <= state[not_shore][0] or state[not_shore][0] == 0):
            new_state = state.copy()
            new_state[shore][1] -= 1
            new_state[shore][2] = 0
            new_state[not_shore][1] += 1
            new_state[not_shore][2] = 1
            new_states.append(new_state)

        # Action 3: Move 2 missionaries
        if state[shore][0] - 2 >= 0 and (state[shore][0] - 2 == 0 or state[shore][0] - 2 >= state[shore][1]):
            new_state = state.copy()
            new_state[shore][0] -= 2
            new_state[shore][2] = 0
            new_state[not_shore][0] += 2
            new_state[not_shore][2] = 1
            new_states.append(new_state)

        # Action 4: Move 2 cannibals
        if state[shore][1] - 2 >= 0 and (state[not_shore][1] + 2 <= state[not_shore][0] or state[not_shore][0] == 0):
            new_state = state.copy()
            new_state[shore][1] -= 2
            new_state[shore][2] = 0
            new_state[not_shore][1] += 2
            new_state[not_shore][2] = 1
            new_states.append(new_state)

        # Action 5: Move 1 missionary and 1 cannibal
        if state[shore][0] - 1 >= 0 and state[shore][1] - 1 >= 0:
            new_state = state.copy()
            new_state[shore][0] -= 1
            new_state[shore][1] -= 1
            new_state[shore][2] = 0
            new_state[not_shore][0] += 1
            new_state[not_shore][1] += 1
            new_state[not_shore][2] = 1
            new_states.append(new_state)

        return new_states

    def reached_goal(self, state):
        return np.array_equal(state, self.goal_state)

# Setup the problem
start_state = np.array([[3, 3, 1], [0, 0, 0]])  # 3 missionaries, 3 cannibals on shore 1, boat on shore 1
goal_state = np.array([[0, 0, 0], [3, 3, 1]])   # Goal: move all to shore 2
env = Environment(start_state, goal_state)

# Initialize search
explored = dict()
frontier = PriorityQueue()
init_state = env.get_start_state()
init_node = Node(parent=None, state=init_state, cost=0)
frontier.push(init_node)
goal_node = None

# Perform the search
while not frontier.is_empty():
    curr_node = frontier.pop()
    if hash(curr_node) in explored:
        continue
    explored[hash(curr_node)] = curr_node

    if env.reached_goal(curr_node.state):
        print("Goal Found")
        goal_node = curr_node
        break

    next_states = env.get_next_states(curr_node.state)
    for state in next_states:
        node = Node(parent=curr_node, state=state, cost=curr_node.cost + 1)
        frontier.push(node)

# Trace the solution path
if goal_node:
    node = goal_node
    l = []
    while node is not None:
        l.append(node)
        node = node.parent

    step = 1
    for node in l[::-1]:
        print(f"Step {step}:")
        print(node)
        print()
        step += 1

#Goal Found
#Step 1:
#[[3 3 1]
 #[0 0 0]]

#Step 2:
#[[2 2 0]
 #[1 1 1]]

#Step 3:
#[[3 2 1]
 #[0 1 0]]

#Step 4:
#[[3 0 0]
 #[0 3 1]]

#Step 5:
#[[3 1 1]
 #[0 2 0]]

#Step 6:
#[[2 0 0]
 #[1 3 1]]

#Step 7:
#[[2 1 1]
 ##[1 2 0]]

#Step 8:
#[[1 0 0]
 #[2 3 1]]

#Step 9:
#[[1 1 1]
 #[2 2 0]]

#Step 10:
#[[0 0 0]
 #[3 3 1]]

