#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np
from collections import deque

#%%
class DirectedGraph(object):
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.f = {}
        self.pointToDict = {}
        self.pointFromDict = {}
        for i in range(self.V):
            self.pointToDict[i] = []
            self.pointFromDict[i] = []
        self.indegree = np.full((self.V,), 0, dtype=int)
        self.outdegree = np.full((self.V,), 0, dtype=int)
    
    def addEdge(self, edge):
        '''edge is a tuple of two vertices to be connected.
        '''
        a, b = edge
        self.pointToDict[a].append(b)
        self.pointFromDict[b].append(a)
        self.outdegree[a] += 1
        self.indegree[b] += 1
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

G1 = DirectedGraph(V)
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
        for r in G.pointToDict[t]:
            if self.marked[r]:
                continue
            self.marked[r] = True
            self.edgeTo[r] = t
            self._pathExploration(G, r)

    def _pathExploration2(self, G, t):
        self.searchStack.append(t)
        while len(self.searchStack) > 0:
            r = self.searchStack.pop()
            for r2 in G.pointToDict[r]:
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
            for r2 in G.pointToDict[r]:
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
        self.counter = np.full((G.V,), 0, dtype=int)
        self.hasRing = False
        self.marked = np.full((G.V,), False, dtype=bool)
        self.num_marked = 0
        for v in range(G.V):
            if not G.pointFromDict[v]:
                self.searchQueue = deque()
                self._pathExploration(G, v)
                if self.hasRing:
                    return
        if self.num_marked < G.V:
            self.hasRing = True
                
    
    def _pathExploration(self, G, v):
        if not self.marked[v]:
            self.num_marked += 1
            self.marked[v] = True
        for t in G.pointToDict[v]:
            self.searchQueue.append(t)
        while self.searchQueue:
            s = self.searchQueue.popleft()
            if not self.marked[s]:
                self.num_marked += 1
                self.marked[s] = True
            self.counter[s] += 1
            if self.counter[s] > G.indegree[s]:
                self.hasRing = True
                return
            for t in G.pointToDict[s]:
                self.searchQueue.append(t)
        
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

G2 = DirectedGraph(V)
for edge in edges:
    G2.addEdge(edge)

G2_ring = GraphRingDetector(G2)
if G2_ring.hasRing:
    print(G2_ring.ringPath)
else:
    print('No ring')
print(G2_ring.counter)
print(G2.indegree)

#%%
edges = [
    (0, 1),
    (1, 2),
    (2, 1)
]
V = len(edges)

G2 = DirectedGraph(V)
for edge in edges:
    G2.addEdge(edge)

G2_ring = GraphRingDetector(G2)
print(G2_ring.hasRing)
print(G2_ring.counter)
print(G2.indegree)

#%%
edges = [
    (0, 1),
    (1, 1),
    (0, 2),
    (2, 3),
    (3, 1)
]
V = len(edges)

G2 = DirectedGraph(V)
for edge in edges:
    G2.addEdge(edge)

G2_ring = GraphRingDetector(G2)
print(G2_ring.hasRing)
print(G2_ring.counter)
print(G2.indegree)

#%%
class GraphSort(object):
    def __init__(self, G):
        self.rank = np.full((G.v,), 0, dtype=int)
