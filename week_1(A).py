#Problem 2
#Missionaries and Cannibals Problem (A)
from collections import deque

# BFS solution for Missionaries and Cannibals
def missionaries_cannibals_bfs():
    # Initial state: 3 missionaries, 3 cannibals, boat on the left
    start_state = (3, 3, 0)
    goal_state = (0, 0, 1)
    
    # Possible moves (Missionaries, Cannibals)
    moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    
    # Queue for BFS, each element is a tuple: (state, path to state)
    queue = deque([(start_state, [])])
    
    # Set to track visited states
    visited = set()
    visited.add(start_state)
    
    while queue:
        (missionaries_left, cannibals_left, boat_left), path = queue.popleft()
        
        # Check if goal is reached
        if (missionaries_left, cannibals_left, boat_left) == goal_state:
            return path + [(0, 0, 1)]  # Return the path including the goal
        
        # For each move, calculate the new state
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
                
                # Ensure constraints: missionaries >= cannibals on both sides or no missionaries
                if (new_missionaries_left == 0 or new_missionaries_left >= new_cannibals_left) and \
                   (missionaries_right == 0 or missionaries_right >= cannibals_right):
                    new_state = (new_missionaries_left, new_cannibals_left, new_boat_left)
                    
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, path + [(missionaries_left, cannibals_left, boat_left)]))
    
    return None  # No solution found

# Run the BFS algorithm
solution = missionaries_cannibals_bfs()

# Print the solution
if solution:
    for step in solution:
        print(step)
else:
    print("No solution found.")
