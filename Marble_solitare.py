#Node
#The Node class greates the graph node. It has the following values

#Parent Node
#State
#Cost
#It makes use of the following built in functions:

#__hash__ : This provides the hash value for every node, which is required for the hashset
#__eq__ : To check if 2 nodes are equal (Operator overload)
#__ne__ : To check if 2 nodes are not equal (Operator overload)
#__str__ : To get string representation of state in node

import numpy as np
class Node:
    def __init__(self, parent, state, pcost, hcost, action=None):
        
        self.parent = parent
        self.state = state
        self.action = action
        self.pcost = pcost
        self.hcost = hcost
        self.cost = pcost + hcost
    
    def __hash__(self):
        
        return hash(str(self.state.flatten()))
    
    def __str__(self):
        return str(self.state)
    
    def __eq__(self, other):
        
        return hash(''.join(self.state.flatten())) == hash(''.join(other.state.flatten())) 
    
    def __ne__(self, other):
        return hash(''.join(self.state.flatten())) != hash(''.join(other.state.flatten()))
   # PriorityQueue
#The Priority Queue is used to store the nodes along with the cost, and pop the node having the least cost for BFS

#It makes use of the following functions:

#1 push : Add node to queue
#2 pop : Pop node having least cost
#3 is_empty : To check if queue is empty
#4 __len__ : To get length of queue
 #5__str__ : To get string representation of queue
 
 class PriorityQueue():
    
    def __init__(self):
        self.queue = []
        self.hashes = {}
        
    def push(self, node):
        if hash(node) not in self.hashes:
            self.hashes[hash(node)] = 1
            self.queue.append(node)
    
    def pop(self):
        
        next_state = None
        state_cost = 10**18
        index = -1
        
        for i in range(len(self.queue)):
            
            if self.queue[i].cost<state_cost:
                state_cost = self.queue[i].cost
                index = i
        
        return self.queue.pop(index)
    
    def is_empty(self):
        
        return len(self.queue)==0
    
    def __str__(self):
        l = []
        for i in self.queue:
            l.append(i.state)
        
        return str(l)
    
    def __len__(self):
        return len(self.queue)
    
    # Environment
# The environment is what the agent plays in. It has the following entities:

# actions : The actions defined in the environment
# depth: the maximum depth of the solution
# goal_state : The goal state of the environment
# start_state : The start state generated at the depth

# It has the following functions:

# get_start_state : returns the start state
# reached_goal : returns goal_state
# get_next_states : Given current state, it returns all possible next states
# generate_start_state : Given goal state and depth d, performs d moves to generate a start state
class Environment():
    
    def __init__(self, start_state=None, goal_state=None):
        self.actions = [1,2,3,4] #1 - Up, 2 - Down, 3 - Right, 4 - Left
        if goal_state is None:
            self.goal_state = self.generate_goal_state()
        else:
            self.goal_state = goal_state
        if start_state is None:
            self.start_state = self.generate_start_state()
        else:
            self.start_state = start_state
    
    def generate_start_state(self):
        
        start = np.zeros((7,7))
        x = (0,1,5,6)
        y = (0,1,5,6)

        for i in x:
            for j in y:
                start[i][j] = -1;

        x = (2,3,4)
        y = range(7)

        for i in x:
            for j in y:
                start[i][j] = 1
                start[j][i] = 1
        start[3][3] = 0
        
        return start
    
    def generate_goal_state(self):
    
        goal = np.zeros((7,7))
        x = (0,1,5,6)
        y = (0,1,5,6)

        for i in x:
            for j in y:
                goal[i][j] = -1;

        x = (2,3,4)
        y = range(7)

        for i in x:
            for j in y:
                goal[i][j] = 0
                goal[j][i] = 0
        goal[3][3] = 1
        return goal

    def get_start_state(self):
        return self.start_state
    
    def get_goal_state(self):
        return self.goal_state
    
    def get_next_states(self, state):
        
        new_states = []
        spaces = []
        for i in range(7):
            for j in range(7):
                if state[i][j]==0:
                    spaces.append((i,j))
        
        for space in spaces:
            
            x, y = space
            #Move from top to bottom
            if x>1:
                if state[x-1][y]==1 and state[x-2][y]==1:
                     new_state = state.copy()

                new_state[x][y] = 1
                new_state[x-2][y] = 0
                new_state[x-1][y] = 0
                action = f'({x-2}, {y}) -> ({x}, {y})'
                new_states.append((new_state, action))
            #Move from bottom to top
            if x<5:
                if state[x+1][y]==1 and state[x+2][y]==1:
                    new_state = state.copy()
                    new_state[x][y] = 1
                    new_state[x+2][y] = 0
                    new_state[x+1][y] = 0
                    action = f'({x+2}, {y}) -> ({x}, {y})'
                    new_states.append((new_state, action))
            
            #Move from left to right
            if y>1:
                if state[x][y-1]==1 and state[x][y-2]==1:
                    new_state = state.copy()
                    new_state[x][y] = 1
                    new_state[x][y-2] = 0
                    new_state[x][y-1] = 0
                    action = f'({x}, {y-2}) -> ({x}, {y})'
                    new_states.append((new_state, action))
            
            if y<5:
                if state[x][y+1]==1 and state[x][y+2]==1:
                    new_state = state.copy()
                    new_state[x][y] = 1
                    new_state[x][y+2] = 0
                    new_state[x][y+1] = 0
                    action = f'({x}, {y+2}) -> ({x}, {y})'
                    new_states.append((new_state, action))
        
        return new_states
    
 def  reached_goal(self, state):
        
   for i in range(7):
            for j in range(7):
                if state[i,j] != self.goal_state[i,j]:
                    return False
                    
        
         return True
    # Agent
