# -*- coding: utf-8 -*-
'''
An instance of the n-puzzle game consists of a board holding n^2 − 1 distinct movable tiles, plus an empty space.
The tiles are numbers from the set {1, …, n^2 − 1}. For any such board, the empty space may be legally swapped
with any tile horizontally or vertically adjacent to it. In this assignment, we will represent the blank space with the number 0.

Given an initial state of the board, the combinatorial search problem is to find a sequence of moves that transitions
this state to the goal state; that is, the configuration with all tiles arranged in ascending order ⟨0, 1, …, n^2 − 1⟩.
The search space is the set of all possible states reachable from the initial state.

The blank space may be swapped with a component in one of the four directions {‘Up’, ‘Down’, ‘Left’, ‘Right’}, one move at a time.
The cost of moving from one configuration of the board to another is the same and equal to one.
Thus, the total cost of path is equal to the number of moves made from the initial state to the goal state.

Author: Apurva Dubey
Date: 29-Jan-2017
'''

#import resource
import sys
import time
import copy
import heapq

#,9,10,11,12,13,14,15]  # Goal state of the puzzle

PATH = {} # A dictionary to keep a track of parent-child nodes. Will be used eventually to find optimal path.

# Offset will eventually be used to calculate the position with which the position is to be swapped
offset = {'Right':1, 'Left':-1, 'Up':-3, 'Down':3}


def gen_legal_moves(n):
    '''
    Generate set of legal moves from a given position in the board (UDLR)
    '''
    legal_moves = {}
    
    for i in range(n):
        if i == 0:
            legal_moves[i] = ['Down','Right']            

        elif i == n**0.5-1:
            legal_moves[i] = ['Down','Left']

        elif i == n- n**0.5:
            legal_moves[i] = ['Up','Right']

        elif i == n-1:
            legal_moves[i] = ['Up','Left']
                    
        elif i > 0 and i < n**0.5-1:
            legal_moves[i] = ['Down','Left','Right']
            
        elif i > (n**0.5-1)*(n**0.5) and i < n-1:
            legal_moves[i] = ['Up','Left','Right']
            
        elif i > 0 and i % (n**0.5) == 0 and i < (n**0.5-1)*(n**0.5):
            legal_moves[i] = ['Up','Down','Right']

        elif i > n**0.5 and (i + 1 - (n**0.5)) % (n**0.5) == 0 and i < n-1:
            legal_moves[i] = ['Up','Down','Left']

        else: legal_moves[i] = ['Up','Down','Left','Right']

    return legal_moves

def gen_coord(n):
    '''
    Generate coordinates of points on the board, used later for forward heuristic
    '''
    
    list1 = [i for i in range(n)]
    list2 = [(x,y) for y in range(int(n**0.5)) for x in range(int(n**0.5))]

    coord = {k:v for (k,v) in zip(list1,list2)}
    return coord


class seq_gen():
    '''
    A simple sequence generator. This will be used to assign "name" to each successive node
    '''

    def __init__(self,in_val):
        self.val = in_val

    def next_in_seq(self):
        self.val = self.val+1
        return self.val


class node():
    '''
    To define each node in the search tree
    '''

    def __init__(self,in_name,in_parent,in_config,in_depth,in_cost):
        self.name = in_name
        self.parent = in_parent
        self.config = in_config
        self.depth = in_depth
        self.cost = in_cost

    def show(self):
        #return str(self.name) + ";" + str(self.parent) + ";" + str(self.config) + ";" + str(self.depth)
        return [(self.name), (self.parent), (self.config) , (self.depth), (self.cost)]

    def show2(self):
        print str(self.config)

            
class queue():
    '''
    Implementation of a simple queue, with queue and dequeue functions
    '''

    def __init__(self):
        self.q = []

    def show(self):
        print [i for i in self.q]
        
    def enqueue(self,x):
        self.q.append(x)
        
    def dequeue(self):
        dq = self.q.pop(0)
        return dq

    def is_empty(self):
        if len(self.q) == 0:
            return True
        else:
            return False

    def length(self):
        return len(self.q)


