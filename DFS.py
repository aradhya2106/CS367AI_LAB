#Missionaries and Cannibals Problem (A)
def missionaries_cannibals_dfs():
    start_state = (3, 3, 0)  # Initial state
    goal_state = (0, 0, 1)   # Goal state
    moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]  # Possible moves
    
    # Stack for DFS, each element is a tuple: (state, path to state)
    stack = [(start_state, [])]
    
    # Set to track visited states
    visited = set()
    visited.add(start_state)
    
    while stack:
        (missionaries_left, cannibals_left, boat_left), path = stack.pop()
        
        # Check if the goal is reached
        if (missionaries_left, cannibals_left, boat_left) == goal_state:
            return path + [(0, 0, 1)]  # Return the solution path
        
        # Explore all valid moves
        for missionaries_move, cannibals_move in moves:
            if boat_left == 0:  # Boat on the left side
                new_missionaries_left = missionaries_left - missionaries_move
                new_cannibals_left = cannibals_left - cannibals_move
                new_boat_left = 1
            else:  # Boat on the right side
                new_missionaries_left = missionaries_left + missionaries_move
                new_cannibals_left = cannibals_left + cannibals_move
                new_boat_left = 0
            
            # Check if new state is valid
            if 0 <= new_missionaries_left <= 3 and 0 <= new_cannibals_left <= 3:
                missionaries_right = 3 - new_missionaries_left
                cannibals_right = 3 - new_cannibals_left
                
                if (new_missionaries_left == 0 or new_missionaries_left >= new_cannibals_left) and \
                   (missionaries_right == 0 or missionaries_right >= cannibals_right):
                    new_state = (new_missionaries_left, new_cannibals_left, new_boat_left)
                    
                    if new_state not in visited:
                        visited.add(new_state)
                        stack.append((new_state, path + [(missionaries_left, cannibals_left, boat_left)]))
    
    return None  # No solution found

# Run the DFS algorithm
solution = missionaries_cannibals_dfs()

# Print the solution
if solution:
    for step in solution:
        print(step)
else:
    print("No solution found.")
#Start State: (3, 3, 0) — All missionaries and cannibals are on the left.
#Moves: Various combinations of missionaries and cannibals can cross the river.
#DFS: The algorithm explores one path deeply before backtracking if no solution is found in that path.
