from copy import deepcopy
import numpy as np

#%%
class selectionSort(object):
    def __init__(self, sort_array, verbose=False):
        self.sort_array = deepcopy(np.array(sort_array))
        self.verbose = verbose
        
    def main(self):
        for index in range(len(self.sort_array)-1):
            minimum = self.sort_array[index]
            arg_min = index
            for i in range(index+1, len(self.sort_array)):
                if self.sort_array[i] < minimum:
                    minimum = deepcopy(self.sort_array[i])
                    arg_min = i
            if self.verbose:
                print "index =", index, "minimum =", minimum, "location =", arg_min
            if arg_min != index:
                self.sort_array[index], self.sort_array[arg_min] = deepcopy(self.sort_array[arg_min]), deepcopy(self.sort_array[index])
            if self.verbose:
                print self.sort_array
        return self.sort_array

#%%
# trivial case
a = np.array([0])
a_sort = selectionSort(a, verbose=True)
print a_sort.main()

#%%
# typical case
a = np.array([5, 4, 1, 2, 3])
a_sort = selectionSort(a, verbose=True)
print a_sort.main()

#%%
# large sample case
import random
a = random.sample(np.arange(10000), 50)
a_sort = selectionSort(a, verbose=False)
print a
print list(a_sort.main())

#%%
class bubbleSort(object):
    def __init__(self, sort_array, verbose=False):
        self.sort_array = deepcopy(np.array(sort_array))
        self.verbose = verbose
        
    def main(self):
        for index in range(len(self.sort_array), 0, -1):
            for i in range(1, index):
                if self.sort_array[i-1] > self.sort_array[i]:
                    self.sort_array[i-1], self.sort_array[i] = deepcopy(self.sort_array[i]), deepcopy(self.sort_array[i-1])
            if self.verbose:
                print self.sort_array
        return self.sort_array

#%%
# trivial case
a = np.array([0])
a_sort = bubbleSort(a, verbose=True)
print a_sort.main()

#%%
# typical case
a = np.array([5, 4, 1, 2, 3])
a_sort = bubbleSort(a, verbose=True)
print a_sort.main()

#%%
# large sample case
import random
a = random.sample(np.arange(10000), 10)
a_sort = bubbleSort(a, verbose=True)
print a
print list(a_sort.main())

#%%
class insertionSort(object):
    def __init__(self, sort_array, verbose=False):
        self.sort_array = deepcopy(np.array(sort_array))
        self.verbose = verbose
        
    def main(self):
        for index in range(len(self.sort_array)-1):
            for i in range(index+1, 0, -1):
                if self.sort_array[i] < self.sort_array[i-1]:
                    self.sort_array[i-1], self.sort_array[i] = deepcopy(self.sort_array[i]), deepcopy(self.sort_array[i-1])
                else:
                    if self.verbose:
                        print "break at", i
                    break
            if self.verbose:
                print self.sort_array
        return self.sort_array

#%%
# trivial case
a = np.array([0])
a_sort = insertionSort(a, verbose=True)
print a_sort.main()

#%%
# typical case
a = np.array([5, 4, 1, 2, 3])
a_sort = insertionSort(a, verbose=True)
print a_sort.main()

#%%
# large sample case
import random
a = random.sample(np.arange(10000), 10)
a_sort = insertionSort(a, verbose=True)
print a
print list(a_sort.main())
