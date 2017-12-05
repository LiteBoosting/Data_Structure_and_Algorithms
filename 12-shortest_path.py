#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import sys
sys.path.append("User/senmao/Python/Algorithm_examples")

#%%
import numpy as np
# from collections import deque
# from Python.Algorithm_examples.priority_queue import PriorityQueue
from queue import PriorityQueue
# exec(open("./Python/Algorithm_examples/priority_queue.py").read(), globals())

#%%
class DirectedEdge(object):
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

# equivalent ndarray format
dtype = np.dtype([('v', np.int), ('distTo', np.float64)])
unit = (1, 1.1) # example of a unit for this dtype
key = 'distTo' # key name used for comparison in priority queue

#%%
class EdgeWeightedDiGraph(object):
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adjacencyDict = {}
        for v in range(self.V):
            self.adjacencyDict[v] = []
        self.sourceDict = {}
        for v in range(self.V):
            self.sourceDict[v] = []
        self.indegree = np.full((self.V,), 0, dtype=int)
        self.outdegree = np.full((self.V,), 0, dtype=int)
        self.inweight = np.full((self.V,), 0.0, dtype=float)
        self.outweight = np.full((self.V,), 0.0, dtype=float)
    
    def addEdge(self, diEdge):
        '''edge is a DirectedEdge class object.
        '''
        v = diEdge.v
        w = diEdge.w
        weight = diEdge.weight
        self.adjacencyDict[v].append(diEdge)
        self.sourceDict[w].append(diEdge)
        self.outdegree[v] += 1
        self.indegree[w] += 1
        self.outweight[v] += weight
        self.inweight[w] += weight
        self.E += 1

#%%
class ShortestPath(object):
    def __init__(self, DiGraph, v):
        self.v = v
        self.marked = np.full((DiGraph.V,), False, dtype=bool)
        self.hasDistance = np.full((DiGraph.V,), False, dtype=bool)
        self.distTo = np.full((DiGraph.V,), float("+inf"), dtype=float)
        self.lastPath = np.full((DiGraph.V,), None) # dtype=int
        self.PQVertices = PriorityQueue()
        self.Dijkstra(DiGraph)
    
    def Dijkstra(self, DiGraph):        
        self.distTo[self.v] = 0
        self.PQVertices.put((self.distTo[self.v], self.v))
        # we do not update distTo in priority queue, but use duplication
        # and check if it is already marked
        if not self.PQVertices.empty():
            PQVertex = self.PQVertices.get()
        else:
            PQVertex = None
        while PQVertex and self.marked[PQVertex[1]] and (not self.PQVertices.empty()):
            PQVertex = self.PQVertices.get()
        while PQVertex:
            self.marked[PQVertex[1]] = True
            for edge in DiGraph.adjacencyDict[PQVertex[1]]:
                if self.distTo[edge.v]+edge.weight < self.distTo[edge.w]:
                    self.hasDistance[edge.w] = True
                    self.distTo[edge.w] = self.distTo[edge.v]+edge.weight
                    self.lastPath[edge.w] = edge.v
                    self.PQVertices.put((self.distTo[edge.w], edge.w))
            if not self.PQVertices.empty():
                PQVertex = self.PQVertices.get()
            else:
                PQVertex = None
            while PQVertex and self.marked[PQVertex[1]] and (not self.PQVertices.empty()):
                if not self.PQVertices.empty():
                    PQVertex = self.PQVertices.get()

#%%
Edges = [
    (0, 1,  5.0),
    (0, 4,  9.0),
    (0, 7,  8.0),
    (1, 2, 12.0),
    (1, 3, 15.0),
    (1, 7,  4.0),
    (2, 3,  3.0),
    (2, 6, 11.0),
    (3, 6,  9.0),
    (4, 5,  4.0),
    (4, 6, 20.0),
    (4, 7,  5.0),
    (5, 2,  1.0),
    (5, 6, 13.0),
    (7, 5,  6.0),
    (7, 2,  7.0)
]
V = max([max(z[0], z[1]) for z in Edges])+1

DiGraph1 = EdgeWeightedDiGraph(V)
for i in range(len(Edges)):
    DiGraph1.addEdge(DirectedEdge(Edges[i][0], Edges[i][1], Edges[i][2]))

#%%
SP1 = ShortestPath(DiGraph1, 0)
print(SP1.distTo)
print(SP1.lastPath)
