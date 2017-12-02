#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ##################################################
# class DirectedGraph (UdGraph)
# class DepthFirstSearch
# class BreadthFirstSearch
# class DiGraphCycleDetector
# class DiGraphSort
# class DFSSort
# class ConnectedComponents
# ##################################################

#%%
import numpy as np
from collections import deque
import itertools

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
V = max(list(itertools.chain.from_iterable(edges)))+1

DG1 = DirectedGraph(V)
for edge in edges:
    DG1.addEdge(edge)

#%%
class DepthFirstSearch(object):    
    def __init__(self, G, v):
        self.v = v
        self.marked = np.full((G.V,), False, dtype=bool)
        self.predecessor = np.full((G.V,), None)
        self._pathExploration2(G, v)
    
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
DFS1 = DepthFirstSearch(DG1, 0)
print(DFS1.isConnected(4))
print(DFS1.marked)
print(DFS1.predecessor)
print(DFS1.connectedSet())
print(DFS1.pathTo(3))
print(DFS1.isConnected(7))

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
BFS1 = BreadthFirstSearch(DG1, 0)
print(BFS1.isConnected(7))
print(BFS1.marked)
print(BFS1.isConnected(4))
print(BFS1.marked)
print(BFS1.predecessor)
print(BFS1.connectedSet())
print(BFS1.pathTo(3))

#%%
class DiGraphCycleDetector(object):
    def __init__(self, G):
        self.counter = np.full((G.V,), 0, dtype=int)
        self.hasCycle = False
        self.marked = np.full((G.V,), False, dtype=bool)
        self.num_marked = 0
        for v in range(G.V):
            if not G.sourceDict[v]:
                self._pathExploration(G, v)
                if self.hasCycle:
                    return
        if self.num_marked < G.V:
            self.hasCycle = True
    
    def _pathExploration(self, G, v):
        searchQueue = deque()
        if not self.marked[v]:
            self.marked[v] = True
            self.num_marked += 1
        for t in G.adjacencyDict[v]:
            searchQueue.append(t)
        while searchQueue:
            s = searchQueue.popleft()
            if not self.marked[s]:
                self.marked[s] = True
                self.num_marked += 1
            self.counter[s] += 1
            if self.counter[s] > G.indegree[s]:
                self.hasCycle = True
                return
            for t in G.adjacencyDict[s]:
                searchQueue.append(t)

#%%
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 5),
    (5, 0)
]
V = max(list(itertools.chain.from_iterable(edges)))+1

G2 = DirectedGraph(V)
for edge in edges:
    G2.addEdge(edge)

G2_cycle = DiGraphCycleDetector(G2)
print(G2_cycle.hasCycle)
print(G2_cycle.counter)
print(G2.indegree)

#%%
class DiGraphSort(object):
    def __init__(self, G):
        self.rank = np.full((G.V,), 0, dtype=int)
        for v in range(G.V):
            if G.indegree[v] == 0:
                self._rankSearch(G, v)
    
    def _rankSearch(self, G, v):
        searchQueue = deque()
        searchQueue.append(v)
        while searchQueue:
            s = searchQueue.popleft()
            for t in G.adjacencyDict[s]:
                self.rank[t] = max(self.rank[t], self.rank[s]+1)
                searchQueue.append(t)

#%%
edges = [
    (0, 1),
    (1, 2),
    (0, 2),
    (2, 3),
    (3, 4),
    (5, 6),
    (7, 8),
    (8, 4),
    (3, 8)
]
V = max(list(itertools.chain.from_iterable(edges)))+1

G2 = DirectedGraph(V)
for edge in edges:
    G2.addEdge(edge)

G2_sort = DiGraphSort(G2)
print(G2_sort.rank)

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
V = max(list(itertools.chain.from_iterable(edges)))+1

DG1 = DirectedGraph(V)
for edge in edges:
    DG1.addEdge(edge)
DG1_sort = DFSSort(DG1)
print(DG1_sort.orderedList)

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
DG1_cc = ConnectedComponents(DG1)
print(DG1_cc.counterVec)
