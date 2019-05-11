#from collections import defaultdict
import math
import random
from helpers import Map, load_map, show_map

def euclid_dist(pos,goal):
    """
    Inputs are 2-element lists containing 2D coordinates
    Return euclidean distances
    """
    dist = math.sqrt(math.pow((pos[0]-goal[0]),2)+math.pow((pos[1]-goal[1]),2))
    return dist


def lowest_f(fScores,frontier):
    x = set(fScores.keys())
    y = x.intersection(frontier)
    
    #find node in frontier with lowest fScore
    print("intersect",y)
    lowest = random.choice(list(y)) #pick a node
    #need to update fscores after updating gscores 
    for node in frontier:
        if node in y: #avoid indexing error
            if fScores[node]<fScores[lowest]: 
                lowest = node        
    return lowest
            
        
def goalTest(goal,explored):
    '''
    Checks if goal node has been removed from the frontier and added to the explored list 
    '''
    return goal in explored

def reconstruct_path(cameFrom,current):
    path = []
    path.append(current)
    while current in cameFrom.keys():
        current = cameFrom[current]
        path.append(current)
    return path[::-1]
    
def shortest_path(M,start,goal):
    #print("shortest path called")
    '''
    Input map M is a map object
    M.intersections gives dictionary of intersection no. with corresponding coordinates on map
    M.roads is a list of list of the nodes [node,node,...] connected to each node M.roads[index]
    Start node 'start' is the start node for the algorithm
    Goal node is the node for the GoalTest, i.e the destination.
    Return the lowest cost path
    '''
    #Getting coordinates of Start and Goal
    goal_pos = M.intersections[goal]
    start_pos = M.intersections[start]
    
    #initialise frontier and explored sets
    frontier = set()
    frontier.add(start)
    explored = set()
    
    #calculate estimated distance from goal for each node using heuristics. h-score in f = g+h
    #using Euclidean distance here
    heur = {}
    for index in M.intersections:
        pos = M.intersections[index]
        heur[index] = euclid_dist(pos,goal_pos)
        #print('pos',index,'heur',heur[index])
        
    

    #Traverse, store the current nodes
    Traversed = []
    #store dictionaries for tracing back the paths from end
    cameFrom = {}
    
    #store score
    gScores = {start:0} #first g score is 0
    fScores = {start:heur[start]} #f(start) = heuristic(start)
    
    current_node = start
    #it=0
    epoch=0
    while len(frontier) > 0:
        current_node = lowest_f(fScores,frontier)
        frontier.remove(current_node)
        print("epoch:",epoch)
        epoch+=1
        print("current node",current_node)
        print("frontier",frontier)
        print("camefrom",cameFrom)
        print("fScore",fScores)
        
        
        Traversed.append(current_node)
        explored.add(current_node)
        if goalTest(goal,explored):
            path = reconstruct_path(cameFrom,current_node)
            show_map(M,start,goal,path)
            return path
            
        
        #add new items to frontier and add to Nodes
        for each in M.roads[current_node]: #neighbors of current node
            cost = gScores[current_node]+euclid_dist(M.intersections[each],M.intersections[current_node])
            if each not in explored:
                
                priority = cost + heur[each]
                frontier.add(each)
                fScores[each]=priority
                #cost = euclid_dist(M.intersections[each],M.intersections[current_node])
                #Nodes[each].append([each,cost,current_node])
                
                #print(cameFrom)
                
                if each in gScores:
                    if cost > gScores[each]:
                        continue
                        
                cameFrom[each]= current_node
                gScores[each] = cost
                #fScores[each] = gScores[each] + heur[each]
                
        print("fScore",fScores)
        print("frontier",frontier)
        
        
        
    #show_map(M,start,goal,Traversed)
    return None
    
    