class stack():
    '''
    Implementation of a simple stack, with push and pop functions
    '''

    def __init__(self):
        self.t = []

    def show(self):
        print [i.show() for i in self.t]
        
    def push(self,x):
        self.t.append(x)
        
    def pop(self):
        p = self.t.pop()
        return p

    def is_empty(self):
        if len(self.t) == 0:
            return True
        else:
            return False

    def length(self):
        return len(self.t)

    
def find_pos_0(in_list):
    '''
    Helper to find_successors functions
    '''  
    return in_list.index(0)

def find_successors(in_node,algo):
    '''
    This functions finds successors of each node and returns them as a list
    '''

    parent_name = in_node.name
    parent_depth = in_node.depth
    parent_cost = in_node.cost
    
    successors = []
    pos_0 = find_pos_0(in_node.config)

    if algo in ["bfs","best_first","astar"]:
        moves = legal_moves[pos_0]
    elif algo in ["dfs","id_astar"]:
        moves = [legal_moves[pos_0][i] for i in range(len(legal_moves[pos_0])-1,-1,-1)]
    else:
        print "Error"
    
    for lm in moves:

        # make a deep copy of the parent configuration
        successor = copy.deepcopy(in_node.config)

        # swap positions
        tmp = successor[pos_0 + offset[lm]]
        successor[pos_0 + offset[lm]] = 0
        successor[pos_0] = tmp

        # get name for the child
        child_seq = seq.next_in_seq()

        # create child node
        child_node = node(child_seq,parent_name,successor,parent_depth+1,parent_cost+1)

        # add parent-child relationship to the PATH
        PATH[child_seq]=(parent_name,lm)
            
        successors.append(child_node)
            
    return successors


def find_path(node_name):
    '''
    Once the goal state has been found, this function will return the optimal path to the goal
    '''
        
    if PATH[node_name][0] == 0:
        #return str(node_name) + " <--" + str(PATH[node_name][1]) + "--" + "0"
        return (PATH[node_name][1])
    else:
        #return str(node_name) + " <--" + str(PATH[node_name][1]) + "--" + str(find_path(PATH[node_name][0]))
        return  find_path(PATH[node_name][0]) + ">" + PATH[node_name][1]


def manhat_dist(i,j):
    '''
    returns manhattan distance between 2 points
    '''
    return abs(coord[i][0] - coord[j][0])+abs(coord[i][1] - coord[j][1])

    
def fwd_cost(config):
    '''
    calculates forward cost from current state to goal state
    '''
    #print [manhat_dist(config.index(n),n) for n in range(0,len(config))]
    return sum([manhat_dist(config.index(n),n) for n in range(0,len(config))])


def bfs(Q):
    '''
    Breadth-First Search implementation
    '''

    S = {} # Closed set, to keep a track of seen nodes (includes both the ones at fringe and explored earlier)
    nodes_expanded = 0
    
    while Q.is_empty() == False:
        current = Q.dequeue()
        
        if nodes_expanded == 0:
            S[tuple(current.config)]=1
            max_fringe_size = -1
            max_search_depth = -1

        if current.config ==  GOAL:
            #print "Success"
            #print current.show()
            break
        else:
            #print "Expanding node: ", current.show()
            nodes_expanded = nodes_expanded + 1          

            children = find_successors(current,"bfs")
            #print len(children)
            
            for child in children:              
                if S.get(tuple(child.config),-99) == -99:
                    S[tuple(child.config)]=1
                    Q.enqueue(child)

                    if child.depth > max_search_depth:
                        max_search_depth = child.depth

        if Q.length() > max_fringe_size:
            max_fringe_size = Q.length()
            
    print "path_to_goal:", find_path(current.name).split('>')
    print "cost_of_path:", current.cost
    print "nodes_expanded:", nodes_expanded
    print "fringe_size:", Q.length()
    print "max_fringe_size:", max_fringe_size
    print "search_depth:", current.depth
    print "max_search_depth:", max_search_depth
    print "running_time:", 1
    print "max_ram_usage:", 1


