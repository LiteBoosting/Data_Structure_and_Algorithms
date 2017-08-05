1. The performance of quick-sort relies greatly on the selection of partition keys, therefore the algorithm suggests a shuffling before the sorting. Here we propse a method to improve the selection of partition keys - to make each key closer to the corresponding middle point (median). The method is, instead of randomly picking one value, randomly picking $K$ values ($K$ could be 3, 5, or higher, but according to our investigation, 5 is enough, we won't gain that much by going beyond 5), then find the middle one among these $K$ values (median), then swap this middle one with the first value of the whole subarray, then start the splitting （the splitting in quick-sort is like 对接二分，两个盾构机相向而行，正确的留下， 错误的互换，直到相遇）.

2. Here is the simulation code (to select proper value for $K$):
```python
import numpy as np

N = 10000
M = 10000
upper_bound_K = 20

vec = np.arange(N)
K = np.arange(start=1, stop=upper_bound_K, step=2)
ratio = np.full((len(K),), None, dtype=float)
theoretical_variance = (N*N-1)/12

for i, k in enumerate(K):
    sample = [np.median(np.random.choice(vec, size=k, replace=False)) for i in np.arange(M)]
    sample = np.array(sample)
    ratio[i] = np.var(sample)/theoretical_variance
    print("k = %2d, mean: %7.2f, var: %10.2f, ratio: %5.2f%%" % (k, np.mean(sample), np.var(sample), ratio[i]*100))
```
Here is thee result:
```python
k =  1, mean: 4993.96, var: 8312260.79, ratio: 99.75%
k =  3, mean: 5041.19, var: 4995541.68, ratio: 59.95%
k =  5, mean: 5008.24, var: 3548260.63, ratio: 42.58%
k =  7, mean: 4992.65, var: 2824385.87, ratio: 33.89%
k =  9, mean: 4990.13, var: 2264805.98, ratio: 27.18%
k = 11, mean: 5010.28, var: 1921166.79, ratio: 23.05%
k = 13, mean: 4995.26, var: 1677672.02, ratio: 20.13%
k = 15, mean: 4980.39, var: 1480211.34, ratio: 17.76%
k = 17, mean: 5003.84, var: 1314474.02, ratio: 15.77%
k = 19, mean: 4998.61, var: 1191109.57, ratio: 14.29%
```
By using K = 3, 5, ..., we get similar expection, and the variance decreases to 60.45%, 43.24%, .... We see that the decreasing after K=5 is not that significant, therefore we suggest using K=5 (or K=3).

4. The computational burden for adding this mimic-distribution-taking-median step is that we need to (1) generate random number 5 times (which is constant time, since we do not need to shuffle the array, just generate a random number from 0 to 1, then multiply by the length of the array, and take integer); (2) find its median (finding median from 5 numbers, constant time); (3) make the swap (still constant time).

5. How many times we need for this operation? For a length N array ($N = 2^k \times 10$), this will be done k layers, each layer (i-th layer, i=1, ...) we have to make 2^(i-1) operations, the total number is 2^k-1, which is N/10-1. Therefore this is affordable, given that for any subarray with length <= 10, we will use insertion sort.
