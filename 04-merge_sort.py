#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np
from copy import deepcopy

#%%
class merge_sort(object):
    """Use merge sort to sort an array, increasing order only.
    """
    def __init__(self, vec):
        self.vec = deepcopy(np.array(vec))
        self.n = len(vec)
        
    def merge(self, vec_a, vec_b):
        """Merge two sorted arrays.
        """
        s_a, s_b = len(vec_a), len(vec_b)
        vec_c = deepcopy(np.concatenate((vec_a, vec_b)))
        i_a, i_b, i_c = 0, 0, 0
        key = True
        if vec_a[s_a-1] <= vec_b[0]:
            return vec_c
        else:
            while key:
                if (i_b > s_b-1) or (vec_a[i_a] <= vec_b[i_b]):
                    vec_c[i_c] = vec_a[i_a]
                    i_a += 1
                    i_c += 1
                else:
                    vec_c[i_c] = vec_b[i_b]
                    i_b += 1
                    i_c += 1
                if i_a > s_a-1:
                    key = False
            return vec_c
            
    def sort_1(self, left=0, right=None):
        """Merge sort using recurrsion.
        """
        if right == None:
            right = self.n
        if right-left == 1:
            return self.vec[left:right]
        else:
            middle = int(left+(right-left)/2)
            return self.merge(self.sort_1(left, middle), self.sort_1(middle, right))
    
    def sort_2(self):
        """Merge sort without using recursion. Do hierarchical partition instead.
        """
        self.log_n = int(np.ceil(np.log2(self.n)))
        step_size = 1
        for layer in np.arange(self.log_n):
            partition_net = np.concatenate((np.arange(0, self.n, step=step_size), np.array([self.n])))
            step_size *= 2
            for i in np.arange(start=0, stop=int((len(partition_net)-1)/2)*step_size, step=step_size, dtype=int):
                left, middle, right = partition_net[i], partition_net[i+1], partition_net[i+2]
                self.vec[left:right] = self.merge(self.vec[left:middle], self.vec[middle:right])

    def sort(self, recursion=False):
        """Main sorting function, will call either sort_1() or sort_2()
        """
        if recursion:
            self.vec = self.sort_1()
        else:
            self.sort_2()
        
#%%
vec = np.array([0])
obj_sort = merge_sort(vec)
obj_sort.sort()
print(obj_sort.vec)

#%%
vec = np.array([0])
obj_sort = merge_sort(vec)
obj_sort.sort(recursion=True)
print(obj_sort.vec)

#%%
vec = np.array([0, 3, 4, 2, 9, 4])
obj_sort = merge_sort(vec)
obj_sort.sort()
print(obj_sort.vec)

#%%
vec = np.array([0, 3, 4, 2, 9, 4])
obj_sort = merge_sort(vec)
obj_sort.sort(recursion=True)
print(obj_sort.vec)

#%%
vec = np.array([0, 1, 0, 1, 0])
obj_sort = merge_sort(vec)
obj_sort.sort()
print(obj_sort.vec)

#%%
vec = np.array([0, 1, 0, 1, 0])
obj_sort = merge_sort(vec)
obj_sort.sort(recursion=True)
print(obj_sort.vec)
