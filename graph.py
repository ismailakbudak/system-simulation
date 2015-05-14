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

class Distribution(object):
    """docstring for Distribution"""
    def __init__(self, LOC=0.0, SCALE=1.0, SIZE=None):
        super(Distribution, self).__init__()
        self.LOC = LOC
        self.SCALE = SCALE
        self.SIZE = SIZE

# Node position class
class Position(object):
    """docstring for Position"""
    def __init__(self, X, Y):
        super(Position, self).__init__()
        self.X = X
        self.Y = Y

# Node objects for graph structure 
class Node(object): 
    
    def __init__(self, ID, CAPACITY, X=0, Y=0):
        self.ID = ID
        self.CAPACITY = CAPACITY
        self.POSITION = Position(X,Y)
        self.VISITED = False
        self.NAME = 'N:%s-C:%s'%(str(ID),str(CAPACITY))
        self.COORDINATOR = self
        self.neighbours={}
        self.log("node initialized..")
    
    def __repr__(self):
        return self.NAME

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

# Graph class
class Graph(object):

    def __init__(self):
        self.nodes={}
        self.positions={}
        self.lastID=0
        self.traceGrowth=True
        self.traceElection=True
        self.traceLog=True
        self.traceGrowthVisual=False
        self.traceElectionVisual=True
        self.useRandomCapacity=True
        self.MAX_CAPACITY=6
        self.GROWTH_LIMIT = 100
        self.GROWTH_RATE = 10
        self.nodeNumber = 10
        self.distributions = [ 
            Distribution(4,9), 
            Distribution(3,5), 
            Distribution(5,8), 
            Distribution(1,4), 
            Distribution(9,4) ]
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
    
    def removeVisitedProperty(self):
        for node in self.nodes.values():
            node.VISITED = False

    """ 
    Start election algorithm on graph
    Args: 
        start: node object that is start point 
    Return: 
        None
    """
    def startElection(self,start):
        self.removeVisitedProperty()
        self.log_election("BEGIN election =============================")
        self.log_election("start node : "+ str(start))
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
        self.log_election("Coordinator : " + str(coordinator) )
        self.log_election("====================================")
        if self.traceElectionVisual:
            #self.draw()
            self.draw_node(coordinator, coordinator_candidates, start)
        
    """ 
    Print nodes coordinator
    Args:
        None  
    Return: 
        None
    """      
    def print_coordinator(self):
        for node in self.nodes.values():
            self.log_election(" %s -> %s " % (str(node), str(node.COORDINATOR)) )    
        
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
        #self.log_election( str(self.number) + " nodes coordinator")
        #self.number += 1
        #self.print_coordinator()
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
        MAX_CAPACITY: max capacity for color index
    Return: 
        None
    """
    def draw(self ):
        self.log("graph is drawing..")
        colors = ["#EFDFBB","orange","lightgreen","lightblue","#FFD300","violet","yellow","#7CB9E8","#E1A95F", "#007FFF","#CCFF00","pink","cyan"]
        length = len(colors) - 1
        # division by zero
        if length >= self.MAX_CAPACITY:
            length = self.MAX_CAPACITY
        amount = self.MAX_CAPACITY / length
        def find_color(node):
            X = node.POSITION.X
            Y = node.POSITION.Y
            if X >= 0 and Y >= 0:
                index = 0
            elif X <= 0 and Y >= 0:
                index = 1
            elif X >= 0 and Y <= 0:
                index = 2
            else:
                index = 3
            return colors[index]         
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
                font_size=9,
                node_size=1800,#node_size,
                font_family='ubuntu',
                font_color='red',
                node_color=node_colors, 
                edgelist=edges,
                edge_color=edge_colors, 
                width=0.4)
        # Information Text
        x=-9.0;y=11
        plt.text(x, y+0.5, 'Some text will come here', bbox=dict(facecolor='red', alpha=0.5)) 
        plt.axis('on')
        plt.grid('on')     
        plt.show()  

    """ 
    Draw coordinator and coordinator candidates
    Args: 
        coordinator: coordinator node
        coordinator_candidates: node objects array
    Return: 
        None
    """
    def draw_node(self, coordinator, coordinator_candidates, start):
        self.log("coordinator is drawing..")
        coordinator_colors = ["orange", "yellow", "pink", "skyblue"]  
        def find_coordinator_color(node):
            if node.ID == coordinator.ID:
                return coordinator_colors[0]
            if node in coordinator_candidates:
                return coordinator_colors[1]
            if node.ID == start.ID:
                return coordinator_colors[2]
            return coordinator_colors[3] 
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
                font_size=9,
                node_size=1800,#node_size,
                font_family='ubuntu',
                font_color='red',
                node_color=node_coordinator_colors, 
                edgelist=coordinator_edges,
                edge_color=coordinator_edge_colors, 
                width=0.4)
        # Information Text
        x=-9.0;y=11;i=1;flag=False;dist=1
        plt.text(x, y+1.5, 'Some text will come here', bbox=dict(facecolor='red', alpha=0.5)) 
        for color in coordinator_colors:
            if color == coordinator_colors[0]:
                text = "Coordinator"
            elif color == coordinator_colors[1]: 
                text = "Coordinator candidate"
            elif color == coordinator_colors[2]: 
                text = "Start point"
            else:  
                text = "Normal nodes" 
            plt.text(x, y, text, bbox=dict(facecolor=color, alpha=0.5))
            y-=dist
        plt.axis('on')
        plt.grid('on')     
        plt.show()  
        #plt.show(block=False) 

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
            ID = 1
            lines = f.readlines()
            for line in lines:
                content = line.strip().split()
                if len(content) == 3: 
                    X = float(content[1])
                    Y = float(content[2])
                    if self.useRandomCapacity: 
                        if X > 0 and Y > 0:
                            index = 0
                        elif X < 0 and Y > 0:
                            index = 1
                        elif X > 0 and Y < 0:
                            index = 2
                        else:
                            index = 3     
                        CAPACITY =  round(  np.random.normal(
                            loc=self.distributions[index].LOC, 
                            scale=self.distributions[index].SCALE, 
                            size=self.distributions[index].SIZE), 2 ) #random.randint(0, self.MAX_CAPACITY)
                    else:
                        CAPACITY = int(content[0])

                    node = Node(ID, CAPACITY, X, Y)
                    self.add(node)
                    self.positions[node] = (X,Y)
                    if ID == (self.nodeNumber * 4):
                        break
                    ID += 1 

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

    def log(self, message):
        if self.traceLog:  
            print("GRAPH:: %s"%(message) )

    def log_pp(self, message, array, is_write ):
        if is_write:
             print("GRAPH:: %s"%(message) )
             pp.pprint(array) 

    def log_grow(self, message):
        if self.traceGrowth:  
            print("GRAPH GROW:: %s"%(message) )

    def log_election(self, message):
        if self.traceElection:  
            print("GRAPH ELECTION:: %s"%(message) )                