# Basic searching algorithms
from util import Stack, Queue, PriorityQueueWithFunction, PriorityQueue
import numpy as np
import math


# Class for each node in the grid
class Node:
    def __init__(self, row, col, cost, parent, goal):
        self.row = row        # coordinate
        self.col = col        # coordinate
        self.cost = cost      # total cost (depend on the algorithm)
        self.goal = goal      # Goal   
        self.parent = parent  # previous node


def neighbors(pos):
    # right, down, left, up
    return [[pos[0], pos[1] + 1], [pos[0] + 1, pos[1]], [pos[0], pos[1] - 1], [pos[0] - 1, pos[1]]]

def neighbour_valid(n,grid):
    # Function to check if cells are 0/1 and the cells lie within grid boundary 
    if( n[0] >= 0 and n[0] < len(grid) and
        n[1] >= 0 and n[1] < len(grid[0]) and
        grid[n[0]][n[1]] == 0):
        
        return True
    return False



def heuristic(type, node, goal):
    if type == 'm':
        # Manhattan distance (L1 norm)
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    elif type == 'e':
        # Euclidean distance (L2 norm)
        return math.sqrt((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2)
    elif type == 'd':
        # Diagonal distance (Chebyshev distance)
        return max(abs(node[0] - goal[0]), abs(node[1] - goal[1]))
    elif type == 'o':
        # Octile distance (8-connected grid)
        dx = abs(node[0] - goal[0])
        dy = abs(node[1] - goal[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
    else:
        raise ValueError("Invalid heuristic type: Use 'm' for Manhattan, 'e' for Euclidean, 'd' for Diagonal, or 'o' for Octile.")

def backtrack(start,goal,parent):
    path = []
    current = tuple(goal)
    while current != tuple(start):
        path.insert(0, list(current))  # Convert back to a list for the path
        current = parent[current]
    path.insert(0, start)  # Add the start node to the path
    return path

def traverse(currcell, visited, grid, open, parent, steps):
    for n in neighbors(currcell):
        n = tuple(n)  # Convert neighbor to a tuple
        if n not in visited and neighbour_valid(n, grid):
            steps += 1
            visited.append(n)
            open.push(n)
            parent[n] = currcell
    return steps,parent    


def bfs(grid, start, goal):
    '''Return a path found by BFS algorithm
       and the number of steps it takes to find it.

    arguments:
    grid - A nested list with datatype int. 0 represents free space while 1 is obstacle.
           e.g. a 3x3 2D map: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    start - The start node in the map. e.g. [0, 0]
    goal -  The goal node in the map. e.g. [2, 2]

    return:
    path -  A nested list that represents coordinates of each step (including start and goal node),
            with data type int. e.g. [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]].
            If no path exists return an empty list [].
    steps - Number of steps it takes to find the final solution,
            i.e. the number of nodes visited before finding a path (including start and goal node)
    '''

    path = []
    steps = 0
    found = False
    parent = {}
    parent[tuple(start)] = tuple(start)  # Convert start to a tuple
    fron = Queue()
    fron.push(tuple(start))
    visited = []


    while not fron.isEmpty():
        currcell = fron.pop()

        if currcell == tuple(goal):
            found = True
            break
        steps,parent = traverse(currcell, visited, grid, fron, parent, steps)
            
    if found:
        print(f"It takes {steps} steps to find a path using BFS")
        path = backtrack(start,goal,parent)
    else:
        print("No path found")

    return path, steps




def dfs(grid, start, goal):
    '''Return a path found by DFS alogirhm 
       and the number of steps it takes to find it.

    arguments:
    grid - A nested list with datatype int. 0 represents free space while 1 is obstacle.
           e.g. a 3x3 2D map: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    start - The start node in the map. e.g. [0, 0]
    goal -  The goal node in the map. e.g. [2, 2]

    return:
    path -  A nested list that represents coordinates of each step (including start and goal node), 
            with data type int. e.g. [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]. If no path exists return
            an empty list []
    steps - Number of steps it takes to find the final solution, 
            i.e. the number of nodes visited before finding a path (including start and goal node)

    '''
    path = []
    steps = 0
    found = False
    parent = {}
    parent[tuple(start)] = tuple(start)  # Convert start to a tuple
    bottom = Stack()
    bottom.push(tuple(start))
    visited = []
    

    while not bottom.isEmpty():
        currcell = bottom.pop()

        if currcell == tuple(goal):
            found = True
            break
        steps,parent = traverse(currcell, visited, grid, bottom, parent, steps)
            
    if found:
        print(f"It takes {steps} steps to find a path using DFS")
        path = backtrack(start,goal,parent)
    else:
        print("No path found")

    return path, steps


def astar(grid, start, goal):
    '''Return a path found by A* algorithm
       and the number of steps it takes to find it.

    arguments:
    grid - A nested list with datatype int. 0 represents free space while 1 is an obstacle.
           e.g. a 3x3 2D map: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    start - The start node in the map. e.g. (0, 0)
    goal -  The goal node in the map. e.g. (2, 2)

    return:
    path -  A nested list that represents coordinates of each step (including start and goal node),
            with data type int. e.g. [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]. If no path exists, return
            an empty list []
    steps - Number of steps it takes to find the final solution,
            i.e. the number of nodes visited before finding a path (including start and goal node)
    visited_cells - List of visited cells during the search

    '''
    path = []
    steps = 0
    found = False
    start = tuple(start)
    goal = tuple(goal)
    parent = {}  # Add a parent dictionary to store the parent of each node
    parent[start] = start  # Start is already a tuple
    visited_cells = []
    type = 'm'
    

    g_cost = {}
    f_cost = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            cell_tuple = (i, j)  # Convert cell coordinates to a tuple
            g_cost[cell_tuple] = float('inf')
            f_cost[cell_tuple] = float('inf')
    g_cost[start] = 0
    f_cost[start] = heuristic(type, start, goal)

    open_list = PriorityQueue()
    open_list.push(start, f_cost[start])

    while not open_list.isEmpty():
        steps += 1
        currcell = open_list.pop()

        if currcell == goal:
            found = True
            break

        visited_cells.append(currcell)

        for n in neighbors(currcell):
            n = tuple(n)  # Convert neighbor to a tuple
            if n not in visited_cells and neighbour_valid(n, grid):

                temp_g_cost = g_cost[currcell] + 1
                temp_f_cost = temp_g_cost + heuristic(type, n, goal)

                if temp_f_cost < f_cost[n]:
                    g_cost[n] = temp_g_cost
                    f_cost[n] = temp_f_cost

                    open_list.push(n, temp_f_cost)
                    parent[n] = currcell
                    visited_cells.append(n)

    if found:
        print(f"It takes {steps} steps to find a path using A*")
        path = backtrack(tuple(start), goal, parent)
    else:
        print("No path found")

    return path, steps

