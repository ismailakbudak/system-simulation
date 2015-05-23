# -*- coding: utf-8 -*-
# Node and graph implementation
# Developer
# Ismail AKBUDAK
# ismailakbudak.com

from matplotlib import pyplot as plt
import networkx as nx
import random
from collections import OrderedDict
import pprint
import math
import numpy as np
pp = pprint.PrettyPrinter(indent=4)

"""
Find coordinate region 
Args:
    X: float 
        x coodinate value
    Y: float
        y coodinate value        
Return:
    int region of x and y coordinates     
"""
def findIndex(X, Y):
    if X > 0 and Y > 0:
        index = 0
    elif X < 0 and Y > 0:
        index = 1
    elif X < 0 and Y < 0:
        index = 2
    else:
        index = 3
    return index

"""
Get distributions for graph node capacity
Args:
    None
Return:
    Array of Distribution class        
"""
def getDistributions():
    return [ 
        Distribution(3,0.6), 
        Distribution(3,0.6), 
        Distribution(3,0.6), 
        Distribution(3,0.6), 
        Distribution(3,0.6) ]

""" 
Normal Distrubution class
Args:  
    LOC: float 
        Median of distribution
    SCALE: float
        Standart divion of distribution
    SIZE: int or tuple of ints, optional
        Output shape
""" 
class Distribution(object):
    """docstring for Distribution"""
    def __init__(self, LOC=0.0, SCALE=1.0, SIZE=None):
        super(Distribution, self).__init__()
        self.LOC = LOC
        self.SCALE = SCALE
        self.SIZE = SIZE

""" 
Node position class
Args:  
    X: int 
        x coordinate
    Y: int 
        y coordinate
""" 
class Position(object):
    """docstring for Position"""
    def __init__(self, X, Y):
        super(Position, self).__init__()
        self.X = X
        self.Y = Y

""" 
Node class for graph structure 
Args: 
    ID: Integer unique id of node
    CAPACITY: Integer capacity of node
    X: Integer node x coordinate
    Y: Integer node y coordinate
""" 
class Node(object): 
    
    def __init__(self, ID, CAPACITY, X=0, Y=0):
        self.ID = ID
        self.CAPACITY = CAPACITY
        self.POSITION = Position(X,Y)
        self.VISITED = False
        self.NAME = 'N:%s-C:%s'%(str(ID),str(CAPACITY))
        self.SHORT_NAME = 'N:%s'%(str(ID))
        self.COORDINATOR = self
        self.neighbours={} 
        self.REGION = findIndex(X, Y)  
        self.log("node initialized..")
    
    def __repr__(self):
        return self.SHORT_NAME

    def __str__(self):
        return self.NAME

    """ 
    Add new node to neighbours
    Args:
        Node object
    Return: 
        Boolean result
        If added True otherwise False   
    """    
    def addNeighbour(self,node):
        if not(self.neighbours.has_key(node.ID)):
            self.neighbours[node.ID]=node
            node.neighbours[self.ID]=self
            self.log("neighbour added..")
            return True
        else:
            self.log("neighbour could not added..")
            self.log("ERROR: key '%s' is exist in '%s'"%(node.ID, self) )
            return False

    """ 
    Remove node from neighbours
    Args:
        Node object
    Return: 
        Boolean result
        If removed True otherwise False   
    """
    def removeNeighbour(self,node):
        if self.neighbours.has_key(node.ID):
            self.neighbours.pop(node.ID)
            node.neighbours.pop(self.ID)
            self.log("neighbour removed..")
            return True
        else:
            self.log("neighbour could not removed..")
            self.log("ERROR: key '%s' is not exist in '%s'"%(node.ID, self) )
            return False


    """ 
    Remove all neighbours
    Args:
        None
    Return: 
        Boolean result
        If removed True otherwise False   
    """         
    def remove(self):
        iterator = self.neighbours.copy()
        for node in iterator.values():
            if not(node.removeNeighbour(self)):
                return False
        self.log("removed all neighbours..")
        return True       

    def log(self, message):
        #print("NODE:: %s"%(message) ) 
        pass

