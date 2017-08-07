#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#%%
from copy import deepcopy
import random
random.seed(a=None)
# print(random.random())
#%%
class quick_sort(object):
    """Use quick sort to sort an array, increasing order only.
    K elements will be selected randomly to find a proper partition key.
    Sub_arrays with length no more than S (10) will be sorted by insertion_sort()
    """
    def __init__(self, array, K=5, S=10):
        self.array = deepcopy(array)
        self.size = len(array)
        self.K = K # see the documentation (md file with same name) for usage of K
        
    def insertion_sort(self, start_index, end_index):
        if end_index <= start_index+1:
            return
        for index in range(start_index, end_index-1):
            for i in range(index+1, 0, -1):
                if self.array[i] < self.array[i-1]:
                    self.array[i-1], self.array[i] = deepcopy((self.array[i], self.array[i-1]))
                else:
                    break

    def partition(self, start_index, end_index):
        """Given the first value in the sub_array as partition key, shift values smaller than partition key to left,
        values greater than or equal to partition key to right
        """
        partition_key = self.array[start_index]
        left = start_index+1
        right = end_index-1
        while left < right+1:
            while self.array[left] < partition_key:
                left += 1
            while self.array[right] >= partition_key:
                right -= 1
            if left < right:
                self.array[left], self.array[right] = deepcopy((self.array[right], self.array[left]))
                left += 1
                right -= 1
        if left-right == 1:
            self.array[start_index], self.array[right] = deepcopy((self.array[right], self.array[start_index]))
            return right
        else:
            raise ValueError('left:', left, 'left-value:', self.array[left], 'right:', right,
                             'right-value', self.array[right], 'partition key:', self.array[start_index])         
        
    def sort(self, left=0, right=None):
        if right == None:
            right = self.size
        middle = self.partition(left, right)
        if left < middle:
            self.sort(left, middle)
        if middle+1 < right:
            self.sort(middle+1, right)

#%%
array = [5]
array_sort = quick_sort(array)
print(array_sort.partition(0, 1))
# print(array_sort.array)

#%%
array = [5, 4, 9, 2, 1]
array_sort = quick_sort(array)
array_sort.sort()
print(array_sort.array)
