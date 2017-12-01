#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np
from collections import deque
deque()
#%%
class DirectedGraph(object):
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.f = {}
        self.adjacencyDict = {}
        self.sourceDict = {}
        for i in range(self.V):
            self.adjacencyDict[i] = []
            self.sourceDict[i] = []
        self.indegree = np.full((self.V,), 0, dtype=int)
        self.outdegree = np.full((self.V,), 0, dtype=int)
    
    def addEdge(self, edge):
        '''edge is a tuple of two vertices to be connected.
        '''
        a, b = edge
        self.adjacencyDict[a].append(b)
        self.sourceDict[b].append(a)
        self.outdegree[a] += 1
        self.indegree[b] += 1
        self.E += 1

#%%
class DFSSort(object):
    def __init__(self, G):
        self.marked = np.full((G.V,), False, dtype=bool)
        self.orderedList = []
        for v in range(G.V):
            if not self.marked[v]:
                self._DFS(G, v)
    
    def _DFS(self, G, v):
        searchStack = []
        searchStack.append(v)
        self.marked[v] = True
        while searchStack:
            hasChild = False
            s = searchStack.pop()
            searchStack.append(s)
            for t in G.adjacencyDict[s]:
                if not self.marked[t]:
                    hasChild = True
                    searchStack.append(t)
                    self.marked[t] = True
            if not hasChild:
                self.orderedList.append(searchStack.pop())
                hasChild = False

#%%
V = 9
edges = [
    (0, 5),
    (4, 3),
    (0, 1),
    (6, 4),
    (5, 4),
    (0, 2),
    (0, 6),
    (7, 8),
    (5, 3),
    (1, 0),
    (3, 1)
]

G1 = DirectedGraph(V)
for edge in edges:
    G1.addEdge(edge)
G1_sort = DFSSort(G1)
print(G1_sort.orderedList)

#%%
class ConnectedComponents(object):
    def __init__(self, G):
        self.orderedList = []
        self.marked = np.full((G.V,), False, dtype=bool)
        self._inverseDFSSort(G)
        self.counter = 0
        self.counterVec = np.full((G.V,), 0, dtype=int)
        self._DFSCount(G)
    
    def _inverseDFSSort(self, G):
        for v in range(G.V):
            if not self.marked[v]:
                self._inverseDFS(G, v)
    
    def _inverseDFS(self, G, v):
        searchStack = []
        searchStack.append(v)
        self.marked[v] = True
        while searchStack:
            hasChild = False
            s = searchStack.pop()
            searchStack.append(s)
            for t in G.sourceDict[s]:
                if not self.marked[t]:
                    hasChild = True
                    searchStack.append(t)
                    self.marked[t] = True
            if not hasChild:
                self.orderedList.append(searchStack.pop())
                hasChild = False
    
    def _DFSCount(self, G):
        self.marked = np.full((G.V,), False, dtype=bool)
        for v in self.orderedList:
            if not self.marked[v]:
                self._DFS(G, v)
    
    def _DFS(self, G, v):
        self.counter += 1
        searchStack = []
        searchStack.append(v)
        self.marked[v] = True
        while searchStack:
            s = searchStack.pop()
            self.counterVec[s] = self.counter
            for t in G.sourceDict[s]:
                if not self.marked[t]:
                    searchStack.append(t)
                    self.marked[t] = True

#%%
G1_cc = ConnectedComponents(G1)
print(G1_cc.counterVec)