""" 
Graph class
Args: 
    None
""" 
class Graph(object):

    def __init__(self):
        self.nodes={}
        self.positions={}
        self.lastID=0 
        self.traceElection=True
        self.traceLog=True 
        self.traceElectionVisual=True
        self.useRandomCapacity=True 
        self.distributions = getDistributions()
        self.log("Graph initialized..")  
            
    """ 
    Add new node to graph 
    Args: 
        node: new node that will add
    Return: 
        Boolean if added True otherwise False
    """ 
    def add(self, node):
        if not(self.nodes.has_key(node.ID)):
            self.nodes[node.ID]=node
            self.lastID += 1
            self.log("node added..")
            return True
        else:
            self.log("node could not added..")
            self.log("ERROR: key '%s' is exist"%(node.ID) )
            return False
    
    """ 
    Remove node from graph
    Args: 
        node: new node that will remove
    Return: 
        None
    """ 
    def remove(self, node):
        node.remove()
        self.nodes.pop(node.ID)
        self.log("node removed..")        
    
    """ 
    Remove all graph nodes 
    Args: 
        None
    Return: 
        None
    """ 
    def removeAll(self):
        self.nodes = {}
        self.positions = {}
        self.lastID=0 
        self.log("all nodes removed..")
    
    """ 
    Connect to nodes eachother
    Args: 
        node1: node object
        node2:  nodes object
    Return: 
        None
    """
    def link(self,node1,node2):
        if node1.addNeighbour(node2):
            self.log("nodes linked..")
            return True
        else:
            return False     
    
    """ 
    Unset graph nodes visited property
    Args: 
        None
    Return: 
        None
    """
    def removeVisitedProperty(self):
        for node in self.nodes.values():
            node.VISITED = False

    """ 
    Get unvisited node in graph
    Args:  
        None
    Return: 
        Node or None
    """
    def getNotVisitedNode(self):
        for node in self.nodes.values():
            if node.VISITED == False:
                return node
        return None                 

    """ 
    Find coordinators in graph for different region
    Args: 
        None
    Return: 
        None
    """        
    def findCoordinates(self):
        self.removeVisitedProperty()
        node = self.getNotVisitedNode()
        coordinator_list = []
        while node is not None:
            value = self.startElection(node)
            coordinator_list.append( value )
            node = self.getNotVisitedNode()
        
        if len(coordinator_list) > 0:
            self.draw_coordinator(coordinator_list ) 
        else:
            self.log('There is not any nodes')    
    """ 
    Start election algorithm on graph
    Args: 
        start: node object that is start point 
    Return: 
        None
    """
    def startElection(self,start):
        self.log_election("BEGIN election =============================")
        self.log_election("start node : "+ start.SHORT_NAME)
        self.log_election("END election =============================")
        graph = self.nodes
        visited = {}
        visited_index = {} 
        queue = [start] 
        while queue:
            vertex = queue.pop(0)  
            visited[vertex] = []
            visited_index[vertex.ID] = []
            vertex.VISITED = True 
            for node in  vertex.neighbours.values(): 
                if not(node.VISITED):
                    visited[vertex].append(node)
                    visited_index[vertex.ID].append(node.ID)
                    queue.append( node )  
                    node.VISITED = True

        self.log_pp( "Graph visit path", visited_index,  self.traceElection  ) 

        coordinator_candidates = self.findMaxArray(visited, start, [start])
        
        coordinator = self.findMax(visited, start, start)
        
        coordinator = random.choice(coordinator_candidates)
        self.log_election("====================================")
        self.log_election("First status for nodes coordinator")
        self.log_election("====================================")
        self.print_coordinator()
        self.informCoordinator(visited, start, coordinator)
        self.log_election("====================================")
        self.log_election("After inform coordinator to nodes ")
        self.log_election("====================================")
        self.print_coordinator()   
        #self.log_election("====================================")
        #self.log_election("One coordinator result: " + str(coordinator) )
        self.log_election("====================================")
        self.log_election("Election result : " + str(coordinator_candidates) )
        self.log_election("====================================")
        self.log_election("Coordinator : " + coordinator.SHORT_NAME )
        self.log_election("====================================")

        return { 'coordinator': coordinator, 'candidates': coordinator_candidates, 'start': start}
        
    """ 
    Print nodes coordinator
    Args:
        None  
    Return: 
        None
    """      
    def print_coordinator(self):
        for node in self.nodes.values():
            self.log_election(" %s -> %s " % (node.SHORT_NAME, node.COORDINATOR.SHORT_NAME) )    
        
    """ 
    Find nodes that has maximum capacity
    Args: 
        visited: graph find path
        start: start point node object 
        max: array of node that has maximum capacity
    Return: 
        Node objects array
    """        
    def findMaxArray(self,visited,start,max=None):   
        if len(visited[start]) == 0:
            if max[0].CAPACITY > start.CAPACITY:
                return max
            elif max[0].CAPACITY == start.CAPACITY:
                if start not in max:
                    max.append(start)
                return max            
            else:    
                return [start]
        if max[0].CAPACITY < start.CAPACITY:
                max = [start]         
        elif max[0].CAPACITY == start.CAPACITY:
            if start not in max:
                max.append(start) 
        for node in visited[start]:
            val = self.findMaxArray(visited,node, max) 
            if max[0].CAPACITY < val[0].CAPACITY:
                max = val         
            elif max[0].CAPACITY == val[0].CAPACITY:
                for node in val:
                    if node not in max:
                        max.append(node)               
        return max   

    """ 
    Find node that has maximum capacity
    Args: 
        visited: graph find path
        start: start point node object 
        max:  node that has maximum capacity
    Return: 
        Node object
    """    
    def findMax(self,visited,start,max=None):  
        if len(visited[start]) == 0:
            if max.CAPACITY > start.CAPACITY:
                return max
            elif max.CAPACITY == start.CAPACITY:
                vals = [max,start]
                return random.choice(vals)        
            else:    
                return start
        if max.CAPACITY < start.CAPACITY:
            max = start         
        elif max.CAPACITY == start.CAPACITY:
            vals = [max,start]
            max = random.choice(vals)  
        for node in visited[start]:
            val = self.findMax(visited,node, max) 
            if max.CAPACITY < val.CAPACITY:
                max = val         
            elif max.CAPACITY == val.CAPACITY:
                vals = [max,val]
                max = random.choice(vals)                 
        return max

    """ 
    Inform  coordinator to all nodes 
    Args: 
        visited: graph find path
        start: start point node object 
        coordinator:  node that is new coordinator
    Return: 
        Node object
    """
    def informCoordinator(self, visited, start, coordinator):
        if len(visited[start]) == 0:
            start.COORDINATOR = coordinator
            return True
        start.COORDINATOR = coordinator  
        for node in visited[start]:
            self.informCoordinator(visited,node, coordinator) 
        return True

    """ 
    Draw all nodes with CAPACITY property
    Args: 
        None
    Return: 
        None
    """
    def draw(self):
        self.log("graph is drawing..")
        colors = ["#EFDFBB","orange","lightgreen","lightblue","#FFD300","violet","yellow","#7CB9E8","#E1A95F", "#007FFF","#CCFF00","pink","cyan"]
        
        def find_color(node): 
            return colors[node.REGION] 

        def find_length(node, node_neighbour):
             return round( math.sqrt( math.pow((node.POSITION.X - node_neighbour.POSITION.X), 2) + math.pow((node.POSITION.Y - node_neighbour.POSITION.Y), 2)), 2)
        
        graph = nx.DiGraph()
        node_size = []
        for node in self.nodes.values():
            node_size.append(100*node.CAPACITY)    
            graph.add_node(node)
            for node_neighbour in node.neighbours.values():
                graph.add_edge(node, 
                                node_neighbour,
                                weight=find_length(node, node_neighbour), 
                                color=find_color(node_neighbour) )
        node_colors = map(find_color, graph.nodes())

        if len(self.nodes) > 1:
            edges,edge_colors = zip(*nx.get_edge_attributes(graph,'color').items()) 
        else:
            edges=[]
            edge_colors="yellow"    

        G=nx.grid_2d_graph(1,1)
        plt.subplot(111)     
        labels = nx.get_edge_attributes(graph,'weight')
        nx.draw_networkx_edge_labels(
            graph,
            self.positions,
            edge_labels=labels,  
            font_family='ubuntu', 
            edgelist=edges,
            edge_color=edge_colors
        )
        nx.draw(graph,
                self.positions,
                with_labels=True,
                font_size=8,
                node_size=1300,#node_size,
                font_family='ubuntu',
                font_color='red',
                node_color=node_colors, 
                edgelist=edges,
                edge_color=edge_colors, 
                width=0.4) 
        plt.axis('on')
        plt.grid('on')     
        plt.show()  

    """ 
    Draw coordinator and coordinator candidates
    Args: 
        coordinator_list: election results
    Return: 
        None
    """
    def draw_coordinator(self, coordinator_list):
        self.log("coordinator is drawing..")
        coordinator_colors = ["orange", "yellow"]  
        region_colors = ["lightgreen","lightblue","violet","#E1A95F", "#007FFF","#CCFF00"]  

        def find_coordinator_color(node):
            for value in coordinator_list:
                coordinator =  value['coordinator']
                coordinator_candidates = value['candidates']
                start = value['start']
                if node.ID == coordinator.ID:
                    return coordinator_colors[0]
                if node in coordinator_candidates:
                    return coordinator_colors[1] 
            return region_colors[node.REGION]

        def find_length(node, node_neighbour):
             return round( math.sqrt( math.pow((node.POSITION.X - node_neighbour.POSITION.X), 2) + math.pow((node.POSITION.Y - node_neighbour.POSITION.Y), 2)), 2)
        
        graph = nx.DiGraph()
        node_size = []
        for node in self.nodes.values():
            node_size.append(100*node.CAPACITY)  
            graph.add_node(node)
            for node_neighbour in node.neighbours.values():
                graph.add_edge( node, 
                                node_neighbour, 
                                weight=find_length(node, node_neighbour), 
                                coordinator_color=find_coordinator_color(node_neighbour) )
        node_coordinator_colors = map(find_coordinator_color, graph.nodes()) 
        coordinator_edges,coordinator_edge_colors = zip(*nx.get_edge_attributes(graph,'coordinator_color').items()) 
        
        G=nx.grid_2d_graph(1,1)
        plt.subplot(111)    
        labels = nx.get_edge_attributes(graph,'weight')
        nx.draw_networkx_edge_labels(
            graph,
            self.positions,
            edge_labels=labels,  
            font_family='ubuntu', 
            edgelist=coordinator_edges,
            edge_color=coordinator_edge_colors
        ) 
        nx.draw(graph,
                self.positions,
                with_labels=True,
                font_size=8,
                node_size=1300,#node_size,
                font_family='ubuntu',
                font_color='red',
                node_color=node_coordinator_colors, 
                edgelist=coordinator_edges,
                edge_color=coordinator_edge_colors, 
                width=0.4)

        node_lengths = [] 
        for value in coordinator_list:
            coordinator =  value['coordinator']
            candidates = value['candidates']
            start = value['start']

            self.log('Coordinator %s :'%(coordinator.SHORT_NAME))
            for candidate in candidates:
                # Compute shortest path lengths in the graph.
                shortest_length = nx.shortest_path_length(graph,source=candidate, weight='weight' )
                total = 0
                for l in shortest_length.values():
                    total += l
                node_lengths.append({ 'total': total, 'node': candidate, 'coordinator': coordinator })   
                self.log_pp('Shortest path length for %s :'%(candidate.SHORT_NAME), shortest_length , True ) 
                self.log('Total length : %s \n'%(str(total)))    
            # Compute shortest paths in the graph. 
            # returns 0 for target and source
            #shortest_path = nx.shortest_path(graph,source=coordinator, target=candidates[0], weight='weight' )          

            # Compute all shortest paths in the graph. 
            # returns same node for target and source
            #print([p for p in  nx.all_shortest_paths(graph,source=coordinator, target=candidates[0], weight='weight')]) 
            
            # Return the average shortest path length.
            #average_shortest_path_length = nx.average_shortest_path_length(graph, weight='weight' )
            
            # Compute shortest path between source and all other nodes reachable from source.   
            #single_source_shortest_path = nx.single_source_shortest_path(graph,source=coordinator)
            
            # Compute the shortest path lengths from source to all reachable nodes.   
            #single_source_shortest_path_length = nx.single_source_shortest_path_length(graph,source=coordinator)
            
            # Returns the shortest path from source to target in a weighted graph G.
            # returns same node for target and source
            #dijkstra_path = nx.dijkstra_path(graph, source=coordinator, target=candidates[0], weight='weight')
            
            # Returns the shortest path from source to target in a weighted graph G.
            # returns same node for target and source
            #dijkstra_path_length = nx.dijkstra_path_length(graph, source=coordinator, target=candidates[0], weight='weight')
            
            # Compute shortest path between source and all other reachable nodes for a weighted graph.
            #shortest_path = nx.single_source_dijkstra_path(graph, source=coordinator, weight='weight')
            
            # Compute the shortest path length between source and all other reachable nodes for a weighted graph.
            #shortest_length = nx.single_source_dijkstra_path_length(graph, source=coordinator, weight='weight')
            
            # Compute shortest paths between all nodes in a weighted graph.
            #shortest_length = nx.all_pairs_dijkstra_path(graph, weight='weight')
            
            # Compute shortest path lengths between all nodes in a weighted graph.
            #shortest_length = nx.all_pairs_dijkstra_path_length(graph, weight='weight')
            
            # Compute shortest paths and lengths in a weighted graph G.
            # returns same node for target and source
            #single_source_dijkstra = nx.single_source_dijkstra(graph, source=coordinator, target=candidates[0], weight='weight')

            # Compute shortest paths and lengths in a weighted graph G.
            # returns same node for target and source
            #shortest_length = nx.bidirectional_dijkstra(graph, source=coordinator, target=candidates[0], weight='weight')

            # Compute shortest paths and lengths in a weighted graph G.
            # returns same node for target and source
            #shortest_length = nx.bidirectional_dijkstra(graph, source=coordinator, target=candidates[0], weight='weight')
                
            # Compute shortest path lengths and predecessors on shortest paths in weighted graphs. 
            #bellman_ford = nx.bellman_ford(graph, source=coordinator, weight='weight')
                
        # Information Text
        x=10.0;y=11;i=1;flag=False;dist=1.2 
        for color in coordinator_colors:
            if color == coordinator_colors[0]:
                text = "Coordinator"
            elif color == coordinator_colors[1]: 
                text = "Coordinator candidate"  
            plt.text(x, y, text, bbox=dict(facecolor=color, alpha=0.8))
            y-=dist
        
        y-=dist
        previous = None
        for node_length in node_lengths:
            node = node_length['node']
            total = node_length['total']     
            if previous == node.REGION:
                y-=dist
            else:
                y-=2*dist
                previous = node.REGION
            text = 'Node: %s Length: %s br'%(node.SHORT_NAME,total)     
            plt.text( x, y, text, bbox=dict(facecolor=region_colors[node.REGION], alpha=1))       
        plt.axis('on')
        plt.grid('on')     
        if self.traceElectionVisual:    
            plt.show()  
        
    """ 
    Read nodes and edges from file 
    Args: 
        None
    Return: 
        None
    """
    def readFiles(self):
        #nodes.txt => node_id capacity
        #edges.txt => node_id node_id 
        try:
            f = open('nodes.txt','r') 
            lines = f.readlines()
            for line in lines:
                content = line.strip().split()
                if len(content) == 4: 
                    ID =  int(content[0])
                    X = float(content[2])
                    Y = float(content[3])
                    if self.useRandomCapacity: 
                        index = findIndex(X, Y)      
                        CAPACITY =  round(  np.random.normal(
                            loc=self.distributions[index].LOC, 
                            scale=self.distributions[index].SCALE, 
                            size=self.distributions[index].SIZE), 0 ) #random.randint(0, self.MAX_CAPACITY)
                    else:
                        CAPACITY = int(content[1])
                    node = Node(ID, CAPACITY, X, Y)
                    self.add(node)
                    self.positions[node] = (X,Y) 

            f = open('edges.txt','r')
            lines = f.readlines()
            for line in lines:
                content = line.strip().split()
                if len(content) == 2:
                    id1 = int(content[0])
                    id2 = int(content[1])
                    if self.nodes.has_key(id1) and self.nodes.has_key(id2):
                        node1 = self.nodes[ id1 ]
                        node2 = self.nodes[ id2 ]
                        self.link( node1, node2 )
                    else:
                        if not(self.nodes.has_key(id1)):
                            self.log("ERROR: key '%s' is not exist"%(id1) )
                        if not(self.nodes.has_key(id2)):
                            self.log("ERROR: key '%s' is not exist"%(id2) )
            self.log('Files readed successfully..')
        except Exception, error:
            self.log('Files could not read..')
            self.log('ERROR: %s' % error)   

    """ 
    Log messages 
    Args: 
        message: string first message
    Return: 
        None
    """
    def log(self, message):
        if self.traceLog:  
            print("GRAPH:: %s"%(message) )

    """ 
    Log messages for prety print array
    Args: 
        message: string first message
        array: array for prety print
        is_write: Boolean default value is True
    Return: 
        None
    """
    def log_pp(self, message, array, is_write=True ):
        if is_write:
             print("GRAPH:: %s"%(message) )
             pp.pprint(array) 

    """ 
    Log messages 
    Args: 
        message: string first message
    Return: 
        None
    """
    def log_election(self, message):
        if self.traceElection:  
            print("GRAPH ELECTION:: %s"%(message) )                