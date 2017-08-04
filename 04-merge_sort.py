# merge 2 sorted arrays (increasing order)
import numpy as np
from copy import deepcopy
def merge(vec_a, vec_b):
    s_a, s_b = len(vec_a), len(vec_b)
    vec_c = deepcopy(np.concatenate((vec_a, vec_b)))
    i_a, i_b = 0, 0
    key = True
    i_c = 0
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

#%% marginal case
vec_a = np.array([0])
vec_b = np.array([1])
print merge(vec_a, vec_b)
#%% small case
vec_a = np.array([0, 1, 2, 3, 10])
vec_b = np.array([1, 5, 7, 9])
print merge(vec_a, vec_b)
