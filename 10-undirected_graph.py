#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np
from collections import deque

#%%
class UndirectedGraph(object):
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adjacencyDict = {}
        for i in range(self.V):
            self.adjacencyDict[i] = []
        self.degree = np.full((self.V,), 0, dtype=int)
    
    def addEdge(self, edge):
        '''edge is a tuple of two vertices to be connected.
        '''
        a, b = edge
        self.adjacencyDict[a].append(b)
        self.degree[a] += 1
        self.adjacencyDict[b].append(a)
        self.degree[b] += 1
        self.E += 1

#%%
edges = [
    (0, 5),
    (4, 3),
    (0, 1),
    (6, 4),
    (5, 4),
    (0, 2),
    (0, 6),
    (7, 8),
    (5, 3)
]
V = len(edges)

UG1 = UndirectedGraph(V)
for edge in edges:
    UG1.addEdge(edge)

#%%
class DepthFirstSearch(object):    
    def __init__(self, G, v):
        self.v = v
        self.marked = np.full((G.V,), False, dtype=bool)
        self.predecessor = np.full((G.V,), None)
        self.marked[self.v] = True
        self._pathExploration2(G, self.v)

    def _pathExploration(self, G, v):
        for s in G.adjacencyDict[v]:
            if not self.marked[s]:
                self.marked[s] = True
                self.predecessor[s] = v
                self._pathExploration(G, s)
    
    def _pathExploration2(self, G, v):
        searchStack = []
        searchStack.append(v)
        while searchStack:
            s = searchStack.pop()
            for t in G.adjacencyDict[s]:
                if not self.marked[t]:
                    searchStack.append(t)
                    self.marked[t] = True
                    self.predecessor[t] = s

    def connectedSet(self):
        return list(np.where(self.marked == True)[0])
    
    def isConnected(self, s):
        return self.marked[s]
    
    def pathTo(self, s):
        if not self.isConnected(s):
            return None
        path = []
        path.append(s)
        t1 = s
        while t1 != self.v:
            t2 = self.predecessor[t1]
            path.append(t2)
            t1 = t2
        return path

#%%
DFS1 = DepthFirstSearch(UG1, 0)
print(DFS1.isConnected(4))
print(DFS1.marked)
print(DFS1.predecessor)
print(DFS1.connectedSet())
print(DFS1.pathTo(3))

#%%
class BreadthFirstSearch(object):
    def __init__(self, G, v):
        self.v = v
        self.marked = np.full((G.V,), False, dtype=bool)
        self.predecessor = np.full((G.V,), None)
        self._pathExploration(G, v)
    
    def _pathExploration(self, G, v):
        searchQueue = deque()
        searchQueue.append(v)
        while searchQueue:
            s = searchQueue.popleft()
            for t in G.adjacencyDict[s]:
                if not self.marked[t]:
                    searchQueue.append(t)
                    self.marked[t] = True
                    self.predecessor[t] = s
    
    def connectedSet(self):
        return list(np.where(self.marked == True)[0])
    
    def isConnected(self, t):
        return self.marked[t]

    def pathTo(self, s):
        if not self.isConnected(s):
            return None
        path = []
        path.append(s)
        t1 = s
        while t1 != self.v:
            t2 = self.predecessor[t1]
            path.append(t2)
            t1 = t2
        return path

#%%
BFS1 = BreadthFirstSearch(UG1, 0)
print(DFS1.isConnected(4))
print(DFS1.marked)
print(DFS1.predecessor)
print(DFS1.connectedSet())
print(DFS1.pathTo(3))

#%%
class UGCycleDetector(object):
    def __init__(self, G):
        self.marked = np.full((G.V,), False, dtype=bool)
        self.predecessor = np.full((G.V,), None)
        self.hasCycle = False
        self.cycleVertex = None
        self.cycleDirection1 = None
        self.cycleDirection2 = None
        for v in range(G.V):
            if not self.marked[v]:
                self._BFS(G, v)
            if self.hasCycle:
                break
        if self.hasCycle:
            self.cyclePath = deque([self.cycleVertex])
            while True:
                if self.cycleDirection1 != self.cycleDirection2:
                    self.cyclePath.append(self.cycleDirection1)
                    self.cyclePath.appendleft(self.cycleDirection2)
                else:
                    self.cyclePath.append(self.cycleDirection1)
                    break
                self.cycleDirection1 = self.predecessor[self.cycleDirection1]
                self.cycleDirection2 = self.predecessor[self.cycleDirection2]
    
    def _BFS(self, G, v):
        searchQueue = deque()
        searchQueue.append(v)
        while searchQueue:
            s = searchQueue.popleft()
            self.marked[s] = True
            for t in G.adjacencyDict[s]:
                if not self.marked[t]:
                    searchQueue.append(t)
                    if self.predecessor[t] is None:
                        self.predecessor[t] = s
                    else:
                        self.hasCycle = True
                        self.cycleVertex = t
                        self.cycleDirection1 = self.predecessor[t]
                        self.cycleDirection2 = s
                        return
        
#%%
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 5)
]
V = len(edges)

G2 = UndirectedGraph(V)
for edge in edges:
    G2.addEdge(edge)

G2_cycle = UGCycleDetector(G2)
print(G2_cycle.hasCycle)
if G2_cycle.hasCycle:
    print(G2_cycle.cycleVertex)
    print(G2_cycle.cyclePath)
else:
    print(G2_cycle.hasCycle)

#%%
class UGCycleDetector2(object):
    '''This method detects cycle while constructing the UndirectedGraph.
       Dynamic connection is used and if two vertices are already connected,
       then a new edge of the two implies a cycle.
    '''
    def __init__(self, V):
        # necessary materials for dynamic connectivity and graph construction
        self.parents = np.arange(V, dtype=int)
        self.treeSizes = np.full((V,), 1, dtype=int)
        self.hasCycle = False
        self.cycleVertex1 = None
        self.cycleVertex2 = None
        
    def addEdge(self, edge):
        '''edge is a tuple of two vertices to be connected.
        '''
        a, b = edge
        if self.isConnected(a, b):
            self.cycleVertex1 = a
            self.cycleVertex2 = b
            self.hasCycle = True
        root_a = self.getRoot(a)
        root_b = self.getRoot(b)
        if self.treeSizes[root_a] >= self.treeSizes[root_b]:
            self.parents[root_b] = root_a
            self.treeSizes[root_a] += self.treeSizes[root_b]
        else:
            self.parents[root_a] = root_b
            self.treeSizes[root_b] += self.treeSizes[root_a]
        
    def isConnected(self, v1, v2):
        return self.getRoot(v1) == self.getRoot(v2)

    def getRoot(self, v):
        s = v
        while not self.isRoot(s):
            s = self.parents[s]
        return s
    
    def isRoot(self, v):
        return self.parents[v] == v
    
#%%
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 5)
]
V = len(edges)

G2_cycle = UGCycleDetector2(V)
G2_cycle.parents
for edge in edges:
    G2_cycle.addEdge(edge)
print(G2_cycle.hasCycle)
if G2_cycle.hasCycle:
    print(G2_cycle.cycleVertex1)
    print(G2_cycle.cycleVertex2)
