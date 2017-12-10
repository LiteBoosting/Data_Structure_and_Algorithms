#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np
import pandas as pd
import random

#%%
class keyIndexedCounting(object):
    def __init__(self, DataArray, valueSetArray):
        self.DataArray = DataArray
        self.valueCount = pd.Series(np.full((len(valueSetArray),), 0), index=valueSetArray)
        self.auxDataArray = self.DataArray.copy()
        self.counting()
        self.cumulate()
        self.copyBack()
    
    def counting(self):
        for value in self.DataArray:
            self.valueCount[value] += 1
    
    def cumulate(self):
        leftMostLoc = 0
        upperBoundLoc = 0
        for value, count in self.valueCount.iteritems():
            upperBoundLoc += count
            self.auxDataArray[leftMostLoc:upperBoundLoc] = value
            leftMostLoc = upperBoundLoc
    
    def copyBack(self):
        self.DataArray[:] = self.auxDataArray[:]

#%%
np.set_printoptions(threshold=np.nan)
n = 10
charSet = ['A', 'B', 'C']
DataArray = np.array([random.choice(charSet)+random.choice(charSet)+random.choice(charSet)
                      for i in range(n)])

valueSetArray = np.array([x+y+z for x in charSet for y in charSet for z in charSet])
print(DataArray)
DataArray_count1 = keyIndexedCounting(DataArray, valueSetArray)
print(DataArray)



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np
import pandas as pd
import random

#%%
class LSD(object):
    '''LSD: LeastSignificantDigitSorting
    1. Preparation of values, containers, and records
    2. For i in width to 0, do modified index counting sort (self.digitSort()) on digit i.
    2.1. Standard indexed-counting sort only records the sufficient statistic - distinct values and
         corresponding counting (these two can be constructed using dict or pandas Series, both use hash
         table), then re-construct the array using this sufficient statistic.
    2.2. Here we can't compress data in this way, because we have other digit location, they are different
         and need to be kept in a stable way (stable sorting). Therefore after we finish the counting, we use
         cumulate counting to indicate location, we re-scan the whole data array, copy each value to correct
         bucket and then make location for that bucket plus one.
    '''

    def __init__(self, dataArray, charSet, width):
        self.dataArray = dataArray
        self.charSetArray = np.array(charSet)
        self.width = width
        self.auxDataArray = self.dataArray.copy()
        for digit in np.arange(start=self.width-1, stop=0-1, step=-1):
            self.digitSort(digit)
    
    def digitSort(self, digit):
        self.charCount = pd.Series(np.full((len(self.charSetArray),), 0), index=self.charSetArray)
        self.counting(digit)
        self.sortCopy(digit)
        self.copyBack()

    def counting(self, digit):
        for value in self.dataArray:
            char = value[digit]
            self.charCount[char] += 1
        self.cumCount = pd.Series(np.cumsum(np.concatenate((np.array([0]), self.charCount.values)))[0:-1],
                                  index=self.charSetArray) # used as initial location for slices
        
    def sortCopy(self, digit):
        for value in self.dataArray:
            char = value[digit]
            self.auxDataArray[self.cumCount[char]] = value
            self.cumCount[char] += 1
    
    def copyBack(self):
        self.dataArray[:] = self.auxDataArray[:]

#%%
np.set_printoptions(threshold=np.nan)
n = 10
charSet = np.array(['A', 'B', 'C'])
width = len(charSet)
dataArray = np.array([random.choice(charSet)+random.choice(charSet)+random.choice(charSet)
                      for i in range(n)])

print(dataArray)
dataArray_count2 = LSD(dataArray, charSet, width)
print(dataArray)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np
import pandas as pd
import random

#%%
class MSD(object):
    '''MSD: MostSignificantself.digitSorting
    '''
    def __init__(self, dataArray, charSet, width):
        self.dataArray = dataArray
        self.charSetArray = np.array(charSet)
        self.width = width
        self.digitSort(digit=0)
    
    def digitSort(self, digit, leftLoc=0, upperLoc=None):
        if digit+1 >= self.width:
            return
        # preparation:
        subDataArray = self.dataArray[leftLoc:upperLoc] # None is valid to be used as upper bound
        if len(subDataArray) <= 1:
            return
        auxDataArray = subDataArray.copy()
        charCount = pd.Series(np.full((len(self.charSetArray),), 0), index=self.charSetArray)
        # counting:
        for value in subDataArray:
            char = value[digit]
            charCount[char] += 1
        cumCount = pd.Series(np.cumsum(np.concatenate((np.array([0]), charCount.values)))[0:-1],
                             index=self.charSetArray) # used as initial location for slices
        cumLoc = pd.Series(cumCount.copy(), index=self.charSetArray)
        # sort:
        for value in subDataArray:
            char = value[digit]
            auxDataArray[cumLoc[char]] = value
            cumLoc[char] += 1
        # copyBack:
        self.dataArray[leftLoc:upperLoc] = auxDataArray[:]
        # clean memory:
        del subDataArray, auxDataArray, charCount, cumLoc
        import gc; gc.collect()
        # next stage:
        for leftLoc, upperLoc in zip(cumCount[0:-1], cumCount[1:None]):
            self.digitSort(digit+1, leftLoc, upperLoc)

#%%
np.set_printoptions(threshold=np.nan)
n = 2000
charSet = np.array(['A', 'B', 'C', 'D', 'E'])
dataArray = np.array([random.choice(charSet)+random.choice(charSet)+random.choice(charSet)
                      for i in range(n)])
width = len(dataArray[0])
print(dataArray)
dataArray_count2 = MSD(dataArray, charSet, width)
print(dataArray)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np
import pandas as pd
import random

# first only consider equal length array
# pick the middle letter (define a middle letter function, if has two middle letters, pick the first one,
# the function also returns how many letters left for left and right parts)
# do 3-way partition (no need to be stable) - only scan once, mimic the logic of quick sort, set two scanning
# directions (left, right), once got equal case, if it is met by left scanner, swap to left most (cumulative
# left most direction) otherwise swap to right. After finishing, shift top and bottom parts back.
# Then recursively 3-way partition on these three parts, with middle part first digit no need to consider

#%%
class RadixQuitSort(object):
    def __init__(self, dataArray, charSet, width):
        self.dataArray = dataArray
        self.charSetArray = np.array(charSet)
        self.width = width
        self.digitSort(digit=0)
    
    def middleLetter(self, leftLoc, upperLoc):
        1+1
        # return (middleLetter, leftSize, rightSize)
    
    def threeWayPartition(self, left, upper):
        1+1
        # input: digit, leftLoc, upperLoc

#%%
np.set_printoptions(threshold=np.nan)
n = 2000
charSet = np.array(['A', 'B', 'C', 'D', 'E'])
dataArray = np.array([random.choice(charSet)+random.choice(charSet)+random.choice(charSet)
                      for i in range(n)])
width = len(dataArray[0])
print(dataArray)
dataArray_count2 = MSD(dataArray, charSet, width)
print(dataArray)
