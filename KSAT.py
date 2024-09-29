from string import ascii_lowercase
import random
from itertools import combinations
import numpy as np

def creatproblem(n,k,m):
        positive_var = list(ascii_lowercase)[:n]
        negative_var = [var.upper() for var in positive_var]
        variables = positive_var + negative_var
        problem = []
        threshold = 10       
        i = 0
        comb = list(combinations(variables,k))
        
        while i<threshold:
            c = random.sample(comb,m)
            if c not in problem:
                problem.append(c)
                i += 1
        
        problems_new = []
        for c in problem:
            temp = []
            temp = [list(sub) for sub in c]
            problems_new.append(temp)
        return  variables,problems_new 
     
    
def random_assign(variables,n):
    litral = list(np.random.choice(2,n))
    negation = [abs(i-1) for i in litral]
    assign = litral + negation
    return dict(zip(variables,assign))
def heruistic(problem,assign):
    count = 0
    for sub in problem:       
        encode = [assign[val] for val in sub]
        count += any(encode)
    return count    
    def next_node(current):
     key = list(current.keys())
    key.sort()
    key = key[0:len(key)//2]
    successors = []
    for k in key:
        temp = current.copy()
        temp[k] = abs(temp[k]-1)
        temp[chr(ord(k)+32)] = abs(temp[chr(ord(k)+32)]-1)
        successors.append(temp)  
    

    
    return successors
    print(next_node({'a': 0, 'b': 0, 'c': 0, 'A': 1, 'B': 1, 'C': 1}))
    #[{'a': 1, 'b': 0, 'c': 0, 'A': 0, 'B': 1, 'C': 1}, {'a': 0, 'b': 1, 'c': 0, 'A': 1, 'B': 0, 'C': 1}, {'a': 0, 'b': 0, 'c': 1, 'A': 1, 'B': 1, 'C': 0}]
    def select_node(succs,problem):
      heruistic_val = []
    for i in succs:
        heruistic_val.append(heruistic(problem,i))
    index = heruistic_val.index(max(heruistic_val))
    return succs[index]
def check_goal_state(state,problem):
    count = 0
    for sub in problem:       
        encode = [state[val] for val in sub]
        count += any(encode)
    return len(problem) == count
def hill_climbing(current_state,problem,step):
    if step == 10000:
        print('halted at depth',step)
        return
    if check_goal_state(current_state,problem)==True:
        print(current_state,step)
        return 
    else:
        step += 1
    successor = new_node(current_state)
    new_node = select_node(successor,problem)
    hill_climbing(new_node,problem,step)

    n = 2
k = 3
m = 2
var,prob = creatproblem(n,k,m) 
print(var)
for i in prob:
    print(i)
   # ['a', 'b', 'A', 'B']
#[['a', 'b', 'B'], ['a', 'b', 'A']]
#[['a', 'b', 'B'], ['a', 'A', 'B']]
#[['a', 'A', 'B'], ['b', 'A', 'B']]
#[['a', 'A', 'B'], ['a', 'b', 'B']]
#[['b', 'A', 'B'], ['a', 'b', 'B']]
#[['b', 'A', 'B'], ['a', 'A', 'B']]
#[['a', 'b', 'A'], ['a', 'A', 'B']]
#[['a', 'b', 'A'], ['b', 'A', 'B']]
#[['b', 'A', 'B'], ['a', 'b', 'A']]
#[['a', 'b', 'B'], ['b', 'A', 'B']]
start_state = random_assign(var, n)
print(start_state,prob[0])
# start_state = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f':0,'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'F':1}
hill_climbing(start_state,prob[0],0)
print(check_goal_state({'a': 0, 'b': 1, 'c': 0, 'd': 1, 'A': 1, 'B': 0, 'C': 1, 'D': 0},prob[7]))
#Beam search
def heruistic(problem,assign):
    count = 0
    for sub in problem:       
        encode = [assign[val] for val in sub]
        count += any(encode)
    return count
def select_node_beam(succs,problem,beamwidth):
    heruistic_val = []
    beam_nodes = []
    for i in succs:
        heruistic_val.append(heruistic(problem,i))
    for i in range(beamwidth):
        index = heruistic_val.index(max(heruistic_val))
        beam_nodes.append(succs[index])
        succs.remove(succs[index])
        
    return beam_nodes
def check_goal_state(state,problem,beamwidth):
    count = 0
    for sub in problem:       
        encode = [state[val] for val in sub]
        count += any(encode)
    return len(problem) == count
def next_node_beam(succs):
    nextnode= []
    for current in succs:
        key = list(current.keys())
        key.sort()
        key = key[0:len(key)//2]
        successors = []
        for k in key:
            temp = current.copy()
            temp[k] = abs(temp[k]-1)
            temp[chr(ord(k)+32)] = abs(temp[chr(ord(k)+32)]-1)
            successors.append(temp)
            nextnode.append(temp)
        
    return nextnode
def beam_search(start,problem,step,beamwidth):
    if step == 10000:
        print('halted at depth',step)
        return
    for current_state in start:
        print(current_state)
        if check_goal_state(current_state,problem)==True:
            print(current_state,step)
            return 
    step +=1    
    successor = next_node_beam(start,problem,beamwidth)
    new_node = select_node_beam(successor,prob[0],beamwidth)
    beam_search(start,problem,step,beamwidth)
    n = 5
k = 3
m = 5
var,probl = creatproblem(n,k,m)
print(var)
for i in probl:
    print(i)
#['a', 'b', 'c', 'd', 'e', 'A', 'B', 'C', 'D', 'E']
#[['e', 'C', 'D'], ['b', 'B', 'C'], ['b', 'C', 'E'], ['A', 'B', 'C'], ['c', 'C', 'D']]
#[['d', 'A', 'B'], ['a', 'd', 'D'], ['a', 'A', 'C'], ['A', 'D', 'E'], ['b', 'A', 'D']]
#[['e', 'A', 'B'], ['b', 'B', 'C'], ['a', 'e', 'E'], ['d', 'e', 'E'], ['B', 'C', 'D']]
#[['a', 'b', 'E'], ['a', 'c', 'd'], ['d', 'A', 'D'], ['A', 'D', 'E'], ['c', 'e', 'B']]
#[['A', 'B', 'E'], ['A', 'C', 'E'], ['B', 'C', 'E'], ['d', 'A', 'B'], ['a', 'b', 'A']]
#[['b', 'C', 'D'], ['a', 'd', 'B'], ['a', 'e', 'C'], ['c', 'B', 'E'], ['d', 'B', 'C']]
#[['b', 'd', 'B'], ['a', 'C', 'D'], ['C', 'D', 'E'], ['e', 'D', 'E'], ['b', 'A', 'C']]
#[['b', 'e', 'D'], ['a', 'b', 'd'], ['b', 'd', 'C'], ['d', 'B', 'D'], ['a', 'c', 'B']]
#[['a', 'B', 'E'], ['a', 'C', 'D'], ['a', 'b', 'C'], ['b', 'e', 'E'], ['c', 'B', 'D']]
#[['b', 'e', 'D'], ['e', 'A', 'D'], ['b', 'c', 'D'], ['d', 'C', 'E'], ['d', 'D', 'E']]

start_state = random_assign(var,n)
print([start_state,start_state])
#[{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}, {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}]
#Beam width should not exceed number of variable
beam_search([start_state,start_state],prob[2],0,1)
#{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
#{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0} 0
#Variable-Neighborhood-Descent with 3 neighborhood functions
def heruistic(problem,assign):
    count = 0
    for sub in problem:       
        encode = [assign[val] for val in sub]
        count += any(encode)
    return count
def check_goal_state(state,problem):
    count = 0
    for sub in problem:       
        encode = [state[val] for val in sub]
        count += any(encode)
    return len(problem) == count
def select_node(succs,problem):
    heruistic_val = []
    for i in succs:
        heruistic_val.append(heruistic(problem,i))
    index = heruistic_val.index(max(heruistic_val))
    return succs[index]
def nghd1(current):
    key = list(current.keys())
    key.sort()
    key = key[0:len(key)//2]
    successors = []
    for k in key:
        temp = current.copy()
        temp[k] = abs(temp[k]-1)
        temp[chr(ord(k)+32)] = abs(temp[chr(ord(k)+32)]-1)
        successors.append(temp)   

    
    return successors
print(nghd1({'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}))
#[{'a': 0, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 1, 'B': 0, 'C': 0, 'D': 0, 'E': 0}, {'a': 1, 'b': 0, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 1, 'C': 0, 'D': 0, 'E': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 0, 'E': 0}, {'a': 1, 'b': 1, 'c': 1, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 1, 'E': 0}, {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 1}]
def nghd2(current):
    key = list(current.keys())
    key.sort()
    key = key[0:len(key)//2]
    successors = []
    for j in range(0,len(key)-1):
        for i in range(j,len(key)-1):
            
            temp = current.copy()
            temp[key[i]] = abs(temp[key[i]]-1)
            temp[key[i+1]] = abs(temp[key[i+1]]-1)
            temp[chr(ord(key[i])+32)] = abs(temp[chr(ord(key[i])+32)]-1)
            temp[chr(ord(key[i+1])+32)] = abs(temp[chr(ord(key[i+1])+32)]-1)
            successors.append(temp)   

    
    return successors
print(nghd2({'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}))
#[{'a': 0, 'b': 0, 'c': 1, 'd': 1, 'e': 1, 'A': 1, 'B': 1, 'C': 0, 'D': 0, 'E': 0}, {'a': 1, 'b': 0, 'c': 0, 'd': 1, 'e': 1, 'A': 0, 'B': 1, 'C': 1, 'D': 0, 'E': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 0}, {'a': 1, 'b': 1, 'c': 1, 'd': 0, 'e': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 1, 'E': 1}, {'a': 1, 'b': 0, 'c': 0, 'd': 1, 'e': 1, 'A': 0, 'B': 1, 'C': 1, 'D': 0, 'E': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 0}, {'a': 1, 'b': 1, 'c': 1, 'd': 0, 'e': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 1, 'E': 1}, {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 0}, {'a': 1, 'b': 1, 'c': 1, 'd': 0, 'e': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 1, 'E': 1}, {'a': 1, 'b': 1, 'c': 1, 'd': 0, 'e': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 1, 'E': 1}]
def nghd3(current):
    key = list(current.keys())
    key.sort()
    key = key[0:len(key)//2]
    successors = []
    for j in range(0,len(key)-2):
        for k in range(j,len(key)-2):
            for i in range(k,len(key)-2):               
            
                temp = current.copy()
                temp[key[i]] = abs(temp[key[i]]-1)
                temp[key[i+1]] = abs(temp[key[i+1]]-1)
                temp[chr(ord(key[i])+32)] = abs(temp[chr(ord(key[i])+32)]-1)
                temp[chr(ord(key[i+1])+32)] = abs(temp[chr(ord(key[i+1])+32)]-1)
                successors.append(temp)   

    
    return successors
print(nghd3({'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}))
#[{'a': 0, 'b': 0, 'c': 1, 'd': 1, 'e': 1, 'A': 1, 'B': 1, 'C': 0, 'D': 0, 'E': 0}, {'a': 1, 'b': 0, 'c': 0, 'd': 1, 'e': 1, 'A': 0, 'B': 1, 'C': 1, 'D': 0, 'E': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 0}, {'a': 1, 'b': 0, 'c': 0, 'd': 1, 'e': 1, 'A': 0, 'B': 1, 'C': 1, 'D': 0, 'E': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 0}, {'a': 1, 'b': 0, 'c': 0, 'd': 1, 'e': 1, 'A': 0, 'B': 1, 'C': 1, 'D': 0, 'E': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 1, 'A': 0, 'B': 0, 'C': 1, 'D': 1, 'E': 0}]
def Variable_Neighborhood1(current_state,problem,step):
    if step == 10000:
        print('halted at depth',step)
        return
    if check_goal_state(current_state,problem)==True:
        return current_state
        
    else:
        step += 1
        successor = new_node(current_state)
        new_node = nghd1(successor,problem)
        Variable_Neighborhood1(new_node,problem,step)
def Variable_Neighborhood2(current_state,problem,step):
    if step == 10000:
        print('halted at depth',step)
        return
    if check_goal_state(current_state,problem)==True:
        return current_state
         
    else:
        step += 1
        successor = new_node(current_state)
        new_node = nghd2(successor,problem)
        Variable_Neighborhood1(new_node,problem,step)
def Variable_Neighborhood3(current_state,problem,step):
    if step == 10000:
        print('halted at depth',step)
        return
    if check_goal_state(current_state,problem)==True:
        print(current_state,step)
        return 
    else:
        step += 1
        successor = new_node(current_state)
        new_node = nghd3(successor,problem)
        Variable_Neighborhood1(new_node,problem,step)
n = 5
k = 3
m = 5
var,probl = creatproblem(n,k,m)
print(var)
for i in probl:
    print(i)
   # ['a', 'b', 'c', 'd', 'e', 'A', 'B', 'C', 'D', 'E']
#[['c', 'd', 'C'], ['d', 'D', 'E'], ['c', 'e', 'A'], ['a', 'B', 'C'], ['c', 'C', 'D']]
#[['d', 'B', 'C'], ['c', 'd', 'e'], ['a', 'e', 'E'], ['A', 'C', 'E'], ['b', 'd', 'C']]
#[['A', 'D', 'E'], ['a', 'b', 'D'], ['a', 'B', 'C'], ['b', 'd', 'e'], ['a', 'c', 'D']]
#[['a', 'C', 'D'], ['c', 'e', 'A'], ['b', 'd', 'e'], ['B', 'C', 'D'], ['a', 'e', 'C']]
#[['b', 'B', 'D'], ['b', 'c', 'D'], ['a', 'B', 'E'], ['a', 'b', 'd'], ['A', 'C', 'D']]
#[['a', 'd', 'D'], ['a', 'A', 'D'], ['A', 'B', 'D'], ['a', 'b', 'c'], ['c', 'A', 'E']]
#[['b', 'C', 'E'], ['b', 'C', 'D'], ['c', 'B', 'C'], ['c', 'd', 'E'], ['a', 'e', 'E']]
#[['a', 'e', 'C'], ['a', 'd', 'C'], ['b', 'c', 'B'], ['a', 'c', 'D'], ['c', 'A', 'E']]
#[['a', 'c', 'B'], ['b', 'e', 'B'], ['d', 'e', 'E'], ['a', 'd', 'B'], ['a', 'A', 'D']]
#[['a', 'd', 'E'], ['A', 'B', 'E'], ['c', 'A', 'E'], ['d', 'e', 'C'], ['a', 'A', 'C']]
start_state = random_assign(var,n)
print([start_state,start_state])
#[{'a': 0, 'b': 0, 'c': 0, 'd': 1, 'e': 1, 'A': 1, 'B': 1, 'C': 1, 'D': 0, 'E': 0}, {'a': 0, 'b': 0, 'c': 0, 'd': 1, 'e': 1, 'A': 1, 'B': 1, 'C': 1, 'D': 0, 'E': 0}]
var1 = start_state
var2 = Variable_Neighborhood1(var1,prob[0],0)
var3 = Variable_Neighborhood2(var2,prob[0],0)
Variable_Neighborhood1(var3,prob[0],0)
#{'a': 0, 'b': 0, 'c': 0, 'd': 1, 'e': 1, 'A': 1, 'B': 1, 'C': 1, 'D': 0, 'E': 0} 0