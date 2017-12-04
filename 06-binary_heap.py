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
class DirectedEdge(object):
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

unit_dtype = np.dtype([('weight', np.float64), ('v', np.int), ('w', np.int)])

#%%
print(unit_dtype['weight'])
print(unit_dtype['v'])
print(unit_dtype['w'])

x = np.array([(3.4, 0, 1), (3.2, 0, 2)], dtype=unit_dtype)
print(x[1])
print(x[1]['weight'])
print(type(x[1]))
print(type(x[1]['v']))
print(x[0]['v'])

queue = np.repeat(np.array([(0.0, 0, 0)], dtype=unit_dtype), 10)
print(queue)

x[1] = (3.3, 0, 2)
print(x)

#%%
class PriorityQueue(object):
    def __init__(self, init_len=1024, ratio_halve=0.10, ratio_double=0.90, bar_size=100):
        self.queue = np.repeat(np.array([(0.0, 0, 0)], dtype=unit_dtype), init_len)
        self.loc = -1 # location of last value in the queue
        self.space = len(self.queue)
        self.length = self.loc+1
        self.ratio = self.length/self.space
        self.ratio_halve = ratio_halve
        self.ratio_double = ratio_double
        self.bar_size = bar_size
    
    def update_loc(self):
        self.length = self.loc+1
        self.ratio = self.length/self.space
        
    def is_empty(self):
        return (self.loc < 0)
    
    def show_min(self):
        """Return the minimum of the binary heap without popping it.
        """
        return (self.queue[0])
    
    def get_parent(self, loc):
        """Return the location (not value) of the parent for this location.
        If the location is 0 (root node), the return value would be -1.
        """
        return ((loc+1)//2-1)
    
    def get_smallest_child(self, loc):
        """Return the location (not value) of the child with smallest value among children
           of the location. If the location does not have children, i.e., children location
           exceeds the length, return -1.
        """
        child0 = (loc+1)*2-1
        child1 = (loc+1)*2
        if (child1 <= self.loc):
            if self.queue[child0]['weight'] <= self.queue[child1]['weight']:
                return child0
            else:
                return child1
        elif (child0 <= self.loc):
            return child0
        else:
            return -1
    
    def insert(self, value):
        self.queue[self.loc+1] = value
        self.loc += 1
        self.update_loc()
        current = self.loc
        parent = self.get_parent(current)
        while (parent >= 0) and (self.queue[current]['weight'] < self.queue[parent]['weight']):
            self.queue[current], self.queue[parent] = self.queue[parent], self.queue[current]
            current = parent
            parent = self.get_parent(current)
        self.sizingCheck()
        return
    
    def pop_min(self):
        if self.is_empty():
            return None
        minimum = self.queue[0]
        self.queue[self.loc], self.queue[0] = self.queue[0], self.queue[self.loc]
        self.loc -= 1
        self.update_loc()
        current = 0
        child = self.get_smallest_child(current)
        while (child <= self.loc) and (self.queue[current]['weight'] > self.queue[child]['weight']):
            self.queue[current], self.queue[child] = self.queue[child], self.queue[current]
            current = child
            child = self.get_smallest_child(current)
        self.sizingCheck()
        return minimum
    
    def sizingCheck(self):
        if (self.ratio < self.ratio_halve) and (self.length > self.bar_size):
            self.space = int(self.space*0.5)
            self.new_queue = self.queue[0:self.space]
            del self.queue
            gc.collect()
            self.ratio = self.length/self.space
            self.queue = self.new_queue
            del self.new_queue
        if self.ratio > self.ratio_double:
            padding_queue = np.repeat(np.array([(0.0, 0, 0)], dtype=unit_dtype), self.space)
            self.new_queue = np.concatenate(self.queue, padding_queue)
            self.space = self.space*2
            del self.queue, padding_queue
            gc.collect()
            self.ratio = self.length/self.space
            self.queue = self.new_queue
            del self.new_queue
        return

#%%
ini = 20
data_stream = np.array([1, 2, 2, 0, 10, 4])
event_stream = np.array([1, 1, 0, 1, -1, 1, -1, 1, -1, 1, -1, -1, -1])

PQ1 = PriorityQueue()
print(PQ1.queue[0:PQ1.length])

i = 0
for event in event_stream:
    if (event == 1):
        print("event: ", event)
        PQ1.insert((data_stream[i], 0, 0))
        print(PQ1.queue[0:PQ1.length])
        i += 1
    elif (event == -1):
        print("event: ", event)
        print(PQ1.pop_min())
        print(PQ1.queue[0:PQ1.length])
    elif (event == 0):
        print("event: ", event)
        print(PQ1.show_min())
    else:
        print("Incorrect event id")

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