# The agent is the player who plays the game against the environment to win. It has the following entities:

# frontier : This is the priority queue used to store the nodes to be explored.
# explored : This is the dictionary which stores the explored nodes
# start_state : Stores the start state
# goal_state : Stores the goal state
# env : Stores the environment
# goal_node : Stores the goal node if found
# heuristic : Stores the heuristic function

# The agent has the following functions:

# run(): Is the function that explores the environment and finds the goal node. Uses the built-in heuristic function to get the path costs
# print_nodes(): To print the path from the start node to goal node

# A-star search
# Using both heuristic cost and path cost
from env import Environment
from priority_queue import * # type: ignore
import numpy as np
from time import time

class Agent:
    
    def __init__(self, env, heuristic):
        self.frontier = PriorityQueue()
        self.explored = dict()
        self.start_state = env.get_start_state()
        self.goal_state = env.get_goal_state()
        self.env = env
        self.goal_node = None
        self.heuristic = heuristic
    
    def run(self):
        init_node = Node(parent = None, state = self.start_state, pcost = 0, hcost = 0)
        self.frontier.push(init_node)
        start = time()
        while not self.frontier.is_empty():

            curr_node = self.frontier.pop()
            next_states = self.env.get_next_states(curr_node.state)

            if hash(curr_node) in self.explored:
                continue
                
            self.explored[hash(curr_node)] = curr_node

            if self.env.reached_goal(curr_node.state):
                print("Reached goal!")
                self.goal_node = curr_node
                break
            goal_state = self.env.get_goal_state()
            
            l = []
            for state in next_states:

                hcost = self.heuristic(state[0])
                node = Node(parent=curr_node, state=state[0], pcost=curr_node.pcost+1, hcost=hcost, action=state[1])
                self.frontier.push(node)

        end = time()
        print(end - start)
        return end-start
    
    def print_nodes(self):
        
        node = self.goal_node
        l = []
        while node is not None:
            l.append(node)
            node = node.parent

        step = 1
        for node in l[::-1]:
            print("Step: ",step)
            print(node.action)
            #print(node)
            step+=1
           # Heuristic 0
#This is a null heuristic, returns 0 for any state. Essentially uniform cost search.
def heuristic0(curr_state):
    return 0
#Heuristic 1
#This is the manhattan distance, it returns the sum of the horizontal and vertical distances of the all marble in current state from center.
def heuristic1(curr_state):
    cost = 0
    for i in range(7):
        for j in range(7):
            if curr_state[i][j]==1:
                cost += abs(i-3)+abs(j-3)
    
    return cost
#Heuristic 2
#This is the exponential distance, it returns the 2max(H,V), where H is the horizontal distance, and V is the vertical distance.
def heuristic2(curr_state):
    cost = 0
    for i in range(7):
        for j in range(7):
            if curr_state[i][j]==1:
                cost += 2**(max(abs(i-3),abs(j-3)))
    
    return cost
#### agent = Agent(Environment(), heuristic2)
t = 0
for i in range(10):
    agent = Agent(Environment(), heuristic2)
    t+=agent.run()
    
print("Average time", t/10)
print("Number of nodes explored:", len(agent.explored))
print("Number of nodes in frontier:", len(agent.frontier))
#Best First Search
#Using Only Heuristic (Heuristic 2 from above cells)
from env import Environment
from priority_queue import * # type: ignore
import numpy as np
from time import time

class Agent:
    
    def __init__(self, env, heuristic):
        self.frontier = PriorityQueue()
        self.explored = dict()
        self.start_state = env.get_start_state()
        self.goal_state = env.get_goal_state()
        self.env = env
        self.goal_node = None
        self.heuristic = heuristic
    
    def run(self):
        init_node = Node(parent = None, state = self.start_state, pcost = 0, hcost = 0)
        self.frontier.push(init_node)
        start = time()
        while not self.frontier.is_empty():

            curr_node = self.frontier.pop()
            next_states = self.env.get_next_states(curr_node.state)

            if hash(curr_node) in self.explored:
                continue
                
            self.explored[hash(curr_node)] = curr_node

            if self.env.reached_goal(curr_node.state):
                print("Reached goal!")
                self.goal_node = curr_node
                break
            goal_state = self.env.get_goal_state()

            l = []
            for state in next_states:
                hcost = self.heuristic(state[0])
                node = Node(parent=curr_node, state=state[0], pcost=0, hcost=hcost, action=state[1])
                self.frontier.push(node)
        
        end = time()
        print(end - start)
        return end-start
    
    def print_nodes(self):
        
        node = self.goal_node
        l = []
        while node is not None:
            l.append(node)
            node = node.parent

        step = 1
        for node in l[::-1]:
            print("Step: ",step)
            print(node.action)
            #print(node)
            step+=1
  
t = 0
for i in range(10):
    agent = Agent(Environment(), heuristic2)
    t+=agent.run()
    
print("Average time", t/10)
print("Number of nodes explored:", len(agent.explored))
print("Number of nodes in frontier:", len(agent.frontier))
#Using Heuristic 1
t = 0
for i in range(10):
    agent = Agent(Environment(), heuristic1)
    t+=agent.run()
    
print("Average time", t/10)
print(len(agent.explored))