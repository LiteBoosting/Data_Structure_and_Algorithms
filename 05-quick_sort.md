1. The performance of quick-sort relies greatly on the selection of partition key, therefore quick-sort algorithm suggests a shuffling before the sorting. Here we propse a method to improve the selection of partition key - to make it closer to the middle point. The method is, instead of randomly pick one value, we randomly pick K values (K could be 3, 5, or higher, but according to our investigation, 5 is enough, we won't gain that much by going beyond 5), then find the middle one (median), then swap this one with the first value, then start the splitting （对接二分，两个盾构机相向而行，直到相遇）.

2. Here is the simulation code:
```python
import numpy as np

N = 10000
M = 10000
vec = np.arange(N)

K = np.arange(start=1, stop=16, step=2)
ratio = np.full((len(K),), None, dtype=float)
theoretical_variance = (N*N-1)/12
for i, k in enumerate(K):
    sample = [np.median(np.random.choice(vec, size=k, replace=False)) for i in np.arange(M)]
    sample = np.array(sample)
    print(np.mean(sample))
    print(np.var(sample))
    ratio[i] = np.var(sample)/theoretical_variance
print(ratio*100)
```
Here is thee result:
```python
5016.8469
8271304.28246
5016.5936
5037785.82224
5017.9882
3603309.47866
5008.7623
2744340.8474
4986.436
2284062.8771
4995.931
1920401.52064
4990.4618
1646849.90774
4988.7481
1488085.38605
[ 99.25565238  60.45343047  43.23971418  32.9320905   27.4087548
  23.04481848  19.76219909  17.85702481]```
We can see by using K = 3, 5, 7, 9, 11, 13, 15, we get unchanged expection, and the variance decreases to 60.45%, 43.24%, 32.93%, 27.41%, 23.04%, 19.76%, and 17.86%. We see that the decreasing after K=5 is not that significant, therefore we suggest use K=5 (or K=3).

4. The computational burden for adding this mimic-distribution-taking-median step is that we need to (1) generate random number 5 times (which is constant time, since we do not need to shuffle the array, just generate a random number from 0 to 1, then multiply by the length of the array, and take integer); (2) find its median (finding median from 5 numbers, constant time); (3) make the swap (still constant time).

5. How many times we need for this operation? For a length N array ($N = 2^k \times 10$), this will be done k layers, each layer (i-th layer, i=1, ...) we have to make 2^(i-1) operations, the total number is 2^k-1, which is N/10-1. Therefore this is affordable, given that for any subarray with length <= 10, we will use insertion sort.
