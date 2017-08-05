1. The performance of quick-sort relies greatly on the selection of partition key, therefore quick-sort algorithm suggests a shuffling before the sorting. Here we propse a method to improve the selection of partition key - to make it closer to the middle point. The method is, instead of randomly pick one value, we randomly pick K values (K could be 3, 5, or higher, but according to our investigation, 5 is enough, we won't gain that much by going beyond 5), then find the middle one (median), then swap this one with the first value, then start the splitting （对接二分，两个盾构机相向而行，直到相遇）.

2. Here is the simulation code:
```python
N = 10000
M = 10000
vec = np.arange(N)

sample_1 = np.random.choice(vec, size=M, replace=True, p=None)
print(np.mean(sample_1))
print(np.var(sample_1))

sample_3 = np.array([np.median(np.random.choice(vec, size=3, replace=False, p=None)) for i in np.arange(M)])
print(np.mean(sample_3))
print(np.var(sample_3))

sample_5 = np.array([np.median(np.random.choice(vec, size=5, replace=False, p=None)) for i in np.arange(M)])
print(np.mean(sample_5))
print(np.var(sample_5))

sample_7 = np.array([np.median(np.random.choice(vec, size=7, replace=False, p=None)) for i in np.arange(M)])
print(np.mean(sample_7))
print(np.var(sample_7))

sample_9 = np.array([np.median(np.random.choice(vec, size=9, replace=False, p=None)) for i in np.arange(M)])
print(np.mean(sample_9))
print(np.var(sample_9))

sample_11 = np.array([np.median(np.random.choice(vec, size=11, replace=False, p=None)) for i in np.arange(M)])
print(np.mean(sample_11))
print(np.var(sample_11))
```
Here is thee result:
```python
4965.6792
8355455.13149
5022.9071
5032570.35607
4984.9409
3568373.81881
5012.6564
2729247.15894
4996.4185
2314803.05596
4988.5951
1924592.75316
```
We can see by using K = 3, 5, 7, 9, 11, we get unchanged expection, and the variance decreases to 58.33%, 44.05%, 32.14%, 27.38%, and 22.62%. We see that the decreasing after K=5 is not that significant, therefore we suggest use K=5 (or K=3).
