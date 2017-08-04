# -*- coding: utf-8 -*-

#%%
import numpy as np
from copy import deepcopy

class dynaConn(object):
    def __init__(self, N):
        """Initialization
        """
        self.trees = np.arange(N, dtype=int)
        self.treesizes = np.full((N,), 1, dtype=int)
        
    def root(self, i):
        """Return the root of node i,
        also do one-pass path compression
        """
        j = deepcopy(i)
        while(self.trees[j] != j):
            j, self.trees[j] = self.trees[j], self.trees[self.trees[j]]
        return j
        
    def connected(self, p, q):
        return (self.root(p) == self.root(q))
        
    def union(self, p, q):
        """Union two trees having node p and q. Also combine the treesize
        Only the value of self.treesizes at a root node can represent the size of this tree
        """
        root_p, root_q = self.root(p), self.root(q)
        if root_p == root_q:
            return
        if self.treesizes[root_p] > self.treesizes[root_q]:
            self.treesizes[root_p] = self.treesizes[root_p] + self.treesizes[root_q]
            self.trees[root_q] = root_p
        else:
            self.treesizes[root_q] = self.treesizes[root_p] + self.treesizes[root_q]
            self.trees[root_p] = root_q
            
#%%
N = 10
conn_obj = dynaConn(N)
connection_record = [[1, 2], [3, 4], [5, 6], [7, 8], [8, 1], [2, 6]]
for i, record in enumerate(connection_record):
    conn_obj.union(record[0], record[1])
print conn_obj.connected(1, 4)

#%%
N = 1000
conn_obj2 = dynaConn(N)
connection_record = []
import random
for i in np.arange(N):
    a = random.randint(0, N-1)
    b = random.randint(0, N-1)
    connection_record += [[a, b]]
    conn_obj2.union(a, b)
print conn_obj2.connected(1, 7)
# print connection_record
#%%
N = 1
conn_obj3 = dynaConn(N)
conn_obj3.union(0, 0)
