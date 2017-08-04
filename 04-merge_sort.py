class merge_sort(object):
    def __init__(self, vec):
        import numpy as np
        from copy import deepcopy
        self.vec_aux = deepcopy(np.array(vec))
        self.n = len(vec)
        
    def merge(self, vec_a, vec_b):
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
            
    def main_sort(self, left=0, right=None):
        if right == None:
            right = self.n
        if right-left == 1:
            return self.vec_aux[left:right]
        else:
            middle = int(left+(right-left)/2)
            return self.merge(self.main_sort(left, middle), self.main_sort(middle, right))
#%%
vec = np.array([0, 3, 4, 2, 9, 4])
obj_ = merge_sort(vec)
print obj_.main_sort()
#%%
vec = np.array([0, 1, 0, 1, 0, 1])
obj_ = merge_sort(vec)
print obj_.main_sort()
