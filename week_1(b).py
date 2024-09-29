#Problem 2
#Rabbit Leap Problem (B)
def rabbit_leap_bfs():
    # Initial state: East-bound rabbits on the left, west-bound rabbits on the right
    start_state = ('E', 'E', 'E', '_', 'W', 'W', 'W')
    goal_state = ('W', 'W', 'W', '_', 'E', 'E', 'E')
    
    # Queue for BFS, each element is a tuple: (state, path to state)
    queue = deque([(start_state, [])])
    
    # Set to track visited states
    visited = set()
    visited.add(start_state)
    
    while queue:
        current_state, path = queue.popleft()
        
        # Check if goal is reached
        if current_state == goal_state:
            return path + [goal_state]  # Return the path including the goal
        
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
                    queue.append((new_state, path + [current_state]))
    
    return None  # No solution found

# Run the BFS algorithm
solution = rabbit_leap_bfs()

# Print the solution
if solution:
    for step in solution:
        print(step)
else:
    print("No solution found.")

