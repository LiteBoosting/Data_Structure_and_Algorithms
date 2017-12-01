#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np

#%%
class Graph(object):
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.graphDict = {}
        for i in range(self.V):
            self.graphDict[i] = []
    
    def addEdge(self, edge):
        '''edge is a tuple of two vertices to be connected.
        '''
        a, b = edge
        self.graphDict[a].append(b)
        self.graphDict[b].append(a)
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
class DepthFirstPaths(object):    
    def __init__(self, s, G):
        self.s = s
        self.marked = np.full((G.V,), False, dtype=bool)
        self.edgeTo = np.full((G.V,), None)
        self.marked[self.s] = True
        self._pathFullExploration(G, self.s)

    def _pathFullExploration(self, G, t):
        for r in G.graphDict[t]:
            if self.marked[r]:
                continue
            else:
                self.marked[r] = True
                self.edgeTo[r] = t
                self._pathFullExploration(G, r)
    
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
            print(path)
            while True:
                s2 = self.edgeTo[s1]
                print('s2', s2)
                if s2 == self.s:
                    path.append(self.s)
                    print(path)
                    return path
                else:
                    path.append(s2)
                    s1 = s2
                    print(path)

#%%
dfp2 = DepthFirstPaths(0, G1)
dfp2.isConnected(4)
dfp2.marked
dfp2.edgeTo
dfp2.connectedSet()
dfp2.pathTo(6)
