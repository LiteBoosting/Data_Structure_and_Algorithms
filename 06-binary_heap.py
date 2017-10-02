#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np

#%%
ini = 20
data_stream = np.array([1, 2, 2, 0, 10, 4])
event_stream = np.array([1, 1, 0, 1, -1, 1, -1, 1, -1, 1, -1, -1, -1])

#%%
class priority_queue(object):
    def __init__(self, value):
        """Initialize the binary heap using this data point.
        BH stands for binary_heap.
        loc stands for the location of the last element of the binary heap.
        """
        self.BH = [value]
        self.loc = 0
    
    def is_empty(self):
        """Return value: True or False.
        """
        return (len(self.BH) == 0)
    
    def length(self):
        """Return the length of the binary heap.
        """
        return (self.loc+1)
    
    def show_max(self):
        """Return the maximum of the binary heap without changing it.
        """
        return (self.BH[0])
    
    def get_parent(self, loc):
        """Return the location (not value) of the parent for this location.
        If the location is 1 (root node), the return value would be 0.
        """
        return ((loc+1)//2-1)
    
    def get_largest_child(self, loc):
        """Return the location (not value) of the child with largest value among children for this location.
        If the location does not have children, i.e., children location exceeds the length, return 0.
        """
        loc_child0 = (loc+1)*2-1
        loc_child1 = (loc+1)*2
        if (loc_child1 <= self.loc):
            if self.BH[loc_child0] >= self.BH[loc_child1]:
                return loc_child0
            else:
                return loc_child1
        elif (loc_child0 <= self.loc):
            return loc_child0
        else:
            return 0
    
    def insert(self, value):
        self.BH.append(value)
        self.loc += 1
        if (self.loc > 1):
            loc_current = self.loc
            loc_parent = self.get_parent(loc_current)
            while (loc_parent >= 0):
                if (self.BH[loc_current] > self.BH[loc_parent]):
                    self.BH[loc_current], self.BH[loc_parent] = self.BH[loc_parent], self.BH[loc_current]
                    loc_current = loc_parent
                    loc_parent = self.get_parent(loc_current)
                else:
                    break
    
    def extract_max(self):
        if self.loc < 0:
            print("Binary Heap is empty")
            return None
        elif self.loc == 0:
            self.max = self.BH.pop()
            self.loc -= 1
            return self.max
        else:
            self.BH[self.loc], self.BH[0] = self.BH[0], self.BH[self.loc]
            self.max = self.BH.pop()
            self.loc -= 1
            loc_current = 0
            loc_child = self.get_largest_child(loc_current)
            while (loc_child != 0):
                if (self.BH[loc_current] < self.BH[loc_child]):
                    self.BH[loc_current], self.BH[loc_child] = self.BH[loc_child], self.BH[loc_current]
                    loc_current = loc_child
                    loc_child = self.get_largest_child(loc_current)
                else:
                    break
            return self.max

#%%
PQ1 = priority_queue(ini)
print(PQ1.BH)

#%%
i = 0
for event in event_stream:
    if (event == 1):
        print("event: ", event)
        PQ1.insert(data_stream[i])
        print(PQ1.BH)
        i += 1
    elif (event == -1):
        print("event: ", event)
        print(PQ1.extract_max())
        print(PQ1.BH)
    elif (event == 0):
        print("event: ", event)
        print(PQ1.show_max())
    else:
        print("Incorrect event id")
