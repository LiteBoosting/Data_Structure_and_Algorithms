#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
array = [20, 1, 2, 3, 0, 10, 4]

#%%
class heap_sort(object):
    def __init__(self, array, inplace=True):
        """Initialize the binary heap using the whole array.
        """
        self.inplace = inplace
        if self.inplace:
            self.BH = array
        else:
            from copy import deepcopy
            self.BH = deepcopy(array)
        self.n = len(self.BH)
    
    def get_parent(self, loc):
        """Return the location (not value) of the parent for this location.
        If the location is 0 (root node), the return value would be -1.
        """
        return ((loc+1)//2-1)
    
    def get_largest_child(self, loc):
        """Return the location (not value) of the child with largest value among children for this location.
        If the location does not have children, i.e., children location exceeds the length, return -1.
        """
        loc_child0 = (loc+1)*2-1
        loc_child1 = (loc+1)*2
        if (loc_child1 <= self.n):
            if self.BH[loc_child0] >= self.BH[loc_child1]:
                return loc_child0
            else:
                return loc_child1
        elif (loc_child0 <= self.n):
            return loc_child0
        else:
            return -1
    
    def insert(self, loc):
        loc_current = loc
        loc_parent = self.get_parent(loc_current)
        while (loc_parent >= 0):
            if (self.BH[loc_current] > self.BH[loc_parent]):
                self.BH[loc_current], self.BH[loc_parent] = self.BH[loc_parent], self.BH[loc_current]
                loc_current = loc_parent
                loc_parent = self.get_parent(loc_current)
            else:
                break

    def extract_max(self, loc):
        if loc > 0:
            self.BH[loc], self.BH[0] = self.BH[0], self.BH[loc]
            loc_current = 0
            loc_child = self.get_largest_child(loc_current)
            while ((loc_child >= 0) & (loc_child < loc)):
                if (self.BH[loc_current] < self.BH[loc_child]):
                    self.BH[loc_current], self.BH[loc_child] = self.BH[loc_child], self.BH[loc_current]
                    loc_current = loc_child
                    loc_child = self.get_largest_child(loc_current, )
                else:
                    break
    
    def sort(self):
        for loc in range(self.n):
            self.insert(loc)
        for loc in range(self.n-1, -1, -1):
            self.extract_max(loc)
        if not self.inplace:
            return self.BH
#%%
array = [20, 1, 2, 2, 19.6, 19.5, 19]
print(heap_sort(array, inplace=False).sort())
