#Rabbit Leap Problem (B)
#DFS Algorithm for Rabbit Leap:
#Initial state: (E, E, E, _, W, W, W).
#Goal state: (W, W, W, _, E, E, E).
#Actions: Rabbits can move 1 or 2 steps forward or jump over another rabbit.
def rabbit_leap_dfs():
    # Initial state: East-bound rabbits on the left, west-bound rabbits on the right
    start_state = ('E', 'E', 'E', '_', 'W', 'W', 'W')
    goal_state = ('W', 'W', 'W', '_', 'E', 'E', 'E')
    
    # Stack for DFS, each element is a tuple: (state, path to state)
    stack = [(start_state, [])]
    
    # Set to track visited states
    visited = set()
    visited.add(start_state)
    
    while stack:
        current_state, path = stack.pop()
        
        # Check if the goal is reached
        if current_state == goal_state:
            return path + [goal_state]  # Return the solution path
        
        empty_index = current_state.index('_')  # Find the empty spot
        
        # Explore valid moves (1 or 2 steps)
        for move in [-1, 1, -2, 2]:  # Possible movements left or right
            new_index = empty_index + move
            if 0 <= new_index < len(current_state):  # Ensure within bounds
                # Swap empty spot with rabbit
                new_state = list(current_state)
                new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                new_state = tuple(new_state)
                
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_state, path + [current_state]))
    
    return None  # No solution found

# Run the DFS algorithm
solution = rabbit_leap_dfs()

# Print the solution
if solution:
    for step in solution:
        print(step)
else:
    print("No solution found.")