def dfs(T):
    '''
    Depth-First Search implementation
    '''
    S = {} # Closed set, to keep a track of seen nodes (includes both the ones at fringe and explored earlier)
    nodes_expanded = 0
    
    while T.is_empty() == False:
        current = T.pop()
        
        if nodes_expanded == 0:
            S[tuple(current.config)]=1
            max_fringe_size = -1
            max_search_depth = -1

        if current.config ==  GOAL:
            #print "Success"
            #print current.show()
            break
        else:
            #print "Expanding node: ", current.show()
            nodes_expanded = nodes_expanded + 1          

            children = find_successors(current,"dfs")
            #print len(children)
            
            for child in children:              
                if S.get(tuple(child.config),-99) == -99:
                    S[tuple(child.config)]=1
                    T.push(child)

                    if child.depth > max_search_depth:
                        max_search_depth = child.depth

        if T.length() > max_fringe_size:
            max_fringe_size = T.length()
            
    print "path_to_goal:", find_path(current.name).split('>')
    print "cost_of_path:", current.cost
    print "nodes_expanded:", nodes_expanded
    print "fringe_size:", T.length()
    print "max_fringe_size:", max_fringe_size
    print "search_depth:", current.depth
    print "max_search_depth:", max_search_depth
    print "running_time:", 1
    print "max_ram_usage:", 1


def best_first(BEST_FIRST_PQ):
    '''
    Best-First Search implementation
    '''
    S = {} # Closed set, to keep a track of seen nodes (includes both the ones at fringe and explored earlier)
    nodes_expanded = 0
    
    while BEST_FIRST_PQ:
        current = heapq.heappop(BEST_FIRST_PQ)[1]
                
        if nodes_expanded == 0:
            S[tuple(current.config)]=1
            max_fringe_size = -1
            max_search_depth = -1

        if current.config ==  GOAL:
            #print "Success"
            #print current.show()
            break
        else:
            #print "Expanding node: ", current.show()
            nodes_expanded = nodes_expanded + 1          

            children = find_successors(current,"best_first")
            #print len(children)
            
            for child in children:              
                if S.get(tuple(child.config),-99) == -99:
                    S[tuple(child.config)]=1
                    heapq.heappush(BEST_FIRST_PQ, (fwd_cost(child.config),child))

                    if child.depth > max_search_depth:
                        max_search_depth = child.depth

        if len(BEST_FIRST_PQ) > max_fringe_size:
            max_fringe_size = len(BEST_FIRST_PQ)
            
    print "path_to_goal:", find_path(current.name).split('>')
    print "cost_of_path:", current.cost
    print "nodes_expanded:", nodes_expanded
    print "fringe_size:", len(BEST_FIRST_PQ)
    print "max_fringe_size:", max_fringe_size
    print "search_depth:", current.depth
    print "max_search_depth:", max_search_depth
    print "running_time:", 1
    print "max_ram_usage:", 1


def astar(ASTAR_PQ):
    '''
    AStar Search implementation
    '''
    S = {} # Closed set, to keep a track of seen nodes (includes both the ones at fringe and explored earlier)
    nodes_expanded = 0
    
    while ASTAR_PQ:
        current = heapq.heappop(ASTAR_PQ)[1]
                
        if nodes_expanded == 0:
            S[tuple(current.config)]=1
            max_fringe_size = -1
            max_search_depth = -1

        if current.config ==  GOAL:
            #print "Success"
            #print current.show()
            break
        else:
            #print "Expanding node: ", current.show()
            nodes_expanded = nodes_expanded + 1
            print nodes_expanded

            children = find_successors(current,"astar")
            #print len(children)
            
            for child in children:              
                if S.get(tuple(child.config),-99) == -99:
                    S[tuple(child.config)]=1
                    heapq.heappush(ASTAR_PQ, (fwd_cost(child.config)+child.cost,child))

                    if child.depth > max_search_depth:
                        max_search_depth = child.depth

        if len(ASTAR_PQ) > max_fringe_size:
            max_fringe_size = len(ASTAR_PQ)
            
    print "path_to_goal:", find_path(current.name).split('>')
    print "cost_of_path:", current.cost
    print "nodes_expanded:", nodes_expanded
    print "fringe_size:", len(ASTAR_PQ)
    print "max_fringe_size:", max_fringe_size
    print "search_depth:", current.depth
    print "max_search_depth:", max_search_depth
    print "running_time:", 1
    print "max_ram_usage:", 1


