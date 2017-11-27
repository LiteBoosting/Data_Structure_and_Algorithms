#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
class hash_table(object):
    def __init__(self, val_set):
        self.M = int(1e2)
        self.table_build(val_set)
    
    def hash_func(self, x, L=77537):
        """This function is specifically designed for 3-sum problem.
           Therefore the input type must be integer.
        """
        return int((abs(x)*L)%self.M)
    
    def table_build(self, val_set):
        import numpy as np
        self.array = np.full((self.M,), None)
        for val in val_set:
            i = self.hash_func(val)
            while True:
                if self.array[i] is None:
                    self.array[i]= val
                    break
                else:
                    i = (i+1)%self.M
        return
    
    def get(self, val):
        i = self.hash_func(val)
        while True:
            if self.array[i] == val:
                return True
            elif self.array[i] is None:
                return False
            else:
                i += 1
    
#%%
import numpy as np
val_set = np.array([1, -1, 2, 0, 4, 5, 7, -7, 8, -8, -2, 12])

A = hash_table(val_set)
np.set_printoptions(threshold=np.nan)
print(A.array)

#%%
print(A.get(-8))

#%%
for val1 in val_set:
    for val2 in val_set:
        val3 = -(val1+val2)
        if (val1 == val3) or (val2 == val3):
            continue
        if (val1 > val2) or (val2 > val3):
            continue
        if A.get(val3):
            print(val1, val2, val3)
            
#%%
# directly using python set
val_set = {1, -1, 2, 0, 4, 5, 7, -7, 8, -8, -2, 12}
for val1 in val_set:
    for val2 in val_set:
        val3 = -(val1+val2)
        if (val1 == val3) or (val2 == val3):
            continue
        if (val1 > val2) or (val2 > val3):
            continue
        if val3 in val_set:
            print(val1, val2, val3)
