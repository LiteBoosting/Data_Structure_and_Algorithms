#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np
from collections import deque

#%%
class Graph(object):
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adjacencyDict = {}
        for i in range(self.V):
            self.adjacencyDict[i] = []
    
    def addEdge(self, edge):
        '''edge is a tuple of two vertices to be connected.
        '''
        a, b = edge
        self.adjacencyDict[a].append(b)
        self.adjacencyDict[b].append(a)
        self.E += 1

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
    (5, 3)
]

G1 = Graph(V)
for edge in edges:
    G1.addEdge(edge)

#%%
class DepthFirstSearch(object):    
    def __init__(self, G, s):
        self.marked = np.full((G.V,), False, dtype=bool)
        self.edgeTo = np.full((G.V,), None)
        self.searchStack = []
        self._pathExploration2(G, s)
    
    def _pathExploration(self, G, t):
        for r in G.adjacencyDict[t]:
            if self.marked[r]:
                continue
            self.marked[r] = True
            self.edgeTo[r] = t
            self._pathExploration(G, r)

    def _pathExploration2(self, G, t):
        self.searchStack.append(t)
        while len(self.searchStack) > 0:
            r = self.searchStack.pop()
            for r2 in G.adjacencyDict[r]:
                if not self.marked[r2]:
                    self.searchStack.append(r2)
                    self.marked[r2] = True
                    self.edgeTo[r2] = r
    
    def connectedSet(self):
        return list(np.where(self.marked == True)[0])
    
    def isConnected(self, t):
        return self.marked[t]

    def pathTo(self, t):
        if not self.isConnected(t):
            return None
        else:
            path = []
            path.append(t)
            s1 = t
            while True:
                s2 = self.edgeTo[s1]
                if s2 == self.s:
                    path.append(self.s)
                    return path
                else:
                    path.append(s2)
                    s1 = s2
#%%
dfp1 = DepthFirstSearch(G1, 0)
dfp1.isConnected(7)
dfp1.marked

#%%
class BreadthFirstSearch(object):
    def __init__(self, G, s):
        self.marked = np.full((G.V,), False, dtype=bool)
        self.edgeTo = np.full((G.V,), None)
        self.searchQueue = deque()
        self._pathExploration(G, s)
    
    def _pathExploration(self, G, t):
        self.searchQueue.append(t)
        while len(self.searchQueue) > 0:
            r = self.searchQueue.popleft()
            for r2 in G.adjacencyDict[r]:
                if not self.marked[r2]:
                    self.searchQueue.append(r2)
                    self.marked[r2] = True
                    self.edgeTo[r2] = r
    
    def connectedSet(self):
        return list(np.where(self.marked == True)[0])
    
    def isConnected(self, t):
        return self.marked[t]

    def pathTo(self, t):
        if not self.isConnected(t):
            return None
        else:
            path = []
            path.append(t)
            s1 = t
            while True:
                s2 = self.edgeTo[s1]
                if s2 == self.s:
                    path.append(self.s)
                    return path
                else:
                    path.append(s2)
                    s1 = s2
#%%
dfp2 = BreadthFirstSearch(G1, 0)
dfp1.isConnected(7)
dfp1.marked

#%%
class GraphRingDetector(object):
    def __init__(self, G):
        self.marked = np.full((G.V,), False, dtype=bool)
        self.edgeTo = np.full((G.V,), None)
        self.hasRing = False
        self.ringVertex = None
        self.ringDirection1 = None
        self.ringDirection2 = None
        for v in range(G.V):
            if not self.marked[v]:
                self.searchQueue = deque()
                self._pathExploration(G, v)
            if self.hasRing:
                break
        if self.hasRing:
            self.ringPath = deque([self.ringVertex])
            while True:
                if self.ringDirection1 != self.ringDirection2:
                    self.ringPath.append(self.ringDirection1)
                    self.ringPath.appendleft(self.ringDirection2)
                else:
                    self.ringPath.append(self.ringDirection1)
                    break
                self.ringDirection1 = self.edgeTo[self.ringDirection1]
                self.ringDirection2 = self.edgeTo[self.ringDirection2]
    
    def _pathExploration(self, G, v):
        self.searchQueue.append(v)
        while self.searchQueue:
            s = self.searchQueue.popleft()
            self.marked[s] = True
            for t in G.adjacencyDict[s]:
                if not self.marked[t]:
                    self.searchQueue.append(t)
                    if self.edgeTo[t] is None:
                        self.edgeTo[t] = s
                    else:
                        self.hasRing = True
                        self.ringVertex = t
                        self.ringDirection1 = self.edgeTo[t]
                        self.ringDirection2 = s
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

G2 = Graph(V)
for edge in edges:
    G2.addEdge(edge)

G2_ = GraphRingDetector(G2)
if G2_.hasRing:
    print(G2_.ringPath)
else:
    print(G2_.hasRing)