def id_astar(root):
    '''
    Iterating Deepening using A Star heuristic
    '''
    IDA_COST = {}
    IDA_COST_USED = []
    found = 0

    IDA_COST[fwd_cost(root.config)+root.cost] = 1

    i = 0
    while found == 0:
        cost_bound = min([c for c in IDA_COST.keys() if c not in IDA_COST_USED])

        found = id_astar_search(root,cost_bound,IDA_COST)
        IDA_COST_USED.append(cost_bound)


def id_astar_search(root,cost_bound,IDA_COST):
    '''
    Iterating Deepening using A Star heuristic
    '''
    T = stack()
    T.push(root)
    
    S = {} # Closed set, to keep a track of seen nodes (includes both the ones at fringe and explored earlier)
    nodes_expanded = 0

    found = 0
    
    while T.is_empty() == False:
        current = T.pop()
        
        if nodes_expanded == 0:
            S[tuple(current.config)]=1
            max_fringe_size = -1
            max_search_depth = -1

        if current.config ==  GOAL:
            found = 1
            #print "Success"
            #print current.show()
            break
        else:
            #print "Expanding node: ", current.show()
            nodes_expanded = nodes_expanded + 1          

            if fwd_cost(current.config)+current.cost <= cost_bound:
                children = find_successors(current,"id_astar")
                #print len(children)
                
                for child in children:              
                    if S.get(tuple(child.config),-99) == -99:
                        S[tuple(child.config)]=1
                        T.push(child)
                        if fwd_cost(child.config)+child.cost > cost_bound:
                            IDA_COST[fwd_cost(child.config)+child.cost] = 1

                        if child.depth > max_search_depth:
                            max_search_depth = child.depth

        if T.length() > max_fringe_size:
            max_fringe_size = T.length()

    if found == 1:
        print "path_to_goal:", find_path(current.name).split('>')
        print "cost_of_path:", current.cost
        print "nodes_expanded:", nodes_expanded
        print "fringe_size:", T.length()
        print "max_fringe_size:", max_fringe_size
        print "search_depth:", current.depth
        print "max_search_depth:", max_search_depth
        print "running_time:", 1
        print "max_ram_usage:", 1
    else:
        return found

if __name__=="__main__":

    algo = "ast" #sys.argv[1:][0]
    start = [3,2,5,6,4,1,7,0,8] #[int(i) for i in sys.argv[1:][1].split(",")]

    #algo = "bfs"
    #start = [7,2,4,5,0,6,8,3,1] #[8,4,1,2,9,5,6,3,12,10,14,7,0,13,15,11]
    #start = [1,2,5,3,4,0,6,7,8]
    
    seq = seq_gen(0)
    legal_moves = gen_legal_moves(len(start))
    coord = gen_coord(len(start))
    GOAL = [i for i in range(0,len(start))]

    print GOAL

    print coord
    
    Q = queue()
    T = stack()
    BEST_FIRST_PQ = []
    ASTAR_PQ = []
 
    root = node(seq.val,None,start,0,0)
    #root = node(seq.val,None,[3,0,1,7,4,6,5,2,8],0)
    
    Q.enqueue(root)
    T.push(root)
    heapq.heappush(BEST_FIRST_PQ, (fwd_cost(start),root))
    heapq.heappush(ASTAR_PQ, (fwd_cost(start)+0,root))

    if algo == "bfs":
        bfs(Q) # Solve using BFS
    elif algo == "dfs":
        dfs(T) # Solve using DFS
    elif algo == "ast":
        astar(ASTAR_PQ) # Solve using Astar
    elif algo =="ida": 
        id_astar(root) # Solve using ID AStar
    elif algo == "bstf":
        best_first(BEST_FIRST_PQ)# Solve using best first
    else:
        print "Error: algotirhtm not found"


    #print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss    
    

    
    

    
    

    
    


