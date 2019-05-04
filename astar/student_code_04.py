#from collections import defaultdict
import math
import random
from helpers import Map, load_map, show_map
from queue import PriorityQueue

def euclid_dist(pos,goal):
    """
    Inputs are 2-element lists containing 2D coordinates
    Return euclidean distances
    """
    dist = math.sqrt(math.pow((pos[0]-goal[0]),2)+math.pow((pos[1]-goal[1]),2))
    return dist


def lowest_f(fScores,frontier,M,cameFrom,start):
    x = set(fScores.keys())
    y = x.intersection(frontier)
    
    camefrom_set = set(cameFrom.keys())
    #find node in frontier with lowest fScore
    
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
    
def reconstruct_path2(cameFrom,current,M,start,goal):
    path = []
    path.append(current)
    camefrom_keyset = set(cameFrom.keys())
    prev=current
    altpaths=[]
    while current in cameFrom.keys():
        prev = current
        current = cameFrom[current]
        if current == start:
            path.append(current)
            break
        current_neighbors=set(M.roads[current])
        current_neighbors.remove(path[-1])
        
        current_neighbors.remove(cameFrom[current])
        
        alt_nodes = current_neighbors.intersection(camefrom_keyset)
        if len(alt_nodes)>0:
            alt_node2=[]
            for each in alt_nodes:
                if cameFrom[each] in camefrom_keyset or cameFrom[each] is start:
                    alt_node2.append(each)
            
            for each in alt_node2:
                altpath = path[:]
                altpath.append(current)
                current_2 = each
                altpath.append(current_2)
                while current_2 in cameFrom.keys():
                    current_2 = cameFrom[current_2]
                    altpath.append(current_2)
                altpaths.append(altpath)            
        path.append(current)
        
    valid_altpaths=[]
    for each in altpaths:
        if each[0]==goal and each[-1]==start:
            valid_altpaths.append(each)
    valid_altpaths.append(path)
    costs=[]
    for each in valid_altpaths:
        total=0.0
        for i in range(len(each)-1):
            total += euclid_dist(M.intersections[each[i]],M.intersections[each[i+1]])
        costs.append(total)
    lowest = [costs[0],0]
    for j in range(len(costs)):
        if costs[j]<lowest[0]:
            lowest[0]=costs[j]
            lowest[1]=j
            
    return valid_altpaths[lowest[1]][::-1]
    

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
    frontier = PriorityQueue()
    frontier.put(start,0.0)
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
    gScores = {start:0.0} #first g score is 0
    fScores = {start:heur[start]} #f(start) = heuristic(start)
    
    current_node = start
    #it=0
    epoch=0
    while not frontier.empty():
        
        print("epoch:",epoch)
        epoch+=1
        print("current node",current_node)
        print("frontier",frontier)
        print("camefrom",cameFrom)
        print("fscores",fScores)
        
        current_node = frontier.get()
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
                fScores[each] = priority
                frontier.put(priority,each)
                if each in gScores:
                    if cost>gScores[each]:
                        continue
                gScores[each] = cost
                fScores[each] = priority
                
                #cost = euclid_dist(M.intersections[each],M.intersections[current_node])
                #Nodes[each].append([each,cost,current_node])
                
                #print(cameFrom)
                
                    
                cameFrom[each]= current_node
                
                    
        
        
        
    #show_map(M,start,goal,Traversed)
    return None