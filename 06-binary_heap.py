#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
# ##################################################
# Implement priority queue using resized array
# ##################################################

#%%
import numpy as np
import gc

#%%
#==============================================================================
# class DirectedEdge(object):
#     def __init__(self, v, w, weight):
#         self.v = v
#         self.w = w
#         self.weight = weight
#==============================================================================

#%%
dtype = np.dtype([('v', np.int), ('w', np.int), ('weight', np.float64)])
unit = (0, 1, 1.1) # example of a unit for this dtype
key = 'weight' # key name used for comparison in priority queue

# Valid operations for user-defined ndarray:
#     (1) np.array()
#     (2) np.repeat()
#     (3) slicing a[0:2]
#     (4) indexing a[0]
#     (5) a.dtype.names
# Do not use:
#     (1) np.full()
#     (2) np.concatenate()
#     (1) standard swap: a[0], a[1] = a[1], a[0], since a[0] is not immutable any more

# It is better to make user-defined ndarray dtype to be flattened, i.e., not a tuple with tuple elements.
# High layer cause more problem in copying, slicing, and more.

#%%
#==============================================================================
# print(dtype['v'])
# print(dtype['w'])
# print(dtype['weight'])
# 
# x = np.array([(0, 1, 3.4), (0, 2, 3.2)], dtype=dtype)
# print(x[1])
# print(x[1]['weight'])
# print(type(x[1]))
# print(type(x[1]['v']))
# print(x[0]['v'])
# 
# x = np.repeat(np.array([unit], dtype=dtype), 10)
# print(x)
# 
# x[1] = (0, 2, 3.3)
# print(x)
# 
# x = np.repeat(np.array([unit], dtype=dtype), 10)
# print(dtype.names)
# print(x.dtype)
# print(dtype)
# print(x.dtype.names)
#==============================================================================

#%%
class PriorityQueue(object):
    def __init__(self, dtype, unit, key, initialSpace=1024, ratioHalve=0.1, ratioDouble=0.9, barSize=100):
        self.dtype = dtype
        self.key = key
        self.unit = unit
        self.queue = np.repeat(np.array([self.unit], dtype=self.dtype), initialSpace)
        self.loc = -1 # location of last value in the queue
        self.space = len(self.queue)
        self.length = self.loc+1
        self.ratio = self.length/self.space
        self.ratioHalve = ratioHalve
        self.ratioDouble = ratioDouble
        self.barSize = barSize
    
    def updateQueueLength(self):
        self.length = self.loc+1
        self.ratio = self.length/self.space
        
    def isEmpty(self):
        return (self.loc < 0)
    
    def showMin(self):
        """Return the minimum of the binary heap without popping it.
        """
        return (self.queue[0])
    
    def getParent(self, loc):
        """Return the location (not value) of the parent for this location.
        If the location is 0 (root node), the return value would be -1.
        """
        return ((loc+1)//2-1)
    
    def getSmallestChild(self, loc):
        """Return the location (not value) of the child with smallest value among children
           of the location. If the location does not have children, i.e., children location
           exceeds the length, return -1.
        """
        child0 = (loc+1)*2-1
        child1 = (loc+1)*2
        if (0 <= child0 <= child1 <= self.loc):
            if self.queue[child0][self.key] <= self.queue[child1][self.key]:
                return child0
            else:
                return child1
        elif (0 <= child0 <= self.loc < child1):
            return child0
        else:
            return -1
    
    def swap(self, loc0, loc1):
        for var in self.dtype.names:
            self.queue[loc0][var], self.queue[loc1][var] = self.queue[loc1][var], self.queue[loc0][var]
        return
    
    def copy(self, loc):
        '''Copy the content in loc, and return a tuple.
        '''
        return tuple(self.queue[loc][var] for var in self.dtype.names)

    def insert(self, value):
        '''value should be a tuple.
        '''
        self.queue[self.loc+1] = value
        self.loc += 1
        self.updateQueueLength()
        current = self.loc
        parent = self.getParent(current)
        while (0 <= parent <= self.loc) and (self.queue[current][self.key] < self.queue[parent][self.key]):
            self.swap(current, parent)
            current = parent
            parent = self.getParent(current)
        self.sizingCheck()
        return
    
    def popMin(self):
        if self.isEmpty():
            return None
        minimum = self.copy(loc=0)
        self.swap(0, self.loc)
        self.loc -= 1
        self.updateQueueLength()
        current = 0
        child = self.getSmallestChild(current)
        while (0 <= child <= self.loc) and (self.queue[current][self.key] > self.queue[child][self.key]):
            self.swap(current, child)
            current = child
            child = self.getSmallestChild(current)
        self.sizingCheck()
        return minimum
    
    def sizingCheck(self):
        if (self.ratio < self.ratioHalve) and (self.length > self.barSize):
            self.space = int(self.space*0.5)
            self.new_queue = self.queue[0:self.space]
            del self.queue
            gc.collect()
            self.ratio = self.length/self.space
            self.queue = self.new_queue
            del self.new_queue
        if self.ratio > self.ratioDouble:
            self.new_queue = np.repeat(np.array([self.unit], dtype=self.dtype), self.space*2)
            self.new_queue[0:self.space] = self.queue
            self.space = self.space*2
            del self.queue
            gc.collect()
            self.ratio = self.length/self.space
            self.queue = self.new_queue
            del self.new_queue
        return

#%%
#==============================================================================
# data_stream = np.array([1, 2, 2, 0, 10, 4])
# event_stream = np.array([1, 1, 0, 1, -1, 1, -1, 1, -1, 1, -1, -1, -1])
# 
# PQ1 = PriorityQueue(dtype, unit, key)
# print(PQ1.queue[0:PQ1.length])
# 
# i = 0
# for event in event_stream:
#     if (event == 1):
#         print("event: ", event)
#         PQ1.insert((0, 0, data_stream[i]))
#         print(PQ1.queue[0:PQ1.length])
#         i += 1
#     elif (event == -1):
#         print("event: ", event)
#         print(PQ1.popMin())
#         print(PQ1.queue[0:PQ1.length])
#     elif (event == 0):
#         print("event: ", event)
#         print(PQ1.showMin())
#     else:
#         print("Incorrect event id")
#==============================================================================

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
        If the location is 0 (root node), the return value would be -1.
        """
        return ((loc+1)//2-1)
    
    def get_largest_child(self, loc):
        """Return the location (not value) of the child with largest value among children for this location.
        If the location does not have children, i.e., children location exceeds the length, return -1.
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
            return -1
    
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
            while (loc_child >= 0):
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
